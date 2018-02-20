#!/usr/bin/env python
"""Test the functions in the lib/graph file.

This test program can also run as a stand-alone application
to demonstrate visually how the smooth function can work.
"""

from context import lib  # flake8: noqa
from lib import config
import json
import tempfile
import pytest


@pytest.yield_fixture(autouse=True)
def run_around_tests():
    # Code that will run before each test, as we need to
    # set the configuration to an empty dictionary:
    config.__configuration = config.recursivedict()

    # A test function will be run at this point
    yield

    # Code to run after each test, goes here:


def test_get_default_default():
    "Without previously setting a value, the get_default should return a default."
    assert config.get_default('foo', 'bar', 'blah') == 'blah'


def test_get_and_set():
    assert config.set('foo', 'bar', 42) == None
    assert config.get('foo', 'bar') == 42


def test_get_and_no_set():
    assert config.get('foo', 'bar') == None


def test_get_and_set_default():
    assert config.get_default('foo', 'ding', 'bing-bing') == 'bing-bing'
    assert config.set('foo', 'ding', 42) == None
    assert config.get_default('foo', 'ding', 'badda-bing') == 42


def test_values_simple_dict():
    "Make sure the ``values`` function returns a simple dictionary by default."
    d = config.values()
    assert isinstance(d, dict)
    assert d == {}


def test_save():
    config.__configuration['bob']['dog'] = 42
    tf = tempfile.NamedTemporaryFile(suffix='.json')
    config.save(tf.name)
    with open(tf.name, "r") as infile:
        d = json.load(infile)
        assert d == {'bob': {'dog': 42}}


def test_save_and_load():
    config.__configuration['bob']['dog'] = 42
    tf = tempfile.NamedTemporaryFile(suffix='.json')
    config.save(tf.name)

    # Reset the configuration:
    config.__configuration = config.recursivedict()
    config.load(tf.name)

    assert config.__configuration['bob']['dog'] == 42


def test_get_regular_dictionary():
    config.__configuration['bob']['dog']['foo'] = 'bar'
    assert config.get('bob', 'dog') == {'foo': 'bar'}


if __name__ == '__main__':
    unittest.main()
