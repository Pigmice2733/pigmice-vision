#!/usr/bin/env python
"""Test the functions in the lib/config file."""

from context import lib  # flake8: noqa
from lib.config import Config
import tempfile
import pytest


@pytest.yield_fixture(autouse=True)
def run_around_tests():
    # Code that will run before each test, as we need to
    # set the configuration to an empty dictionary:
    global empty_config
    empty_config = Config(None, {})

    # A test function will be run at this point
    yield

    # Code to run after each test, goes here:


def test_get_default_default():
    "Without previously setting a value, the get_default should return a default."
    global empty_config
    assert empty_config.get_default('foo', 'bar', 'blah') == 'blah'


def test_get_and_set():
    global empty_config
    assert empty_config.set('foo', 'bar', 42) == 42
    assert empty_config.get('foo', 'bar') == 42


def test_get_and_no_set():
    global empty_config
    with pytest.raises(KeyError):
        assert empty_config.get('foo', 'bar')


def test_get_and_set_default():
    global empty_config
    assert empty_config.get_default('foo', 'ding', 'bing-bing') == 'bing-bing'
    assert empty_config.set('foo', 'ding', 42) == 42
    assert empty_config.get_default('foo', 'ding', 'badda-bing') == 42


def test_save():
    "Tests that we don't get an exception if we try to save a configuration file"
    tf = tempfile.NamedTemporaryFile(suffix='.yaml')
    c = Config(tf.name, {'foo':42, 'bar': 71})
    c.save()


def test_save_and_load():
    # Load an configuration file:
    c = Config("tests/test_config.yaml")
    print(c.params)

    assert c.params['channel'] == 1
