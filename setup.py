from setuptools import setup, find_packages


__author__ = "James King"
__email__ = "james@agentultra.com"
__version__ = "0.1.1"
__license__ = "MIT"


setup(
    name="Horton",
    version=".".join(__version__),
    packages=find_packages(),

    author=__author__,
    author_email=__email__,
    license=__license__,
    description="A library for building grid-based simulations.",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries",
    ]
)
