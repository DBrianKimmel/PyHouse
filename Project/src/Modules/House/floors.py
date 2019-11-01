"""
@name:      Modules/House/floors.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 21, 2019
@summary:   Handle the floor information for a house.

"""

__updated__ = '2019-10-31'
__version_info__ = (19, 10, 2)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities import extract_tools
from Modules.Core.data_objects import BaseObject

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Floors         ')

CONFIG_NAME = 'floors'


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
        self.Floor = None
        self.Description = None


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj - p_pyhouse_obj

    def decode(self, p_topic, p_message, p_logmsg):
        p_logmsg += '\tFloors:\n'
        if p_topic[1] == 'add':
            p_logmsg += '\tName: {}\n'.format(extract_tools.get_mqtt_field(p_message, 'Name'))
        elif p_topic[1] == 'delete':
            p_logmsg += '\tName: {}\n'.format(extract_tools.get_mqtt_field(p_message, 'Name'))
        elif p_topic[1] == 'update':
            p_logmsg += '\tName: {}\n'.format(extract_tools.get_mqtt_field(p_message, 'Name'))
        elif p_topic[1] == 'request':
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
        # l_json = encode_json(p_room_obj)
        # l_topic = 'house/room/' + p_topic


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_one_floor(self, p_config):
        """
        @return: a FloorInformation() object with all data filled in.
        """
        l_obj = FloorInformation()
        l_required = ['Name', 'Floor']
        for l_key, l_value in p_config.items():
            try:
                _l_x = getattr(l_obj, l_key)
            except AttributeError:
                LOG.warn('floors.yaml contains a bad floor item "{}" = {} - Ignored.'.format(l_key, l_value))
                continue
            setattr(l_obj, l_key, l_value)
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('Location Yaml is missing an entry for "{}"'.format(l_key))
        LOG.info('Extracted floor "{}"'.format(l_obj.Name))
        return l_obj

    def _extract_all_floors(self, p_config):
        """ Fill in the House.Floors from the Yaml config file
        Read in the config file, extract each floor's data, and copy the data to the pyhouse_obj
        """
        # LOG.debug(PrettyFormatAny.form(l_yaml, 'Yaml'))
        l_floors = {}
        # LOG.debug('')
        for l_ix, l_floor in enumerate(p_config):
            l_floors[l_ix] = self._extract_one_floor(l_floor)
        self.m_pyhouse_obj.House.Floors = l_floors
        LOG.info('Extracted {} Floors'.format(len(l_floors)))
        return l_floors  # For testing.

    def load_yaml_config(self):
        LOG.info('Loading Config - Version:{}'.format(__version__))
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            self.m_pyhouse_obj.House.Floors = None
            return None
        try:
            l_yaml = l_yaml['Floors']
        except:
            LOG.warn('The config file does not start with "Floors:"')
            self.m_pyhouse_obj.House.Floors = None
            return None
        l_floors = self._extract_all_floors(l_yaml)
        self.m_pyhouse_obj.House.Floors = l_floors
        return l_floors  # for testing purposes

# ----------

    def _copy_floors_to_yaml(self):
        """ Prepare floors to export to yaml config file
        """
        l_node = None  # self.m_pyhouse_obj._Config.YamlTree[CONFIG_NAME]
        l_config = l_node.Yaml['Floors']
        l_working = self.m_pyhouse_obj.House.Floors
        try:
            for l_key in [l_attr for l_attr in dir(l_working) if not l_attr.startswith('_')  and not callable(getattr(l_working, l_attr))]:
                l_val = getattr(l_working, l_key)
                l_config[l_key] = l_val
        except Exception as e_err:
            LOG.error('Error - Key: {}; Val: {}; Err: {}'.format(l_key, l_val, e_err))
        # self.m_pyhouse_obj._Config.YamlTree[CONFIG_NAME].Yaml['Floors'] = l_config
        l_ret = {'Floors': l_config}
        return l_ret

    def save_yaml_config(self):
        """
        """
        # LOG.debug('Saving Config - Version:{}'.format(__version__))
        l_yaml = self._copy_floors_to_yaml()
        self.m_config.write_config(CONFIG_NAME, l_yaml, addnew=True)


class Api:
    """
    """

    m_pyhouse_obj = None
    m_local_config = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        p_pyhouse_obj.House.Floors = FloorsInformation()

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_local_config.load_yaml_config()
        LOG.info('Loaded {} Floors'.format(len(self.m_pyhouse_obj.House.Floors)))

    def Start(self):
        pass

    def SaveConfig(self):
        """
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        self.m_local_config.save_yaml_config()

    def Stop(self):
        _x = PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse_obj')

#  ## END DBK
