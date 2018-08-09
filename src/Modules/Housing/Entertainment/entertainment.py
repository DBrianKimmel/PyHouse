"""

@name:      PyHouse/src/Modules/Entertainment/entertainment.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
@summary:   Entertainment component access module.

Start up entertainment systems.

"""

__updated__ = '2018-08-09'

# Import system type stuff
import importlib
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Housing.Entertainment.entertainment_data import EntertainmentData
from Modules.Core.Utilities.xml_tools import XmlConfigTools
from Modules.Housing.Entertainment.onkyo.onkyo import API as onkyoApi
from Modules.Housing.Entertainment.pandora.pandora import MqttActions as pandoraMqtt
from Modules.Housing.Entertainment.pioneer.pioneer import MqttActions as pioneerMqtt
from Modules.Housing.Entertainment.pioneer.pioneer import API as pioneerApi
from Modules.Housing.Entertainment.samsung.samsung import API as samsungApi
from Modules.Housing.Entertainment.samsung.samsung import MqttActions as samsungMqtt
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Entertainment  ')

VALID_ENTERTAINMENT_MFGRS = [
    "onkyo",
    "pioneer",
    "samsung"
    ]


class Utility:

    def get_all_entertainment_slots(self):
        """
        """
        self.m_logger.info("Retrieving Entertainment Info")
        return self.Entertainment_Data


class MqttActions:
    """ Mqtt section
    """

    m_onkyo = None
    m_panasonic = None
    m_pandora = None
    m_pioneer = None
    m_samsung = None
    m_sharp = None
    m_sony = None

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
        ==> pyhouse/<house name>/entertainment/<device>/<name>/...
        <device> = one of the VALID_ENTERTAINMENT_MFGRS

        These messages probably come from some external source such as node-red or alexa.

        """
        if self.m_pandora == None:
            self.m_pandora = pandoraMqtt(self.m_pyhouse_obj)
        if self.m_pioneer == None:
            self.m_pioneer = pioneerMqtt(self.m_pyhouse_obj)
        if self.m_samsung == None:
            self.m_samsung = samsungMqtt(self.m_pyhouse_obj)

        l_logmsg = '\tEntertainment:\n'
        if p_topic[1] == 'pandora':
            l_logmsg += self.m_pandora.decode(p_topic, p_message)
        elif p_topic[1] == 'pioneer':
            l_logmsg += self.m_pioneer.decode(p_topic, p_message)
        elif p_topic[1] == 'samsung':
            l_logmsg += self.m_samsung.decode(p_topic, p_message)

        elif p_topic[1] == 'add':
            l_logmsg += '\tName: {}\n'.format(self._get_field(p_message, 'Name'))
        elif p_topic[1] == 'delete':
            l_logmsg += '\tName: {}\n'.format(self._get_field(p_message, 'Name'))
        elif p_topic[1] == 'sync':
            l_logmsg += '\tName: {}\n'.format(self._get_field(p_message, 'Name'))
        elif p_topic[1] == 'update':
            l_logmsg += '\tName: {}\n'.format(self._get_field(p_message, 'Name'))
        else:
            l_logmsg += '\tUnknown entertainment sub-topic {} {}'.format(p_topic[1], p_message)
        return l_logmsg


class PlugIn:
    """ Treat all the various modules as plugins.
    No need to bloat the runtime with all the potential modules.
    """

    def __init__(self):
        self.m_onkyo = onkyoApi(p_pyhouse_obj)
        self.m_samsung = samsungApi(p_pyhouse_obj)
        pass

    def LoadXml(self, p_pyhouse_obj):
        l_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
        if l_xml == None:
            return
        l_xml = l_xml.find('EntertainmentSection')
        if l_xml == None:
            return
        l_xml = l_xml.find('OnkyoSection')
        if l_xml == None:
            return


class API(Utility):
    """ Entertainment is a core module.
    However, there are a large number of subsystems possible.
    We do not want to load all the modules so we implement a load if Defined/Enabled in XML here.
    """

    def __init__(self, p_pyhouse_obj):
        LOG.info("Initializing.")
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_onkyo = onkyoApi(p_pyhouse_obj)
        self.m_pioneer = pioneerApi(p_pyhouse_obj)
        self.m_samsung = samsungApi(p_pyhouse_obj)
        LOG.info("Initialized.")

    def LoadXml(self, p_pyhouse_obj):
        """ Read the entertainment section.
        If a subsection is available, load its module and let it read the xml for itself.
        """
        LOG.info('XML Loading')
        p_pyhouse_obj.House.Entertainment = EntertainmentData()  # Clear before loading
        l_xml = XmlConfigTools.find_section(p_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        for l_section in l_xml:
            # print('Section', l_section.tag, l_section.attrib)
            try:
                # This gets 'pandora' from 'PandoraSection'
                l_name = l_section.tag.lower()[:-7]
            except AttributeError:
                l_name = None
            try:
                l_attrib = l_section.attrib['Active']
            except (AttributeError, KeyError):
                l_attrib = False
            # print('Name:', l_name, l_attrib)
            if l_attrib:
                l_module_name = 'Modules.Housing.Entertainment.' + l_name + '.' + l_name
                # print('Module', l_module_name)
                l_module = importlib.import_module(l_module_name)
                l_api = l_module.API(p_pyhouse_obj)
                pass
        self.m_onkyo.LoadXml(p_pyhouse_obj)
        self.m_pioneer.LoadXml(p_pyhouse_obj)
        self.m_samsung.LoadXml(p_pyhouse_obj)
        LOG.info('XML Loaded')
        return l_xml

    def Start(self):
        LOG.info("Starting.")

        self.m_onkyo.Start()
        self.m_pioneer.Start()
        self.m_samsung.Start()
        LOG.info("Started.")

    def SaveXml(self, p_xml):
        """ Stick in the entertainment section
        """
        LOG.info("Saving XML.")
        l_xml = ET.Element('EntertainmentSection')
        l_xml = self.m_onkyo.SaveXml(l_xml)
        p_xml.append(l_xml)
        l_xml = self.m_pioneer.SaveXml(l_xml)
        p_xml.append(l_xml)
        l_xml = self.m_samsung.SaveXml(l_xml)
        p_xml.append(l_xml)
        LOG.info("Saved XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopping.")
        # self.m_onkyo.Stop()
        # self.m_samsung.Stop()
        LOG.info("Stopped.")

# ## END DBK
