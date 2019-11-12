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


House.Entertainment.Plugins{}.Api
                             .Devices{}

"""
from Modules.Core.Config import import_tools

__updated__ = '2019-11-02'
__version_info__ = (19, 9, 26)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.Config.config_tools import Api as configApi
from Modules.House.Entertainment.entertainment_data import EntertainmentDeviceControl, EntertainmentPluginInformation, EntertainmentInformation
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.House.Entertainment.pandora.pandora import PandoraServiceInformation

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Entertainment  ')

CONFIG_NAME = 'entertainment'

MODULES = [  # All modules for the House must be listed here.  They will be loaded if configured.
    'Firestick',
    'Onkyo',
    'Panasonic',
    'Pandora',
    'Pioneer',
    'Samsung',
    'Sharp',
    'Sony'
    ]


class MqttActions:
    """ Mqtt section
    """

    m_pyhouse_obj = None

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
        p_logmsg = '\tEntertainment: '
        l_module = p_topic[0].lower()
        # Does the called for plugin exist?
        try:
            l_module_obj = self.m_pyhouse_obj.House.Entertainment.Plugins[l_module]
        except:
            l_msg = 'The entertainment module {} does not exist, skipping'.format(l_module)
            # No need to clutter the log - LOG.warn(l_msg)
            return l_msg
        try:
            LOG.debug(PrettyFormatAny.form(l_module_obj, 'Entertain Module'))
            l_module_api = l_module_obj._Api
            p_logmsg += l_module_api.decode(p_topic[1:], p_message)
        except (KeyError, AttributeError) as e_err:
            l_module_api = None
            p_logmsg += 'Module {} not defined {}'.format(l_module, e_err)
            LOG.error('Error in calling decode {}\n\tTopic: {}\n\tMessage: {}'.format(e_err, p_topic, p_message))
        return p_logmsg


class LocalConfig:
    """
    """

    m_config = None
    m_modules_needed = []
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)
        self.m_import_tools = import_tools.Tools(p_pyhouse_obj)

    def load_defined_plugins(self):
        """ Load the plugins called for in the config file.

        All plugins have been read in from entertainment.yaml
        Load the modules and their configs.
        """
        for l_module, l_plugin in self.m_pyhouse_obj.House.Entertainment.Plugins.items():
            LOG.info('Loading Plugin "{}"'.format(l_module))
            l_path = 'Modules.House.Entertainment.' + l_module  # + '.' + l_module
            # LOG.debug('Importing Plugin Module "{}"'.format(l_module))
            l_plugin._Module = l_module
            l_api = self.m_import_tools.import_module_get_api(l_module, l_path)
            # Initialize Plugin
            l_plugin._Api = l_api
            # LOG.debug(PrettyFormatAny.form(l_plugin, 'Plugin'))
            l_plugin._Api.LoadConfig()
            LOG.info('Loaded Entertainment Plugin "{}".'.format(l_module))

    def find_first_element(self, p_ordered):
        """ Return the first element from an ordered collection
           or an arbitrary element from an unordered collection.
           Raise StopIteration if the collection is empty.
        """
        return next(iter(p_ordered))

    def _extract_services(self, p_config):
        """ Get all service loaded
        """
        # LOG.debug('Services:\n\t{}'.format(p_config))
        l_count = 0
        for l_service in p_config:
            # LOG.debug('Services:\n\t{}'.format(l_service))
            l_obj = EntertainmentPluginInformation()
            l_name = self.find_first_element(l_service)  # self.m_config.find_first_element(l_service)
            l_name_lower = l_name.lower()
            LOG.info('Service "{}"'.format(l_name))
            self.m_modules_needed.append(l_name_lower)
            l_obj.Name = l_name
            l_obj.Type = 'Service'
            self.m_pyhouse_obj.House.Entertainment.Plugins[l_name_lower] = l_obj
            self.m_pyhouse_obj.House.Entertainment.PluginCount += 1
            # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'Entertainment'))
            # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins, 'Plugins'))
            l_count += 1
        return l_obj

    def _extract_devices(self, p_config):
        """ Get all devices loaded.
        """
        LOG.debug('Devices:\n\t{}'.format(p_config))
        l_count = 0
        for l_device in p_config:
            LOG.debug('Devices:\n\t{}'.format(l_device))
            l_obj = EntertainmentPluginInformation()
            l_name = self.find_first_element(l_device)
            l_name_lower = l_name.lower()
            LOG.info('Device "{}"'.format(l_name))
            self.m_modules_needed.append(l_name_lower)
            l_obj.Name = l_name
            l_obj.Type = 'Device'
            self.m_pyhouse_obj.House.Entertainment.Plugins[l_name_lower] = l_obj
            self.m_pyhouse_obj.House.Entertainment.PluginCount += 1
            l_count += 1
        # LOG.debug('Devices: {}'.format(PrettyFormatAny.form(p_pyhouse_obj.House.Entertainment)))
        return l_obj

    def _extract_all_entertainment(self, p_config):
        """ Update Entertainment.
        This iterates thru the entertainment config file and finds the names of all components that we will need to load as plugins.
        """
        # Extract all the services (if any).
        l_entertain = EntertainmentInformation()
        # LOG.debug('Yaml: {}'.format(p_config))
        # LOG.debug(PrettyFormatAny.form(p_config, 'Config'))
        for l_ix, l_value in p_config.items():
            # LOG.debug(l_value)
            if l_ix == 'Services':
                self._extract_services(l_value)
            if l_ix == 'Devices':
                self._extract_devices(l_value)
        LOG.info('Plugins Requested: {}'.format(self.m_modules_needed))
        return l_entertain
        #
        try:
            l_services = p_config.Services
            self._extract_services(l_services)
        except Exception as e_err:
            LOG.warn('There is no "Services" section in the entertainment.yaml file!\n\t{}'.format(e_err))

        # Extract all the devices.
        try:
            l_devices = p_config['Devices']
            self._extract_devices(l_devices)
        except Exception as e_err:
            LOG.warn('There is no "Devices" section in the entertainment.yaml file\n\t{}'.format(e_err))
        #
        LOG.info('Plugins Requested: {}'.format(self.m_modules_needed))
        return l_entertain

    def load_yaml_config(self):
        """ Read the Entertainment.Yaml file.
        This config file will contain the names of all the service and device names to load.
        It does not contain any information about the services or devices.

        Here we gather the information about which plugins we will load.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj.House.Entertinment = None
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Entertainment']
        except:
            LOG.warn('The config file does not start with "Entertainment:"')
            return None
        self.m_pyhouse_obj.House.Entertinment = EntertainmentInformation()
        l_entertain = self._extract_all_entertainment(l_yaml)
        self.load_defined_plugins()
        return l_entertain  # for testing purposes


