#!/bin/env python3
#
#   Copyright © 2021 Simó Albert i Beltran
#
#   This file is part of MkDocs i18n plugin.
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

"""PyPI Version Check"""

import logging
import sys

import click
import click_log
import pkg_resources
import requests

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


def main(pypi_urls=None):
    """Check if PyPI has the current version of the package

    :param pypi_url: PyPI URL to check published versions
    :type pypi_url: str
    :rtype: bool
    :return: False if there isn't any distribution published with its specific version.
        True if there is a distribution published or unexpected error.
    """
    if not pypi_urls:
        pypi_urls = ["https://pypi.org"]
    found = False
    for distribution in pkg_resources.find_distributions("."):
        found = True
        name = distribution.project_name
        version = distribution.version
        logger.debug("Package %s with version %s found", name, version)
        for pypi_url in pypi_urls:
            request = requests.get(f"{pypi_url}/pypi/{name}/json")
            if request.status_code == 404:
                logger.warning("Package %s not found in PyPI", name)
            elif request.status_code == 200:
                if version in request.json()["releases"].keys():
                    logger.error(
                        "PyPI has the version %s for %s",
                        version,
                        name,
                    )
                    return True
                logger.info("PyPI hasn't the version %s for %s", version, name)
            else:
                logger.error("PyPI returns %s as status_code", request.status_code)
                return True
    if not found:
        logger.error("Distribution not found")
        return True
    return False


@click.command()
@click_log.simple_verbosity_option(logger)
@click.argument("pypi_url", nargs=-1)
def cli(pypi_url=None):
    """Tool to check if PyPI publishes the current package version.

    See also https://gitlab.com/pypi-version-check/pypi-version-check/"""
    sys.exit(main(pypi_url))


def init():
    """Calls cli function if run module as script"""
    if __name__ == "__main__":
        cli()


init()
