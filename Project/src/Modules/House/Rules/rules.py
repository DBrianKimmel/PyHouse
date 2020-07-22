"""
@name:      Modules/House/Rules/rules.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 27, 2015
@Summary:

If garage door opens and after sunset and before sunrise, turn on outside garage door lights.

"""

__updated__ = '2020-02-04'
__version_info__ = (19, 12, 20)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
from typing import Optional

# Import PyMh files and modules.
from Modules.Core.Config.config_tools import Api as configApi

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Rules          ')

CONFIG_NAME = 'rules'


class RulesInformation:
    """ The collection of information about a house.
    Causes JSON errors due to Api type data methinks.

    ==> PyHouse.House.xxx as in the def below.
    """

    def __init__(self) -> None:
        self.Name: Optional[str] = None
        self.Comment: Optional[str] = None
        self.Event = None  # List of Names of the events that triggers this rule
        self.Condition = None  # List of additional conditions to activate the rule
        self.Device = None  # the device to control
        self.Type = None  # The type (On/Off)
        self.Action = None  # On, Off
        self.Delay = None  # How long to delay after trigger to action (time in seconds)
        self.Duration = None


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_one_rule(self, p_config):
        """
        """
        l_obj = RulesInformation()
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
                LOG.warning('Rules Yaml is missing an entry for "{}"'.format(l_key))
        # LOG.debug(PrettyFormatAny.form(l_obj, 'Button'))
        # LOG.debug(PrettyFormatAny.form(l_obj.Family, 'Button.Family'))
        LOG.info('Extracted Rule "{}"'.format(l_obj.Name))
        return l_obj

    def _extract_all_rules(self, p_config):
        """
        """
        l_dict = {}
        for l_ix, l_rule in enumerate(p_config):
            # print('Light: {}'.format(l_light))
            l_rule_obj = self._extract_one_rule(l_rule)
            l_dict[l_ix] = l_rule_obj
        return l_dict

    def load_yaml_config(self):
        LOG.info('Loading Config - Version:{}'.format(__version__))
        l_yaml = self.m_config.read_config_file(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Rules']
        except:
            LOG.warning('The config file does not start with "Rules:"')
            return None
        l_rules = self._extract_all_rules(l_yaml)
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Schedules[0], 'Schedule[0]'))
        return l_rules

# ----------

    def save_yaml_config(self):
        pass


class Api:

    m_pyhouse_obj = None
    m_local_config = None

    def __init__(self, p_pyhouse_obj) -> None:
        LOG.info("Initializing - Version:{}".format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_local_config = LocalConfig(p_pyhouse_obj)

    def _add_storage(self):
        """
        """
        self.m_pyhouse_obj.House.Rules = {}

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config')
        self.m_pyhouse_obj.House.Rules = self.m_local_config.load_yaml_config()

    def Start(self):
        """
        """
        LOG.info('Starting Rules')

    def SaveConfig(self):
        """
        """
        LOG.info('Saving Config')
        self.m_local_config.save_yaml_config()

    def Stop(self):
        pass

# ## END DBK
