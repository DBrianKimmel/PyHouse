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

__updated__ = '2019-12-25'
__version_info__ = (19, 9, 26)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.Config.config_tools import Api as configApi
from Modules.House.Entertainment.entertainment_data import EntertainmentDeviceControl, EntertainmentPluginInformation
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
# from Modules.House.Entertainment.Pandora.pandora import PandoraServiceInformation
from Modules.House.Entertainment.__init__ import MODULES

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Entertainment  ')

CONFIG_NAME = 'entertainment'


class MqttActions:
    """ Mqtt section
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_msg):
        """ Decode Mqtt message
        ==> pyhouse/<house name>/entertainment/<device-or-service>/...

        <device-or-service> = one of the MODULES

        These messages probably come from some external source such as node-red or alexa.

        @param p_topic: is the topic after 'entertainment'
        @return: a message to be logged as a Mqtt message
        """
        _l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        p_logmsg = '\tEntertainment: '
        l_module = p_msg.UnprocessedTopic[0].lower()
        # Does the called for plugin exist?
        try:
            l_module_obj = self.m_pyhouse_obj.House.Entertainment.Plugins[l_module]
        except:
            l_msg = 'The entertainment module {} does not exist, skipping'.format(l_module)
            # No need to clutter the log - LOG.warning(l_msg)
            return l_msg
        try:
            LOG.debug(PrettyFormatAny.form(l_module_obj, 'Entertain Module'))
            l_module_api = l_module_obj._Api
            p_logmsg += l_module_api.decode(p_msg)
        except (KeyError, AttributeError) as e_err:
            l_module_api = None
            p_logmsg += 'Module {} not defined {}'.format(l_module, e_err)
            LOG.error('Error in calling decode {}\n\tTopic: {}\n\tMessage: {}'.format(e_err, p_msg.Topic, p_msg.Payload))
        return p_logmsg


class LocalConfig:
    """
    """

    m_config = None
    m_config_tools = None
    m_modules_needed = []
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)
        self.m_config_tools = configApi(p_pyhouse_obj)

    def load_defined_plugins(self):
        """ Load the plugins called for in the config file.

        All plugins have been read in from entertainment.yaml
        Load the modules and their configs.
        """
        for l_module, l_plugin in self.m_pyhouse_obj.House.Entertainment.Plugins.items():
            LOG.info('Loading Plugin "{}"'.format(l_module))
            l_path = 'Modules.House.Entertainment.' + l_module  # + '.' + l_module
            LOG.debug('Importing Plugin Module "{}"'.format(l_module))
            l_plugin._Module = l_module
            l_api = self.m_config_tools.import_module_get_api(l_module, l_path)
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
        for l_service in p_config:
            l_obj = EntertainmentPluginInformation()
            l_name = self.find_first_element(l_service)
            l_name_lower = l_name.lower()
            LOG.info('Service "{}"'.format(l_name))
            self.m_modules_needed.append(l_name_lower)
            l_obj.Name = l_name
            l_obj.Type = 'Service'
            self.m_pyhouse_obj.House.Entertainment[l_name_lower] = l_obj
            # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'Entertainment'))
        return l_obj

    def _extract_devices(self, p_config):
        """ Get all devices loaded.
        """
        # LOG.debug('Devices:\n\t{}'.format(p_config))
        for l_device in p_config:
            # LOG.debug('Devices:\n\t{}'.format(l_device))
            l_obj = EntertainmentPluginInformation()
            l_name = self.find_first_element(l_device)
            l_name_lower = l_name.lower()
            LOG.info('Device "{}"'.format(l_name))
            self.m_modules_needed.append(l_name_lower)
            l_obj.Name = l_name
            l_obj.Type = 'Device'
            self.m_pyhouse_obj.House.Entertainment[l_name_lower] = l_obj
        # LOG.debug('Devices: {}'.format(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment)))
        return l_obj

    def _extract_all_entertainment(self, p_config):
        """ Update Entertainment.
        This iterates thru the entertainment config file and finds the names of all components that we will need to load as plugins.
        """
        # Extract all the services (if any).
        l_entertain = {}
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

    def load_yaml_config(self):
        """ Read the Entertainment.Yaml file.
        This config file will contain the names of all the service and device names to load.
        It does not contain any information about the services or devices.

        Here we gather the information about which plugins we will load.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Entertainment']
        except:
            LOG.warning('The config file does not start with "Entertainment:"')
            return None
        l_entertain = self._extract_all_entertainment(l_yaml)
        LOG.debug(PrettyFormatAny.form(l_entertain, 'HouseZZZ'))
        return l_entertain


class Api:
    """ Entertainment is a core module.
    However, there are a large number of subsystems possible.
    We do not want to load all the modules so we implement a load if Defined/Enabled in XML here.
    """

    m_config_tools = None
    m_local_config = None
    m_pyhouse_obj = None
    m_modules = None

    def __init__(self, p_pyhouse_obj):
        """ Create all the empty structures needed to load, run and save the entertainment information.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_config_tools = configApi(p_pyhouse_obj)
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        #
        l_path = 'Modules.House.Entertainment.'
        l_modules = self.m_config_tools.find_module_list(MODULES)
        self.m_modules = self.m_config_tools.import_module_list(l_modules, l_path)
        LOG.info('Initialized')

    def _add_storage(self):
        self.m_pyhouse_obj.House.Entertainment = {}

    def LoadConfig(self):
        """ Read the entertainment config.

        @return: the Entertainment object of PyHouse_obj
        """
        LOG.info("Config Loading - Version:{}".format(__version__))
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'HouseZZZ'))
        # self.m_pyhouse_obj.House.Entertainment = self.m_local_config.load_yaml_config()
        for l_module in self.m_modules.values():
            l_module.LoadConfig()

    def Start(self):
        LOG.info("Starting")
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'Entertainment'))
        for l_module in self.m_modules.values():
            l_module.Start()
        LOG.info('Started.')

    def SaveConfig(self):
        """ Stick in the entertainment section
        """
        LOG.info("Saving Config.")
        for l_module in self.m_modules.values():
            l_module.SaveConfig()
        LOG.info("Saved Config.")

    def Stop(self):
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House))
        LOG.info("Stopped.")

# ## END DBK
