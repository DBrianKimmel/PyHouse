"""
@name:      Modules/House/Security/garage_door.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on aug 26, 2019
@Summary:

"""

__updated__ = '2019-09-18'
__version_info__ = (19, 8, 1)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

# Import PyMh files
from Modules.Core.Config import config_tools
from Modules.House.Family.family import Config as familyConfig
from Modules.House.rooms import Config as roomConfig

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.GarageDoor     ')

CONFIG_NAME = 'garagedoor'


class GarageDoorInformation:
    """

    ==> PyHouse.House.Security.GarageDoors.xxx as in the def below
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.DeviceType = 'Security'
        self.DeviceSubType = 'GarageDoor'
        self.Family = None  # FamilyInformation()
        self.Room = None  # RoomInformation()
        self.Status = None  # Open | Closed


class Config:
    """
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _extract_one_garage_door(self, p_config) -> dict:
        """ Extract the config info for one button.
        - Name: Button 1
          Comment: This is _test button 1
          Family:
             Name: Insteon
             Address: 11.44.33
          Dimmable: true  # Optional
          Room:
             Name: Living Room
        @param p_config: is the config fragment containing one button's information.
        @return: a ButtonInformation() obj filled in.
        """
        l_obj = GarageDoorInformation()
        l_required = ['Name', 'Family']
        for l_key, l_value in p_config.items():
            if l_key == 'Family':
                l_obj.Family = familyConfig().extract_family_group(l_value, self.m_pyhouse_obj)
            elif l_key == 'Room':
                l_obj.Room = roomConfig(self.m_pyhouse_obj).load_room_config(l_value)
                pass
            else:
                setattr(l_obj, l_key, l_value)
        # Check for required data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('Location Yaml is missing an entry for "{}"'.format(l_key))
        # LOG.debug(PrettyFormatAny.form(l_obj, 'Button'))
        # LOG.debug(PrettyFormatAny.form(l_obj.Family, 'Button.Family'))
        return l_obj

    def _extract_all_garage_doors(self, p_config):
        """ Get all of the button sets configured
        A Button set is a (mini-remote) with 4 or 8 buttons in the set
        The set has one insteon address and each button is in a group
        """
        l_dict = {}
        for l_ix, l_button in enumerate(p_config):
            # print('Light: {}'.format(l_light))
            l_button_obj = self._extract_one_garage_door(l_button)
            l_dict[l_ix] = l_button_obj
        return l_dict

    def load_yaml_config(self):
        """ Read the lights.yaml file if it exists.  No file = no lights.
        It must contain 'Lights:'
        All the lights are a list.
        """
        LOG.info('Loading _Config - Version:{}'.format(__version__))
        try:
            l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(CONFIG_NAME)
        except:
            self.m_pyhouse_obj.House.Security.GarageDoors = None
            return None
        try:
            l_yaml = l_node.Yaml['GarageDoors']
        except:
            LOG.warn('The xxx.yaml file does not start with "GarageDoors:"')
            self.m_pyhouse_obj.House.Security.GarageDoors = None
            return None
        l_gdo = self._extract_all_garage_doors(l_yaml)
        self.m_pyhouse_obj.House.Security.GarageDoors = l_gdo
        return l_gdo  # for testing purposes


class API:
    """
    """
    m_pyhouse_obj = None
    m_config = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = Config(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """
        """
        LOG.info('Load Config')
        self.m_config.load_yaml_config()
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Buttons, 'buttons.API.LoadConfig'))
        return {}

    def SaveConfig(self):
        """
        """

# ## END DBK
