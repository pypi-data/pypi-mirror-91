"""AutoML

Execute an AutoML procedure on a well-formated `DataFrame` containing a
`label` column. Uses AutoGluon.

Graphs may be constructed (with sane defaults) to visually illustrate
classifier performance.

"""
import itertools

import matplotlib.pyplot as plt
import seaborn as sns
from autogluon import TabularPrediction as task
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import (
    roc_curve,
    auc,
    precision_recall_curve,
    average_precision_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)


sns.set_style('ticks')
sns.set_context(rc={'lines.linewidth': 1.75})


class AutoML:
    """Execute AutoGluon on a `DataFrame` with a `label` column.

    Models and results are output to file.

    """
    linestyles = ('-', '--', '-.', ':')

    graphs_dirname = 'graphs'
    models_dirname = 'models'

    #: Parameter defaults and options
    EVAL_METRIC = 'accuracy'
    EVAL_METRICS_ALL = (
        'accuracy', 'balanced_accuracy', 'f1', 'f1_macro', 'f1_micro',
        'f1_weighted', 'roc_auc', 'average_precision', 'precision',
        'precision_macro', 'precision_micro', 'precision_weighted', 'recall',
        'recall_macro', 'recall_micro', 'recall_weighted', 'log_loss',
        'pac_score',
    )

    QUALITY = 0
    QUALITY_PRESETS = (
        'medium_quality_faster_train',
        'good_quality_faster_inference_only_refit',
        'high_quality_fast_inference_only_refit',
        'best_quality',
    )

    N_THREADS = None

    TEST_SIZE = 0.3

    TIME_LIMITS = 5 * 60

    VERBOSITY = 1

    def __init__(self, data, outpath):
        self.data = data
        self.outpath = outpath

    @property
    def graphs_path(self):
        return self.outpath / self.graphs_dirname

    @property
    def models_path(self):
        return self.outpath / self.models_dirname

    def __call__(self, test_size=TEST_SIZE, eval_metric=EVAL_METRIC, quality=QUALITY,
                 time_limits=TIME_LIMITS, n_threads=N_THREADS, verbosity=VERBOSITY):
        """Train, test, and evaluate models."""
        (train_data, test_data) = train_test_split(self.data, test_size=test_size)
        predictor = self.train(train_data, eval_metric, quality, time_limits,
                               n_threads, verbosity=verbosity)
        self.test(predictor, test_data)
        self.graph_all(predictor, test_data)

    def train(self, train_data, eval_metric=EVAL_METRIC, quality=QUALITY,
              time_limits=TIME_LIMITS, n_threads=N_THREADS, verbosity=VERBOSITY):
        """Train prospective models."""
        # predictor gives us default access to the *best* predictor that
        # was trained on the task (otherwise we're just wrapping AutoGluon)
        return task.fit(train_data=train_data, label='label',
                        eval_metric=eval_metric,
                        output_directory=self.outpath,
                        time_limits=time_limits,
                        presets=self.QUALITY_PRESETS[quality],
                        nthreads_per_trial=n_threads,
                        verbosity=verbosity)

    def test(self, predictor, test_data):
        """Evaluate models on the test set and write the results to file."""
        leaderboard = predictor.leaderboard(test_data, silent=True)
        leaderboard.set_index('model').sort_index().to_csv(self.outpath / 'leaderboard.csv')

    def graph_all(self, predictor, test_data):
        """Generate ROC, PR and confusion matrix graphs for the
        classification tasks.

        Uses sane defaults; (customization is left to the user with the
        models written to file).

        """
        y_true = test_data['label']
        test_no_label = test_data.drop(labels=['label'], axis=1)
        binarizer = LabelBinarizer().fit(y_true)
        binarized_labels = binarizer.transform(y_true)

        y_pred = predictor.predict(test_no_label)
        y_proba = predictor.predict_proba(test_no_label)
        self.make_pr(binarizer.classes_, binarized_labels, y_proba)
        self.make_roc(binarizer.classes_, binarized_labels, y_proba)
        self.make_cfmx(binarizer.classes_, y_true, y_pred)

    def make_cfmx(self, classes, y_true, y_pred):
        """Make confusion matrix without printing exact values.

        (Printing exact values of confusion can go poorly with large
        magnitudes of samples.)

        """
        cfmx = confusion_matrix(y_true, y_pred)
        cfmx_display = ConfusionMatrixDisplay(cfmx, display_labels=classes)
        cfmx_display.plot(include_values=False,
                          cmap=plt.cm.Blues,
                          xticks_rotation=45)

        self.print_graph('cfmx.pdf',
                         x_label='Predicted Label',
                         y_label='True Label')

    def make_pr(self, classes, y_true_bin, y_proba):
        """PR curve that splits on the binary case (no enumeration
        needed).

        """
        # Binary case does not enumerate
        if len(classes) == 2:
            plt_ax = self._make_binary_pr(y_true_bin.ravel(), y_proba.ravel())
        else:
            for i, class_label in enumerate(classes):
                plt_ax = self._make_binary_pr(y_true_bin[:, i], y_proba[:, i],
                                              class_label=class_label)

        # Split up the line styles to make them unique
        for (linestyle, line) in zip(itertools.cycle(self.linestyles),
                                     plt_ax.lines):
            line.set_linestyle(linestyle)

        self.print_graph('pr.pdf', x_lim=[0.0, 1.0],
                         y_lim=[0.0, 1.05], legend_loc='lower left',
                         x_label='Recall', y_label='Precision')

    def _make_binary_pr(self, y_true, y_proba, class_label=None):
        """Make a PR curve for the given data.

        Includes the average precision score for the given data.

        """
        (precision, recall, _) = precision_recall_curve(y_true, y_proba)
        cl_ap = average_precision_score(y_true, y_proba)

        if class_label:
            label = '{0} - AP: {1:.2f}'.format(class_label, cl_ap)
        else:
            label = 'AP: {0:.2f}'.format(cl_ap)

        return sns.lineplot(x=recall, y=precision, label=label)

    def make_roc(self, classes, y_true_bin, y_proba):
        """ROC curve that splits on the binary case (no enumeration
        needed).

        """
        # Binary case does not enumerate
        if len(classes) == 2:
            plt_ax = self._make_binary_roc(y_true_bin.ravel(), y_proba.ravel())
        else:
            for i, class_label in enumerate(classes):
                plt_ax = self._make_binary_roc(y_true_bin[:, i], y_proba[:, i],
                                               class_label=class_label)

        # Split up the line styles to make them unique
        for (linestyle, line) in zip(itertools.cycle(self.linestyles),
                                     plt_ax.lines):
            line.set_linestyle(linestyle)

        self.print_graph('roc.pdf', x_lim=[0.0, 1.0],
                         y_lim=[0.0, 1.05], x_label='False Positive Rate',
                         y_label='True Positive Rate',
                         legend_loc='lower right')

    def _make_binary_roc(self, y_true, y_proba, class_label=None):
        """Make ROC curve for given data.

        Includes roc_auc_score.

        """
        (fpr, tpr, _) = roc_curve(y_true, y_proba)
        cl_auc = auc(fpr, tpr)

        if class_label:
            label = '{0} - AUC: {1:.2f}'.format(class_label, cl_auc)
        else:
            label = 'AUC: {0:.2f}'.format(cl_auc)

        return sns.lineplot(x=fpr, y=tpr, label=label)

    def print_graph(self, ofn, x_lim=None, y_lim=None, legend_loc=None,
                    title=None, x_label=None, y_label=None):
        """Output graph."""
        plt.xlim(x_lim)
        plt.ylim(y_lim)

        if legend_loc:
            plt.legend(loc=legend_loc)

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.tight_layout()

        self.graphs_path.mkdir(parents=True, exist_ok=True)
        plt.savefig(self.graphs_path / ofn)

        plt.clf()
