#!/usr/bin/env python
"""
Find the color range of our target object.
"""

import cv2
from context import lib          # flake8: noqa pylint: disable=unused-import
import json
import argparse
from lib import color_mask
from lib import util


# If true, we can print some extra information (as well save capture images)
DEBUG = False

# Image analyzed for color (when pressing the 'c' key) may be written to this
# file to help with debugging and troubleshooting:
CAPTURE_FILENAME = 'captured-image.jpg'


def save_image(img):
    """
    Saves the image to the default CAPTURE_FILENAME. Since
    this is only for debugging purposes, this only happens
    when the DEBUG flag is set.
    """
    if DEBUG:
        cv2.imwrite(CAPTURE_FILENAME, img)
        print("Wrote file to " + CAPTURE_FILENAME)


def save_data(lower, upper, filename):
    """
    Simple wrapper around the color_'s save_mask()
    function. If DEBUG, this prints extra information.
    """
    if DEBUG:
        print("Saved to {}-- lower: {}  upper: {}".format(filename, lower, upper))
    color_mask.save_range(lower, upper, filename)


def capture_color_range(channel, filename):
    """
    Given a USB channel to a camera, wait for the 'c' key is
    pressed, and calculate the most range of the most
    prominent color found (the range makes this easier to
    figure out a mask). The results are stored in `filename`.
    """
    camera = cv2.VideoCapture(channel)
    while True:
        success, image = camera.read()
        if success:
            cv2.imshow("image", image)

        key = cv2.waitKey(1)
        if util.has_pressed(key, 'q'):
            break

        if util.has_pressed(key, 'c') and success:
            lower, upper = color_mask.color_range(image)
            save_data(lower, upper, filename)
            save_image(image)

    # When everything done, release the capture
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description=__doc__)
    PARSER.add_argument('-p', '--channel', default=1, type=int,
                        help='the USB channel containing camera, 0, 1, or 2')
    PARSER.add_argument('-s', '--savefile', default=".color_range.json",
                        help='the file name to save the color range values')
    PARSER.add_argument('-d', '--debug', action='store_true',
                        help='saves captured image as: ' + CAPTURE_FILENAME)
    ARGS = PARSER.parse_args()

    DEBUG=ARGS.debug

    print("""
    Place the target in front of the camera so the target
    fills the camera image.

    Press the 'c' to capture the image. This writes the
    values containing the color range (used by the
    `color_mask()` function), into the file, {}

    Press the 'q' key to quit.
    """.format(ARGS.savefile))

    capture_color_range(ARGS.channel, ARGS.savefile)
