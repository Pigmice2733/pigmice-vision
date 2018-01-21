#!/usr/bin/env python
"Test the static functions in the lib/util file."

from context import lib  # flake8: noqa
from lib import util


def test_has_pressed_a():
    "has_pressed 'a' should return True."
    assert util.has_pressed(97, 'a')
    assert not util.has_pressed(98, 'a')


def test_has_pressed_stripped():
    "has_pressed with high keycodes should be stripped."
    assert util.has_pressed(0x2061, 'a')
