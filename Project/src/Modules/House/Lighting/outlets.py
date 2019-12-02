"""
@name:      Modules/House/Lighting/outlets.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@note:      Created on Jul 18, 2019
@license:   MIT License
@summary:   Handle the home lighting system automation.


"""

__updated__ = '2019-12-02'
__version_info__ = (19, 11, 27)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.Config.config_tools import Api as configApi

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Outlets        ')

CONFIG_NAME = 'outlets'


class OutletInformation:
    """ This is the information that the user needs to enter to uniquely define a Outlet.
    """

    def __init__(self):
        self.Name = None
        self.Comment = None  # Optional
        self.DeviceType = 'Lighting'
        self.DeviceSubType = 'Outlet'
        self.LastUpdate = None  # Not user entered but maintained
        self.Uuid = None  # Not user entered but maintained
        self.Family = None  # LightFamilyInformation()
        self.Room = None  # LightRoomInformation() Optional


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_msg):
        """
        --> pyhouse/<housename>/house/outlet/<name>/...
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        # l_light_name = extract_tools.get_mqtt_field(p_msg.Payload, 'LightName')
        if l_topic[0] == 'STATE':
            p_msg.LogMessage += '\tState:\n'
        elif l_topic[0] == 'RESULT':
            p_msg.LogMessage += '\tResult:\n'
        elif l_topic[0] == 'POWER':
            p_msg.LogMessage += '\tResult:\n'
        elif l_topic[0] == 'LWT':
            p_msg.LogMessage += '\tResult:\n'
        else:
            p_msg.LogMessage += '\tUnknown house/outlet sub-topic: {}; - {}'.format(p_msg.Topic, p_msg.Payload)
            LOG.warn('Unknown "house/outlet" sub-topic: {}\n\tTopic: {}\n\tMessge: {}'.format(l_topic[0], p_msg.Topic, p_msg.Payload))


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
            # print('Light Key: {}; Val: {}'.format(l_key, l_val))
            if l_key == 'Family':
                l_obj.Family = self.m_config.extract_family_group(l_value)
            elif l_key == 'Room':
                l_obj.Room = self.m_config.extract_room_group(l_value)
            else:
                setattr(l_obj, l_key, l_value)
        # Check for required data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('Location Yaml is missing an entry for "{}"'.format(l_key))
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
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Outlets']
        except:
            LOG.warn('The config file does not start with "Outlets:"')
            return None
        l_outlets = self._extract_all_outlets(l_yaml)
        self.m_pyhouse_obj.House.Lighting.Outlets = l_outlets
        return l_outlets  # for testing purposes


class Api:
    """
    """

    m_local_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_local_config.load_yaml_config()

    def SaveConfig(self):
        """
        """

# ## END DBK
