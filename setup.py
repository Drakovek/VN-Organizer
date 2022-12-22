#!/usr/bin/env python3

"""
Setuptools setup file.
"""

import setuptools

console_scripts = ["vn-organizer = vn_organizer.vn_organizer_parser:main"]

with open("README.md", "r") as fh:
    long_description = fh.read()

desc = "Utility for keeping track of branches and saves in visual novels or other interactive stories."

setuptools.setup(
    name="vn_organizer",
    version="0.1.0",
    author="Drakovek",
    author_email="DrakovekMail@gmail.com",
    description=desc,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Drakovek/VN-Organizer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.0',
    entry_points={"console_scripts": console_scripts}
)
