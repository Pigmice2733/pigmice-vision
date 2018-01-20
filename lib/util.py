#!/usr/bin/env python

"""Small collection of 'static' utility functions."""

import cv2


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
