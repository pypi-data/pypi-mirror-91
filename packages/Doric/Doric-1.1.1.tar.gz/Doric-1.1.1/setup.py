import pathlib
from setuptools import setup, find_packages

from Doric import DORIC_VERSION

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="Doric",
    version=DORIC_VERSION,
    description="Doric is a lightweight library for implementing and extending progressive neural networks.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/arcosin/Doric",
    author="Maxwell J. Jacobson",
    author_email="jacobs57@purdue.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pytorch"],
)

#===============================================================================
