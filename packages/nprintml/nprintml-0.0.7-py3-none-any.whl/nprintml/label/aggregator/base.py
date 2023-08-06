import abc
import collections.abc
import importlib
import io
import pkgutil

import pandas as pd


class LabelAggregator(abc.ABC):
    """LabelAggregator provides general methods for working with nPrint
    data, such as attaching labels, compressing nPrint data, and
    generating new columns for flattened nPrint data.

    Inheritors of this class are expected to implement the abstract
    method `__call__()` to provide their method of feature aggregation.

    """
    def __init__(self, npt_csv, label_csv):
        self.npt_csv = npt_csv
        self.label_csv = label_csv

    @abc.abstractmethod
    def __call__(self, compress=False, sample_size=1):
        """Abstract method, expected to be implemented on a per-example
        label aggregation method.

        """

    def load_npt(self, npt_csv):
        """Load nPrint data.

        The index column is expected to *always* be the 0th column.

        """
        return pd.read_csv(npt_csv, index_col=0)

    def load_label(self, labels_csv):
        """Load labels, which are expected to be in item, label column
        format where item is the index.

        A header line "item,label" (case-insensitive) is optional.

        For example:

            item,label
            key1,label1
            key2,label2
            key3,label3

        """
        # enforce column names (item, label)
        label = pd.read_csv(labels_csv, index_col='item', names=('item', 'label'))

        # check for optional header line
        if not label.empty:
            row0 = label.iloc[0]
            if row0.name.lower() == 'item' and row0.label.lower() == 'label':
                return label.iloc[1:]

        return label

    def compress_npt(self, npt):
        """Compress columns out of an nPrint that provide no predictive
        signal.

        More specifically, this method drops *all* columns in a given nPrint
        dataframe where each bit is the same value.

        """
        nunique = npt.apply(pd.Series.nunique)
        cols_to_drop = nunique[nunique == 1].index
        return npt.drop(cols_to_drop, axis=1)

    def attach_label(self, npt, label):
        """Attach labels to a dataframe of nPrints, returning the labels
        that are missing, the new dataframe, and the number of samples
        that were lost.

        """
        samples0 = len(npt)
        missing_labels = npt.index.difference(label.index).tolist()

        try:
            npt = npt.join(label).dropna(subset=['label'])
        except KeyError as exc:
            raise LabelError("label input is malformed") from exc

        samples1 = len(npt)

        return (npt, missing_labels, samples0, samples1)

    def flatten_columns(self, columns, sample_size):
        """When we attach labels to more than one nPrint we need to
        create new columns that essentially are the original columns
        multiplied by the number of packets in each flattened sample.

        """
        return [
            f'pkt_{index}_{column}'
            for index in range(sample_size)
            for column in columns
        ]

    @staticmethod
    def filerepr(fd):
        return fd.name if isinstance(fd, io.TextIOWrapper) else str(fd)


class LabelError(Exception):
    pass


class PluginRegistry(collections.abc.Mapping):
    """Lazy class registry.

    The specified `package` is crawled -- lazily -- for well-named
    modules containing class-based plugins; and, as needed, subclasses
    of the specified `class_or_tuple` base (as with `issubclass()`)
    are imported and registered for retrieval.

    The registry operates as an immutable mapping.

    Values are imported plugin classes, stored under the names of the
    modules in which they are found.

    Plugin module discovery may be customized by overriding
    `__generate_names__`. Recognition and retrieval of plugin classes
    may be customized by overriding `__retrieve_member__`.

    """
    def __init__(self, class_or_tuple, package, ignore=()):
        # issubclass supports a class or a tuple of base classes, and so we do as well;
        # however, we also need to check for identity, and so we'll enforce type here:
        self.base = class_or_tuple if isinstance(class_or_tuple, tuple) else (class_or_tuple,)

        # at least ensure we have access to the base package
        self.package = importlib.import_module(package) if isinstance(package, str) else package

        self.ignore = ignore if isinstance(ignore, frozenset) else frozenset(ignore)

        self.__cache__ = None

    def __generate_names__(self):
        """Discover the plugin package's modules.

        Sub-packages and modules whose names are contained with `ignore`
        are ignored.

        This method should only be called internally and only *once*.
        It is factored out so as to be available for customization.

        """
        for module in pkgutil.iter_modules(self.package.__path__):
            if not module.ispkg and module.name not in self.ignore:
                yield module.name

    def __retrieve_member__(self, name):
        """Import the named module and return its contained plugin
        class.

        It is assumed that the module contains exactly one subclass of
        the `class_or_tuple` base.

        This method should only be called internally and only *once*.
        It is factored out so as to be available for customization.

        """
        module = importlib.import_module(f'{self.package.__name__}.{name}')
        (value,) = (member for member in vars(module).values()
                    if isinstance(member, type) and
                       issubclass(member, self.base) and  # noqa: E127
                       member not in self.base)           # noqa: E127
        return value

    def __populate_names__(self):
        """Construct and populate the keys of the registry cache if the
        cache does not exist.

        """
        if self.__cache__ is None:
            self.__cache__ = dict.fromkeys(self.__generate_names__())

    def __iter__(self):
        self.__populate_names__()
        yield from self.__cache__

    def __len__(self):
        self.__populate_names__()
        return len(self.__cache__)

    def __getitem__(self, name):
        self.__populate_names__()

        value = self.__cache__[name]

        if value is None:
            value = self.__cache__[name] = self.__retrieve_member__(name)

        return value
