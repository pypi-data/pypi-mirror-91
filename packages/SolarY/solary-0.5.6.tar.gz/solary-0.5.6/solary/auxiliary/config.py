"""
config.py

Auxiliary functions for all library relevant configuration files

"""

# Import standard libraries
import configparser
import os

# Import the ROOT directory of SolarY
from solary import ROOT_DIR


def get_constants():
    """
    Function to get the constants.ini file from the _config directory

    Returns
    -------
    config : configparser.ConfigParser
        Configuration Parser that contains miscellaneous constants (like astrodynmical, time,
        etc.)

    """

    # Set config parser
    config = configparser.ConfigParser()

    # Get the constants ini file
    constants_ini_path = os.path.join(ROOT_DIR, '_config', 'constants.ini')

    # Read and parse the config file
    config.read(constants_ini_path)

    return config

def get_paths(test=False):
    """
    Function to get the paths.dir file from the _config directory

    Parameters
    ----------
    test : bool
        Boolean value whether to use the default (prod.) or test configs. Default: False

    Returns
    -------
    config : configparser.ConfigParser
        Configuration Parser that contains miscellaneous paths to store / access / etc. downloaded
        files, created database etc.

    """

    # Set the config parser
    config = configparser.ConfigParser()

    # Get the paths ini file, differentiate between prod and test
    if test:
        paths_ini_path = os.path.join(ROOT_DIR, 'tests/_resources/_config', 'test_paths.ini')
    else:
        paths_ini_path = os.path.join(ROOT_DIR, '_config', 'paths.ini')

    # Read and parse the config file
    config.read(paths_ini_path)

    return config
