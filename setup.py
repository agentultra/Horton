from setuptools import setup, find_packages


__author__ = "James King"
__email__ = "james@agentultra.com"
__version__ = "0.1.1"
__license__ = "MIT"
__description__ = """
A library of grids and other fine amusements. Contains a Grid and
Grid-like data structures and optional modules for rendering them with
pygame, creating cellular-automata simulations, games, and such
things.
"""


setup(
    name="Horton",
    version=__version__,
    packages=find_packages(),

    install_requires = [
        "sphinx_bootstrap_theme", # for docs
    ],

    extras_require = {
        'pygame': ["pygame"],
    },

    author=__author__,
    author_email=__email__,
    license=__license__,
    description=__description__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Artistic Software",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries",
    ]
)
