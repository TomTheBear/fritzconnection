"""
fritzwlan.py

Module to inspect the FritzBox API for Powerline devices.
CLI interface.

This module is part of the FritzConnection package.
https://github.com/kbr/fritzconnection
License: MIT (https://opensource.org/licenses/MIT)
Author: Thomas Gruber
"""

from fritzconnection import FritzConnection
from fritzconnection.lib.fritzpowerline import FritzPowerline
from fritzconnection.cli.utils import get_cli_arguments, get_instance, print_header


def add_arguments(parser):
    return


def main():
    args = get_cli_arguments(add_arguments)
    if not args.password:
        print('Exit: password required.')
    else:
        fp = get_instance(FritzPowerline, args)
        print_header(fp)


if __name__ == '__main__':
    main()
