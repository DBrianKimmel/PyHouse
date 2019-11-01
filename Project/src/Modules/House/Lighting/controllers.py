"""
@name:      Modules/House/Lighting/controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2019 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system automation.

First we have the basic information about the controller.
Then we have the Lighting system information.
Then we have the information specific to the family of the controller (Insteon, USB, Zigbee, etc.).
Then we have the interface information (Ethernet, USB, Serial, ...).
And we also have information about the controller class of devices.
"""

__updated__ = '2019-10-30'
__version_info__ = (19, 10, 4)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.Config.config_tools import Api as configApi

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Controllers    ')

CONFIG_NAME = 'controllers'


class ControllerInformation:
    """
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.DeviceType = 'Lighting'
        self.DeviceSubType = 'Controller'
        self.Family = None  # LightFamilyInformation()
        self.Interface = None  # Interface module specific  DriverInterfaceInformation()
        self.Access = None  # Optional ==> SecurityInformation()
        #
        self._Message = bytearray()
        self._Queue = None
        self._isLocal = False


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


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_one_controller(self, p_config):
        """ Extract the config info for one Controller.

        @return: ==> ControllerInformation()
        """
        l_obj = ControllerInformation()
        l_obj.DeviceType = 'Lighting'
        l_obj.DeviceSubType = 'Controller'
        l_required = ['Name', 'Family', 'Interface']
        # l_groupfields = ['Family', 'Interface', 'Access']
        try:
            for l_key, l_value in p_config.items():
                # LOG.debug('Controller Key "{}"; Value: "{}"'.format(l_key, l_value))
                if l_key == 'Family':
                    l_obj.Family = self.m_config.extract_family_group(l_value)
                    self.m_pyhouse_obj.House.Family[l_obj.Family.Name.lower()] = l_obj.Family
                elif l_key == 'Access':
                    l_obj.Access = self.m_config._get_name_password(l_value)
                elif l_key == 'Interface':
                    l_obj.Interface = self.m_config.extract_interface_group(l_value)
                    if l_obj.Interface.Host.lower() == self.m_pyhouse_obj.Computer.Name.lower():
                        l_obj._isLocal = True
                    # LOG.debug(PrettyFormatAny.form(l_obj, 'Controller'))
                    # LOG.debug(PrettyFormatAny.form(l_obj.Interface, 'Interface'))
                else:
                    setattr(l_obj, l_key, l_value)
        except Exception as e_err:
            LOG.warn('Invalid entry of some type in "{}.yaml"\n\t{}'.format(CONFIG_NAME, e_err))
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.error('The Controller "{}" is missing a required entry for "{}"'.format(l_obj.Name, l_key))
                # LOG.debug(PrettyFormatAny.form(l_obj, 'Controller'))
                return l_obj
        # LOG.debug('Controller "{}" is Local: {}'.format(l_obj.Name, l_obj._isLocal))
        LOG.info('Extracted controller "{}"'.format(l_obj.Name))
        return l_obj

    def _extract_all_controllers(self, p_config):
        """
        PyHouse.House.Lighting.Controllers
        """
        l_dict = {}
        for l_key, l_value in enumerate(p_config):
            l_obj = self._extract_one_controller(l_value)
            l_dict[l_key] = l_obj
        # LOG.debug(PrettyFormatAny.form(l_dict, 'Controllers'))
        # LOG.info('Loaded {} controllers'.format(len(l_dict)))
        return l_dict

    def load_yaml_config(self):
        """ Read the controllers.yaml file if it exists.
        It contains Controllers data for the house.
        """
        # LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj.House.Lighting.Controllers = None
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Controllers']
        except:
            LOG.warn('The control file does not start with "Controllers:"')
            return None
        l_controllers = self._extract_all_controllers(l_yaml)
        self.m_pyhouse_obj.House.Lighting.Controllers = l_controllers
        # LOG.debug(PrettyFormatAny.form(l_controllers, 'Controllers'))
        return l_controllers  # for testing purposes


class Api:
    """
    """

    m_local_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """
        """
        LOG.info('Loading config.')
        self.m_local_config.load_yaml_config()
        LOG.info('Loaded {} Controllers.'.format(len(self.m_pyhouse_obj.House.Lighting.Controllers)))

    def Start(self):
        """
        """
        LOG.info('Starting.')
        l_controllers = self.m_pyhouse_obj.House.Lighting.Controllers
        for l_controller in l_controllers.values():
            if l_controller._isLocal:
                LOG.info('Starting controller "{}"'.format(l_controller.Name))
            pass

    def SaveConfig(self):
        """
        """

#  ## END DBK
