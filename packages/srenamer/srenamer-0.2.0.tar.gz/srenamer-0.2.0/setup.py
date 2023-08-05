import codecs
import os
from setuptools import find_packages, setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="srenamer",
    version=get_version("srenamer/__init__.py"),
    description="This is a simple file renamer for TV shows and anime.",
    author="Maxim Makovskiy",
    author_email="makovskiyms@gmail.com",
    url="https://github.com/evorition/srenamer",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=["tmdbsimple", "click"],
    entry_points={"console_scripts": ["srenamer=srenamer.srenamer:cli"]},
    python_requires=">=3.6",
)
