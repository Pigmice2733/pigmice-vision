#!/usr/bin/env python
"Make sure we can connect to a NetworkTables server"

from context import lib  # flake8: noqa
from lib import tables
import time
import argparse

def run(server):
    tables.setup(server)
    time.sleep(60)
    print("Whew!")

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description=__doc__)
    PARSER.add_argument('-s', '--server', default="localhost",
                        help='the NetworkTables IP address. Default to local')
    ARGS = PARSER.parse_args()

    print("""
    This program is connecting to server, {}
    Look for a 'status' message.
    """.format(ARGS.server))
    run(ARGS.server)
