"""
@name:      Modules/Housing/Lighting/lighting_controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2019 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system automation.

Reading and writing XML to save controller information is fairly complete.
First we have the basic information about the controller.
Then we have the Lighting system information.
Then we have the information specific to the family of the controller (Insteon, USB, Zigbee, etc.).
Then we have the interface information (Ethernet, USB, Serial, ...).
And we also have information about the controller class of devices.


"""

__updated__ = '2019-07-24'
__version_info__ = (19, 7, 2)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.Utilities import config_tools
from Modules.Drivers.interface import Config as interfaceConfig
from Modules.Families.family import Config as familyConfig
from Modules.Housing.Security.login import Config as loginConfig

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.LightController')

CONFIG_FILE_NAME = 'controllers.yaml'


class ControllerInformation:
    """
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.DeviceType = 'Lighting'
        self.DeviceSubType = 'Controller'
        self.Family = None  # LightFamilyInformation()
        self.Interface = None  # Interface module specific Information()
        self.Login = None  # LoginInformation() Optional
        self._Message = bytearray()
        self._Queue = None
        self._DriverAPI = None


class MqttActions:
    """ Mqtt section
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_topic, p_message):
        """ Decode Mqtt message
        ==> pyhouse/<house name>/house/lighting/controller/<action>

        @param p_topic: is the topic after 'controller'
        @return: a message to be logged as a Mqtt message
        """
        l_logmsg = '\tLighting/Controllers: {}\n\t'.format(p_topic)
        if p_topic[0] == 'control':
            l_logmsg += 'Controller Control: {}'.format(PrettyFormatAny.form(p_message, 'Controller Control'))
            LOG.debug('MqttLightingControllersDispatch Control Topic:{}\n\tMsg: {}'.format(p_topic, p_message))
        elif p_topic[0] == 'status':
            # The status is contained in LightData() above.
            l_logmsg += 'Controller Status: {}'.format(PrettyFormatAny.form(p_message, 'Controller Status'))
            LOG.debug('MqttLightingControllersDispatch Status Topic:{}\n\tMsg: {}'.format(p_topic, p_message))
        else:
            l_logmsg += '\tUnknown Lighting/Controller sub-topic:{}\n\t{}'.format(p_topic, PrettyFormatAny.form(p_message, 'Controller Status'))
            LOG.warn('Unknown Controllers Topic: {}'.format(p_topic[0]))
        return l_logmsg


class Config:
    """
    """

    def _extract_family(self, p_config):
        """
        """
        l_ret = familyConfig().load_family_config(p_config, self.m_pyhouse_obj)
        return l_ret

    def _extract_interface(self, p_config):
        """
        """
        l_ret = interfaceConfig().load_interface(p_config)
        return l_ret

    def _extract_login(self, p_config):
        """
        """
        l_ret = loginConfig.load_name_password(p_config)
        return  l_ret

    def _load_one_controller(self, p_config):
        """ Extract the config info for one Controller.
        """
        l_obj = ControllerInformation()
        l_required = ['Name', 'Family', 'Interface']
        for l_key, l_value in p_config.items():
            # print('Controller Key: {}; Value: {}'.format(l_key, l_value))
            if l_key == 'Family':
                l_ret = self._extract_family(l_value)
                l_obj.Family = l_ret
            elif l_key == 'Interface':
                l_ret = self._extract_interface(l_value)
                l_obj.Interface = l_ret
            elif l_key == 'Login':
                l_ret = self._extract_login(l_value)
                l_obj.Interface = l_ret
            else:
                setattr(l_obj, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.error('The Controller "{}" is missing a rquired entry for "{}"'.format(l_obj.Name, l_key))
                return None
        LOG.info('Loaded controller {}'.format(l_obj.Name))
        return l_obj

    def _load_all_controllers(self, p_config):
        """
        PyHouse.House.Lighting.Controllers
        """
        l_dict = {}
        for l_ix, l_key in enumerate(p_config):
            # print('Controllers Key: {}'.format(l_key))
            l_obj = self._load_one_controller(l_key)
            l_dict[l_ix] = l_obj
        return l_dict

    def LoadYamlConfig(self, p_pyhouse_obj):
        """ Read the controllers.yaml file if it exists.
        It contains Controllers data for the house.
        """
        # LOG.info('Loading _Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj = p_pyhouse_obj
        try:
            l_node = config_tools.Yaml(p_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        except:
            p_pyhouse_obj.House.Lighting.Controllers = None
            return None
        try:
            l_yaml = l_node.Yaml['Controllers']
        except:
            LOG.warn('The controllers.yaml file does not start with "Controllers:"')
            p_pyhouse_obj.House.Lighting.Controllers = None
            return None
        l_controllers = self._load_all_controllers(l_yaml)
        p_pyhouse_obj.House.Lighting.Controllers = l_controllers
        return l_controllers  # for testing purposes

# ----------

    def _copy_to_yaml(self, p_pyhouse_obj):
        """ Update the yaml information.
        The information in the YamlTree is updated to be the same as the running pyhouse_obj info.

        The running info is a dict and the yaml is a list!

        @return: the updated yaml ready information.
        """
        l_node = p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME]
        l_config = l_node.Yaml['Controllers']
        l_working = p_pyhouse_obj.House.Lighting.Controllers
        for l_key in [l_attr for l_attr in dir(l_working) if not l_attr.startswith('_')  and not callable(getattr(l_working, l_attr))]:
            l_val = getattr(l_working, l_key)
            setattr(l_config, l_key, l_val)
        p_pyhouse_obj._Config.YamlTree[CONFIG_FILE_NAME].Yaml['Controllers'] = l_config
        l_ret = {'Controllers': l_config}
        return l_ret

    def SaveYamlConfig(self, p_pyhouse_obj):
        """
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        l_config = self._copy_to_yaml(p_pyhouse_obj)
        config_tools.Yaml(p_pyhouse_obj).write_yaml(l_config, CONFIG_FILE_NAME, addnew=True)
        return l_config


class API:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def LoadConfig(self):
        """
        """
        Config().LoadYamlConfig(self.m_pyhouse_obj)

    def SaveConfig(self):
        """
        """

#  ## END DBK
