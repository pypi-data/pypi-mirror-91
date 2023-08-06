import setuptools

requirements = ["numpy>=1.16"]

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="pytikz",
    version="0.0.1",
    description="pytikz: generate pgf/tikz files with python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pglammers/pytikz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
)
