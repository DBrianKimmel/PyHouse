"""
@name:      Modules/House/Rules/rules.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 27, 2015
@Summary:

If garage door opens and after sunset and before sunrise, turn on outside garage door lights.

"""
from _ast import Pass

__updated__ = '2019-08-01'
__version_info__ = (19, 8, 0)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

# Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.RulesXml       ')


class RulesInformation:
    """ The collection of information about a house.
    Causes JSON errors due to API type data methinks.

    ==> PyHouse.House.xxx as in the def below.
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.Event = None  # List of Names of the events that triggers this rule
        self.Condition = None  # List of additional conditions to activate the rule
        self.Device = None  # the device to control
        self.Type = None  # The type (On/Off)
        self.Action = None  # On, Off
        self.Delay = None  # How long to delay after trigger to action (time in seconds)
        self.Duration = None


class Config:
    """
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def load_yaml_config(self):
        LOG.info('Loading Config - Version:{}'.format(__version__))
        pass

# ----------

    def save_yaml_config(self):
        pass


class API:

    m_pyhouse_obj = None
    m_config = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = Config(p_pyhouse_obj)

    def Start(self):
        pass

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_config.load_yaml_config()

    def SaveConfig(self):
        """
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        self.m_config.save_yaml_config()

    def Stop(self):
        pass

# ## END DBK
