"""
@name:      Modules/House/location.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Handle the location information for a house.

There is location information for the house.
This is for calculating the time of sunrise and sunset.
Additional calculations may be added such things as moon rise, tides, etc.
"""

__updated__ = '2019-07-31'
__version_info__ = (19, 6, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
# from mypy.main import config_types

#  Import PyMh files
from Modules.Core.data_objects import RiseSetData
from Modules.Core.Utilities import config_tools
from Modules.House.house_data import LocationInformationPrivate, LocationInformation

# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Location       ')

CONFIG_FILE_NAME = 'location.yaml'


class Config:
    """ Update the Yaml config files.
    This will handle the location.yaml file
    ==> PyHouseObj._Config.YamlTree{'location.yaml'}.xxx
    --> xxx = {Yaml, YamlPath, Filename}
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _extract_location(self, p_config) -> dict:
        """ Extract the config info for location.
        Warn if there are extra attributes in the config.
        Warn if there are missing attributes in the config.

        @param p_config: is the yaml fragment containing location information.
        @return: a LocattionInformation() obj filled in.
        """
        l_required = ['Latitude', 'Longitude']
        l_obj = LocationInformation()
        for l_key, l_value in p_config.items():
            # print('Location Key:  {}'.format(l_key))
            if not hasattr(l_obj, l_key):
                LOG.warn('location.yaml contains an extra entry "{}" = {} - Ignored.'.format(l_key, l_value))
                continue
            setattr(l_obj, l_key, l_value)
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('Location Yaml is missing an entry for "{}"'.format(l_key))
        self.m_pyhouse_obj.House.Location = l_obj
        return l_obj  # For testing

    def LoadYamlConfig(self):
        """ Read the location.yaml file.
        It contains Location data for the house.
        """
        # LOG.info('Loading _Config - Version:{}'.format(__version__))
        try:
            l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        except:
            LOG.error('Location config file is missing.')
            self.m_pyhouse_obj.House.Location = None
            return None
        try:
            l_yaml = l_node.Yaml['Location']
        except:
            LOG.warn('The location.yaml file does not start with "Location:"')
            self.m_pyhouse_obj.House.Location = None
            return None
        l_locat = self._extract_location(l_yaml)
        # self.m_pyhouse_obj.House.Location = l_locat
        return l_locat  # for testing purposes

# ----------

    def _copy_to_yaml(self, p_pyhouse_obj):
        """ Update the yaml information.
        The information in the YamlTree is updated to be the same as the running pyhouse_obj info.

        The running info is a dict and the yaml is a list!

        @return: the updated yaml ready information.
        """
        l_node = p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME]
        l_config = l_node.Yaml['Location']
        # LOG.debug(PrettyFormatAny.form(l_config, 'Location', 190))
        l_working = p_pyhouse_obj.House.Location
        # LOG.debug(PrettyFormatAny.form(l_working, 'House', 190))
        for l_key in [l_attr for l_attr in dir(l_working) if not l_attr.startswith('_')  and not callable(getattr(l_working, l_attr))]:
            l_val = getattr(l_working, l_key)
            l_config[l_key] = l_val
        p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME].Yaml['Location'] = l_config
        # LOG.debug(PrettyFormatAny.form(l_node, 'Updated', 190))
        l_ret = {'Location': l_config}
        return l_ret

    def SaveYamlConfig(self):
        """
        """
        # LOG.info('Saving Config - Version:{}'.format(__version__))
        l_config = self._copy_to_yaml(self.m_pyhouse_obj)
        config_tools.Yaml(self.m_pyhouse_obj).write_yaml(l_config, CONFIG_FILE_NAME, addnew=True)
        return l_config


class Api:
    """ Location sub-module of a house.
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        """ Set up the location info.
        """
        LOG.info('Initializing - Version:{}'.format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.House.Location = LocationInformationPrivate()

    def LoadConfig(self):
        """ Load the Yaml config file into the system.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_config = Config(self.m_pyhouse_obj)
        self.m_config.LoadYamlConfig()

    def SaveConfig(self):
        """ Take a snapshot of the running system and save it in Yaml to be loaded on restart.
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        self.m_config.SaveYamlConfig()

#  ## END DBK
