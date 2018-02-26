"An interface to the NetworkTables service"
from networktables import NetworkTables
import time

__table = None
__verbose = False


def _print(message):
    """
    Prints the message to the console if verbose = True.
    """
    if __verbose:
        print(message)


def setup(server, name='vision', printtoo=True):
    """
    Configures and connects to a NetworkTables service running
    on the server given (typically an IP address).
    It then connects to the table given by `name`.
    """
    global __table, __verbose
    __verbose = printtoo

    # Initiates the connection, but won't say if it has connected.
    NetworkTables.initialize(server=server)

    __table = NetworkTables.getTable(name)

    while __table.getValue("status", None) is not "connecting":
        send_status("connecting")
        time.sleep(0.5)
        _print("Connecting...")

    send_status("connected")
    return __table


def send(key, value):
    """
    Sends a value to the NetworkTables.
    """
    try:
        if __table:
            __table.putValue(key, value)
            _print("  - {0}: {1}".format(key, value))
        else:
            msg = "Not connected to NetworkTables server. Run setup() first."
            raise Exception(msg)
    except Exception as e:
        print("ERROR: {0}".format(e))


def send_status(message="connected"):
    """
    Sends the NetworkTables connections status.
    """
    send("status", message)


def send_target(distance, angle):
    """
    Places the target's direction and angle in the NetworkTables.
    Note: this may change based on what we want to send.
    """
    send("target-distance", distance)
    send("target-angle", angle)
