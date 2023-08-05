import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="plot_ann",
    version="1.0.1",
    description="Plot an Artificial Neural Network (ANN) model",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Marco Necci",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=["matplotlib", "numpy"],
)