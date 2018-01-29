from networktables import NetworkTables
from networktables.util import ntproperty
import time


NetworkTables.initialize(server='127.0.0.1')

class VisionClient(object):
    '''Demonstrates an object with magic networktables properties'''
    numcubes = ntproperty('/pigmicevsion/numcubes', 0)
c = VisionClient()


i = 0
while True:
    print("numcubes",i)
    c.numcubes = i
    time.sleep(1)
    i += 1
