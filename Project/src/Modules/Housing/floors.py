"""
@name:      PyHouse/Project/src/Modules/Housing/f.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 21, 2019
@summary:   Handle the floor information for a house.

"""
from Modules.Core.data_objects import BaseObject

__updated__ = '2019-07-07'
__version_info__ = (19, 6, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities import \
    extract_tools, \
    config_tools

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Floors         ')

CONFIG_FILE_NAME = 'floors.yaml'


class FloorsInformation:
    """ A room of the house.
    Used to draw pictures of the house
    Used to define the location of switches, lights etc.

    ==> PyHouse.House.Rooms.xxx as in the def below
    """

    def __init__(self):
        super(FloorsInformation, self).__init__()
        self.Floor = {}  # FloorInformation()


class FloorInformation(BaseObject):
    """ A room of the house.
    Used to draw pictures of the house
    Used to define the location of switches, lights etc.

    ==> PyHouse.House.Rooms.xxx as in the def below
    """

    def __init__(self):
        super(FloorInformation, self).__init__()
        self.Description = None


class Yaml:
    """
    """

    def _extract_floor_config(self, p_yaml):
        """
        @return: a FloorInformation() object with all data filled in.
        """
        l_obj = FloorInformation()
        # Every k,v in the yaml file needs exist in the FloorInformaton object.
        for l_key, l_val in p_yaml.items():
            try:
                _l_x = getattr(l_obj, l_key)
            except AttributeError:
                LOG.warn('floors.yaml contains a bad floor item "{}" = {} - Ignored.'.format(l_key, l_val))
                continue
            setattr(l_obj, l_key, l_val)
        for l_key in [l_attr for l_attr in dir(l_obj) if not callable(getattr(l_obj, l_attr)) and not l_attr.startswith('_')]:
            l_val = getattr(l_obj, l_key)
            if l_val == None:
                LOG.warn('"floors.yaml" is missing an entry for "{}"'.format(l_key))
        return l_obj

    def _update_floors_from_yaml(self, p_pyhouse_obj, p_yaml):
        """ Fill in the House.Floors from the Yaml config file
        Read in the config file, extract each floor's data, and copy the data to the pyhouse_obj
        """
        try:
            l_yaml = p_yaml['Floors']
        except:
            LOG.error('The "Floors" tag is missing in the "floors.yaml" file!')
            return None
        # LOG.debug(PrettyFormatAny.form(l_yaml, 'Yaml'))
        l_loc = p_pyhouse_obj.House.Floors
        l_floors = {}
        for l_ix, l_floor in enumerate(l_yaml):
            l_floors[l_ix] = self._extract_floor_config(l_floor)
        p_pyhouse_obj.House.Floors = l_floors
        return l_loc  # For testing.

    def LoadYamlConfig(self, p_pyhouse_obj):
        """ Read the Rooms.Yaml file.
        It contains Floor and Rooms sections.
        """
        l_node = config_tools.Yaml(p_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        LOG.debug('Yaml from floors.yaml {}\n{}'.format(l_node, l_node.Yaml))
        self._update_floors_from_yaml(p_pyhouse_obj, l_node.Yaml)
        return p_pyhouse_obj.House.Floors  # for testing purposes

    def _copy_floors_to_yaml(self, p_pyhouse_obj):
        """ Prepare floors to export to yaml config file
        """
        l_node = p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME]
        l_config = l_node.Yaml['Floors']
        l_working = p_pyhouse_obj.House.Floors
        try:
            for l_key in [l_attr for l_attr in dir(l_working) if not l_attr.startswith('_')  and not callable(getattr(l_working, l_attr))]:
                l_val = getattr(l_working, l_key)
                l_config[l_key] = l_val
        except Exception as e_err:
            LOG.error('Error - Key: {}; Val: {}; Err: {}'.format(l_key, l_val, e_err))
        p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME].Yaml['Floors'] = l_config
        l_ret = {'Floors': l_config}
        return l_ret

    def SaveYamlConfig(self, p_pyhouse_obj):
        """
        """
        # LOG.debug('Saving Config - Version:{}'.format(__version__))
        l_yaml = self._copy_floors_to_yaml(p_pyhouse_obj)
        config_tools.Yaml(p_pyhouse_obj).write_yaml(l_yaml, CONFIG_FILE_NAME, addnew=True)


class Mqtt:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj - p_pyhouse_obj

    def _decode_room(self, p_topic, p_message, p_logmsg):
        p_logmsg += '\tRooms:\n'
        if p_topic[1] == 'add':
            p_logmsg += '\tName: {}\n'.format(extract_tools.get_mqtt_field(p_message, 'Name'))
        elif p_topic[1] == 'delete':
            p_logmsg += '\tName: {}\n'.format(extract_tools.get_mqtt_field(p_message, 'Name'))
        elif p_topic[1] == 'sync':
            p_logmsg += '\tName: {}\n'.format(extract_tools.get_mqtt_field(p_message, 'Name'))
        elif p_topic[1] == 'update':
            p_logmsg += '\tName: {}\n'.format(extract_tools.get_mqtt_field(p_message, 'Name'))
        else:
            p_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Rooms msg', 160))
        return p_logmsg

    def dispatch(self, p_topic, p_message):
        pass

    def send_message(self, p_pyhouse_obj, p_topic, p_room_obj):
        """ Messages are:
                room/add - to add a new room to the database.
                room/delete - to delete a room from all nodes
                room/sync - to keep all nodes in sync periodically.
                room/update - to add or modify a room
        """
        l_topic = 'house/room/' + p_topic
        p_pyhouse_obj._APIs.Core.MqttAPI.MqttPublish(l_topic, p_room_obj)


class Api:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.House.Floors = FloorsInformation()

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        Yaml().LoadYamlConfig(self.m_pyhouse_obj)
        LOG.info('Loaded {} Floors'.format(len(self.m_pyhouse_obj.House.Floors)))

    def SaveConfig(self):
        """
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        Yaml().SaveYamlConfig(self.m_pyhouse_obj)

#  ## END DBK
