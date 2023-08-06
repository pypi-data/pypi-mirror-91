import os


def _write_file(file_name, contents):
    """Simple helper function for (over)writing a file_name with contents."""
    with open(file_name, "w") as f:
        f.write(contents)


class Figure:
    """A Figure represents a single pgf/tikz figure, and handles the pgf/tikz string, the files, and the latex processing.

    Args:
        name (str): The filename for the Figure.
        target_directory (None or str): The target directory for the Figure files; default is os.getcwd().

    Attributes:
        name (str): The filename for the Figure.
        target_directory (None or str): The target directory for the Figure files; default is os.getcwd().
        _string (str): The pgf/tikz contents string.

    """

    def __init__(self, name, target_directory=None):
        self.name = name
        default_target_directory = os.getcwd() if os.getcwd() else "."
        self.path_target_directory = (
            target_directory
            if target_directory is not None
            else default_target_directory
        )
        self._string = ""

    def append_string(self, string):
        """Appends the string to the internal pgf/tikz string.

        Args:
            string (str): The string to be appended.

        """
        self._string += string

    def draw(self, drawable):
        """Casts the drawable into a string and appends it to the internal pgf/tikz string.

        Args:
            drawable (Drawable): The drawable to be drawn.

        """
        self.append_string(f"{drawable}\n")

    def path_target_file(self, suffix):
        """Returns the filename of the file described by the suffix.

        Args:
            suffix (str): The name of the file type.

        Returns:
            str: The full path to the file described by suffix.

        """
        return os.path.join(self.path_target_directory, f"{self.name}_{suffix}")

    @property
    def path_data(self):
        """The path to the data tex file.

        Returns:
            str: The path to the data tex file.

        """
        return self.path_target_file("data.tex")

    @property
    def path_include(self):
        """The path to the include tex file.

        Returns:
            str: The path to the include tex file.

        """
        return self.path_target_file("include.tex")

    @property
    def path_standalone(self):
        """The path to the standalone tex file.

        Returns:
            str: The path to the standalone tex file.

        """
        return self.path_target_file("standalone.tex")

    @property
    def contents_data(self):
        """The file contents for the data tex file.

        Returns:
            str: The file contents for the data tex file.

        """
        return self._string

    @property
    def contents_include(self):
        """The file contents for the include tex file.

        Returns:
            str: The file contents for the include tex file.

        """
        return (
            "\\begin{tikzpicture}\n"
            f"\\input{{{self.path_data}}}\n"
            "\\end{tikzpicture}\n"
        )

    @property
    def contents_standalone(self):
        """The file contents for the standalone tex file.

        Returns:
            str: The file contents for the standalone tex file.

        """
        return (
            "\\documentclass[preview]{standalone}\n"
            "\\usepackage{tikz}\n"
            "\\begin{document}\n"
            "\\begin{tikzpicture}\n"
            f"\\input{{{self.path_data}}}\n"
            "\\end{tikzpicture}\n"
            "\\end{document}\n"
        )

    def write_data(self):
        """Writes the data tex file."""
        _write_file(self.path_data, self.contents_data)

    def write_include(self):
        """Writes the include tex file."""
        _write_file(self.path_include, self.contents_include)

    def write_standalone(self):
        """Writes the standalone tex file."""
        _write_file(self.path_standalone, self.contents_standalone)

    def write_all(self, include=False):
        """Writes all of the above files, including the include tex file whenever the include flag is True."""
        self.write_data()
        self.write_standalone()
        self.write_include() if include else None

    def process(self):
        """Calls latexmk to process the standalone tex file."""
        os.system(
            f"pdflatex -output-directory={self.path_target_directory} {self.path_standalone}"
        )