class Api:
    """ Entertainment is a core module.
    However, there are a large number of subsystems possible.
    We do not want to load all the modules so we implement a load if Defined/Enabled in XML here.
    """

    m_pyhouse_obj = None
    m_local_config = None

    def __init__(self, p_pyhouse_obj):
        """ Create all the empty structures needed to load, run and save the entertainment information.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        self._add_storage()
        LOG.info("Initialized - Version:{}".format(__version__))

    def _add_storage(self):
        self.m_pyhouse_obj.House.Entertainment = EntertainmentInformation()  # Clear before loading

    def LoadConfig(self):
        """ Read the entertainment config.

        @return: the Entertainment object of PyHouse_obj
        """
        LOG.info("Config Loading - Version:{}".format(__version__))
        self.m_local_config.load_yaml_config()

    def _service_start(self, p_service):
        """
        """
        LOG.debug('Service {}'.format(p_service.Name))
        LOG.debug(PrettyFormatAny.form(p_service, 'Service'))
        l_topic = 'house/entertainment/{}/status'.format(p_service)
        l_obj = PandoraServiceInformation()
        l_obj.Model = p_service.Name
        l_obj.HostName = self.m_pyhouse_obj.Computer.Name
        LOG.debug('Send MQTT message.\n\tTopic:{}\n\tMessage:{}'.format(l_topic, l_obj))
        # p_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, l_obj)

    def _device_start(self, p_device):
        """
        """
        LOG.debug('Sevice {}'.format(p_device.Name))
        LOG.debug(PrettyFormatAny.form(p_device, 'Device'))
        l_topic = 'house/entertainment/{}/status'.format(p_device.Name)
        l_obj = EntertainmentDeviceControl()
        l_obj.Model = p_device.Name
        l_obj.HostName = self.m_pyhouse_obj.Computer.Name
        LOG.debug('Send MQTT message.\n\tTopic:{}\n\tMessage:{}'.format(l_topic, l_obj))
        # p_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, l_obj)

    def _module_start_loop(self, p_plugin):
        """
        """
        l_name = p_plugin.Name
        # Start Plugin
        LOG.debug('Starting {}'.format(l_name))
        LOG.debug(PrettyFormatAny.form(p_plugin, 'Plugin'))
        if p_plugin.ServiceCount > 0:
            for l_service in p_plugin.Services.values():
                self._service_start(l_service)
        if p_plugin.DeviceCount > 0:
            for l_device in p_plugin.Devices.values():
                self._device_start(l_device)

        # p_plugin._Api.Start()
        # l_topic = 'house/entertainment/{}/status'.format(p_device.Name)
        # l_obj = EntertainmentDeviceControl()
        # l_obj.Model = l_name
        # l_obj.HostName = self.m_pyhouse_obj.Computer.Name
        # LOG.debug('Send MQTT message.\n\tTopic:{}\n\tMessage:{}'.format(l_topic, l_obj))
        # p_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, l_obj)

    def Start(self):
        LOG.info("Starting")
        l_count = 0
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'Entertainment'))
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins, 'Plugins'))
        for l_plugin in self.m_pyhouse_obj.House.Entertainment.Plugins.values():
            LOG.debug('Starting "{}"'.format(l_plugin.Name))
            self._module_start_loop(l_plugin)
            l_count += 1
        LOG.info("Started {} plugin(s)- Version:{}".format(l_count, __version__))

    def SaveConfig(self):
        """ Stick in the entertainment section
        """
        LOG.info("Saving Config.")
        self.m_local_config.save_yaml_config()
        LOG.info("Saved Config.")

    def Stop(self):
        LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House))
        LOG.info("Stopped.")

# ## END DBK
