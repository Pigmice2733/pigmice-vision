#!/usr/bin/env python

"""
Interface to our configuration system. To use, instantiate the Config class:

    conf = Config()

By default, the `.pigmice-config.yaml` file is read and configuration values
stored in that file are available through the params dictionary:

    config.params['channel']

Values nested within the YAML file are available as nested subdictionaries,
for instance, the YAML file:

    channel: 1
    color:
      lower: [70, 86, 6]
      upper: [90, 255, 255]

Allows us to read:

    config.params['color']['lower']

The `get` (or `get_default`) are convenience functions to retrieve values
that may be deeply nested. For instance:

    config.get('channel')

Is the same as:

    config.params['channel']

This helper function is more useful when accessing sub-dictionarys
(where a key in the params dictionary is itself a dictionary):

    config.get('foo', 'bar', 'baz')

Is the same as:

    config.params['foo']['bar']['baz']

Set a value where the parameters list a series of nested keys, as in:

    config.set('color', 'lower', [12, 43, 52])

Notice the last parameter is the value to set!
"""

import yaml
from os.path import expanduser, exists
from functools import reduce
from operator import getitem


class Config:
    # All configuration parameters are stored in this dictionary:
    params = {}

    def __init__(self, filename=None, defaults={}):
        """
        Create a new configuration instance by optionally specifying a YAML
        file containing the configuration values, or specifying those defaults
        as a dictionary.
        """
        self.params = defaults

        # The _default_ configuration file name (if never specified) should be
        # in the HOME directory (since it is computer-specific). We use the
        # `expanduser` function to convert ~ to the actual home directory:
        if filename:
            self.config_file = filename
        else:
            self.config_file = expanduser("~/.pigmice-config.yaml")
        self.load()

    def load(self):
        """
        Read the YAML configuration file specified when this was instantiated.
        Note: Specific configuration values from the file overwrite existing
        values, but existing values are not automatically removed. For
        instance, if the original params was:

            { 'foo': 42,
              'bar': 71
            }

        And the YAML configuration file contained:

            bar: 72
            baz: 11

        Then the resulting `params` would be:

            { 'foo': 42,
              'bar': 72,
              'baz': 11
            }
        """
        if exists(self.config_file):
            with open(self.config_file) as infile:
                ps = yaml.load(infile)
                if ps is not None:
                    self.params.update(ps)

    def save(self):
        """
        Creates a YAML configuration file based on the values of the `params`
        dictionary.
        """
        with open(self.config_file, 'w') as outfile:
            yaml.dump(self.params, outfile)

    def get(self, *kvs):
        """
        Instead of accessing the `params` entry directly, you can used this
        _helper_ method where each parameter given is part of the key. For
        instance:

            config.get('channel')

        Is the same as:

            config.params['channel']

        This helper function is more useful when accessing sub-dictionarys
        (where a key in the params dictionary is itself a dictionary):

            config.get('foo', 'bar', 'baz')

        Is the same as:

            config.params['foo']['bar']['baz']
        """
        # Keep in mind, the parameter `kvs` is really a list of all the
        # parameters we give it, for instance, calling:
        #     config.get('a', 'b', 'c')
        # Means that `kvs` is ['a', 'b', 'c']

        # Because this can take an optional number of parameters, Python
        # will allow us to call it with no parameters...however, this does
        # not make sense, so if we forget to call it with some key, then
        # we should throw an exception.
        if len(kvs) < 1:
            raise ValueError("config.get requires a `key` as an argument")

        # Walk down the dictionary keys using the magical `reduce` function.
        # Reduce functions take applies a function to every item in a list
        # (in this case, we _apply_ `getitem` to each parameter we are
        # given). The `getitem` is given two values, one parameter as well
        # as a _current dictionary_ to look things up in. This dictionary
        # changes as it goes along, beginning with the entire dictionary,
        # but then returning each subdictionary (based on the current key we
        # are looking at) until we are left with either the value in the
        # dictionary, or None if not found.
        return reduce(getitem, kvs, self.params)

    def get_default(self, *kvs):
        """
        Searches the configuration dictionary where the keys are specified as
        parameters. If the parameter of keys do not refer to a value in
        dict, this returns the _last parameter_ specified. For instance:

            lower = config.get_default('color', 'white', 'lower', [0,0,0])

        """
        # Because this can take an optional number of parameters, we throw an
        # exception if we are not given one key, and a default value:
        if len(kvs) < 2:
            raise ValueError("config.get_default requires a `key` and a "
                             "default value, as arguments")

        default_value = kvs[-1]  # The last parameter given

        try:
            return self.get(*kvs[:-1])    # All parameters but the last one
        except KeyError:
            return default_value

    def set(self, *kvs):
        """
        Set a value where the parameters list a series of nested keys, as in:

            config.set('color', 'white', 'lower', [12, 43, 52])

        Notice the last parameter is the value to set!
        """
        if len(kvs) < 2:
            raise ValueError("config.set takes at least two arguments, "
                             "key and value.")

        value = kvs[-1]  # The last parameter given is the value
        keys = kvs[:-1]  # Everything before the last parameter are keys

        # The _real work_ is done in this helper function that just
        # needs to get a good start with initial parameters:
        return self._setter(self.params, keys, value)

    def _setter(self, dc, keys, value):
        """
        This is a _recursive_ helper function for the `set` method.
        We call it with a dictionary, a list of keys and a value, where
        the dictionary _begins_ as our `params` dictionary, as in:

            _setter(params, ['foo', 'bar'], 42)

        If `params` is an empty dictionary, e.g. {}, we need to set it to:

            params = {
              'foo': {
                'bar': 42
              }
            }

        To create dictionaries _inside_ other dictionaries, we _walk_ inside
        the top dictionary down a level (creating a subdirectory if one
        doesn't exist), but _call this function again, but this time with
        the current level. When a function calls itself with slightly
        different parameters, we call this function _recursive_ (think of
        the definition of factorial).

        To do this, we look at the first member in `keys`, (in this case,
        `foo`), and check to see if it exists in our dictionary. If the key
        isn't set, we need to have the value of `foo` be a dictionary, so we
        would need to do something like:

            params['foo'] = {}

        At this point, we call ourselves again, but this time with the
        subdictionary, and one less key from our list. Of course, when we
        reach the _bottom_ of the list, we don't create a dictionary, we
        just set the value.
        """
        key = keys[0]  # First entry in keys is our _current key_

        # No more keys to process? Set the value and leave.
        if len(keys) == 1:
            dc[key] = value
            return value

        # If the key doesn't refer to a sub-dictionary, then we just
        # create one:
        if key not in dc:
            dc[key] = {}

        # Call our helper function again, but this time, with a smaller
        # part of both the dictionary, as well as one fewer key:
        return self._setter(dc[key], keys[1:], value)
