"""
@name:      Modules/House/Family/hue/hue_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Dec 18, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2019-10-08'
__version_info__ = (19, 9, 26)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

# Import PyMh files
from Modules.Core.Config.config_tools import Api as configApi
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


class LocalConfig:
    """
    """

    m_config = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

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

    def _extract_one_hue(self, p_config):
        """
        """
        LOG.debug('Config: {}'.format(p_config))
        l_required = ['Name', 'Family', 'Host', 'Access']
        l_obj = HueInformation()
        for l_key, l_value in p_config.items():
            LOG.debug('Key: {}; Value: {}'.format(l_key, l_value))
            if l_key == 'Access':
                l_obj.Access = self.m_config.extract_access_group(l_value)
            setattr(l_obj, l_key, l_value)
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('hue.yaml is missing an entry for "{}"'.format(l_key))
        return l_obj

    def _extract_all_devices(self, p_config):
        """
        """
        l_hue = {}
        for l_ix, l_value in enumerate(p_config):
            l_obj = self._extract_one_hue(l_value)

    def load_yaml_config(self):
        """ Read the Rooms.Yaml file.
        It contains Rooms data for all rooms in the house.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        # self.m_pyhouse_obj.
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Hue']
        except:
            LOG.warn('The config file does not start with "Hue:"')
            return None
        l_hue = self._extract_all_devices(l_yaml)
        # self.m_pyhouse_obj.House.Name = l_house.Name
        return l_hue  # for testing purposes


class Api:
    """
    """

    m_local_config = None
    m_pyhouse_obj = None
    m_hue_hub = None

    def __init__(self, p_pyhouse_obj):
        LOG.info("Initializing - Version:{}".format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        self.m_local_config.load_yaml_config()
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
