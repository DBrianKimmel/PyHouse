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

__updated__ = '2019-12-25'
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
        self.Access = None  # Optional ==> AccessInformation()
        self.LinkList = {}
        #
        self._Message = bytearray()
        self._Queue = None
        self._isLocal = False


class MqttActions:
    """ Mqtt section
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_msg):
        """ Decode Mqtt message
        ==> pyhouse/<house name>/house/lighting/controller/<action>

        @param p_msg.Topic: is the topic after 'controller'
        @return: a message to be logged as a Mqtt message
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        p_msg.LogMessage += '\tLighting/Controllers: {}\n\t'.format(p_msg.Topic)
        if l_topic[0] == 'control':
            p_msg.LogMessage += 'Controller Control: {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Controller Control'))
            LOG.debug('MqttLightingControllersDispatch Control Topic:{}\n\tMsg: {}'.format(p_msg.Topic, p_msg.Payload))
        elif l_topic[0] == 'status':
            # The status is contained in LightData() above.
            p_msg.LogMessage += 'Controller Status: {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Controller Status'))
            LOG.debug('MqttLightingControllersDispatch Status Topic:{}\n\tMsg: {}'.format(p_msg.Topic, p_msg.Payload))
        else:
            p_msg.LogMessage += '\tUnknown Lighting/Controller sub-topic:{}\n\t{}'.format(p_msg.Topic, PrettyFormatAny.form(p_msg.Payload, 'Controller Status'))
            LOG.warning('Unknown Controllers Topic: {}'.format(l_topic[0]))


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
        l_required = ['Name', 'Family', 'Interface']
        # l_groupfields = ['Family', 'Interface', 'Access']
        try:
            for l_key, l_value in p_config.items():
                # LOG.debug('Controller Key "{}"; Value: "{}"'.format(l_key, l_value))
                if l_key == 'Family':
                    l_obj.Family = self.m_config.extract_family_group(l_value)
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
            LOG.warning('Invalid entry of some type in "{}.yaml"\n\t{}'.format(CONFIG_NAME, e_err))
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
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Controllers']
        except:
            LOG.warning('The control file does not start with "Controllers:"')
            return None
        l_controllers = self._extract_all_controllers(l_yaml)
        # LOG.debug(PrettyFormatAny.form(l_controllers, 'Controllers'))
        return l_controllers


class Api:
    """
    """

    m_local_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def _add_storage(self) -> None:
        """
        """
        self.m_pyhouse_obj.House.Lighting.Controllers = {}

    def LoadConfig(self):
        """
        """
        LOG.info('Loading config.')
        self.m_pyhouse_obj.House.Lighting.Controllers = self.m_local_config.load_yaml_config()
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

    def Stop(self):
        pass  # Nothing needs stoping ATM

#  ## END DBK
