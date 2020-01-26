"""
@name:      Modules/House/Irrigation/irrigation.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 4, 2014
@Summary:

"""

__updated__ = '2020-01-25'
__version_info__ = (20, 1, 25)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files
from Modules.Core.Config import config_tools
from Modules.House.Irrigation import IrrigationInformation, MODULES

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Irrigation     ')


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _decode_control(self, _p_topic, _p_message):
        l_logmsg = '\tIrrigation Control'
        return l_logmsg

    def _decode_status(self, _p_topic, _p_message):
        l_logmsg = '\tIrrigation Status'
        return l_logmsg

    def decode(self, p_msg):
        """ pyhouse/<HouseName>/irrigation/<action>
        where <action> is control, status
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        l_logmsg = ' Irrigation '
        if l_topic[0].lower() == 'control':
            l_logmsg += '\tControl: {}\n'.format(self._decode_control(p_msg.Topic, p_msg.Payload))
        elif l_topic[0].lower() == 'status':
            l_logmsg += '\tStatus: {}\n'.format(self._decode_status(p_msg.Topic, p_msg.Payload))
        else:
            l_logmsg += '\tUnknown irrigation sub-topic {}'.format(p_msg.Payload)
            LOG.warning('Unknown Irrigation Topic: {}'.format(l_topic[0]))
        return l_logmsg


class lightingUtilityIrr:
    """
    """

    def update_pyhouse_obj(self, p_pyhouse_obj):
        p_pyhouse_obj.House.Irrigation = IrrigationInformation()

    def add_api_references(self, p_pyhouse_obj):
        pass


class LocalConfig:
    """
    """
    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = config_tools.Api(p_pyhouse_obj)

    def load_yaml_config(self):
        """ Read the house.yaml file.
         """
        LOG.info('Loading Config - Version:{}'.format(__version__))


class Api(lightingUtilityIrr):

    m_pyhouse_obj = None
    m_config_tools = None
    m_local_config = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_config_tools = config_tools.Yaml(p_pyhouse_obj)
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        l_modules = self.m_config_tools.find_module_list(MODULES)
        l_path = 'Modules.House.Irrigation.'
        self.m_modules_apis = self.m_config_tools.import_module_list(l_modules, l_path)
        LOG.info('Initialized - Version:{}'.format(__version__))

    def _add_storage(self):
        """
        """
        self.m_pyhouse_obj.House.Irrigation = IrrigationInformation()

    def LoadConfig(self):
        """ Load the Irrigations config info.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_local_config.load_yaml_config()
        for l_module in self.m_modules_apis.values():
            l_module.LoadConfig()
        LOG.info('Loaded Config')

    def Start(self):
        LOG.info('Started Irrigation')

    def SaveConfig(self):
        LOG.info("Saved Irrigation Config.")

    def Stop(self):
        LOG.info('Stopped Irrigation')

#  ## END DBK
