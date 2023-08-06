"""
Imports the configuration values for an automation test framework and makes them available for use.
"""
from json import load
from os.path import isfile


class ConfigMeta(type):
    """
    Metaclass for Config.
    """

    # Local path
    _path = "config.json"

    _values = None

    def __getattr__(cls, name):
        if not cls._values:
            with open(cls._path if isfile(cls._path) else "../" + cls._path, "r") as file:
                cls._values = load(file)
        _name = name.replace("_", "-")
        return cls._values.get(_name) if cls._values.get(_name, None) else cls._values.get(name, None)


class Config(metaclass=ConfigMeta):
    """
    Makes the configuration values from config.json available for use in the testing framework.
    There are two ways to use this class:
    You can do Config.get(<parameter name>), or:
    Config.<parameter_name>, replacing all dashes with underscores
    """

    @staticmethod
    def get(name):
        """
        Keeping this for backwards compatibility; use Config.[attribute-name]
        instead.
        Returns the value of the named configuration option.
        """
        return Config.__class__.__getattr__(Config.__class__, name)
