"""
@name:      Modules/House/Security/door_bells.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep  1, 2019
@Summary:

"""

__updated__ = '2019-12-23'
__version_info__ = (19, 12, 23)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

# Import PyMh files
from Modules.Core.Config.config_tools import Api as configApi

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.DoorBells      ')

CONFIG_NAME = 'doorbells'


class DoorBellInformation:
    """

    ==> PyHouse.House.Security.Garage_Doors.xxx as in the def below
    """


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def load_yaml_config(self):
        """
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Garage+Doors']
        except:
            LOG.warning('The config file does not start with "Garage_Doors:"')
            return None
        l_gdo = {}
        return l_gdo


class Api:
    """
    """
    m_pyhouse_obj = None
    m_local_config = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def _add_storage(self) -> None:
        """
        """
        self.m_pyhouse_obj.House.Security.Door_Bells = {}

    def LoadConfig(self):
        """
        """
        LOG.info('Load Config')
        self.m_local_config.load_yaml_config()
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Buttons, 'buttons.Api.LoadConfig'))

    def Start(self):
        """
        """

    def SaveConfig(self):
        """
        """
        pass

    def Stop(self):
        """
        """
        pass

# ## END DBK
