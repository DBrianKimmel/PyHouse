"""
@name:      Modules/Computer/Bridges/bridges.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Dec 21, 2017
@license:   MIT License
@summary:   The entry point for dealing with bridges.

Bridges may be attached locally (USB) or via the network (Ethernet, WiFi).

Locally attached are generally controllers.

"""

__updated__ = '2019-11-29'
__version_info__ = (19, 10, 6)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.Config.config_tools import Api as configApi

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Bridges        ')

CONFIG_NAME = 'bridges'

BridgeList = []


class BridgesInformation:
    """
    ==> PyHouse.Computer.Bridges.
    """

    def __init__(self):
        super(BridgesInformation, self).__init__()
        self.Bridges = {}  # BridgeInformation()


class BridgeInformation:
    """
    ==> PyHouse.Computer.Bridges[x].xxx as below
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.Type = None  # Insteon, Hue
        self.Access = None  # AccessInformation()
        self.Connection = None  # ???
        self.Host = None  # HostInformation()
        self.Family = None  # FamilyInformation()
        self._Queue = None


class LocalConfig:
    """ Load the bridges.yaml config file.
    If the config file has an !include xxx.yaml, schedule the family to load and set up.
    """

    m_config = None
    m_pyhouse_obj = None
    m_bridges_defined = []

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_one_bridge(self, p_config):
        """
        """
        l_obj = BridgeInformation()
        LOG.info('One Bridge: {}'.format(p_config))
        return l_obj

    def _extract_all_bridges(self, p_config):
        """ Get the list of bridges we have
        """
        # LOG.debug('Bridges: {}'.format(p_config))
        l_dict = {}
        # for l_key, l_value in enumerate(p_config):  # ### List
        for l_key, l_value in p_config.items():  # ### Mapping
            # LOG.debug('Bridge Key 2: {}; Value: {}'.format(l_key, l_value))
            BridgeList.append(l_key.lower())
            l_obj = self._extract_one_bridge(l_value)
            l_dict[l_key.lower()] = l_obj
        return l_dict

    def load_yaml_config(self):
        """ Read the .yaml file.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj.Computer.Bridges = {}
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Bridges']
        except:
            LOG.warning('The config file does not start with "Bridges:"')
            return None
        l_bridges = self._extract_all_bridges(l_yaml)
        self.m_pyhouse_obj.Computer.Bridges = l_bridges
        return l_bridges  # for testing purposes

# ----------

    def save_yaml_config(self):
        """
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        # l_config = self._copy_to_yaml(self.m_pyhouse_obj)
        # self.m_config.write_yaml(l_config, CONFIG_NAME, addnew=True)
        # return l_config


class Api:
    """This interfaces to all of PyHouse.
    """

    m_local_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        # LOG.debug(PrettyFormatAny.form(p_pyhouse_obj.Computer.Bridges, 'Bridges'))
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """ Load the config info.
        This usually is only !include records
        """
        self.m_local_config.load_yaml_config()
        LOG.info("Loaded Config - Version:{}".format(__version__))

    def Start(self):
        l_count = 0
        LOG.info("Starting Bridges")
        for l_bridge in self.m_pyhouse_obj.Computer.Bridges.values():
            LOG.info('Starting bridge "{}"'.format(l_bridge.Name))
            if l_bridge.Type == 'Hue':
                # Atempt to not load unless used
                from Modules.House.Family.hue.hue_hub import HueHub
                LOG.info('Hue Bridge Active: {}'.format(l_bridge.Name))
                HueHub(self.m_pyhouse_obj).HubStart(l_bridge)
            else:
                LOG.info('Other Bridge Active: "{}"'.format(l_bridge.Name))
            l_count += 1

    def SaveConfig(self):
        """
        @param p_pyhouse_obj: the master obj
        """
        # self.m_local_config.save_yaml_config()
        LOG.info("Saved Bridges Config")

    def Stop(self):
        LOG.info("Stopped.")
        _x = PrettyFormatAny.form('x', 'X')

# ## END DBK
