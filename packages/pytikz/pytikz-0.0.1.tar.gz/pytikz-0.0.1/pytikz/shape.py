from abc import ABC, abstractmethod
from .abstract import Drawable, AbstractList
from .vector import Transformable


class Shape(ABC):
    """Abstract Shape class for instances that represent a pgf/tikz path."""

    @abstractmethod
    def __str__(self):
        """Must return the representation of the Shape as a pgf/tikz string."""
        pass


class ClosedShape(Shape, ABC):
    """Abstract ClosedShape class for instances that represent a closed pgf/tikz path.

    Such paths can be filled or used to clip other Drawables.

    """

    def clip(self, text):
        """Wraps the input string in the clipping commands.

        Args:
            text (str): The pgf/tikz string representing the drawables to be clipped.

        Returns:
            str: The input string wrapped in the clipping commands.

        """
        return "\\begin{scope}\n" f"\\clip {self};\n" f"{text}\n" "\\end{scope}"


class StyledShape(Drawable, Transformable):
    """A StyledShape instance combines Shape and ShapeStyle data and can be drawn directly onto the canvas.

    Args:
        shape (Shape): The Shape to be drawn.
        shape_style (ShapeStyle): The ShapeStyle containing the .draw method for drawing the Shape.

    Attributes:
        shape (Shape): The Shape to be drawn.
        shape_style (ShapeStyle): The ShapeStyle containing the .draw method for drawing the Shape.

    """

    def __init__(self, shape, shape_style):
        self.shape = shape
        self.shape_style = shape_style

    def __str__(self):
        """Implements the __str__ method from Drawable.

        Returns:
            str: The shape_style pgf/tikz string representation of the shape.

        """
        return self.shape_style.draw(self.shape)

    def copy(self):
        """Implements the copy method from Shiftable.

        Returns:
            StyledShape: A copy of the StyledShape.

        """
        return StyledShape(self.shape.copy(), self.shape_style)

    def apply(self, transformation):
        """Implements the apply method from Shiftable.

        Applies the transformation to the shape.

        Args:
            transformation (Transformation or function): The transformation to be applied.

        """
        self.shape.apply(transformation)


class ShapeStyle:
    """Fundamental ShapeStyle class which features the draw method for drawing a Shape.

    Attributes:
        line (bool): If the Shape should be drawn as a line.
        line_width (None or LineWidth): The width of the previous line.
        line_join (None or LineJoin): The way the corners of the previous line should be styled.
        fill (bool): If the Shape should be filled with a color.
        fill_color (None or str): The string representation of the fill color.

    """

    line = True
    line_color = None
    line_width = None
    line_join = None

    fill = False
    fill_color = None

    def __call__(self, shape):
        """Combines self with the provided shape into a Drawable StyledShape instance.

        Args:
            shape (Shape): The Shape to be styled.

        Returns:
            StyledShape: The resulting StyledShape.

        """
        return StyledShape(shape, self)

    def draw(self, shape):
        """Turns the provided shape into a pgf/tikz string given the configuration in self.

        Args:
            shape (Shape): The Shape to be processed.

        Returns:
            str: The pgf/tikz representation of the styled shape.

        Raises:
            AssertionError: Whenever the fill attribute is true, but the Shape not a ClosedShape.

        """
        if self.fill:
            assert isinstance(shape, ClosedShape)

        if not self.line:
            if self.fill:
                return f"\\fill[{self.fill_color}] {shape};"
            if not self.fill:
                return ""

        if self.line:

            options = []
            if self.line_color:
                options.append(self.line_color)
            if self.line_width:
                options.append(self.line_width.value)
            if self.line_join:
                options.append(f"line join={self.line_join.value}")
            if self.fill:
                options.append(f"fill={self.fill_color}")
            options = f"[{', '.join(options)}]" if options else ""

            return f"\\draw{options} {shape};"


class Path(Shape, Transformable, AbstractList):
    """A Path is an AbstractList of Vectors that evaluate into a path."""

    def __str__(self):
        """Implements the __str__ method from Shape."""
        return " -- ".join(str(v) for v in self)

    def apply(self, transformation):
        """Implements the apply method from Transformable."""
        self._list = [transformation(v) for v in self._list]

    def copy(self):
        """Implements the copy method from Transformable."""
        return Path(self._list.copy())


class ClosedPath(Path, ClosedShape):
    """Identical to a Path, except that the last vector is linked to the first vector in the AbstractList."""

    def __str__(self):
        """Implements the __str__ method from Shape."""
        return super().__str__() + " -- cycle"

    def copy(self):
        """Implements the copy method from Transformable."""
        return ClosedPath(self._list.copy())


class Circle(ClosedShape, Transformable):
    """A Circle is a ClosedShape that consists of a Transformable center and a nontransformable radius.

    Args:
        center (VectorType or VectorLike): The center of the circle.
        radius (int or float): The radius of the circle.

    Attributes:
        center (VectorType or VectorLike): The center of the circle.
        radius (int or float): The radius of the circle.

    """

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def __str__(self):
        """Implements the __str__ method from Shape."""
        return f"{self.center} circle ({self.radius})"

    def apply(self, transformation):
        """Implements the apply method from Transformable."""
        self.center = transformation(self.center)

    def copy(self):
        """Implements the copy method from Transformable."""
        return Circle(self.center, self.radius)
