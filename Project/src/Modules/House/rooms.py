"""
@name:      PyHouse/Project/src/Modules/House/rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Handle the rooms information for a house.

"""

__updated__ = '2019-08-09'
__version_info__ = (19, 6, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import datetime

#  Import PyMh files
from Modules.Core.Utilities import extract_tools, config_tools
from Modules.Core.Utilities.coordinate_tools import Coords
from Modules.Core.Utilities.json_tools import encode_json
from Modules.Core.Utilities.config_tools import ConfigYamlNodeInformation
from Modules.House.house_data import \
    RoomInformation, \
    RoomsInformationPrivate

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Rooms          ')

CONFIG_FILE_NAME = 'rooms.yaml'


class RoomInformation:
    """ A room of the house.
    Used to draw pictures of the house
    Used to define the location of switches, lights etc.

    ==> PyHouse.House.Rooms.xxx as in the def below
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.Corner = None  # CoordinateInformation()
        self.Floor = None  # Outside | Basement | 1st | 2nd | 3rd | 4th | Attic | Roof
        self.RoomType = None
        self.Size = None  # CoordinateInformation()
        self.Trigger = None


class Config:
    """ This will handle the rooms.yaml file
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def load_room_config(self, p_config):
        """ Get the room information for some other config
        """
        l_obj = RoomInformation()
        try:
            for l_key, l_value in p_config.items():
                # print('RoomKey:{}; Value:{}'.format(l_key, l_value))
                setattr(l_obj, l_key, l_value)
            return l_obj
        except:
            l_obj.Name = p_config

    def _extract_one_room(self, p_config) -> dict:
        """ Extract the config info for one room.
        Warn if there are extra attributes in the config.
        Warn if there are missing attributes in the config.

        @param p_yaml: is the config fragment containing one room's information.
        @return: a RoomInformation() obj filled in.
        """
        l_required = ['Name']
        l_obj = RoomInformation()
        for l_key, l_value in p_config.items():
            # Check for extra attributes in the config file.
            try:
                _l_x = getattr(l_obj, l_key)
            except AttributeError:
                LOG.warn('rooms.yaml contains a bad room item "{}" = {} - Ignored.'.format(l_key, l_value))
                continue
            setattr(l_obj, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('Location Yaml is missing an entry for "{}"'.format(l_key))
        return l_obj

    def _extract_all_rooms(self, p_config):
        """ Copies the data from the yaml config file to the Rooms part of the PyHouse obj.
        Check for duplicate room names!
        @param p_pyhouse_obj: is the entire house object
        @param p_node_yaml: is ConfigYamlNodeInformation filled with room data.
            {'Rooms': [{'Name': 'Outside', 'Active': 'True', 'Comment': 'Things outsi...
        """
        l_rooms = {}
        for l_ix, l_value in enumerate(p_config):
            l_obj = self._extract_one_room(l_value)
            l_rooms.update({l_ix:l_obj})
        self.m_pyhouse_obj.House.Rooms = l_rooms
        return l_rooms  # For testing.

    def LoadYamlConfig(self):
        """ Read the Rooms.Yaml file.
        It contains Rooms data for all rooms in the house.
        """
        # LOG.info('Loading _Config - Version:{}'.format(__version__))
        try:
            l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        except:
            self.m_pyhouse_obj.House.Rooms = None
            return None
        try:
            l_yaml = l_node.Yaml['Rooms']
        except:
            LOG.warn('The rooms.yaml file does not start with "Rooms:"')
            self.m_pyhouse_obj.House.Rooms = None
            return None
        l_rooms = self._extract_all_rooms(l_yaml)
        self.m_pyhouse_obj.House.Rooms = l_rooms
        return l_rooms  # for testing purposes

# ----------

    def _copy_to_yaml(self, p_pyhouse_obj):
        """ Update the yaml information.
        The information in the YamlTree is updated to be the same as the running pyhouse_obj info.

        The running info is a dict and the yaml is a list!

        @return: the updated yaml ready information.
        """
        l_node = p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME]
        l_config = l_node.Yaml['Rooms']
        l_working = p_pyhouse_obj.House.Rooms
        for l_key in [l_attr for l_attr in dir(l_working) if not l_attr.startswith('_')  and not callable(getattr(l_working, l_attr))]:
            l_val = getattr(l_working, l_key)
            setattr(l_config, l_key, l_val)
        p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME].Yaml['Rooms'] = l_config
        l_ret = {'Rooms': l_config}
        return l_ret

    def SaveYamlConfig(self):
        """
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        l_config = self._copy_to_yaml(self.m_pyhouse_obj)
        config_tools.Yaml(self.m_pyhouse_obj).write_yaml(l_config, CONFIG_FILE_NAME, addnew=True)
        return l_config


class Maint:
    """ Maintain the room internal database.
    """

    @staticmethod
    def _json_2_obj(p_json):
        l_obj = RoomInformation
        l_obj.Name = p_json['Name']
        # l_obj.Active = p_json['Active']
        l_obj.Key = 0
        l_obj.UUID = p_json['UUID']
        l_obj.Comment = p_json['Comment']
        l_obj.Corner = Coords._get_coords(p_json['Corner'])
        l_obj.Floor = p_json['Floor']
        l_obj.Size = Coords._get_coords(p_json['Size'])
        l_obj.RoomType = p_json['RoomType']
        l_obj._AddFlag = p_json['Add']
        l_obj._DeleteFlag = p_json['Delete']
        return l_obj

    def from_web(self, p_pyhouse_obj, p_json):
        """ The web browser has sent back an add/change/delete request.
        """
        # LOG.info('Room debug {}'.format(p_json))
        l_obj = Maint._json_2_obj(p_json)
        if l_obj._DeleteFlag:
            l_room = Sync.find_room_uuid(p_pyhouse_obj, l_obj.UUID)
            if l_room is None:
                LOG.error("Trying to delete non existent room {}".format(l_obj.Name))
            else:
                LOG.info('Deleting Room {}'.format(l_obj.Name))
                Maint._delete_room(p_pyhouse_obj, l_obj)
        else:  # Add/Change
            l_rooms = self._add_change_room(p_pyhouse_obj, l_obj)
            p_pyhouse_obj.House.Rooms = l_rooms

    def _add_change_room(self, p_pyhouse_obj, p_room_obj):
        """
        Update a room or add a new room if the UUID does not exist
        """
        l_rooms = p_pyhouse_obj.House.Rooms
        l_len = len(l_rooms)

        for l_key, l_val in l_rooms.items():
            if l_val.UUID == p_room_obj.UUID:
                LOG.info('Updating room {}'.format(p_room_obj.Name))
                l_rooms[l_key] = l_val
                l_rooms[l_key].LastUpdate = datetime.datetime.now()
                # Mqtt().send_message(p_pyhouse_obj, "update", p_room_obj)
                return l_rooms

        LOG.info('Adding room {}'.format(p_room_obj.Name))
        if Api(p_pyhouse_obj).find_room_uuid(p_pyhouse_obj, p_room_obj.UUID) is None and p_room_obj._DeleteFlag:
            pass
        p_room_obj.Key = l_len
        p_room_obj.LastUpdate = datetime.datetime.now()
        l_rooms[len(l_rooms)] = p_room_obj
        p_pyhouse_obj.House.Rooms = l_rooms
        # Mqtt().send_message(p_pyhouse_obj, "add", p_room_obj)
        return l_rooms

    @staticmethod
    def _delete_room(p_pyhouse_obj, p_room_obj):
        l_room_ix = int(p_room_obj.Key)
        try:
            del p_pyhouse_obj.House.Rooms[l_room_ix]
        except AttributeError:
            LOG.error("web_rooms - Failed to delete - JSON: {}".format(p_room_obj.Name))
        # Mqtt().send_message(p_pyhouse_obj, "delete", p_room_obj)
        return


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
        l_json = encode_json(p_room_obj)
        l_topic = 'house/room/' + p_topic
        p_pyhouse_obj._APIs.Core.MqttAPI.MqttPublish(l_topic, l_json)


class Sync:
    """ Used to sync the rooms between all the nodes.
    """

    @staticmethod
    def find_room_name(p_pyhouse_obj, p_name):
        l_rooms = p_pyhouse_obj.House.Rooms
        for l_room in l_rooms.values():
            if l_room.Name == p_name:
                return l_room
        return None

    @staticmethod
    def find_room_uuid(p_pyhouse_obj, p_uuid):
        l_rooms = p_pyhouse_obj.House.Rooms
        for l_room in l_rooms.values():
            if l_room.UUID == p_uuid:
                return l_room
        return None


class Api:
    """
    """

    m_pyhouse_obj = None
    m_config = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = Config(p_pyhouse_obj)
        p_pyhouse_obj.House.Rooms = RoomsInformationPrivate()
        p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME] = ConfigYamlNodeInformation()

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_config.LoadYamlConfig()
        LOG.info('Loaded {} Rooms'.format(len(self.m_pyhouse_obj.House.Rooms)))

    def SaveConfig(self):
        """
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        self.m_config.SaveYamlConfig()

#  ## END DBK
