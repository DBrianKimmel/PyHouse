"""
@name:      Modules/House/Entertainment/entertainment.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
@summary:   Entertainment component access module.

Start up entertainment systems.

Listen to Mqtt message to control things...
==> pyhouse/<house name>/entertainment/<thing>

where <thing> is:
    onkyo          to control the Onkyo A/V devices
    pandora        to control the pandora player
    pioneer        to control the Pioneer A/V devices
    samsung        to control the Samsung A/V devices


House.Entertainment.Plugins{}.API
                             .Devices{}

"""

__updated__ = '2019-08-05'
__version_info__ = (18, 10, 2)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
import importlib

#  Import PyMh files and modules.
from Modules.Core.Utilities import extract_tools, config_tools
from Modules.House.Entertainment.entertainment_data import \
        EntertainmentDeviceControl
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Entertainment  ')

CONFIG_FILE_NAME = 'entertainment.yaml'


class EntertainmentInformation():
    """
    This is the PyHouse.House.Entertainment node of the master object.
    It is a dynamic structure for the various entertainment devices in a house.

    Top level

    ==> PyHouse.House.Entertainment.xxx as in the def below.
    """

    def __init__(self):
        self.PluginCount = 0
        # Plugins are indexed by the entertainment-family name (always lower cased).
        self.Plugins = {}  # EntertainmentPluginInformation()


class EntertainmentPluginInformation():
    """ This is filled in for every xxxSection under the Entertainment entry of the config file

    ==> PyHouse.House.Entertainment.Plugins[PluginName].xxx
    The family is the PluginName - onkyo, pandora, etc. - Always lower case.

    Valid Types:
        Service is a provided service such as Pandora, Netflix, Hulu, etc.
        Device is a Component such as a TV, DVD Player, A/V Receiver, etc.
    """

    def __init__(self):
        self.Name = None
        self.Type = 'Missing Type'  # Service: Component (a device):
        #
        # Devices are indexed by the device number 0..x
        self.DeviceCount = 0
        self.Devices = {}  # EntertainmentDeviceInformation()
        #
        # Services are indexed by the service number 0..x
        self.ServiceCount = 0
        self.Services = {}  # EntertainmentServiceInformation()
        #
        self._API = None  # The API pointer for this class of plugin (Pioneer, onkyo, ,,,)
        self._Module = None
        self._OpenSessions = 0


