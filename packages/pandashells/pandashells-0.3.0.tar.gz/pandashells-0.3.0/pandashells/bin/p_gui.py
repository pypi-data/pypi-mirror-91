#! /usr/bin/env python

# standard library imports
import argparse
import importlib
import textwrap

from pandashells.lib import module_checker_lib, arg_lib

module_checker_lib.check_for_modules(['pandas', 'pandasgui'])
from pandashells.lib import io_lib


# # this silly function makes mock testing easier
# def get_imports(name):  # pragma no cover
#     return importlib.import_module(name)


# this silly function helps use side_effect in mocking tests
def get_module(name):  # pragma nocover
    return importlib.import_module(name)


def get_input_args():
    msg = textwrap.dedent(
        """
        Opens the input dataframe in an interactive GUI environment.
        See: https://github.com/adamerose/pandasgui

        -----------------------------------------------------------------------
        Examples:

            * Open a CSV file in pandasgui
                p.example_data -d tips | p.gui

        -----------------------------------------------------------------------
        """
    )

    #  read command line arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=msg)

    arg_lib.add_args(parser, 'io_in')

    return parser.parse_args()


def main():
    pandasgui = get_module('pandasgui')

    # parse arguments
    args = get_input_args()

    # get the input dataframe
    df = io_lib.df_from_input(args)
    pandasgui.show(df)


if __name__ == '__main__':  # pragma: no cover
    main()
