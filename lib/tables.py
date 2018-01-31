"""
An interface to the NetworkTables service
"""

from networktables import NetworkTables
import time

# We store a reference to the NetworkTables interface
# in this global variable:
table = None
verbose = False


def setup(server, name='vision', printtoo=False):
    """
    Configures and connects to a NetworkTables service running
    on the server given (an IP address, typically). It then
    connects to the table given by `name`.
    """
    # Need to tell Python we wish to modify this `table`
    # global variable:
    global table, verbose
    verbose = printtoo

    # Step 1. Initiate the connection. These always pass:
    NetworkTables.initialize(server=server)
    table = NetworkTables.getTable(name)
    time.sleep(1)
    return table


def _print(message):
    """
    Prints the message to the console if the `verbose` variable has
    been set to True.
    """
    if verbose:
        print(message)


def send(key, value):
    """
    Sends a value to the NetworkTables service under the `key`
    name. It also prints the value if the debug option is given.
    """
    global table, verbose
    try:
        #if table:
            table.putValue(key, value)
    except Exception as e:
        print("ERROR: {0}".format(e))

    finally:
        _print("  - {0}: {1}".format(key, value))
