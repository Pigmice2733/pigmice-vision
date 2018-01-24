#!/usr/bin/env python
"Test the static functions in the lib/util file."

from context import lib  # flake8: noqa
from lib import util
import numpy as np
import mock

def test_has_pressed_a():
    "has_pressed 'a' should return True."
    assert util.has_pressed(97, 'a')
    assert not util.has_pressed(98, 'a')


def test_has_pressed_stripped():
    "has_pressed with high keycodes should be stripped."
    assert util.has_pressed(0x2061, 'a')


@mock.patch('numpy.load')
def test_calibration(mock_loader):
    "validates that a calibration file can be analyzed properly."
    # This is a bit complicated for testing ... hopefully, still readable.
    # We want to test the _logic_ in the `calibration` function, specifically
    # that it can return the correct *parts* of Numpy's array collection files
    # (npz). Obviously, we don't care to test Numpy's ability to read and parse
    # files, but we do want to test _our code_.
    #
    # One option could be to create an example data file and have it read it.
    # However, if that file ever gets *munged* (or it could even be used and
    # mess up our readers), so we _mock it_.
    #
    # What that means, is that when our calibration function attempts to call
    # `numpy.load()`, we tell it not to try to read a file, but instead, simply
    # return some values that our test wants. We can then compare what our
    # function does with those results, and we're sure our function behaves
    # correctly. Check out the following web article for more information:
    # https://www.toptal.com/python/an-introduction-to-mocking-in-python

    # The mtx value is an array of arrays, that looks something like:
    mtx = [[894.11909474,  0.0,       641.08311831],
           [  0.0,       895.48860404,342.36986394],
           [  0.0,         0.0,         1.0       ]]
    # The dist is also an array of array, just fewer numbers, like:
    dist = [[ 0.04980364, -0.31822297, -0.00178616, -0.00415542, 0.32718128]]
    # Finally, what we are labeling, newcamera_mtx, is similar to mtx:
    newcam_mtx = [[880.47076416,    0.0,        635.06210301],
                  [  0.0,         879.73077393, 340.85366314],
                  [  0.0,           0.0,          1.0,        ]]

    # If we were to call `np.load` to read a filename, we want it to
    # return values like what we've described above:
    mock_loader.return_value = { 'mtx': mtx, 'newcammtx': newcam_mtx, 'dist': dist }

    # Time to finally call our function to test, calibration:
    ret_mtx, ret_dist, ret_newmtx = util.calibration()

    assert ret_mtx == mtx
    assert ret_dist == dist
    assert ret_newmtx == newcam_mtx
