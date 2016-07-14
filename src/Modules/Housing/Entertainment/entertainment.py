"""

@name:      PyHouse/src/Modules/Entertainment/entertainment.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
@summary:   Entertainment component access module.

Depending on node type, start up entertainment systems.

"""

__updated__ = '2016-07-14'

# Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Housing.Entertainment.onkyo import API as onkyoApi
from Modules.Utilities.debug_tools import PrettyFormatAny
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
            p_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Rooms msg', 160))
        return p_logmsg
        pass


class API(Utility):
    def __init__(self, p_pyhouse_obj):
        LOG.info("Initializing.")
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_onkyo = onkyoApi(p_pyhouse_obj)
        LOG.info("Initialized.")

    def LoadXml(self, p_pyhouse_obj):
        LOG.info('XML Loading')
        self.m_onkyo.LoadXml(p_pyhouse_obj)
        LOG.info('XML Loaded')

    def Start(self):
        LOG.info("Starting.")
        self.m_onkyo.Start()
        LOG.info("Started.")

    def SaveXml(self, p_xml):
        LOG.info("Saving XML.")
        l_xml = ET.Element('EntertainmentSection')
        l_xml = self.m_onkyo.SaveXml(l_xml)
        p_xml.append(l_xml)
        LOG.info("Saved XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopping.")
        self.m_onkyo.Stop()
        LOG.info("Stopped.")

# ## END DBK
