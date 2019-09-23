"""
@name:      Modules/House/Lighting/outlets.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@note:      Created on Jul 18, 2019
@license:   MIT License
@summary:   Handle the home lighting system automation.


"""

__updated__ = '2019-09-18'
__version_info__ = (19, 9, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.Config import config_tools
from Modules.House.Family.family import Config as familyConfig
from Modules.House.rooms import Config as roomsConfig

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

    def decode(self, p_topic, p_message, p_logmsg):
        """
        --> pyhouse/<housename>/house/outlet/<name>/...
        """
        p_logmsg += ''
        # l_light_name = extract_tools.get_mqtt_field(p_message, 'LightName')
        if len(p_topic) > 0:
            l_name = p_topic[0]
            p_topic = p_topic[1:]
            if len(p_topic) > 0:
                if p_topic[0] == 'STATE':
                    p_logmsg += '\tState:\n'
                elif p_topic[0] == 'RESULT':
                    p_logmsg += '\tResult:\n'
                elif p_topic[0] == 'POWER':
                    p_logmsg += '\tResult:\n'
                elif p_topic[0] == 'LWT':
                    p_logmsg += '\tResult:\n'
                else:
                    p_logmsg += '\tUnknown house/outlet sub-topic: {}; - {}'.format(p_topic, p_message)
                    LOG.warn('Unknown "house/outlet" sub-topic: {}\n\tTopic: {}\n\tMessge: {}'.format(p_topic[0], p_topic, p_message))
        return p_logmsg


class Config:
    """ The major work here is to load and save the information about a light switch.
    """
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _extract_room(self, p_config):
        """ Get the room and position within the room of the device.
        """
        l_ret = roomsConfig(self.m_pyhouse_obj).load_room_config(p_config)
        return l_ret

    def _extract_family(self, p_config):
        """
        """
        l_ret = familyConfig().extract_family_group(p_config, self.m_pyhouse_obj)
        return l_ret

    def _extract_one_outlet(self, p_config) -> dict:
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
        l_obj = OutletInformation()
        l_required = ['Name', 'Family']
        for l_key, l_value in p_config.items():
            # print('Light Key: {}; Val: {}'.format(l_key, l_val))
            if l_key == 'Family':
                l_ret = self._extract_family(l_value)
                l_obj.Family = l_ret
            elif l_key == 'Room':
                l_ret = self._extract_room(l_value)
                l_obj.Room = l_ret
                pass
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
        try:
            l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(CONFIG_NAME)
        except:
            self.m_pyhouse_obj.House.Lighting.Outlets = None
            return None
        try:
            l_yaml = l_node.Yaml['Outlets']
        except:
            LOG.warn('The outlets.yaml file does not start with "Outlets:"')
            self.m_pyhouse_obj.House.Lighting.Outlets = None
            return None
        l_outlets = self._extract_all_outlets(l_yaml)
        self.m_pyhouse_obj.House.Lighting.Outlets = l_outlets
        return l_outlets  # for testing purposes


class API:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))

    def SaveConfig(self):
        """
        """

# ## END DBK
