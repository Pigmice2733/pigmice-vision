#!/usr/bin/env python
"""
Find the color range of our target object.
"""

import cv2
from context import lib
from lib.color_range import color_range
import json
import argparse

def save_range(filename, data):
    with open(filename, data) as outfile:
        json.dump(data, outfile)

def run(channel, filename):
    camera = cv2.VideoCapture(channel)
    while True:
        success, image = camera.read()
        if success:
            cv2.imshow("image", image)
        key = cv2.waitKey(1)
        if has_pressed(key, 'q'):
            break
        if has_pressed(key, 'c') and success:
            cv2.imwrite("../support/samples/cube1.jpg", img)
            r = color_range(image)
            save_range(filename, r)


if __name__ == '__main__':
    print("""Place the target in front of the camera so the target
    fills the camera image. Press the 'c' to capture the image.
    This writes a JSON file containing the color range, used by the
    color mask function.
    """)
    PARSER = argparse.ArgumentParser(description=__doc__)
    PARSER.add_argument('-p', '--channel', default=1, type=int,
                        help='the USB channel containing camera, 0, 1, or 2')
    PARSER.add_argument('-s', '--savefile', default="color_range.JSON",
                        help='the file name to save the color range values')
    ARGS = PARSER.parse_args()

    run(ARGS.channel, ARGS.savefile)
