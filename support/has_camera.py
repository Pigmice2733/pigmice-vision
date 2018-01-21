#!/usr/bin/env python
"""
Simple program to verify we can read from a USB camera.
"""
import argparse
import cv2
from context import lib  # flake8: noqa
from lib.util import is_pressing


def run(channel):
    """
    Start the video capture on the given 'channel' (port). The number we pass
    is the camera number starting with 0 (typically for a built-in camera).
    External cameras are often on 1.
    """
    cap = cv2.VideoCapture(channel)

    while True:
        _, frame = cap.read()  # Capture frame-by-frame

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame', gray)
        if is_pressing('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description=__doc__)
    PARSER.add_argument('-p', '--channel', default=1, type=int,
                        help='the USB channel containing camera, 0, 1, or 2')
    ARGS = PARSER.parse_args()

    print("""
    This program reads image frames from a connected camera, converts them to
    gray-scale, and displays them in a window. Call this program with a
    `--channel` option with a number. The number we pass is the camera number
    starting with 0 (typically for a built-in camera). External cameras are
    often on 1.

    Press 'q' to quit and close the window.
    """)

    run(ARGS.channel)
