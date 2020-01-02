"""
@name:      Modules/House/Lighting/lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2020 by D. Brian Kimmel
@note:      Created on May 1, 2011
@license:   MIT License
@summary:   This module handles the lights component of the lighting system.

Light switches such as Insteon.

Each entry should contain enough information to allow functionality of various family of lighting controllers.

Insteon is the first type coded and UPB is to follow.

The real work of controlling the devices is delegated to the modules for that family of devices.

"""

__updated__ = '2019-12-30'
__version_info__ = (19, 12, 2)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from typing import Optional, Union

#  Import PyHouse files
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.data_objects import CoreLightingData
from Modules.Core.Utilities import extract_tools
from Modules.Core.state import State
from Modules.House.Lighting.utility import lightingUtility as lightingUtility
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Lights         ')

CONFIG_NAME = 'lights'


class LightInformation:
    """ This is the information that the user needs to enter to uniquely define a light.
    """
    yaml_tag = u'!light'

    def __init__(self, Name=None) -> None:
        self.Name: Optional[str] = Name
        self.Comment: Optional[str] = None  # Optional
        self.DeviceType: str = 'Lighting'
        self.DeviceSubType: str = 'Light'
        self.Family: Optional[LightFamilyInformation] = None  # LightFamilyInformation()
        self.Room = None  # LightRoomInformation() Optional


class LightFamilyInformation:
    """ This is the family information we need for a light

    Families may stuff other necessary information in here.
    """

    def __init__(self):
        self.Name = None
        self.Comment = None  # Optional
        self.Address = None


class LightRoomInformation:
    """ This is the room information we need for a light.
    This allows duplicate light names such as 'Ceiling' in different rooms.
    It also allows for group control by room.

    """

    def __init__(self):
        self.Name = None
        self.Comment = None  # Optional
        self.Uuid = None  # Not user entered but maintained


class LightData(CoreLightingData):
    """ This is the idealized light info.
    This class contains all the reportable and controllable information a light might have.

    ==> PyHouse.House.Lighting.Lights.xxx as in the def below
    """

    def __init__(self):
        super(LightData, self).__init__()
        self.BrightnessPct = 0  # 0% to 100%
        self.Hue = 0  # 0 to 65535
        self.Saturation = 0  # 0 to 255
        self.ColorTemperature = 0  # degrees Kelvin - 0 is not supported
        self.RGB = 0xffffff
        self.TransitionTime = 0  # 0 to 65535 ms = time to turn on or off (fade Time or Rate)
        self.State = State.UNKNOWN
        self.IsDimmable = False
        self.IsColorChanging = False
        self.Trigger = False


class LocalConfig:
    """ The major work here is to load and save the information about a light switch.
    """

    m_config = None
    m_pyhouse_obj = None
    m_path: str = None  # type: ignore  # the path of the config file

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_one_light(self, p_config) -> dict:
        """ Extract the config info for one Light.
        - Name: Light 1
          Comment: This is _test light 1
          Family:
             Name: Insteon
             Address: 11.44.33
          Dimmable: true  # Optional
          Room:
             Name: Living Room
        @param p_config: is the config fragment containing one light's information.
        @return: a LightInformation() obj filled in.
        """
        l_obj = LightInformation()
        l_required = ['Name', 'Family']
        for l_key, l_value in p_config.items():
            # LOG.debug('Light Key: {}; Val: {}'.format(l_key, l_value))
            if l_key == 'Family':
                l_obj.Family = self.m_config.extract_family_group(l_value)  # type: ignore
                l_obj.Family.Type = 'Light'  # type: ignore
            elif l_key == 'Room':
                l_obj.Room = self.m_config.extract_room_group(l_value)  # type: ignore
            else:
                setattr(l_obj, l_key, l_value)
        # Check for required data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('Location Yaml is missing an entry for "{}"'.format(l_key))
        LOG.info('Extracted light "{}"'.format(l_obj.Name))
        return l_obj  # type: ignore

    def _extract_all_lights(self, p_config):
        """ Get all of the lights configured
        """
        l_dict = {}
        for l_ix, l_light in enumerate(p_config):
            l_light_obj = self._extract_one_light(l_light)
            l_dict[l_ix] = l_light_obj
        LOG.info('Extracted {} lights'.format(len(l_dict)))
        return l_dict

    def load_yaml_config(self) -> Union[None, str]:
        """ Read the lights.yaml file if it exists.  No file = no lights.
        It must contain 'Lights:'
        All the lights are a list.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        l_yaml = self.m_config.read_config_file(CONFIG_NAME)  # type: ignore
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Lights']
        except:
            LOG.warning('The config file does not start with "Lights:"')
            return None
        l_lights = self._extract_all_lights(l_yaml)
        return l_lights

# -------------

    def _build_yaml(self):
        """
        """

    def _save_one_light(self, p_light_obj):
        """ Create a Yaml map of all light attributes to save
        """
        LOG.debug('Saving one light: {}'.format(p_light_obj))
        l_ret = p_light_obj.Name
        return l_ret

    def _save_all_lights(self):
        """ Lights are list items

        @param p_config: is the yaml['Lights'] structure
        @return: a complete yaml tree ready to save
        """
        # LOG.debug(p_config)
        l_dict = {}
        l_lights = self.m_pyhouse_obj.House.Lighting.Lights
        for l_light_obj in l_lights.values():
            _l_config = self._save_one_light(l_light_obj)
            try:
                LOG.debug('Inserting one light')
                l_dict[l_light_obj.Name] = l_light_obj
                # p_config.insert(-1, l_config)
            except:
                LOG.debug('Create a list of lights')
            # p_config[-1] = l_config
        return l_dict

    def save_yaml_config(self):
        """ Save all the lights in a separate config file.
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        _l_data = self._save_all_lights()
        # self.m_config.write_config(CONFIG_NAME, l_data, addnew=True)
        # return l_config


