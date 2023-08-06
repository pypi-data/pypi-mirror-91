# -*- coding: utf-8 -*-

from setuptools import setup

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="arithmeticmeancurve",
    author="David Scheliga",
    author_email="david.scheliga@ivw.uni-kl.de",
    url="https://gitlab.com/david.scheliga/arithmeticmeancurve",
    project_urls={
        "Documentation": "https://arithmeticmeancurve.readthedocs.io/en/latest/",
        "Source Code Repository": "https://gitlab.com/david.scheliga/arithmeticmeancurve",
    },
    description="Module for calculating an arithmetic mean curve from a family of curves.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GNU General Public License v3 (GPLv3)",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
    ],
    keywords="pandas, arithmetic, curve",
    py_modules=["arithmeticmeancurve"],
    python_requires=">=3.6",
    install_requires=["trashpanda>=0.8b0", "pandas", "numpy", "matplotlib", "scipy"],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
)
