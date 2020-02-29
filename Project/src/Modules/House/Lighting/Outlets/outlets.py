"""
@name:      Modules/House/Lighting/outlets.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2020 by D. Brian Kimmel
@note:      Created on Jul 18, 2019
@license:   MIT License
@summary:   Handle the home lighting system automation.


"""

__updated__ = '2020-02-21'
__version_info__ = (20, 2, 9)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.Utilities import extract_tools
from Modules.House.Lighting import LightingClass
from Modules.House.Lighting.utility import lightingUtility as lightingUtility
from Modules.House.Lighting.Outlets import OutletInformation
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Outlets        ')

CONFIG_NAME = 'outlets'


class OutletControlInformation:
    """ This is the idealized light info.
    This class contains all the reportable and controllable information a light might have.

    ==> PyHouse.House.Lighting.Lights.xxx as in the def below
    """

    def __init__(self):
        self.BrightnessPct = 0  # 0% to 100%
        self.TransitionTime = 0  # 0 to 65535 ms = time to turn on or off (fade Time or Rate)
        self.IsDimmable = False
        self.Trigger = False
        self.Type: str = 'outlet'


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _decode_control(self, p_msg):
        """
        pyhouse/<housename>/house/lighting/outlets/xxx
        """
        LOG.debug(PrettyFormatAny.form(p_msg, 'Msg'))
        l_control = OutletControlInformation()
        l_control.Name = l_light_name = extract_tools.get_mqtt_field(p_msg, 'LightName')
        l_control.RoomName = extract_tools.get_mqtt_field(p_msg, 'RoomName')
        l_control.BrightnessPct = _l_brightness = extract_tools.get_mqtt_field(p_msg, 'Brightness')
        LOG.info('Mqtt Control "{}"'.format(l_light_name))
        # LOG.debug(PrettyFormatAny.form(l_control, 'Control'))
        #
        l_outlet_obj = lightingUtility().get_object_by_id(self.m_pyhouse_obj.House.Lighting.Outlets, name=l_light_name)
        if l_outlet_obj == None:
            LOG.warning(' Outlet "{}" was not found.'.format(l_light_name))
            return
        LOG.debug(PrettyFormatAny.form(l_outlet_obj.Family, 'Outlet.Family'))
        #
        l_controller_obj = lightingUtility().get_controller_objs_by_family(self.m_pyhouse_obj.House.Lighting.Controllers, 'insteon')
        # LOG.debug(PrettyFormatAny.form(l_controller_obj[0], 'Controller'))
        if len(l_controller_obj) > 0:
            l_api = l_controller_obj[0]._HandlerApi
            # LOG.debug(PrettyFormatAny.form(l_api, 'API'))
            if l_api == None:
                return
            l_api.Control(l_outlet_obj, l_controller_obj[0], l_control)

    def _decode_status(self, p_msg):
        """
        ==> pyhouse/<housename>/house/lighting/lights/control
        """
        LOG.debug(PrettyFormatAny.form(p_msg, 'Msg'))


class LocalConfig:
    """ The major work here is to load and save the information about a light switch.
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_one_outlet(self, p_config) -> dict:
        """ Extract the config info for one Light.
        - Name: Light 1
          Comment: This is _test light 1
          Family:
             Name: Insteon
             Address: 11.44.33
          Room:
             Name: Living Room
        @param p_config: is the config fragment containing one outlet's information.
        @return: an OutletInformation() obj filled in.
        """
        l_obj = OutletInformation()
        l_required = ['Name', 'Family']
        for l_key, l_value in p_config.items():
            # print('Light Key: {}; Val: {}'.format(l_key, l_value))
            if l_key == 'Family':
                l_obj.Family = self.m_config.extract_family_group(l_value)
            elif l_key == 'Room':
                l_obj.Room = self.m_config.extract_room_group(l_value)
            else:
                setattr(l_obj, l_key, l_value)
        # Check for required data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('Location Yaml is missing an entry for "{}"'.format(l_key))
        LOG.info('Extracted light "{}"'.format(l_obj.Name))
        return l_obj

    def _extract_all_outlets(self, p_config):
        """ Get all of the lights configured
        """
        l_dict = {}
        for l_ix, l_outlet in enumerate(p_config):
            l_obj = self._extract_one_outlet(l_outlet)
            l_dict[l_ix] = l_obj
        return l_dict

    def load_yaml_config(self):
        """ Read the outlets.yaml file if it exists.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj.House.Lighting.Outlets = None
        l_yaml = self.m_config.read_config_file(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Outlets']
        except:
            LOG.warning('The config file does not start with "Outlets:"')
            return None
        l_outlets = self._extract_all_outlets(l_yaml)
        self.m_pyhouse_obj.House.Lighting.Outlets = l_outlets
        return l_outlets


class Api(MqttActions):
    """
    """

    m_local_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def _add_storage(self) -> None:
        """
        """
        if not hasattr(self.m_pyhouse_obj.House, 'Lighting'):
            self.m_pyhouse_obj.House.Lighting = LightingClass()
        self.m_pyhouse_obj.House.Lighting.Outlets = {}

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj.House.Lighting.Outlets = self.m_local_config.load_yaml_config()
        LOG.info('Loaded {} Outlets.'.format(len(self.m_pyhouse_obj.House.Lighting.Outlets)))

    def Start(self):
        pass  # Nothing needs starting ATM

    def SaveConfig(self):
        """
        """

    def Stop(self):
        pass  # Nothing needs stoping ATM

    def Control(self, p_device_obj, p_controller_obj, p_control):
        """
        Insteon specific version of control light
        All that Insteon can control is Brightness and Fade Rate.

        @param p_controller_obj: optional  ==> ControllerInformation
        @param p_device_obj: the device being controlled
        @param p_control: the idealized control params
        """
        if self.m_plm == None:
            LOG.info('No PLM was defined - Quitting.')
            return
        l_api = p_controller_obj._HandlerApi  # The family
        l_api.Control(p_device_obj, p_controller_obj, p_control)

    def MqttDispatch(self, p_msg):
        """ Decode Mqtt message  ==> pyhouse/<house name>/house/lighting/outlets/<action>
        @param p_topic: is the topic after 'lighting'
        @return: a message to be logged as a Mqtt message
        """
        LOG.debug(PrettyFormatAny.form(p_msg, 'Msg'))
        l_topic = p_msg.UnprocessedTopic[0].lower()
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        p_msg.LogMessage += '\tLighting/Outlets: {}\n\t'.format(p_msg.Topic)
        if l_topic == 'control':
            self._decode_control(p_msg)
            p_msg.LogMessage += 'Outlet Control: {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Light Control'))
            LOG.debug('Outlet Control Topic:{}\n\t{}'.format(p_msg.Topic, p_msg.Payload))
        elif l_topic == 'status':
            # The status is contained in LightControlInformation() above.
            self._decode_status(p_msg)
            p_msg.LogMessage += 'Outlet Status: {}'.format(p_msg.Payload)
            LOG.debug('Outlet Status Topic:{}\n\t{}'.format(p_msg.Topic, p_msg.Payload))
        else:
            p_msg.LogMessage += '\tUnknown Lighting/Outlets sub-topic:{}\n\t{}'.format(p_msg.Topic, PrettyFormatAny.form(p_msg.Payload, 'Light Status'))
            LOG.warning('Unknown Outlets Topic: {}'.format(l_topic))

# ## END DBK
