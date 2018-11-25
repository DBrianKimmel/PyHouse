"""

@name:      PyHouse/src/Modules/Entertainment/entertainment.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2018 by D. Brian Kimmel
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

__updated__ = '2018-11-25'
__version_info__ = (18, 10, 2)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
import importlib
# import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Housing.Entertainment.entertainment_data import \
        EntertainmentData, \
        EntertainmentPluginData, \
        EntertainmentDeviceControl
from Modules.Housing.Entertainment.entertainment_xml import XML as entertainmentXML
from Modules.Core.Utilities.xml_tools import XmlConfigTools  # , PutGetXML
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Entertainment  ')


class Ent:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj


class MqttActions:
    """ Mqtt section
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _get_field(self, p_message, p_field):
        try:
            l_ret = p_message[p_field]
        except KeyError:
            l_ret = 'The "{}" field was missing in the MQTT Message.'.format(p_field)
            LOG.error(l_ret)
        return l_ret

    def decode(self, p_topic, p_message):
        """ Decode Mqtt message
        ==> pyhouse/<house name>/entertainment/<device>/...

        <device-or-service> = one of the VALID_ENTERTAINMENT_MFGRS

        These messages probably come from some external source such as node-red or alexa.

        @param p_topic: is the topic after 'entertainment'
        @return: a message to be logged as a Mqtt message
        """
        l_topic = p_topic[0].lower()
        l_logmsg = '\tEntertainment: '
        try:
            l_module = self.m_pyhouse_obj.House.Entertainment.Plugins[l_topic]._API
            l_logmsg += l_module.decode(p_topic[1:], p_message)
        except (KeyError, AttributeError) as e_err:
            l_module = None
            l_logmsg += 'Module {} not defined here -ignored.'.format(l_topic)
        return l_logmsg
        #
        try:
            l_logmsg += l_module.decode(p_topic[1:], p_message)

            if l_topic == 'pandora':
                l_logmsg += l_module.decode(p_topic[1:], p_message)
            #
            elif l_topic == 'pioneer':
                l_logmsg += l_module.decode(p_topic[1:], p_message)
            #
            elif l_topic == 'samsung':
                l_logmsg += l_module.decode(p_topic[1:], p_message)
            #
            else:
                l_logmsg += '\tUnknown entertainment sub-topic\n\t\tTopic:{}\n\t\tMessage:{}'.format(p_topic, p_message)
        except Exception as e_err:
            LOG.error('Error {}'.format(e_err))
            l_logmsg += "(entertainment-102.decode) Error: {}\n\tTopic:{}\n\tMessage:{}".format(e_err, p_topic, p_message)
        return l_logmsg


class API(Ent):
    """ Entertainment is a core module.
    However, there are a large number of subsystems possible.
    We do not want to load all the modules so we implement a load if Defined/Enabled in XML here.
    """

    def __init__(self, p_pyhouse_obj):
        """ Create all the empty structures needed to load, run and save the entertainment information.
        """
        p_pyhouse_obj.House.Entertainment = EntertainmentData()  # Create empty entertainment plugin section
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def XXX_create_module_refs(self, p_element):
        """
        Create the structure we will need to Load, Start and Save the modules defined for this house.
        If there is no subsection (sony e.g.) in the Xml, we will not be called.
        If the subsection is present and Active is false, we should load the XML but not load the module.
        If the subsection is present and Active, we should load the module.
        This leaves only the active entertainment modules in memory expanding the size of PyHouse.
        The XML is present so it will be properly saved.

        There will be a Plugin record even if the module is not loaded.

        @param p_element: is an Xml element for the EntertainmentSection xxxSection
        @return: a EntertainmentPluginData filled in from the section
        """

    def XXX_start_modules(self, p_module):
        """
        """
        # print(PrettyFormatAny.form(p_module, 'ent_sm1 - p+module', 180))
        if p_module.API == None:
            LOG.error('Missing info for module')
        else:
            p_module.API.Start()

    def XXX_module_load_loop(self, p_pyhouse_obj, p_section_element):
        """
        """
        l_active = True
        l_plugin_data = EntertainmentPluginData()
        l_plugin_data.Name = l_name = XmlConfigTools.extract_section_name(p_section_element)
        l_plugin_data.Active = l_active  # = PutGetXML.get_bool_from_xml(p_section_element, 'Active', True)
        LOG.debug('Working on {}'.format(l_name))
        if l_active:
            # Create the module plugin
            l_module_name = 'Modules.Housing.Entertainment.' + l_name + '.' + l_name
            l_module = importlib.import_module(l_module_name)
            l_plugin_data._Module = l_module
            # Initialize Plugin
            l_plugin_data._API = l_module.API(self.m_pyhouse_obj)
            p_pyhouse_obj.House.Entertainment.Plugins[l_name] = l_plugin_data
            LOG.info('Created Entertainment Plugin "{}".'.format(l_name))
            # Load XML for Plugin
            l_devices = l_plugin_data._API.LoadXml(p_pyhouse_obj)
            l_plugin_data.Devices = l_devices.Devices

    def _module_start_loop(self, p_pyhouse_obj, p_plugin):
        """
        """
        l_name = p_plugin.Name
        # Start Plugin
        p_plugin._API.Start()
        l_topic = 'entertainment/{}/status'.format(l_name)
        l_obj = EntertainmentDeviceControl()
        l_obj.Device = l_name
        l_obj.HostName = p_pyhouse_obj.Computer.Name
        # LOG.debug('Send MQTT message.\n\tTopic:{}\n\tMessage:{}\n\tAPI:{}'.format(
        #    l_topic, l_obj, PrettyFormatAny.form(p_pyhouse_obj.APIs.Computer.MqttAPI, 'API', 180)))
        p_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_obj)

    def LoadXml(self, p_pyhouse_obj):
        """ Read the entertainment section.
        Everything present in the XML must be read into the pyhouse_obj structure.

        SubSections not active will not be loaded or instantiated.

        If a subsection is available, load its module and let it read the xml for itself.

        @return: the Entertainment object of PyHouse_obj
        """
        LOG.info("XML Loading - Version:{}".format(__version__))
        l_xml = XmlConfigTools.find_section(p_pyhouse_obj, 'HouseDivision/EntertainmentSection')

        """
        if l_xml == None:
            l_entertain.Active = False
            return l_entertain
        l_count = 0
        for _section_element in l_xml:
            # self._module_load_loop(p_pyhouse_obj, l_section_element)
            l_count += 1
        l_entertain.Active = True
        l_entertain.PluginCount = l_count
        LOG.info('XML Loaded {} Entertainment Sections'.format(l_count))
        return l_entertain
        """

        l_entertainment_obj = entertainmentXML().read_entertainment_all(p_pyhouse_obj)
        p_pyhouse_obj.House.Entertainment = l_entertainment_obj
        return l_entertainment_obj

    def Start(self):
        LOG.info("Starting.")
        l_count = 0
        for l_plugin in self.m_pyhouse_obj.House.Entertainment.Plugins.values():
            self._module_start_loop(self.m_pyhouse_obj, l_plugin)
            l_count += 1
        LOG.info("Started {} plugin(s)- Version:{}".format(l_count, __version__))

    def SaveXml(self, p_xml):
        """ Stick in the entertainment section
        """
        LOG.info("Saving XML.")
        l_entertainment_xml = entertainmentXML().write_entertainment_all(self.m_pyhouse_obj)
        p_xml.append(l_entertainment_xml)
        LOG.info("Saved XML.")
        return l_entertainment_xml  # For debugging

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
