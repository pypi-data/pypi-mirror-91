#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2019 Christoph Fink, University of Helsinki
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 3
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.

""" Search small ad listings on OLX market places """


import argparse

from .config import (
    Config
)
from .youtubevideometadatadownloader import (
    YouTubeVideoMetadataDownloader
)


def main():
    """ TODO """
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        "-p",
        "--connection-string",
        help="""Store the retrieved data in this database (sqlalchemy-compatible URL)"""
    )

    argparser.add_argument(
        "-a",
        "--youtube-api-key",
        help="""Use this API key for the YouTube Data API v3"""
    )

    argparser.add_argument(
        "-P",
        "--do-not-pseudonymise",
        help="""Keep identifiers in the downloaded dataset""",
        action="store_true"
    )

    argparser.add_argument(
        "search_terms",
        help="""Query the YouTube API for these search terms""",
        nargs='?'
    )

    args = argparser.parse_args()

    _config = {}
    if args.connection_string is not None:
        _config["connection_string"] = args.connection_string
    if args.youtube_api_key is not None:
        _config["youtube_api_key"] = args.youtube_api_key
    if args.do_not_pseudonymise:
        _config["pseudonymise"] = False
    if args.search_terms is not None:
        _config["search_terms"] = args.search_terms

    config = Config(_config)

    YouTubeVideoMetadataDownloader().download()
    del config
