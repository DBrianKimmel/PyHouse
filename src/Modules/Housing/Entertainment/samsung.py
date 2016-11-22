"""
-*- test-case-name: /home/briank/PyHouse/src/Modules/Entertainment/samsung.py -*-

@name:      src.Modules.Entertainment.samsung
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@note:      Created on Jul 11, 2016
@license:   MIT License
@summary:


"""
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Utilities.xml_tools import XmlConfigTools, PutGetXML
from Modules.Core.data_objects import BaseUUIDObject

__updated__ = '2016-11-21'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet import error

#  Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Samsung        ')

SAMSUNG_ADDRESS = '192.168.1.120'
SAMSUNG_PORT = 55000


class SamsungData(BaseUUIDObject):
    def __init__(self):
        self.DeviceCount = 0
        self.Factory = None
        self.Api = None
        self.IPv4 = None
        self.Port = None


class Xml(object):
    """
    """

    @staticmethod
    def _read_one_device(p_device_xml):
        l_obj = SamsungData()
        XmlConfigTools.read_base_UUID_object_xml(l_obj, p_device_xml)
        l_obj.IPv4 = PutGetXML.get_ip_from_xml(p_device_xml, 'IPv4')
        l_obj.Port = PutGetXML.get_int_from_xml(p_device_xml, 'Port', 55000)
        return l_obj

    @staticmethod
    def read_samsung_section_xml(p_pyhouse_obj):
        l_ret = {}
        l_count = 0
        l_xml = p_pyhouse_obj.Xml.XmlRoot
        l_xml = l_xml.find('HouseDivision')
        if l_xml is None:
            return l_ret
        l_xml = l_xml.find('EntertainmentSection')
        if l_xml is None:
            return l_ret
        l_xml = l_xml.find('SamsungSection')
        if l_xml is None:
            return l_ret
        try:
            for l_device_xml in l_xml.iterfind('Device'):
                l_device_obj = Xml._read_one_device(l_device_xml)
                l_device_obj.Key = l_count
                l_ret[l_count] = l_device_obj
                LOG.info('Loaded Samsung Device {}'.format(l_device_obj.Name))
                l_count += 1
        except AttributeError as e_err:
            LOG.error('ERROR if getting Samsung Device Data - {}'.format(e_err))
        LOG.info('Loaded {} Samsung Devices.'.format(l_count))
        return l_ret

    @staticmethod
    def _write_one_device(p_obj):
        l_entry = XmlConfigTools.write_base_object_xml('Device', p_obj)
        return l_entry

    @staticmethod
    def write_samsung_section_xml(p_pyhouse_obj):
        l_xml = ET.Element('SamsungSection')
        l_count = 0
        l_obj = p_pyhouse_obj.House.Entertainment.Samsung
        for l_room_object in l_obj.itervalues():
            l_room_object.Key = l_count
            l_entry = Xml.write_one_room(l_room_object)
            l_xml.append(l_entry)
            l_count += 1
        LOG.info('Saved {} Rooms XML'.format(l_count))
        return l_xml


class SamsungProtocol(Protocol):
    """
    """

    def dataReceived(self, data):
        Protocol.dataReceived(self, data)

    def connectionMade(self):
        Protocol.connectionMade(self)

    def connectionLost(self, reason=error.ConnectionDone):
        Protocol.connectionLost(self, reason=reason)


class SamsungClient(SamsungProtocol):
    """
    """

    def __init__(self, p_pyhouse_obj, p_samsung_obj, p_clientID=None):
        """
        At this point all config has been read in and Set-up
        """
        self.m_pyhouse_obj = p_pyhouse_obj


class SamsungFactory(ReconnectingClientFactory):
    """
    """

    def __init__(self, p_pyhouse_obj, p_samsung_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_samsung_obj = p_samsung_obj

    def startedConnecting(self, p_connector):
        # ReconnectingClientFactory.startedConnecting(self, p_connector)
        l_msg = PrettyFormatAny.form(p_connector, 'Samsung Factory connector.')
        LOG.info('Started to connect. {}'.format(p_connector))

    def buildProtocol(self, p_addr):
        LOG.info('BuildProtocol - Addr = {}'.format(p_addr))
        l_client = SamsungClient(self.m_pyhouse_obj, self.m_samsung_obj)
        l_ret = ReconnectingClientFactory.buildProtocol(self, p_addr)
        return l_ret

    def clientConnectionLost(self, p_connector, p_reason):
        LOG.warn('Lost connection.\n\tReason:{}'.format(p_reason))
        ReconnectingClientFactory.clientConnectionLost(self, p_connector, p_reason)

    def clientConnectionFailed(self, p_connector, p_reason):
        LOG.error('Connection failed.\n\tReason:{}'.format(p_reason))
        ReconnectingClientFactory.clientConnectionFailed(self, p_connector, p_reason)

    def connectionLost(self, p_reason):
        """ This is required. """
        LOG.error('ConnectionLost.\n\tReason: {}'.format(p_reason))

    def makeConnection(self, p_transport):
        """ This is required. """
        LOG.warn('makeConnection - Transport: {}'.format(p_transport))


class API(object):
    def __init__(self, p_pyhouse_obj):
        LOG.info("Initializing.")
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def LoadXml(self, p_pyhouse_obj):
        LOG.info('XML Loading')
        l_samsung_obj = SamsungData()
        l_host = SAMSUNG_ADDRESS
        l_port = SAMSUNG_PORT
        l_samsung_obj.Factory = SamsungFactory(p_pyhouse_obj, l_samsung_obj)
        _l_connector = p_pyhouse_obj.Twisted.Reactor.connectTCP(l_host, l_port, l_samsung_obj.Factory)
        LOG.info('XML Loaded')

    def Start(self):
        LOG.info("Starting.")
        LOG.info("Started.")

    def SaveXml(self, p_xml):
        LOG.info("Saving XML.")
        l_xml = ET.Element('EntertainmentSection')
        LOG.info("Saved XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopping.")
        LOG.info("Stopped.")

# ## END DBK
