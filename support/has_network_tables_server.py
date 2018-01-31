import time
from context import lib  # flake8: noqa
from lib import tables

tables.setup("localhost")
tables.send("test", "Hello Linnea")
time.sleep(60)

#putValue will differentiate the values
#no need for loop to check connection
