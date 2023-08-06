from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# extract version
path = path.realpath("mpl_playback/_version.py")
version_ns = {}
with open(path, encoding="utf8") as f:
    exec(f.read(), {}, version_ns)
version = version_ns["__version__"]

name = "mpl-playback"

setup_args = dict(
    name=name,
    version=version,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.3",
    ],
    author="Ian Hunt-Isaak",
    author_email="ianhuntisaak@gmail.com",
    license="BSD 3-Clause",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Matplotlib"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Jupyter",
        "Framework :: Matplotlib",
    ],
    url="https://github.com/ianhi/mpl-interactions",
    extras_require={
        "doc": [
            "sphinx>=1.5",
            "sphinx-copybutton",
            "sphinx_gallery",
        ],
        "test": [
            "black",
        ],
    },
)

if __name__ == "__main__":
    setup(**setup_args)
