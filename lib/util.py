#!/usr/bin/env python

"""Small collection of 'static' utility functions."""

import cv2
import numpy as np
import time


def has_pressed(key, letter):
    """
    Compare a key pressed with an expected letter. The 'key' is a value from
    calling 'cv2.waitKey()'.
    """
    return key & 0xFF == ord(letter)


def is_pressed(letter):
    """
    Read the keyboard and compare a key pressed with an expected letter.
    Note: This function waits for a key press before returning control.
    """
    key = cv2.waitKey(0)
    return has_pressed(key, letter)


def is_pressing(letter):
    """
    Read the keyboard and compare a key pressed with an expected letter.
    Note: This function returns `false` immediately if no key was pressed,
    so use this function in a loop.
    """
    key = cv2.waitKey(1)
    return has_pressed(key, letter)


def calibration(filename="calibration-values.npz"):
    """Returns the camera matrix, distortion, and optimal camera
    matrix values from the callibration file created by the script,
    `camera_calibrator.py`.

    To use this function, call it, and then call `undistort`, like:
    mtx, dist, newcammtx = calibration('calibration-values.npz')
    newimage = cv2.undistort(img, mtx, dist, None, newcammtx)
    """
    cal = np.load(filename)
    return cal["mtx"], cal["dist"], cal["newcammtx"]


def get_video(channel=1):
    """
    Returns a camera frame. This should be called once at the
    beginning of your program, and the results are passed to
    most other functions in this module.
    """
    # initialize the camera and grab a reference to the raw camera capture
    camera = cv2.VideoCapture(channel)
    # allow the camera to warmup
    time.sleep(0.1)

    # If you need to flip the camera view (camera needs to be upside down
    # include:
    #    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
    #    frame = cv2.flip(frame,0)
    #    out.write(frame)

    width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)

    return [camera, width, height]


def get_hsv(camera):
    """
    Grab a frame and convert to hsv.
    """
    grabbed, img = camera.read()
    # h, w, c = frame.shape
    # width = 600
    # height = int((w/600)*h)

    # frame = cv2.resize(frame, (width, height))

    # convert to HSV color space
    blurred = cv2.GaussianBlur(img, (11, 11), 0)
    hsv_img = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    return hsv_img, img
