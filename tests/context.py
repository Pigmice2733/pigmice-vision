"This module is helping set the import path correctly. No code should go here."

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..')))
import lib  # flake8: noqa
