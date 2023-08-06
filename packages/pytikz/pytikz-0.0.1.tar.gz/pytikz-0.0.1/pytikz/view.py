from .abstract import Drawable, AbstractList
from .vector import Transformable, compose


class View(Drawable, Transformable, AbstractList):
    """Matches a list of Drawables with a common transformation.

    Drawables are transformed through this transformation upon access.

    Args:
        transformation (function): The transformation applied when viewing each Drawable.
        clip (None or ClosedShape): The region to clip when producing a pgf/tikz string of the entire View.

    Attributes:
        _list (list): The wrapped list of Drawables.
        transformation (function): The transformation applied when viewing each Drawable.
        clip (None or ClosedShape): The region to clip when producing a pgf/tikz string of the entire View.

    """

    def __init__(self, transformation=lambda v: v, clip=None):
        self._list = []
        self.transformation = transformation
        self.clip = clip

    def _view(self, item):
        """Implements the _view method from AbstractList.

        Args:
            item (Drawable): The item to be viewed.

        Returns:
            Drawable: The transformed item.

        """
        return self.transformation(item)

    def __str__(self):
        """Implements the __str__ method from Drawable.

        Returns a string with the transformed Drawables concatenated, and clipped whenever a ClosedShape is provided.

        Returns:
            str: The string pgf/tikz string representation of the view.

        """
        data = "\n".join(str(d) for d in self)
        return data if self.clip is None else self.clip.clip(data)

    def copy(self):
        """Implements the copy method from Shiftable.

        Returns:
            View: A copy of the View, where the list is passed as a reference.

        """
        view = View(self.transformation, self.clip)
        view._list = self._list
        return view

    def apply(self, transformation):
        """Implements the apply method from Shiftable.

        Applies the transformation to the View, by composing it with the internal transformation, and applying it to the ClosedShape.

        Args:
            transformation (Transformation or function): The transformation to be applied.

        """
        self.transformation = compose(transformation, self.transformation)
        if self.clip is not None:
            self.clip = transformation(self.clip)
