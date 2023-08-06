#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Command Line Interface."""
from argparse import ArgumentParser
from sys import stderr
from copy import copy

from snap_tam.aggregate_filesystem import run


def _required_fields(parser):
    """Add required fields to parser.

    Args:
        parser (ArgumentParser): Argparse object.

    Returns:
        ArgumentParser: Argeparse object.
    """
    return parser


def _optional_fields(parser):
    """Add optional fields.

    Args:
        parser (ArgumentParser): Argparse object.

    Returns:
        ArgumentParser: Argeparse object.
    """
    parser.add_argument(
        '-p', '--onedrive-path', help='Path to OneDrive installation.')

    return parser


def _add_arguments(parser):
    """Add arguments to parser.

    Args:
        parser (ArgumentParser): Argparse object.

    Returns:
        ArgumentParser: Argeparse object.
    """
    parser2 = _optional_fields(parser)
    parser3 = _required_fields(parser2)

    return parser3


def cli():
    """Command line interface for package.

    Side Effects: Executes program.
    """
    prog_desc = 'Aggregate SNaP reports on OneDrive.'
    argeparser = ArgumentParser(description=prog_desc)
    parser = _add_arguments(copy(argeparser))
    args = parser.parse_args()

    try:
        run(onedrive_dir_path=args.onedrive_path)
    except Exception as err:
        print(err, file=stderr)


if __name__ == '__main__':
    cli()
