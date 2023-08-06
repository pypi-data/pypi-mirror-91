from abc import ABC, abstractmethod


class Drawable(ABC):
    """Abstract Drawable class for instances that can be drawn onto the pgf/tikz canvas.

    The string representation of the instance should be self-contained.

    """

    @abstractmethod
    def __str__(self):
        """Must return the representation of the Drawable as a pgf/tikz string."""
        pass


class AbstractList(ABC):
    """An AbstractList is a wrapped list which transforms elements through the .view method upon access.

    Args:
        data (list): The wrapped list.

    Attributes:
        _list (list): The wrapped list.

    """

    _list = None

    def __init__(self, data=None):
        self._list = []
        if data is not None:
            self._list = data

    def _view(self, item):
        """The _view method equals the identity transformation by default."""
        return item

    def append(self, item):
        """Appends the item to the wrapped list."""
        self._list.append(item)

    def __setitem__(self, k, value):
        """Sets the k-th entry of the wrapped list to the value provided."""
        self._list[k] = value

    def __getitem__(self, k):
        """Retrieves the transformed version of the k-th entry of the wrapped list."""
        return self._view(self._list[k])

    def __iter__(self):
        """Iterates over the transformed entries of the wrapped list."""
        for k in range(len(self._list)):
            yield self[k]
