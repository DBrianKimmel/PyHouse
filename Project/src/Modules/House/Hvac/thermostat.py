"""
@name:      Modules/House/Hvac/thermostat.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2019 by D. Brian Kimmel
@note:      Created on Aug 28, 2019
@license:   MIT License
@summary:   Handle the hvac thermostat

"""

__updated__ = '2019-12-02'
__version_info__ = (19, 10, 11)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyHouse files
from Modules.Core.Config.config_tools import Api as configApi

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Thermostat    ')

CONFIG_NAME = 'thermostat'


class ThermostatInformation:
    """

    ==> PyHouse.House.Hvac.Thermostats.xxx as in the def below
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.CoolSetPoint = 0
        self._CurrentTemperature = 0
        self.HeatSetPoint = 0
        self.Mode = 'Cool'  # Cool | Heat | Auto | EHeat
        self.Scale = 'F'  # F | C
        self._Status = 'Off'  # On
        self.Family = None  # FamilyInformation()


class ThermostatStatusInformation:
    """
    """

    def __init__(self):
        self.Name = None
        self.Status = None
        self.Fan = None
        self.Mode = None
        self.Family = 'insteon'
        self.BrightnessPct = None


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_one_thermostat(self, p_config) -> dict:
        """ Extract the config info for one button.
        @param p_config: is the config fragment containing one button's information.
        @return: a ButtonInformation() obj filled in.
        """
        l_obj = ThermostatInformation()
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
                LOG.warning('"{}" is missing an entry for "{}"'.format(CONFIG_NAME, l_key))
        # LOG.debug(PrettyFormatAny.form(l_obj, 'Thermostat'))
        # LOG.debug(PrettyFormatAny.form(l_obj.Family, 'Thermostat.Family'))
        return l_obj

    def _extract_all_thermostats(self, p_config):
        """ Get all of the button sets configured
        A Button set is a (mini-remote) with 4 or 8 buttons in the set
        The set has one insteon address and each button is in a group
        """
        l_dict = {}
        for l_ix, l_item in enumerate(p_config):
            # print('Light: {}'.format(l_light))
            l_button_obj = self._extract_one_thermostat(l_item)
            l_dict[l_ix] = l_button_obj
        return l_dict

    def load_yaml_config(self):
        """ Read the thermostat.yaml file if it exists.  No file = not used.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj.House.Hvac.Thermostats = None
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Thermostats']
        except:
            LOG.warning('The config file does not start with "Thermostats:"')
            return None
        l_obj = self._extract_all_button_sets(l_yaml)
        self.m_pyhouse_obj.House.Hvac.Thermostats = l_obj
        return l_obj  # for testing purposes


class Api:
    """
    """
    m_pyhouse_obj = None
    m_local_config = None

    def __init__(self, p_pyhouse_obj):
        p_pyhouse_obj.House.Hvac.Thermostats = None
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """
        """
        LOG.info('Load Config')
        self.m_local_config.load_yaml_config()
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Lighting.Buttons, 'buttons.Api.LoadConfig'))
        return

    def SaveConfig(self):
        """
        """

    def Stop(self):
        _x = PrettyFormatAny.form(self.m_pyhouse_obj, 'PyHouse')

# ## END DBK

