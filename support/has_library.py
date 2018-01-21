#!/usr/bin/env python
"""
Simple command to validate that the OpenCV library is installed and working.
"""

# Can we import the OpenCV library, cv2?
# If so, we are almost there ...
import argparse
import cv2
from context import lib  # flake8: noqa
from lib.util import is_pressed


def run(filename):
    """
    Display an image given by `filename`. Press 's' to save it as a
    gray-scaled image.
    """
    img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    cv2.imshow('image', img)

    # Just to show that we can do something special, if the program is quit by
    # pressing the 's' key, we save the image displayed as a gray-scale image
    # by converting both the filename and the pixels:
    if is_pressed('s'):
        # Look for the point where the file extension begins (final period):
        pivot = filename.rfind('.')

        # Use string subscripting to build a new filename, see this web page:
        # https://www.pythoncentral.io/cutting-and-slicing-strings-in-python/
        outfile = filename[:pivot] + '-gray' + filename[pivot:]
        print("    Writing gray-scale to ", outfile)

        newimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(outfile, newimg)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description=__doc__)
    PARSER.add_argument('-i', '--image', default='samples/random-pix.jpg',
                        help='filename of image to display.')
    ARGS = PARSER.parse_args()

    print("""
    This program will display an image in a window on your computer screen...
    unless you don't have the python3 with the OpenCV library installed.  See:
    https://docs.opencv.org/3.4.0/da/df6/tutorial_py_table_of_contents_setup.html

    Press 's' to save the image in gray-scale. Any other key closes the window.
    """)

    run(ARGS.image)
