"""
@name:      Modules/House/Lighting/buttons.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2019 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system automation.

"""

__updated__ = '2019-11-28'
__version_info__ = (19, 9, 2)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyHouse files
from Modules.Core.Config.config_tools import Api as configApi

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Buttons        ')

CONFIG_NAME = 'buttons'


class ButtonInformation:

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.DeviceType = 'Lighting'
        self.DeviceSubType = 'Button'
        self.Family = None  # FamilyInformation()
        self.Room = None  # RoomInformation()


class ButtonFamilyInformation:
    """ This is the family information we need for a light

    Families may stuff other necessary information in here.
    """

    def __init__(self):
        self.Name = None
        self.Comment = None  # Optional
        self.Address = None


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_one_button_set(self, p_config) -> dict:
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
        l_obj = ButtonInformation()
        l_required = ['Name', 'Family']
        for l_key, l_value in p_config.items():
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
        # LOG.debug(PrettyFormatAny.form(l_obj, 'Button'))
        # LOG.debug(PrettyFormatAny.form(l_obj.Family, 'Button.Family'))
        LOG.info('Extracted button "{}"'.format(l_obj.Name))
        return l_obj

    def _extract_all_button_sets(self, p_config):
        """ Get all of the button sets configured
        A Button set is a (mini-remote) with 4 or 8 buttons in the set
        The set has one insteon address and each button is in a group
        """
        l_dict = {}
        for l_ix, l_button in enumerate(p_config):
            # print('Light: {}'.format(l_light))
            l_button_obj = self._extract_one_button_set(l_button)
            l_dict[l_ix] = l_button_obj
        return l_dict

    def load_yaml_config(self):
        """ Read the buttons.yaml file if it exists.  No file = no buttons.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj.House.Lighting.Buttons = None
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Buttons']
        except:
            LOG.warn('The config file does not start with "Buttons:"')
            return None
        l_buttons = self._extract_all_button_sets(l_yaml)
        self.m_pyhouse_obj.House.Lighting.Buttons = l_buttons
        return l_buttons  # for testing purposes


class Api:
    """
    """
    m_pyhouse_obj = None
    m_local_config = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """
        """
        LOG.info('Load Config')
        self.m_local_config.load_yaml_config()
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Buttons, 'buttons.Api.LoadConfig'))
        return {}

    def SaveConfig(self):
        """
        """

    def Stop(self):
        _x = PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse')

#  ## END DBK
