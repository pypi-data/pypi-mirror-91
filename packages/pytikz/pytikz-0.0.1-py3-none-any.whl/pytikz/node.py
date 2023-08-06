from .abstract import Drawable
from .vector import Transformable


class Node(Drawable, Transformable):
    """A text node at a certain position on the canvas.

    Args:
        position (VectorType or VectorLike): The position of the text node.
        text (str): The text of the text node.
        orientation (None or Orientation): The orientation of the position relative to the text.

    Attributes:
        position (VectorType or VectorLike): The position of the text node.
        text (str): The text of the text node.
        orientation (None or Orientation): The orientation of the position relative to the text.

    """

    def __init__(self, position, text, orientation=None):
        self.position = position
        self.text = text
        self.orientation = orientation

    def __str__(self):
        """Implements the __str__ method from Drawable.

        Returns:
            str: The string pgf/tikz string representation of the node.

        """
        options = f"[anchor={self.orientation.value}]" if self.orientation else ""
        return f"\\node{options} at {self.position} {{{self.text}}};"

    def copy(self):
        """Implements the copy method from Shiftable.

        Returns:
            Node: A copy of the Node.

        """
        return Node(self.position, self.text, self.orientation)

    def apply(self, transformation):
        """Implements the apply method from Shiftable.

        Applies the transformation to the position attribute.

        Args:
            transformation (Transformation or function): The transformation to be applied.

        """
        self.position = transformation(self.position)
