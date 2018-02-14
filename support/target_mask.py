#!/usr/bin/env python
"Displays window masked with a target color."

import cv2
import argparse
from context import lib  # flake8: noqa
from lib.color_mask import load_range, color_range
from lib.util import has_pressed


def get_frame(cap, scaling_factor):
    """
    Captures the input frame from webcam.
    """
    ret, frame = cap.read()
    # Resize the input frame
    frame = cv2.resize(frame, None,
                       fx=scaling_factor,
                       fy=scaling_factor,
                       interpolation=cv2.INTER_AREA)
    return frame


def run_mask(capture_channel, data_file):
    """
    Only displays colors in a determined range of the most frequent colors in
    video feed.
    """
    cap = cv2.VideoCapture(capture_channel)
    # Video Capture from 1 (external usb camera), use 0 for built in camera
    scaling_factor = 0.5
    lower, upper = load_range(data_file)

    while True:
        # Check if the user pressed ESC key
        key = cv2.waitKey(1)
        if has_pressed(key, 'q'):
            break

        frame = get_frame(cap, scaling_factor)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Convert the HSV colorspace

        # If "c" is pressed recall color_range function to mask again
        if has_pressed(key, 'c'):
            lower, upper = color_range(hsv)
            print("lower", lower, "upper", upper)

        mask = cv2.inRange(hsv, lower, upper)
        # mask image with range of colors given from the color_range function

        res = cv2.bitwise_and(frame, frame, mask=mask)
        res = cv2.medianBlur(res, 5)

        cv2.imshow('Original image', frame)  # Show the orginal image
        cv2.imshow("Mask", mask)  # masked object in black and white
        cv2.imshow('Color Detector', res)  # Show image with completed mask

    cv2.destroyAllWindows()


if __name__ == '__main__':  # If ran on terminal:
    PARSER = argparse.ArgumentParser(description=__doc__)
    PARSER.add_argument('-p', '--channel', default=1, type=int,
                        help='the USB channel containing camera, 0, 1, or 2')
    PARSER.add_argument('-f', '--datafile', default=".color_range.json",
                        help='the file name to load the color range values')
    ARGS = PARSER.parse_args()

    print("""
    Place the target in front of the camera, and notice that if the
    `color_calibration.py` successfully isolated the target's color range,
    you should only see the target in the display.

    Press the 'c' to re-calibrate the color range from the image shown.

    Press the 'q' key to quit.
    """)

    run_mask(ARGS.channel, ARGS.datafile)