class MqttActions:
    """ Mqtt section
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _decode_control(self, p_message):
        """
        ==> pyhouse/<housename>/house/lighting/light/control
        """
        l_control = LightData()
        l_control.Name = l_light_name = extract_tools.get_mqtt_field(p_message, 'LightName')
        l_control.RoomName = extract_tools.get_mqtt_field(p_message, 'RoomName')
        l_control.BrightnessPct = _l_brightness = extract_tools.get_mqtt_field(p_message, 'Brightness')
        LOG.info('Mqtt Control "{}"'.format(l_light_name))
        # LOG.debug(PrettyFormatAny.form(l_control, 'Control'))
        #
        l_light_obj = lightingUtility().get_object_by_id(self.m_pyhouse_obj.House.Lighting.Lights, name=l_light_name)
        if l_light_obj == None:
            LOG.warning(' Light "{}" was not found.'.format(l_light_name))
            return
        LOG.debug(PrettyFormatAny.form(l_light_obj.Family, 'Light.Family'))
        #
        l_controller_obj = lightingUtility().get_controller_objs_by_family(self.m_pyhouse_obj.House.Lighting.Controllers, 'insteon')
        # LOG.debug(PrettyFormatAny.form(l_controller_obj[0], 'Controller'))
        if len(l_controller_obj) > 0:
            # l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, l_light_obj)
            l_api = l_controller_obj[0]._HandlerApi
            # LOG.debug(PrettyFormatAny.form(l_api, 'API'))
            if l_api == None:
                return
            l_api.Control(l_light_obj, l_controller_obj[0], l_control)

    def decode(self, p_msg):
        """ Decode Mqtt message  ==> pyhouse/<house name>/house/lighting/light/<action>
        @param p_topic: is the topic after 'lighting'
        @return: a message to be logged as a Mqtt message
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        p_msg.LogMessage += '\tLighting/Lights: {}\n\t'.format(p_msg.Topic)
        # LOG.debug('LightingLightsDispatch Topic:{}\n\t{}'.format(p_msg.Topic, p_msg.Payload))
        if l_topic[0] == 'control':
            self._decode_control(p_msg.Payload)
            p_msg.LogMessage += 'Light Control: {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Light Control'))
            LOG.debug('MqttLightingLightsDispatch Control Topic:{}\n\t{}'.format(p_msg.Topic, p_msg.Payload))
        elif l_topic[0] == 'status':
            # The status is contained in LightData() above.
            # p_msg.LogMessage += 'Light Status: {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Light Status'))
            p_msg.LogMessage += 'Light Status: {}'.format(p_msg.Payload)
            # LOG.debug('MqttLightingLightsDispatch Status Topic:{}\n\t{}'.format(p_msg.Topic, p_msg.Payload))
        else:
            p_msg.LogMessage += '\tUnknown Lighting/Light sub-topic:{}\n\t{}'.format(p_msg.Topic, PrettyFormatAny.form(p_msg.Payload, 'Light Status'))
            LOG.warning('Unknown Lights Topic: {}'.format(l_topic[0]))


class Api(MqttActions):
    """
    """

    m_pyhouse_obj = None
    m_local_config = None  # Points to the one instance of this class

    def __init__(self, p_pyhouse_obj) -> None:
        # p_pyhouse_obj.House.Lighting.Lights = {}
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def _add_storage(self) -> None:
        """
        """
        self.m_pyhouse_obj.House.Lighting.Lights = {}

    def LoadConfig(self):
        """
        """
        LOG.info('Load Config')
        self.m_pyhouse_obj.House.Lighting.Lights = self.m_local_config.load_yaml_config()
        LOG.info('Loaded {} Lights.'.format(len(self.m_pyhouse_obj.House.Lighting.Lights)))

    def Start(self):
        pass  # Nothing needs starting ATM

    def SaveConfig(self):
        """ Save the Lighting section.
        It will contain several sub-sections
        """
        LOG.info('Save Config')
        self.m_local_config.save_yaml_config()

    def Stop(self):
        pass  # Nothing needs stoping ATM

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
        l_api = p_controller_obj._HandlerApi
        l_api.Control(p_device_obj, p_controller_obj, p_control)

#  ## END DBK
