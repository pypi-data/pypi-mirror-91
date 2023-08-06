import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="nlp_defaults",
    version="0.0.0",
    description="nlp_defaults package",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["nlp_defaults"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)
