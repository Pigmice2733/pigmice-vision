#!/usr/bin/env python
"Create calibration values file by imaging a checkerboard pattern"

import argparse
import numpy as np
import cv2                       # pylint: disable=import-error
import glob
from context import lib          # flake8: noqa pylint: disable=unused-import
from lib.util import has_pressed # pylint: disable=import-error


# termination criteria
CRITERIA = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


def colorize_image(img, vert_corners=7, horz_corners=6):
    """
    Given an image and an expected number of corners, display an image with
    calculated corners.
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (vert_corners,horz_corners), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        corners2=cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), CRITERIA)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (vert_corners,horz_corners), corners2, ret)
    cv2.imshow('img', img)


def run_with_images(images, rows, columns):
    """
    Given one or more filenames of images or patterns for images, e.g. *.jpg,
    this will display each image with calibration corners on checkerboards
    found. Note: these need to have to correct number of rows and columns
    specified.
    """
    for i in images.split():  # images is a string, split on spaces
        images = glob.glob(i) # substitute * as a wildcard
        for fname in images:
            img = cv2.imread(fname)
            colorize_image(img, rows-1, columns-1)
            key = cv2.waitKey(15000) # Wait 15 seconds or until a key is pressed
    cv2.destroyAllWindows()


def run_with_video(channel, rows, columns):
    """
    Read a video feed from the given channel, and attempt to display the
    checkboard image seen.
    """
    cap = cv2.VideoCapture(channel)
    key = 0

    while not has_pressed(key, 'q'):
        ret, frame = cap.read() # Capture frame-by-frame
        colorize_image(frame, rows-1, columns-1)
        key = cv2.waitKey(1)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description=__doc__)
    PARSER.add_argument('-i', '--images', default='samples/checkerboard-*',
                        help='images separated by spaces or a glob pattern')
    PARSER.add_argument('-p', '--channel', default=-1, type=int,
                        help='the USB channel containing camera, 0, 1, or 2')
    PARSER.add_argument('-r', '--rows', default=10, type=int,
                        help='the number of expected rows on our checkerboard pattern')
    PARSER.add_argument('-c', '--columns', default=13, type=int,
                        help='the number of columns expected on our checkerboard pattern')

    ARGS = PARSER.parse_args()

    print("""
    If displaying a video feed (by specifying the port number with `--channel`),
    the camera image should be displayed as soon as it recognizes a checkerboard
    pattern with {} rows and {} columns. Press the 'q' key to quit.

    Otherwise, it attempts to display some images given with the `--images` option.
    If this option isn't specified, default images will be displayed as an example.

    *Note:* The keys must be pressed with the image window is the foremost
    window, otherwise, you can cancel this application with Control-C.
    """.format(ARGS.rows, ARGS.columns))

    if (ARGS.channel >= 0):
        run_with_video(ARGS.channel, ARGS.rows, ARGS.columns)
    else:
        run_with_images(ARGS.images, ARGS.rows, ARGS.columns)
