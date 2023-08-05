#!/usr/bin/env python3

# Copyright (C) 2020-2021 by ÿnérant, eichhornchen, nicomarg, charlse
# SPDX-License-Identifier: GPL-3.0-or-later

import subprocess

from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

# Compile messages
for language in ["de", "es", "fr"]:
    args = ["msgfmt", "--check-format",
            "-o", f"squirrelbattle/locale/{language}/LC_MESSAGES"
                  "/squirrelbattle.mo",
            f"squirrelbattle/locale/{language}/LC_MESSAGES"
            "/squirrelbattle.po"]
    print(f"Compiling {language} messages...")
    subprocess.Popen(args)

setup(
    name="squirrel-battle",
    version="23.14",
    author="ÿnérant, eichhornchen, nicomarg, charlse",
    author_email="squirrel-battle@crans.org",
    description="Watch out for squirrel's knives!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.crans.org/ynerant/squirrel-battle",
    packages=find_packages(),
    license='GPLv3',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console :: Curses",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Games/Entertainment",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    package_data={"squirrelbattle": ["assets/*", "locale/*/*/*.mo"]},
    entry_points={
        "console_scripts": [
            "squirrel-battle = squirrelbattle.bootstrap:Bootstrap.run_game",
        ]
    }
)
