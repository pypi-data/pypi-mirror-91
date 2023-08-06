#!/bin/env python3
# -*- coding: utf-8 -*-
#
#   Copyright © 2021 Simó Albert i Beltran
#
#   This file is part of PyPI Version Check.
#
#   Mkdocs i18n plugin is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or (at your
#   option) any later version.
#
#   Foobar is distributed in the hope that it will be useful, but WITHOUT ANY
#   WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#   FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
#   details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with MkDocs i18n plugin. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later

""" Setup for PyPI Version Check """

import pathlib

import setuptools

here = pathlib.Path(__file__).parent.resolve()

setuptools.setup(
    name="pypi-version-check",
    version="0.0.0",
    description="PyPI Version Check",
    long_description=(here / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/pypi-version-check/pypi-version-check",
    author="Simó Albert i Beltran",
    author_email="sim6@bona.gent",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Affero General Public License v3 or "
        "later (AGPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="pypi",
    packages=setuptools.find_packages(),
    python_requires=">=3.7, <4",
    install_requires=["click", "click-log", "requests"],
    extras_require={
        "test": [
            "isort",
            "black",
            "bandit",
            "flake8",
            "pylint",
            "mamba",
            "expects",
            "coverage",
        ],
    },
    entry_points={
        "console_scripts": [
            "pypi-version-check = pypi_version_check.__main__:cli",
        ],
    },
    project_urls={
        "Bug Reports": "https://gitlab.com/pypi-version-check/"
        "pypi-version-check/-/issues",
        "Funding": "https://liberapay.com/sim6/donate",
        "Source": "https://gitlab.com/pypi-version-check/"
        "pypi-version-check/-/tree/master",
    },
    license="AGPL-3.0-or-later",
)
