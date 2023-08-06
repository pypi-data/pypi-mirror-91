from enum import Enum


class LineWidth(Enum):
    """Encodes the physical width of a pgf/tikz path on the canvas."""

    ULTRA_THIN = "ultra thin"
    VERY_THIN = "very thin"
    THIN = "thin"
    SEMITHICK = "semithick"
    THICK = "thick"
    VERY_THICK = "very thick"
    ULTRA_THICK = "ultra thick"


class LineJoin(Enum):
    """Encodes the style of the corners of pgf/tikz paths on the canvas."""

    MITER = "miter"
    BEVEL = "bevel"
    ROUND = "round"


class Orientation(Enum):
    """Encodes the different relative orientations that elements on the canvas may have."""

    CENTER = "center"
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    NORTH_EAST = "north east"
    NORTH_WEST = "north west"
    SOUTH_EAST = "south east"
    SOUTH_WEST = "south west"
