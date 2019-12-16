"""
@name:      Modules/Core/setup_pyhouse_obj.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Oct 19, 2019
@summary:


"""

__updated__ = '2019-12-15'
__version_info__ = (19, 10, 10)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from twisted.internet import reactor

#  Import PyMh files
from Modules.Core.data_objects import PyHouseInformation
from Modules.Core.Mqtt.mqtt import MqttInformation
# from Modules.Core.Config.config_tools import ConfigInformation

# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.SetupPyH_obj   ')

CONFIG_DIR = '/etc/pyhouse/'
xxxCONFIG_NAME = 'pyhouse'


class CoreInformation:
    """
    ==> PyHouse.Core.xxx

    """

    def __init__(self):
        self.Mqtt = None  # MqttInformation()
        # self.Config = {}


class TwistedInformation:
    """ Twisted info is kept in this class
    """

    def __init__(self):
        self.Application = None  # Application('PyHouse')
        self.Reactor = None  # reactor
        self.Site = None


def setup_Core():
    """
    """
    LOG.info('Setting up Core modules.')
    l_obj = CoreInformation()
    l_obj.Mqtt = MqttInformation()
    return l_obj


def setup_Twisted():
    """
    """
    l_obj = TwistedInformation()
    l_obj.Reactor = reactor
    return l_obj


def setup_Parameters():
    """
    """
    l_obj = None  # ParameterInformation()
    return l_obj


def setup_pyhouse():
    l_pyhouse_obj = PyHouseInformation()
    l_pyhouse_obj.Core = setup_Core()  # First
    l_pyhouse_obj._Parameters = setup_Parameters()
    l_pyhouse_obj._Twisted = setup_Twisted()
    l_pyhouse_obj._Config = {}
    # LOG.debug(PrettyFormatAny.form(l_pyhouse_obj, 'PyHouse'))
    return l_pyhouse_obj

# ## END DBK
