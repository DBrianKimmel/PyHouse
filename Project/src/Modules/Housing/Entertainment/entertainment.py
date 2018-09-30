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

__updated__ = '2018-09-29'
__version_info__ = (18, 9, 1)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
# from builtins import setattr
import importlib
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Housing.Entertainment.entertainment_data import \
        EntertainmentData, \
        EntertainmentPluginData, \
        EntertainmentDeviceControl
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
# from Modules.Housing.Entertainment.pandora.pandora import MqttActions as pandoraMqtt
# from Modules.Housing.Entertainment.pioneer.pioneer import MqttActions as pioneerMqtt
# from Modules.Housing.Entertainment.samsung.samsung import MqttActions as samsungMqtt
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Entertainment  ')

m_onkyo = None
m_panasonic = None
m_pandora = None
m_pioneer = None
m_samsung = None
m_sharp = None
m_sony = None


class Ent:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj


class Utility:

    def XXXget_all_entertainment_slots(self):
        """
        """
        self.m_logger.info("Retrieving Entertainment Info")
        return self.Entertainment_Data


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
        try:
            l_module = self.m_pyhouse_obj.House.Entertainment.Plugins[l_topic].API
        except KeyError:
            print("{}".format(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment.Plugins, "Plugins", 180)))
            l_module = None
        l_logmsg = '\tEntertainment: '
        #
        try:
            if l_topic == 'pandora':
                l_logmsg += l_module.decode(p_topic[1:], p_message)
            #
            elif l_topic == 'pioneer':
                l_logmsg += l_module.decode(p_topic[1:], p_message)
            #
            elif l_topic == 'samsung' and m_samsung != None:
                l_logmsg += l_module.decode(p_topic[1:], p_message)
            #
            else:
                l_logmsg += '\tUnknown entertainment sub-topic\n\t\tTopic:{}\n\t\tMessage:{}'.format(p_topic, p_message)
        except Exception as e_err:
            l_logmsg += "(entertainment.decode) Error: {}\n\tTopic:{}\n\tMessage:{}".format(e_err, p_topic, p_message)
        return l_logmsg


class API(Utility, Ent):
    """ Entertainment is a core module.
    However, there are a large number of subsystems possible.
    We do not want to load all the modules so we implement a load if Defined/Enabled in XML here.
    """

    def __init__(self, p_pyhouse_obj):
        """
        """
        p_pyhouse_obj.House.Entertainment = EntertainmentData()  # Create empty entertainment plugin section
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def _create_module_refs(self, p_element):
        """
        Create the structure we will need to Load, Start and Save the modules defined for this house.
        If there is no subsection (sony e.g.) in the Xml, we will not be called.
        If the subsection is present and Active is false, we should not load the module.
        If the subsection is present and Active, we should load the module.
        This leaves only the active entertainment modules in memory expanding the size of PyHouse.

        There will be a Plugin record even if the module is not loaded.

        @param p_element: is an Xml element for the EntertainmentSection xxxSection
        @return: a EntertainmentPluginData filled in from the section
        """

    def _start_modules(self, p_module):
        """
        """
        # print(PrettyFormatAny.form(p_module, 'ent_sm1 - p+module', 180))
        if p_module.API == None:
            LOG.error('Missing info for module')
        else:
            p_module.API.Start()

    def _module_loop(self, p_pyhouse_obj, p_section_element):
        """
        """
        l_name = XmlConfigTools.extract_section_name(p_section_element)
        l_active = PutGetXML.get_bool_from_xml(p_section_element, 'Active', False)
        l_plugin_data = EntertainmentPluginData()
        l_plugin_data.Name = l_name
        l_plugin_data.Active = l_active
        if l_active:
            # Create the module plugin
            l_module_name = 'Modules.Housing.Entertainment.' + l_name + '.' + l_name
            l_module = importlib.import_module(l_module_name)
            l_plugin_data.Module = l_module
            l_plugin_data.API = l_module.API(self.m_pyhouse_obj)
            p_pyhouse_obj.House.Entertainment.Plugins[l_name] = l_plugin_data
            LOG.info('Created Entertainment Plugin for {}'.format(l_name))
            l_devices = l_plugin_data.API.LoadXml(p_pyhouse_obj)
            l_plugin_data.Devices = l_devices.Devices
            l_plugin_data.API.Start()
            l_topic = 'entertainment/{}/status'.format(l_name)
            l_obj = EntertainmentDeviceControl()
            l_obj.Device = l_name
            l_obj.HostName = p_pyhouse_obj.Computer.Name
            self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_obj)

    def LoadXml(self, p_pyhouse_obj):
        """ Read the entertainment section.
        If a subsection is available, load its module and let it read the xml for itself.

        @return: the Entertainment object of PyHouse_obj
        """
        LOG.info('XML Loading')
        l_entertain = p_pyhouse_obj.House.Entertainment
        l_xml = XmlConfigTools.find_section(p_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        if l_xml == None:
            l_entertain.Active = False
            return l_entertain
        l_count = 0
        for l_section_element in l_xml:
            self._module_loop(p_pyhouse_obj, l_section_element)
            l_count += 1
        l_entertain.Active = True
        l_entertain.Count = l_count
        LOG.info('XML Loaded {} Entertainment Sections'.format(l_count))
        return l_entertain

    def Start(self):
        LOG.info("Starting.")
        LOG.info("Started.")

    def SaveXml(self, p_xml):
        """ Stick in the entertainment section
        """
        LOG.info("Saving XML.")
        l_entertainment_xml = ET.Element('EntertainmentSection')
        if self.m_pyhouse_obj.House.Entertainment.Active == True:
            # print(PrettyFormatAny.form(l_entertainment_xml, 'Entertainment XML - 1', 190))
            for l_plug in self.m_pyhouse_obj.House.Entertainment.Plugins.values():
                l_module_xml = l_plug.API.SaveXml(l_entertainment_xml)
                # print(PrettyFormatAny.form(l_module_xml, 'Entertainment XML - 2', 190))
                if l_module_xml != None:
                    l_entertainment_xml.append(l_module_xml)
            p_xml.append(l_entertainment_xml)
            # print(PrettyFormatAny.form(l_entertainment_xml, 'Entertainment XML - 3', 190))
        LOG.info("Saved XML.")
        return l_entertainment_xml  # For debugging

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
