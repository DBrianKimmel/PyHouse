"""
@name:      PyHouse/Project/src/Modules/Housing/f.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 21, 2019
@summary:   Handle the floor information for a house.

"""

__updated__ = '2019-06-26'
__version_info__ = (19, 6, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
# import os
import datetime

#  Import PyMh files
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities import \
    extract_tools, \
    config_tools
from Modules.Housing.house_data import \
    FloorsInformationPrivate, \
    FloorInformation

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Floors         ')

CONFIG_FILE_NAME = 'floors.yaml'


class Yaml:
    """
    """

    def _extract_floor_config(self, p_yaml):
        """
        """
        l_obj = FloorInformation()
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
        return l_loc  # For testing.

    def LoadConfig(self, p_pyhouse_obj):
        """ Read the Rooms.Yaml file.
        It contains Floor and Rooms sections.
        """
        l_node = config_tools.Yaml(p_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        LOG.debug('Yaml from floors.yaml {}\n{}'.format(l_node, l_node.Yaml))
        p_pyhouse_obj.House.Floors = self._update_floors_from_yaml(p_pyhouse_obj, l_node.Yaml)
        return p_pyhouse_obj.House.Floors  # for testing purposes

    def _copy_floors_to_yaml(self, p_pyhouse_obj, p_filename):
        """ Prepare floors to export to yaml config file
        """
        l_loc = p_pyhouse_obj.House.Floors
        # print(PrettyFormatAny.form(l_loc, 'Floors', 190))
        l_yaml = p_pyhouse_obj._Config.YamlTree[p_filename]
        # print(PrettyFormatAny.form(l_yaml, 'Yaml', 190))
        for l_key in [l_attr for l_attr in dir(l_loc) if not callable(getattr(l_loc, l_attr)) and not l_attr.startswith('_')]:
            l_val = getattr(l_loc, l_key)
        return l_loc

    def SaveConfig(self, p_pyhouse_obj):
        """
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        l_yaml = self._copy_floors_to_yaml(p_pyhouse_obj, CONFIG_FILE_NAME)
        # l_data = p_pyhouse_obj.House.Rooms._Yaml
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
        p_pyhouse_obj._APIs.Computer.MqttAPI.MqttPublish(l_topic, p_room_obj)


class Api:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.House.Floors = FloorsInformationPrivate()

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        Yaml().LoadConfig(self.m_pyhouse_obj)

    def SaveConfig(self):
        """
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        Yaml().SaveConfig(self.m_pyhouse_obj)

#  ## END DBK
