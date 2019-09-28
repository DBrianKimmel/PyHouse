"""
@name:      Modules/House/Family/hue/hue_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Dec 18, 2017
@license:   MIT License
@summary:

"""
from Modules.Core.Config import config_tools

__updated__ = '2019-09-26'
__version_info__ = (19, 9, 26)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

# Import PyMh files
from Modules.House.Family.hue.hue_hub import HueHub

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Hue_device     ')

CONFIG_NAME = 'hue'


class HueInformation:
    """
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.Family = None
        self.Host = None
        self.Access = None


class Config:
    """
    """

    m_config_tools = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config_tools = config_tools.Yaml(p_pyhouse_obj)

    def _extract_modules_info(self, p_yaml):
        """
        """
        _l_required = ['Name']
        l_obj = HueInformation()
        try:
            l_modules = p_yaml['Modules']
        except:
            LOG.warn('No "Modules" list in "house.yaml"')
            return
        for l_module in l_modules:
            LOG.debug('found Module "{}" in house config file.'.format(l_module))
        return l_obj

    def _extract_hue_info(self, p_config):
        """
        """
        l_required = ['Name', 'Family', 'Host', 'Access']
        l_obj = HueInformation()
        for l_key, l_value in p_config.items():
            if l_key == 'Access':
                l_obj.Access = self.m_config_tools.extract_access_group(l_value)
            setattr(l_obj, l_key, l_value)
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('house.yaml is missing an entry for "{}"'.format(l_key))
        return l_obj

    def load_yaml_config(self):
        """ Read the Rooms.Yaml file.
        It contains Rooms data for all rooms in the house.
        """
        LOG.debug('Loading Config - Version:{}'.format(__version__))
        try:
            l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(CONFIG_NAME)
        except:
            return None
        try:
            l_yaml = l_node.Yaml['Hue']
        except:
            LOG.warn('The hue.yaml file does not start with "Hue:"')
            return None
        l_house = self._extract_hue_info(l_yaml)
        # self.m_pyhouse_obj.House.Name = l_house.Name
        return l_node  # for testing purposes


class API:
    """
    """

    m_pyhouse_obj = None
    m_hue_hub = None

    def __init__(self, p_pyhouse_obj):
        LOG.info("Initializing - Version:{}".format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        Config(p_pyhouse_obj).load_yaml_config()
        self.m_hue_hub = HueHub(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """
        """
        LOG.info('Loading')
        # HueHub(self.m_pyhouse_obj).Start(p_pyhouse_obj)

    def Start(self):
        """
        """
        # if self.m_pyhouse_obj.Computer != {}:
        self.m_hue_hub.Start()
        LOG.info('Started')

    def SaveConfig(self):
        """ Handled by Bridges
        """
        return

    def ControlDevice(self, p_device_obj, p_bridge_obj, p_control):
        """ Control some device using the Philips Hue HUB.
        @param p_device_obj: is the device being controlled.
        @param p_bridge_obj: is the HUB
        @param p_control: is the generic control actions to be performed on the device
        """
        pass

# ## END DBK
