"""
@name:      Modules/Core/__init__.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2020 by D. Brian Kimmel
@note:      Created on Mar 1, 2014
@license:   MIT License

Core is the main portion of every PyHouse node.
It is always present.
"""

__updated__ = '2020-02-17'
__version_info__ = (20, 2, 3)
__version__ = '.'.join(map(str, __version_info__))

# These parts are required!
# Parts are on the same level as Core
PARTS = [
    'Computer',
    'House'
    ]

# Modules are subcategories of Core
MODULES = [
    'Mqtt'
    ]

CONFIG_DIR = '/etc/pyhouse/'
CONFIG_NAME = 'pyhouse'


class PyHouseInformation:
    """
    ==> PyHouse.xxx as in the def below.

    The master object, contains all other 'configuration' objects.

    """

    def __init__(self):
        self.Core = None
        self.Computer = None
        self.House = None

        self._Config = None
        self._Parameters = None
        self._Twisted = None


class CoreInformation:
    """
    """

    def __init__(self):
        self.Components = None
        self.Modules = None
        self._Apis = {}


class CoreComponentInformation:
    """
    """

    def __init__(self):
        self.Computer = None
        self.House = None
        self._Api = None
        self._Apis = {}


class CoreModuleInformation:
    """
    ==> PyHouse.Core.xxx

    """

    def __init__(self):
        self.Mqtt = None  # MqttInformation()


class ParameterInformation:
    """
    ==> PyHouse._Parameters.xxx

    These are filled in first and hold things needed for early initialization.
    """

    def __init__(self):
        self.Name = 'Nameless House'
        self.Computer = 'Nameless'
        self.UnitSystem = 'Metric'
        self.ConfigVersion = 2.0


class TwistedInformation:
    """ Twisted info is kept in this class
    """

    def __init__(self):
        self.Application = None  # Application('PyHouse')
        self.Reactor = None  # reactor
        self.Site = None

# ## END DBK
