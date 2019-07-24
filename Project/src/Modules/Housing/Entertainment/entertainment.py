"""
@name:      Modules/Housing/Entertainment/entertainment.py
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

__updated__ = '2019-07-12'
__version_info__ = (18, 10, 2)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
import importlib

#  Import PyMh files and modules.
from Modules.Core.Utilities import extract_tools, config_tools
# from Modules.Core.Utilities.xml_tools import XmlConfigTools
from Modules.Housing.Entertainment.entertainment_data import \
        EntertainmentInformation, \
        EntertainmentDeviceControl, EntertainmentPluginInformation
from Modules.Housing.Entertainment.entertainment_xml import XML as entertainmentXML

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Entertainment  ')

CONFIG_FILE_NAME = 'entertainment.yaml'


class Ent:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj


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
            if not l_module_obj.Active:
                p_logmsg += ' Module: {} is not active - skipping'.format(l_module)
                LOG.debug('Return {}'.format(p_logmsg))
                return p_logmsg
            # LOG.debug('Plugin Active')
        except KeyError:
            p_logmsg += ' {} not defined here.'.format(l_module)
            LOG.debug('Error {}'.format(p_logmsg))
            return p_logmsg
        try:
            l_module_api = l_module_obj._API
            p_logmsg += l_module_api.decode(p_topic[1:], p_message)
            # LOG.debug('{}'.format(p_logmsg))
        except (KeyError, AttributeError) as e_err:
            l_module_api = None
            p_logmsg += 'Module {} not defined {}'.format(l_module, e_err)
            LOG.error('Error in calling decode {}'.format(e_err))
        return p_logmsg


class Yaml:
    """
    """

    def load_defined_plugins(self, p_pyhouse_obj):
        """
        """
        for l_name, l_plugin in p_pyhouse_obj.House.Entertainment.Plugins.items():
            l_plugin_name = 'Modules.Housing.Entertainment.' + l_name + '.' + l_name
            l_module = importlib.import_module(l_plugin_name)
            l_plugin._Module = l_module
            # Initialize Plugin
            l_plugin._API = l_module.API(p_pyhouse_obj)
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
        # LOG.debug('Services: {}'.format(PrettyFormatAny.form(p_pyhouse_obj.House.Entertainment)))

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
        # LOG.debug('Devices: {}'.format(PrettyFormatAny.form(p_pyhouse_obj.House.Entertainment)))

    def _update_entertain_from_yaml(self, p_pyhouse_obj, p_node_yaml):
        """ Update Entertainment.
        This iterates thru the entertainment config file and finds the names of all components that we will need to load as plugins.
        """
        LOG.debug('Entertainment\n\t{}\n'.format(p_node_yaml))
        try:
            l_yaml = p_node_yaml['Entertainment']
        except:
            LOG.error('The "Entertainment" tag is missing in the "entertainment.yaml" file!')
            return None
        # Extract all the services (if any).
        try:
            l_services = l_yaml['Services']
            self._extract_services(p_pyhouse_obj, l_services)
        except Exception as e_err:
            LOG.warn('There is no "Services" section in the entertainment.yaml file!\n\t{}'.format(e_err))
        # Extract all the devices.
        try:
            l_devices = l_yaml['Devices']
            self._extract_devices(p_pyhouse_obj, l_devices)
        except Exception as e_err:
            LOG.warn('There is no "Devices" section in the entertainment.yaml file\n\t{}'.format(e_err))
        #
        LOG.debug('Plugins Requested: {}'.format(PrettyFormatAny.form(p_pyhouse_obj.House.Entertainment.Plugins)))

    def LoadYamlConfig(self, p_pyhouse_obj):
        """ Read the Entertainment.Yaml file.
        This config file will contain all the service and device names to load.
        """
        # LOG.info('Loading _Config - Version:{}'.format(__version__))
        l_node = config_tools.Yaml(p_pyhouse_obj).read_yaml(CONFIG_FILE_NAME)
        l_entertain = self._update_entertain_from_yaml(p_pyhouse_obj, l_node.Yaml)
        self.load_defined_plugins(p_pyhouse_obj)
        return l_entertain  # for testing purposes


class API(Ent):
    """ Entertainment is a core module.
    However, there are a large number of subsystems possible.
    We do not want to load all the modules so we implement a load if Defined/Enabled in XML here.
    """

    def __init__(self, p_pyhouse_obj):
        """ Create all the empty structures needed to load, run and save the entertainment information.
        """
        p_pyhouse_obj.House.Entertainment = EntertainmentInformation()  # Create empty entertainment plugin section
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        """ Read the entertainment config.

        @return: the Entertainment object of PyHouse_obj
        """
        LOG.info("Config Loading - Version:{}".format(__version__))
        Yaml().LoadYamlConfig(self.m_pyhouse_obj)
        return

    def _module_start_loop(self, p_pyhouse_obj, p_plugin):
        """
        """
        l_name = p_plugin.Name
        # Start Plugin
        p_plugin._API.Start()
        l_topic = 'house/entertainment/{}/status'.format(l_name)
        l_obj = EntertainmentDeviceControl()
        l_obj.Model = l_name
        l_obj.HostName = p_pyhouse_obj.Computer.Name
        LOG.debug('Send MQTT message.\n\tTopic:{}\n\tMessage:{}'.format(l_topic, l_obj))
        # p_pyhouse_obj._APIs.Core.MqttAPI.MqttPublish(l_topic, l_obj)

    def Start(self):
        LOG.info("Starting - Version:{}".format(__version__))
        l_count = 0
        for l_plugin in self.m_pyhouse_obj.House.Entertainment.Plugins.values():
            self._module_start_loop(self.m_pyhouse_obj, l_plugin)
            l_count += 1
        LOG.info("Started {} plugin(s)- Version:{}".format(l_count, __version__))

    def SaveConfig(self):
        """ Stick in the entertainment section
        """
        LOG.info("Saving Config.")
        l_entertainment_xml = entertainmentXML().write_entertainment_all(self.m_pyhouse_obj)
        # p_xml.append(l_entertainment_xml)
        LOG.info("Saved Config.")
        return l_entertainment_xml  # For debugging

    def Stop(self):
        LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House))
        LOG.info("Stopped.")

# ## END DBK
