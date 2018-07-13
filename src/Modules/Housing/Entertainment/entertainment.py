"""

@name:      PyHouse/src/Modules/Entertainment/entertainment.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
@summary:   Entertainment component access module.

Start up entertainment systems.

"""

__updated__ = '2018-07-12'

# Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Housing.Entertainment.entertainment_data import EntertainmentData
from Modules.Housing.Entertainment.onkyo.onkyo import API as onkyoApi
from Modules.Housing.Entertainment.pioneer.pioneer import API as pioneerApi
from Modules.Housing.Entertainment.samsung.samsung import API as samsungApi
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Entertainment  ')


class Utility(object):

    def get_all_entertainment_slots(self):
        """
        """
        self.m_logger.info("Retrieving Entertainment Info")
        return self.Entertainment_Data


class MqttActions(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _get_field(self, p_message, p_field):
        try:
            l_ret = p_message[p_field]
        except KeyError:
            l_ret = 'The "{}" field was missing in the MQTT Message.'.format(p_field)
        return l_ret

    def decode(self, p_logmsg, p_topic, p_message):
        """ .../entertainment/xxxx
        """
        p_logmsg += '\tEntertainment:\n'
        if p_topic[1] == 'add':
            p_logmsg += '\tName: {}\n'.format(self._get_field(p_message, 'Name'))
        elif p_topic[1] == 'delete':
            p_logmsg += '\tName: {}\n'.format(self._get_field(p_message, 'Name'))
        elif p_topic[1] == 'sync':
            p_logmsg += '\tName: {}\n'.format(self._get_field(p_message, 'Name'))
        elif p_topic[1] == 'update':
            p_logmsg += '\tName: {}\n'.format(self._get_field(p_message, 'Name'))
        else:
            p_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Entertainment msg', 160))
        return p_logmsg
        pass


class PlugIn(object):
    """ Treat all the various modules as plugins.
    No need to bloat the runtime with all the potential modules.
    """

    def __init__(self):
        # self.m_onkyo = onkyoApi(p_pyhouse_obj)
        # self.m_samsung = samsungApi(p_pyhouse_obj)
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

    def __init__(self, p_pyhouse_obj):
        LOG.info("Initializing.")
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_onkyo = onkyoApi(p_pyhouse_obj)
        self.m_pioneer = pioneerApi(p_pyhouse_obj)
        self.m_samsung = samsungApi(p_pyhouse_obj)
        LOG.info("Initialized.")

    def LoadXml(self, p_pyhouse_obj):
        LOG.info('XML Loading')
        p_pyhouse_obj.House.Entertainment = EntertainmentData()  # Clear before loading
        self.m_onkyo.LoadXml(p_pyhouse_obj)
        self.m_pioneer.LoadXml(p_pyhouse_obj)
        self.m_samsung.LoadXml(p_pyhouse_obj)
        LOG.info('XML Loaded')

    def Start(self):
        LOG.info("Starting.")

        self.m_onkyo.Start()
        self.m_pioneer.Start()
        self.m_samsung.Start()
        LOG.info("Started.")

    def SaveXml(self, p_xml):
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
