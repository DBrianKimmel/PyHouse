"""
@name:      Modules/House/Lighting/lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2020 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system automation.

PyHouse.House.Lighting.
                       Buttons
                       Controllers
                       Lights
                       Outlets
"""

__updated__ = '2020-02-21'
__version_info__ = (20, 1, 25)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyHouse files
from Modules.Core.Config.config_tools import Api as configApi
from Modules.House.Lighting import MODULES, LightingClass

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Lighting       ')


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None
    m_schedule_altered = False

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)
        self.m_schedule_altered = False

    def _update_lighting_from_yaml(self, _p_pyhouse_obj, p_node_yaml):
        """
        """
        l_lighting = {}
        try:
            l_yaml = p_node_yaml['Lighting']
        except:
            LOG.error('The "Lighting" tag is missing in the "lighting.yaml" file!')
            return None
        for l_key, l_val in l_yaml.items():
            LOG.debug('\n\tKey: {}\n\tValue: {}'.format(l_key, PrettyFormatAny.form(l_val, 'Lighting.Update', 190)))
        return l_lighting  # For testing.

    def load_yaml_config(self, p_pyhouse_obj):
        """ Read the lighting.yaml file.
        It contains lighting data for the house.
        """
        pass

# ----------

    def save_yaml_config(self, _p_pyhouse_obj):
        """
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))


class Api:
    """ Handles all the components of the lighting sub-system.
    """

    m_config_tools = None
    m_local_config = None
    m_pyhouse_obj = None
    m_module_apis = None

    def __init__(self, p_pyhouse_obj) -> None:
        LOG.info("Initialing - Version:{}".format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        self.m_config_tools = configApi(p_pyhouse_obj)
        l_path = 'Modules.House.Lighting.'
        l_modules = self.m_config_tools.find_module_list(MODULES)
        self.m_module_apis = self.m_config_tools.import_module_list(l_modules, l_path)
        p_pyhouse_obj.House.Lighting._Apis = self.m_module_apis
        LOG.info("Initialized - Version:{}".format(__version__))

    def _add_storage(self) -> None:
        self.m_pyhouse_obj.House.Lighting = LightingClass()

    def LoadConfig(self):
        LOG.info('Loading all Lighting config files.')
        LOG.debug(PrettyFormatAny.form(self.m_module_apis, 'Apis'))
        for l_module in self.m_module_apis.values():
            l_module.LoadConfig()
        LOG.info('Loaded Lighting config files.')

    def Start(self):
        LOG.info("Starting.")
        for l_module in self.m_module_apis.values():
            l_module.Start()
        LOG.info("Started.")

    def SaveConfig(self):
        LOG.info('SaveConfig')
        for l_module in self.m_module_apis.values():
            l_module.SaveConfig()
        LOG.info("Saved Lighting Config.")
        return

    def Stop(self):
        for l_module in self.m_module_apis.values():
            l_module.Stop()
        LOG.info("Stopped.")

    def Control(self, p_device_obj, p_controller_obj, p_control):
        """
        Insteon specific version of control light
        All that Insteon can control is Brightness and Fade Rate.

        @param p_controller_obj: optional  ==> ControllerInformation
        @param p_device_obj: the device being controlled
        @param p_control: the idealized light control params
        """
        if self.m_plm == None:
            LOG.info('No PLM was defined - Quitting.')
            return
        self.m_plm.Control(p_device_obj, p_controller_obj, p_control)

    def MqttDispatch(self, p_msg):
        """
        """
        LOG.debug(PrettyFormatAny.form(p_msg, 'Msg'))
        p_msg.LogMessage += '\tLighting: {}\n'.format(self.m_pyhouse_obj.House.Name)
        l_topic = p_msg.UnprocessedTopic[0].lower()
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        if l_topic in self.m_module_apis:
            self.m_module_apis[l_topic].MqttDispatch(p_msg)
        else:
            p_msg.LogMessage += '\tUnknown sub-topic: "{}"'.format(l_topic)
            LOG.warning('Unknown lighting Topic: {}\n\tTopic: {}\n\tMessge: {}'.format(l_topic, p_msg.Topic, p_msg.Payload))
            LOG.debug(PrettyFormatAny.form(self.m_module_apis, 'Modules'))

#  ## END DBK
