"""
An interface to the NetworkTables service
"""

from networktables import NetworkTables
import time

# We store a reference to the NetworkTables interface
# in this global variable:
table = None
verbose = False


def setup(server, name='tracker', printtoo=False):
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

    # Step 2. Wait for an actual connection before proceeding:
    tries = 0

    while not table.isConnected() and tries < 5:
        print("Trying to connect to: {0}".format(server))
        tries = tries + 1
        time.sleep(1)

    # Step 3. If we still can't connect, the library will continue to
    # try and connect, so we might as well return the table and get
    # going.   NOTE: IS THIS A VALID ASSUMPTION!?
    return table


def _print(message):
    """
    Prints the message to the console if the `verbose` variable has
    been set to True.
    """
    if verbose:
        print(message)


def send(key, value, table=table):
    """
    Sends a value to the NetworkTables service under the `key`
    name. It also prints the value if the debug option is given.
    """
    try:
        if table:
            if isinstance(value, str):
                table.putString(key, value)
            else:
                table.putNumber(key, value)
    except Exception as e:
        print("ERROR: {0}".format(e))

    finally:
        _print("  - {0}: {1}".format(key, value))
