from networktables import NetworkTables
from networktables.util import ntproperty
import time
import logging

logging.basicConfig(level=logging.DEBUG)
NetworkTables.initialize(server='127.0.0.1')

epoch = -1
i = 0

class VisionClient(object):
    '''Demonstrates an object with magic networktables properties'''
    numcubes = ntproperty('/pigmicevsion/numcubes', [epoch,i], persistent = True)
c = VisionClient()
time.sleep(1)

while True:
    val = c.numcubes
    print("read numcubes as", val)
    netepoch = val[0]
    if netepoch > epoch or netepoch == -1:
        epoch = netepoch + 1
    print("writing numcubes as", epoch,i)
    c.numcubes = [epoch,i]
    time.sleep(1)
    i += 1

""" assign epoch to a value in nt table"""