class MqttActions():
    """ Mqtt section
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_topic, p_message, _p_logmsg):
        """ Decode Mqtt message
        ==> pyhouse/<house name>/entertainment/<device-or-service>/...

        <device-or-service> = one of the VALID_ENTERTAINMENT_MFGRS

        These messages probably come from some external source such as node-red or alexa.

        @param p_topic: is the topic after 'entertainment'
        @return: a message to be logged as a Mqtt message
        """
        _l_sender = extract_tools.get_mqtt_field(p_message, 'Input')
        # LOG.debug('MqttEntertainmentDispatch Topic:{}\tSender:{}'.format(p_topic, l_sender))
        l_module = p_topic[0].lower()
        # Test entertainment exists and that plugins exist.
        try:
            if self.m_pyhouse_obj.House.Entertainment.PluginCount == 0:
                l_msg = 'This node contains no Entertainment Plugins, skipping.'
                LOG.info(l_msg)
                return l_msg
        except Exception as e_err:
            LOG.error('Should not happen. {}'.format(e_err))
        # Does the called for plugin exist?
        try:
            l_module_obj = self.m_pyhouse_obj.House.Entertainment.Plugins[l_module]
        except:
            l_msg = 'The entertainment module {} does not exist, skipping'.format(l_module)
            LOG.info(l_msg)
            return l_msg
        # Ok
        p_logmsg = '\tEntertainment: '
        try:
            l_module_api = l_module_obj._API
            p_logmsg += l_module_api.decode(p_topic[1:], p_message)
            # LOG.debug('{}'.format(p_logmsg))
        except (KeyError, AttributeError) as e_err:
            l_module_api = None
            p_logmsg += 'Module {} not defined {}'.format(l_module, e_err)
            LOG.error('Error in calling decode {}'.format(e_err))
        return p_logmsg


class Config:
    """
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def load_defined_plugins(self):
        """ Load the plugins called for in the config file.

        All plugins have been read in from entertainment.yaml
        Load the modules and their configs.
        """
        for l_name, l_plugin in self.m_pyhouse_obj.House.Entertainment.Plugins.items():
            l_plugin_name = 'Modules.House.Entertainment.' + l_name + '.' + l_name
            l_module = importlib.import_module(l_plugin_name)
            l_plugin._Module = l_module
            # Initialize Plugin
            l_plugin._API = l_module.API(self.m_pyhouse_obj)
            l_plugin._API.LoadConfig()
            LOG.info('Loaded Entertainment Plugin "{}".'.format(l_plugin_name))
            pass

    def _extract_services(self, p_pyhouse_obj, p_yaml):
        """ Get a service loaded
        """
        # LOG.debug('Services:\n\t{}'.format(p_yaml))
        for l_service in p_yaml:
            # LOG.debug('Key:\n\t{}'.format(l_service))
            l_obj = EntertainmentPluginInformation()
            l_name = config_tools.Yaml(p_pyhouse_obj).find_first_element(l_service)
            l_ix = l_name.lower()
            l_obj.Name = l_name
            l_obj.Active = True
            l_obj.Type = 'Service'
            p_pyhouse_obj.House.Entertainment.Plugins[l_ix] = l_obj
            p_pyhouse_obj.House.Entertainment.PluginCount += 1
        # LOG.debug('Services: {}'.format(PrettyFormatAny.form(p_pyhouse_obj.House.Entertainment)))
        return l_obj

    def _extract_devices(self, p_pyhouse_obj, p_yaml):
        """
        """
        # LOG.debug('Devices:\n\t{}'.format(p_yaml))
        for l_device in p_yaml:
            # LOG.debug('Key:\n\t{}'.format(l_device))
            l_obj = EntertainmentPluginInformation()
            l_name = config_tools.Yaml(p_pyhouse_obj).find_first_element(l_device)
            l_ix = l_name.lower()
            l_obj.Name = l_name
            l_obj.Active = True
            l_obj.Type = 'Device'
            p_pyhouse_obj.House.Entertainment.Plugins[l_ix] = l_obj
            p_pyhouse_obj.House.Entertainment.PluginCount += 1
        # LOG.debug('Devices: {}'.format(PrettyFormatAny.form(p_pyhouse_obj.House.Entertainment)))
        return l_obj

    def _extract_all_entertainment(self, p_config):
        """ Update Entertainment.
        This iterates thru the entertainment config file and finds the names of all components that we will need to load as plugins.
        """
        # Extract all the services (if any).
        try:
            l_services = p_config['Services']
            self._extract_services(self.m_pyhouse_obj, l_services)
        except Exception as e_err:
            LOG.warn('There is no "Services" section in the entertainment.yaml file!\n\t{}'.format(e_err))
        # Extract all the devices.
        try:
            l_devices = p_config['Devices']
            self._extract_devices(self.m_pyhouse_obj, l_devices)
        except Exception as e_err:
            LOG.warn('There is no "Devices" section in the entertainment.yaml file\n\t{}'.format(e_err))
        #
        # LOG.debug('Plugins Requested: {}'.format(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins)))

    def LoadYamlConfig(self):
        """ Read the Entertainment.Yaml file.
        This config file will contain all the service and device names to load.
        """
        # LOG.info('Loading _Config - Version:{}'.format(__version__))
        try:
            l_node = config_tools.Yaml(self.m_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        except:
            self.m_pyhouse_obj.House.Entertinment = None
            return None
        try:
            l_yaml = l_node.Yaml['Entertainment']
        except:
            LOG.warn('The entertainment.yaml file does not start with "Entertainment:"')
            self.m_pyhouse_obj.House.Entertinment = None
            return None
        l_entertain = self._extract_all_entertainment(l_yaml)
        self.load_defined_plugins()
        return l_entertain  # for testing purposes

# ----------

    def _copy_to_yaml(self):
        """
        """

    def SaveYamlConfig(self):
        """
        """
        LOG.info('Saving Config - Version:{}'.format(__version__))
        l_config = self._copy_to_yaml()
        config_tools.Yaml(self.m_pyhouse_obj).write_yaml(l_config, CONFIG_FILE_NAME, addnew=True)
        return l_config


class API:
    """ Entertainment is a core module.
    However, there are a large number of subsystems possible.
    We do not want to load all the modules so we implement a load if Defined/Enabled in XML here.
    """

    m_pyhouse_obj = None
    m_config = None

    def __init__(self, p_pyhouse_obj):
        """ Create all the empty structures needed to load, run and save the entertainment information.
        """
        p_pyhouse_obj.House.Entertainment = EntertainmentInformation()  # Create empty entertainment plugin section
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = Config(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """ Read the entertainment config.

        @return: the Entertainment object of PyHouse_obj
        """
        LOG.info("Config Loading - Version:{}".format(__version__))
        self.m_config.LoadYamlConfig()
        return

    def _module_start_loop(self, p_plugin):
        """
        """
        l_name = p_plugin.Name
        # Start Plugin
        p_plugin._API.Start()
        l_topic = 'house/entertainment/{}/status'.format(l_name)
        l_obj = EntertainmentDeviceControl()
        l_obj.Model = l_name
        l_obj.HostName = self.m_pyhouse_obj.Computer.Name
        LOG.debug('Send MQTT message.\n\tTopic:{}\n\tMessage:{}'.format(l_topic, l_obj))
        # p_pyhouse_obj._APIs.Core.MqttAPI.MqttPublish(l_topic, l_obj)

    def Start(self):
        LOG.info("Starting - Version:{}".format(__version__))
        l_count = 0
        LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins, 'Plugins', 190))
        for l_plugin in self.m_pyhouse_obj.House.Entertainment.Plugins.values():
            self._module_start_loop(l_plugin)
            l_count += 1
        LOG.info("Started {} plugin(s)- Version:{}".format(l_count, __version__))

    def SaveConfig(self):
        """ Stick in the entertainment section
        """
        LOG.info("Saving Config.")
        self.m_config.SaveYamlConfig()
        LOG.info("Saved Config.")

    def Stop(self):
        LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House))
        LOG.info("Stopped.")

# ## END DBK
