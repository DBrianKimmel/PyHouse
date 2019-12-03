"""
@name:      Modules/House/Lighting/lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2019 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system automation.

PyHouse.House.Lighting.
                       Buttons
                       Controllers
                       Lights
                       Outlets
"""

__updated__ = '2019-12-02'
__version_info__ = (19, 10, 2)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyHouse files
from Modules.Core.Config.config_tools import Api as configApi

from Modules.House.Lighting.buttons import Api as buttonsApi, MqttActions as buttonMqtt
from Modules.House.Lighting.controllers import Api as controllersApi, MqttActions as controllerMqtt
from Modules.House.Lighting.lights import Api as lightsApi, MqttActions as lightMqtt
from Modules.House.Lighting.outlets import Api as outletsApi, MqttActions as outletMqtt

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Lighting       ')

CONFIG_NAME = 'lighting'

MODULES = [
    'Buttons',
    'Controllers',
    'Lights',
    'Outlets'
    ]


class LightingInformation:
    """
    ==> PyHouse.House.Lighting.xxx as in the def below
    """

    def __init__(self):
        self.Buttons = None  # ==> ButtonInformation()
        self.Controllers = None  # ==> ControllerInformation()
        self.Lights = None  # ==> LightInformation()
        self.Outlets = None  # ==> OutletInformation


class ScheduleLightingInformation:
    """ This is the lighting specific part.
    """

    def __init__(self):
        self.Type = 'Light'
        self.Brightness = 0
        self.Name = None  # Light name
        self.Rate = 0
        self.Duration = None
        self.Room = None  # Room Name


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_msg):
        """
        --> pyhouse/<housename>/lighting/<category>/xxx
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        p_msg.LogMessage += '\tLighting: {}\n'.format(self.m_pyhouse_obj.House.Name)
        # LOG.debug('MqttLightingDispatch Topic:{}'.format(p_topic))
        if l_topic[0] == 'button':
            buttonMqtt(self.m_pyhouse_obj).decode(p_msg)
        elif l_topic[0] == 'controller':
            controllerMqtt(self.m_pyhouse_obj).decode(p_msg)
        elif l_topic[0] == 'light':
            lightMqtt(self.m_pyhouse_obj).decode(p_msg)
        elif l_topic[0] == 'outlet':
            outletMqtt(self.m_pyhouse_obj).decode(p_msg)
        else:
            p_msg.LogMessage += '\tUnknown Lighting sub-topic {}'.format(p_msg.Payload)
            LOG.warning('Unknown Lighting Topic: {}'.format(l_topic[0]))


class LocalConfig:
    """
    """

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

    m_local_config = None
    m_modules = None
    m_pyhouse_obj = None
    m_buttons = None
    m_controllers = None
    m_lights = None
    m_outlets = None

    def __init__(self, p_pyhouse_obj):
        LOG.info("Initialing - Version:{}".format(__version__))
        p_pyhouse_obj.House.Lighting = LightingInformation()
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = configApi(p_pyhouse_obj)
        #
        self.m_buttons = buttonsApi(p_pyhouse_obj)
        self.m_controllers = controllersApi(p_pyhouse_obj)
        self.m_lights = lightsApi(p_pyhouse_obj)
        self.m_outlets = outletsApi(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """ Load the Lighting config info.
        """
        LOG.info('Loading all Lighting config files.')
        self.m_local_config.read_config(CONFIG_NAME)
        self.m_buttons.LoadConfig()
        self.m_controllers.LoadConfig()
        self.m_lights.LoadConfig()
        self.m_outlets.LoadConfig()
        LOG.info('Loaded Lighting config files.')

    def Start(self):
        """ Allow loading of sub modules and drivers.
        """
        LOG.info("Started.")

    def SaveConfig(self):
        """ Save the Lighting section.
        It will contain several sub-sections
        """
        LOG.info('SaveConfig')
        # self.m_local_config.write_config(CONFIG_NAME, self.m_pyhouse_obj.House.Lighting, addnew=True)
        self.m_buttons.SaveConfig()
        self.m_controllers.SaveConfig()
        self.m_lights.SaveConfig()
        self.m_outlets.SaveConfig()
        LOG.info("Saved Lighting Config.")
        return

    def Stop(self):
        """ Allow cleanup of all drivers.
        """
        LOG.info("Stopping all lighting families.")
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
        # l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, p_device_obj)
        self.m_plm.Control(p_device_obj, p_controller_obj, p_control)

#  ## END DBK
