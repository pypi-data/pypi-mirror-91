from abc import ABC, abstractmethod
import numpy as np


def _tikz_representation(array):
    """Returns the pgf/tikz string representation of the array.

    Args:
        array (np.ndarray): The array which requires a string representation.

    Returns:
        str: The pgf/tikz string representation.

    Raises:
        ValueError: If the dimension of the array is not 1 or 2.

    """
    if array.ndim == 1:
        return f"({', '.join(str(c) for c in array)})"
    elif array.ndim == 2:
        return " -- ".join(str(v) for v in array)
    else:
        raise ValueError(
            f"Arrays of dimension {array.ndim} have no TikZ representation."
        )


np.set_string_function(
    _tikz_representation, False
)  # Presents this .__str__ method to numpy.


VectorType = type(np.array([]))  # Vectors have type np.ndarray.


class VectorLike(ABC):
    """Abstract class for instances that can be cast to VectorType."""

    @property
    @abstractmethod
    def vector(self):
        """Returns the VectorType representation of the instance."""
        pass

    def __str__(self):
        """Returns the pgf/tikz string representation of the instance."""
        return str(self.vector)


def Vector(*args):
    """Generates a VectorType instance.

    Args:
        *args: Variable length arguments list, of one of the following types.
            [VectorType]: A single VectorType instance.
            [VectorLike]: A single VectorLike instance.
            [x, y, ...]: A variable number of real numbers.

    Returns:
        np.ndarray: The VectorType representation of the vector.

    """
    args = list(args)
    if len(args) == 1 and isinstance(args[0], VectorType):
        return args[0]
    elif len(args) == 1 and isinstance(args[0], VectorLike):
        return args[0].vector
    else:
        return np.array(args)


class Shiftable(ABC):
    """Abstract class for instances that may be subjected to Shift instances."""

    @abstractmethod
    def copy(self):
        """Returns a copy of the instance."""
        pass

    @abstractmethod
    def apply(self, transformation):
        """Applies the transformation internally to the instance.

        Args:
            transformation (Transformation): The transformation that should act on the instance.

        This method must return None.

        """
        pass


class Scalable(Shiftable):
    """Abstract class for instances that may be subjected to Scaling instances."""

    pass


class Transformable(Scalable):
    """Abstract class for instances that may be subjected to Transformation instances."""

    pass


class Transformation:
    """Wrapper class for functions that act on Transformable instances.

    Args:
        transformation (function): The wrapped function.

    Attributes:
        _transformation (function): The wrapped function.
        _subject_type (type): The type of arguments that may be passed to the wrapped function, other than VectorType.

    """

    _subject_type = Transformable

    def __init__(self, transformation):
        self._transformation = transformation

    def __call__(self, subject, inplace=False):
        """Applies ._transformation to subject.

        Args:
            subject (_subject_type or VectorType): The subject that is passed.
            inplace (bool): If the subject should be copied before application.

        Returns:
            _subject_type or VectorType: The transformed subject.

        Raises:
            ValueError: If subject is not of type VectorType or of type _subject_type.

        If subject is of VectorType, the transformation is applied directly to the argument.
        Otherwise, the method calls subject.apply(self), and the subject handles the further internal application of the transformation.
        If inplace is False, then the subject is copied before application.

        """
        if isinstance(subject, VectorType):
            return self._transformation(subject)
        elif not isinstance(subject, self._subject_type):
            raise ValueError(subject, self._subject_type)
        else:
            if not inplace:
                subject = subject.copy()
            subject.apply(self)
            return subject


class Scaling(Transformation):
    """Wrapper class for functions that act on Scalable instances.

    A Scaling is a specific type of Transformation, and applies to a wider range of instances.

    Args:
        x (float): The horizontal scaling factor.
        y (float): The vertical scaling factor.
        origin (VectorType): The origin that should be shifted to (0, 0) before scaling.

    """

    _subject_type = Scalable

    def __init__(self, x, y, origin=Vector(0, 0)):
        self.x = x
        self.y = y
        self.origin = origin

    def _transformation(self, vector):
        return Vector(
            self.x * (vector[0] - self.origin[0]), self.y * (vector[1] - self.origin[1])
        )


class Shift(Scaling):
    """Wrapper class for functions that act on Shiftable instances.

    A Shift is a specific type of Scaling, and applies to a wider range of instances.

    Args:
        origin (VectorType): The origin that should be shifted to (0, 0).

    """

    _subject_type = Shiftable

    def __init__(self, origin):
        self.x = 1
        self.y = 1
        self.origin = origin


def compose(a, b):
    """A simple function for composing two Transformations.

    Args:
        a (Transformation): The Transformation that should be applied last.
        b (Transformation): The Transformation that should be applied first.

    Returns:
        function: The composition of the two function calls.

    """
    return lambda v: a(b(v))


class AnchoredObject(ABC):
    """Abstract class for anchored instances.

    When a transformation is applied to an AnchoredObject, the Transformation is only applied to the anchor attribute.

    Attributes:
        anchor (VectorType or VectorLike): The anchor that the Transformation should work on.

    """

    anchor = None

    def apply(self, transformation):
        if self.anchor is None:
            self.apply_internally(transformation)
        else:
            self.anchor = transformation(self.anchor)
        return self

    def anchor_resolve(self, vector):
        """Returns the position of a vector relative to the anchor.

        Args:
            vector (VectorType or VectorLike): The relative vector to be resolved.

        Returns:
            VectorType: The absolute position of the resolved vector.

        """
        if self.anchor is None:
            return Vector(vector)
        else:
            return Vector(vector) + Vector(self.anchor)


class AnchoredVector(VectorLike, AnchoredObject, Transformable):
    """VectorLike instance which consists of two vector: an absolute and a relative vector.

    When a Transformation is applied to an AnchoredVector, it is only applied to the anchor.
    The offset attribute remains unchanged.
    When an AnchoredVector is cast to VectorType, the two vectors are summed.

    Args:
        anchor (VectorType or VectorLike): The transformable anchor vector.
        offset (VectorType or VectorLike): The offset vector that is not transformed.

    """

    def __init__(self, anchor, offset):
        self.anchor = anchor
        self.offset = offset

    @property
    def vector(self):
        return self.anchor_resolve(self.offset)

    def copy(self):
        return AnchoredVector(self.anchor, self.offset)
