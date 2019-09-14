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

__updated__ = '2019-09-12'
__version_info__ = (19, 9, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyHouse files
from Modules.Core.Config import config_tools
from Modules.House.Lighting.buttons import API as buttonsApi
from Modules.House.Lighting.controllers import API as controllersApi, MqttActions as controllerMqtt
from Modules.House.Lighting.lights import API as lightsApi, MqttActions as lightMqtt
from Modules.House.Lighting.outlets import API as outletsApi

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Lighting       ')

CONFIG_NAME = 'lighting'


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

    def decode(self, p_topic: list, p_message, p_logmsg) -> str:
        """
        --> pyhouse/<housename>/lighting/<category>/xxx
        """
        p_logmsg += '\tLighting: {}\n'.format(self.m_pyhouse_obj.House.Name)
        # LOG.debug('MqttLightingDispatch Topic:{}'.format(p_topic))
        if p_topic[0] == 'button':
            pass
            # p_logmsg += but
        elif p_topic[0] == 'controller':
            p_logmsg += controllerMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message)
        elif p_topic[0] == 'light':
            p_logmsg += lightMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message)
        else:
            p_logmsg += '\tUnknown Lighting sub-topic {}'.format(p_message)
            LOG.warn('Unknown Lighting Topic: {}'.format(p_topic[0]))
        return p_logmsg


class Config:
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
        l_node = config_tools.Yaml(p_pyhouse_obj).read_yaml(CONFIG_NAME)
        return l_node  # for testing purposes

# ----------

    def _copy_to_yaml(self, p_pyhouse_obj):
        """ Create or Update the yaml information.
        The information in the YamlTree is updated to be the same as the running pyhouse_obj info.

        The running info is a dict and the yaml is a list!

        @return: the updated yaml ready information.
        """
        try:
            l_node = p_pyhouse_obj._Config.YamlTree[CONFIG_NAME]
            l_config = l_node.Yaml['Lighting']
        except:
            l_node = config_tools.Yaml(p_pyhouse_obj).create_yaml_node('Lighting')
            l_config = l_node.Yaml['Lighting']
        LOG.debug(PrettyFormatAny.form(p_pyhouse_obj.House, 'PyHouseObj', 190))
        l_working = p_pyhouse_obj.House.Lighting.Lights
        for l_key in [l_attr for l_attr in dir(l_working) if not l_attr.startswith('_')  and not callable(getattr(l_working, l_attr))]:
            l_val = getattr(l_working, l_key)
            setattr(l_config, l_key, l_val)
        p_pyhouse_obj._Config.YamlTree[CONFIG_NAME].Yaml['Lighting'] = l_config
        l_ret = {'Lighting': l_config}
        return l_ret

    def save_yaml_config(self, _p_pyhouse_obj):
        """
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        # config_tools.Yaml(p_pyhouse_obj).write_yaml(l_config, CONFIG_NAME, addnew=True)
        # return l_config


class API:
    """ Handles all the components of the lighting sub-system.
    """

    m_pyhouse_obj = None
    m_buttons = None
    m_controllers = None
    m_lights = None
    m_outlets = None

    def __init__(self, p_pyhouse_obj):
        LOG.info("Initialing - Version:{}".format(__version__))
        p_pyhouse_obj.House.Lighting = LightingInformation()
        self.m_pyhouse_obj = p_pyhouse_obj
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
        Config().load_yaml_config(self.m_pyhouse_obj)
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
        Config().save_yaml_config(self.m_pyhouse_obj)
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
        #  self.m_pyhouse_obj._APIs.House.FamilyAPI.stop_lighting_families(self.m_pyhouse_obj)
        LOG.info("Stopped.")

    def AbstractControlLight(self, p_device_obj, p_controller_obj, p_control):
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
        self.m_plm.AbstractControlLight(p_device_obj, p_controller_obj, p_control)

#  ## END DBK
