from networktables import NetworkTables
from networktables.util import ntproperty
import time

NetworkTables.initialize(server='127.0.0.1')

class VisionClient(object):
    '''Demonstrates an object with magic networktables properties'''
    numcubes = ntproperty('/pigmicevsion/numcubes', 0)
c = VisionClient()


"""def valueChanged(key, value, isNew):
    print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))

NetworkTables.addEntryListener(valueChanged)
"""

while True:
    print(c.numcubes)
    time.sleep(1)
