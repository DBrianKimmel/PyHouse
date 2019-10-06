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

__updated__ = '2019-10-06'
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
        self.UUID = None
        self.Connection = None  # 'Ethernet, Serial, USB
        self.FamilyName = None
        self.Type = None  # Insteon, Hue
        self.IPv4Address = '9.8.7.6'
        self.Tcp_port = None
        self.Security = None  # SecurityInformation()
        self._Queue = None


class LocalConfig:
    """ Load the bridges.yaml config file.
    If the config file has an !include xxx.yaml, schedule the family to load and set up.
    """

    m_config = None
    m_pyhouse_obj = None
    m_bridges__defined = []

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
        # for l_ix, l_value in enumerate(p_config):
        #    LOG.debug('Bridge Key 1: {}; Value: {}'.format(l_ix, l_value))
        for l_key, l_value in p_config.items():
            # LOG.debug('Bridge Key 2: {}; Value: {}'.format(l_key, l_value))
            BridgeList.append(l_key.lower())
            l_obj = self._extract_one_bridge(l_value)
            l_dict[l_key.lower()] = l_obj
        return l_dict

    def load_yaml_config(self):
        """ Read the .Yaml file.
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
            LOG.warn('The config file does not start with "Bridges:"')
            return None
        l_bridges = self._extract_all_bridges(l_yaml)
        self.m_pyhouse_obj.Computer.Bridges = l_bridges
        return l_bridges  # for testing purposes

# ----------

    def _copy_to_yaml(self, p_pyhouse_obj):
        """ Update the yaml information.
        The information in the YamlTree is updated to be the same as the running pyhouse_obj info.

        The running info is a dict and the yaml is a list!

        @return: the updated yaml ready information.
        """
        l_node = p_pyhouse_obj._Config.YamlTree[CONFIG_NAME]
        l_config = l_node.Yaml['Bridges']
        l_working = p_pyhouse_obj.Computer.Bridges
        for l_key in [l_attr for l_attr in dir(l_working) if not l_attr.startswith('_')  and not callable(getattr(l_working, l_attr))]:
            l_val = getattr(l_working, l_key)
            l_config[l_key] = l_val
        p_pyhouse_obj._Config.YamlTree[CONFIG_NAME].Yaml['Bridges'] = l_config
        l_ret = {'Bridges': l_config}
        return l_ret

    def save_yaml_config(self):
        """
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        l_config = self._copy_to_yaml(self.m_pyhouse_obj)
        self.m_config.write_yaml(l_config, CONFIG_NAME, addnew=True)
        return l_config


class Api:
    """This interfaces to all of PyHouse.
    """

    m_local_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        LOG.debug(PrettyFormatAny.form(p_pyhouse_obj.Computer.Bridges, 'Bridges'))
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
            if l_bridge.Type == 'Hue':
                # Atempt to not load unless used
                from Modules.House.Family.hue.hue_hub import HueHub
                LOG.info('Hue Bridge Active: {}'.format(l_bridge.Name))
                HueHub(self.m_pyhouse_obj).HubStart(l_bridge)
            else:
                LOG.info('Other Bridge Active: {}'.format(l_bridge.Name))
            l_count += 1

    def SaveConfig(self):
        """
        @param p_pyhouse_obj: the master obj
        """
        # self.m_local_config.save_yaml_config()
        LOG.info("Saved Bridges Config")

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
