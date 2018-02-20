#!/usr/bin/env python
"""
Interface to our configuration system. Typically, one would just call
``get`` and ``set``, as in:

    import config

    # Notice the last parameter is the value to set!
    config.set('color', 'white', 'lower', [12, 43, 52])
    config.set('color', 'white', 'upper', [24, 124, 250])

And:

    lower = config.get('color', 'white', 'lower')

Or, if the value isn't set, call the ``get_default`` function:

    # Notice the last parameter to function is the default value:
    lower = config.get_default('color', 'white', 'lower', [0,0,0])
"""

from collections import defaultdict
from functools import reduce
from os.path import expanduser
import operator
import json

DEFAULT_CONFIG_FILE=expanduser("~/.pigmice-config.json")


def values():
    """
    Return all configuration values as a dictionary. For instance:

        config.values()['color']['white']

    See ``get`` as an alternative approach for searching deeply nested values.
    """
    global __configuration
    return to_dict(__configuration)


def get(*kvs):
    """
    Searches the configuration dictionary where the keys are specified as
    parameters. Walks _into_ the dict using the magical ``reduce`` function. If
    the parameter of keys do not refer to a value in dict, this returns None.
    """
    if len(kvs) < 1:
        raise ValueError("config.get requires a `key` as an argument")

    # If values haven't been loaded from the default place, load them:
    data = __get_configuration_dict()
    # Find the value buried in the data structure we loaded from disk:
    value = reduce(operator.getitem, kvs, data)

    if value == {}:
        return None
    elif isinstance(value, defaultdict):  # TODO
        return to_dict(value)
    else:
        return value


def get_default(*kvs):
    """
    Searches the configuration dictionary where the keys are specified as
    parameters. If the parameter of keys do not refer to a value in dict, this
    returns the _last parameter_ specified. For instance:

        lower = config.get_default('color', 'white', 'lower', [0,0,0])
    """
    if len(kvs) < 2:
        raise ValueError("config.set takes at least two arguments, key and value.")

    default_value = kvs[-1]  # The last parameter given
    value = get(*kvs[:-1])    # All parameters but the last one

    if value != None:
        return value
    else:
        return default_value


def set(*kvs):
    """
    Set a value where the parameters list a series of nested keys, as in:

         config.set('color', 'white', 'lower', [12, 43, 52])

    Notice the last parameter is the value to set!
    """
    if len(kvs) < 2:
        raise ValueError("config.set takes at least two arguments, key and value.")

    global __configuration

    value = kvs[-1]  # The last parameter given
    key = kvs[-2]
    rest = kvs[:-2]

    if rest == []:
        __configuration[key] = value
    else:
        subdict = reduce(operator.getitem, rest, __configuration)
        subdict[key] = value


# This bit of magic makes a dictionary that is able to set aribtrarily
# deep keys without defining the values before. For instance:
#    >>> __configuration['color']['white'] = 42
# Works as expected, so this works too:
#    >>> __configuration['color']['white']
#    42
# See the long discussion on this thread: https://is.gd/KEOROq
recursivedict = lambda: defaultdict(recursivedict)  # flake8: noqa E731


def to_dict(rd):
    "Convert a recursivedict into a regular dict"
    newdict = {}
    __dict_merge(newdict, rd)
    return newdict


# Note: This system breaks all good convention in the name of ease-of-use.
#       It stores all configuration values in a global variable.
__configuration = recursivedict()
__configuration['loaded'] = False


def __get_configuration_dict(filename=DEFAULT_CONFIG_FILE):
    """
    If the default configuration file has not been loaded, then load and parse
    it before returning a reference to the configuration data structure.
    """
    global __configuration

    if not __configuration['loaded']:
        load(filename)

    return __configuration


def load(filename=DEFAULT_CONFIG_FILE):
    """
    Reads the configuration file as a JSON-formatted file.
    It merges the values with the current settings (if any)

    """
    global __configuration

    try:
        with open(filename, 'r') as infile:
            updates = json.load(infile)
            print("Read", updates)
            __dict_merge(__configuration, updates)
            __configuration['loaded'] = True
    except Exception:
        pass


def save(filename=DEFAULT_CONFIG_FILE):
    """
    Saves the current configuration values into a file. Note, that this
    overwrites specific settings, but does not remove old values. For instance,
    suppose the

    """
    global __configuration

    # Make a copy of the configuration as we may be replacing parts:
    bothdicts = __configuration.copy()

    try:
        with open(filename, 'r') as infile:
            stored_vals = json.load(infile)
            __dict_merge(bothdicts, stored_vals)

            # To make sure we didn't override anything important, Let's put the
            # current configuration back in, but on top of whatever we read in:
            __dict_merge(bothdicts, __configuration)
            bothdicts['loaded'] = True
    except Exception:
        pass

    with open(filename, 'w') as outfile:
        json.dump(bothdicts, outfile)


def contains(key):
    """
    Default values for our _recursive dictionary_ is an empty hash, so this
    function makes our conditionals easier to read.
    """
    return __configuration[key] == {}


def __dict_merge(dct, merge_dct):
    """
    Recursive dictionary merge. Instead of updating only top-level keys,
    __dict_merge recurses down into sub-dicts nested to an arbitrary depth,
    updating keys. The ``merge_dct`` is merged into ``dct``.

    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            __dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]
