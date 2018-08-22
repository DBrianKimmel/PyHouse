"""
-*- test-case-name: PyHouse/src/Modules/Entertainment/test_onkyo.py -*-

@name:      PyHouse/src/Modules/Entertainment/onkyo.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c)2016-2017 by D. Brian Kimmel
@note:      Created on Jul 9, 2016
@license:   MIT License
@summary:

"""

__updated__ = '2018-08-19'
__version_info__ = (18, 8, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.error import ConnectionDone
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Housing.Entertainment.entertainment_data import EntertainmentDeviceData
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Onkyo          ')

DEFAULT_EISCP_IPV4 = '192.168.1.138'
DEFAULT_EISCP_PORT = 60128
SECTION = 'onkyo'


class OnkyoDeviceData(EntertainmentDeviceData):

    def __init__(self):
        super(OnkyoDeviceData, self).__init__()
        self.IPv4 = None
        self.Port = None
        self.RoomName = None
        self.RoomUUID = None
        self.Type = None
        self.Volume = None  # Default volume for initial turn on (usually low but audible)
        # self._Factory = None


class XML(object):
    """
    """

    @staticmethod
    def _read_device(p_xml):
        """ Read an entire <Device> section of XML and fill in the OnkyoDeviceData Object

        @return: a completed OnkyoDeviceData object
        """
        l_device = OnkyoDeviceData()
        XmlConfigTools.read_base_UUID_object_xml(l_device, p_xml)
        l_device.IPv4 = PutGetXML.get_ip_from_xml(p_xml, 'IPv4')
        l_device.Port = PutGetXML.get_int_from_xml(p_xml, 'Port')
        l_device.RoomName = PutGetXML.get_text_from_xml(p_xml, 'RoomName')
        l_device.RoomUUID = PutGetXML.get_uuid_from_xml(p_xml, 'RoomUUID')
        l_device.Type = PutGetXML.get_text_from_xml(p_xml, 'Type')
        l_device.Volume = PutGetXML.get_int_from_xml(p_xml, 'Volume')
        return l_device

    @staticmethod
    def _write_device(p_obj):
        l_xml = XmlConfigTools.write_base_UUID_object_xml('Device', p_obj)
        PutGetXML.put_ip_element(l_xml, 'IPv4', p_obj.IPv4)
        PutGetXML.put_int_element(l_xml, 'Port', p_obj.Port)
        PutGetXML.put_text_element(l_xml, 'RoomName', p_obj.RoomName)
        PutGetXML.put_text_element(l_xml, 'RoomUUID', p_obj.RoomUUID)
        PutGetXML.put_text_element(l_xml, 'Type', p_obj.Type)
        PutGetXML.put_text_element(l_xml, 'Volume', p_obj.Volume)
        return l_xml

    @staticmethod
    def read_onkyo_section_xml(p_pyhouse_obj):
        """ Get the entire OnkyoDeviceData object from the xml.
        """
        # Clear out the data sections
        l_xml = XmlConfigTools.find_section(p_pyhouse_obj, 'HouseDivision/EntertainmentSection/OnkyoSection')
        l_entry_obj = p_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        l_entry_obj.Name = SECTION
        l_device_obj = OnkyoDeviceData()
        l_count = 0
        if l_xml is None:
            l_entry_obj.Name = 'Did not find xml section '
            return l_entry_obj
        try:
            l_entry_obj.Type = PutGetXML.get_text_from_xml(l_xml, 'Type')
            for l_device_xml in l_xml.iterfind('Device'):
                l_device_obj = XML._read_device(l_device_xml)
                l_device_obj.Key = l_count
                l_entry_obj.Devices[l_count] = l_device_obj
                l_entry_obj.Count += 1
                LOG.info('Loaded Onkyo Device {}'.format(l_entry_obj.Name))
                l_count += 1
        except AttributeError as e_err:
            LOG.error('ERROR if getting Onkyo Device Data - {}'.format(e_err))
        if l_count > 0:
            l_entry_obj.Active = True
        LOG.info('Loaded {} Onkyo Devices.'.format(l_count))
        return l_entry_obj

    @staticmethod
    def write_onkyo_section_xml(p_pyhouse_obj):
        """ Create the entire OnkyoSection of the XML.
        @param p_pyhouse_obj: containing an object with onkyo
        """
        l_active = p_pyhouse_obj.House.Entertainment.Plugins[SECTION].Count > 0
        l_xml = ET.Element('OnkyoSection', attrib={'Active': str(l_active)})
        l_count = 0
        l_obj = p_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        PutGetXML.put_text_element(l_xml, 'Type', l_obj.Type)
        for l_device_object in l_obj.Devices.values():
            l_device_object.Key = l_count
            l_entry = XML._write_device(l_device_object)
            l_xml.append(l_entry)
            l_count += 1
        LOG.info('Saved {} Onkyo device(s) XML'.format(l_count))
        return l_xml


class OnkyoProtocol(Protocol):
    """
    """

    def dataReceived(self, p_data):
        Protocol.dataReceived(self, p_data)
        # LOG.info('Data Received.\n\tData:{}'.format(p_data))

    def connectionMade(self):
        Protocol.connectionMade(self)

    def connectionLost(self, reason=ConnectionDone):
        Protocol.connectionLost(self, reason=reason)
        LOG.warn('Lost connection.\n\tReason:{}'.format(reason))


class OnkyoClient(OnkyoProtocol):
    """
    """

    def __init__(self, p_pyhouse_obj, p_onkyo_obj, _p_clientID=None):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_onkyo_obj = p_onkyo_obj


class OnkyoFactory(ReconnectingClientFactory):
    """
    """

    def __init__(self, p_pyhouse_obj, p_onkyo_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_onkyo_obj = p_onkyo_obj

    def startedConnecting(self, p_connector):
        # ReconnectingClientFactory.startedConnecting(self, p_connector)
        LOG.info('Started to connect. {}'.format(p_connector))

    def buildProtocol(self, p_addr):
        _protocol = OnkyoProtocol()
        LOG.info('BuildProtocol - Addr = {}'.format(p_addr))
        l_client = OnkyoClient(self.m_pyhouse_obj, self.m_onkyo_obj)
        # l_ret = ReconnectingClientFactory.buildProtocol(self, p_addr)
        return l_client

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


class Util(object):
    """
    """

    def start_factory(self):
        pass


class API(object):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadXml(self, p_pyhouse_obj):
        """ Read the XML for all Onkyo devices.
        """
        l_onkyo_obj = XML.read_onkyo_section_xml(p_pyhouse_obj)
        p_pyhouse_obj.House.Entertainment.Plugins[SECTION] = l_onkyo_obj
        LOG.info("Loaded Onkyo XML")
        return l_onkyo_obj

    def Start(self):
        """ Start all the Onkyo factories if we have any Onkyo devices.
        """
        l_count = 0
        l_mfg = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        print(PrettyFormatAny.form(l_mfg, 'onkyo.Start() Plugins'))
        for l_onkyo_obj in l_mfg.Devices.values():
            if not l_onkyo_obj.Active:
                continue
            l_host = l_onkyo_obj.IPv4
            l_port = l_onkyo_obj.Port
            l_onkyo_obj.Factory = OnkyoFactory(self.m_pyhouse_obj, l_onkyo_obj)
            _l_connector = self.m_pyhouse_obj.Twisted.Reactor.connectTCP(l_host, l_port, l_onkyo_obj.Factory)
            LOG.info("Started Onkyo {} {}".format(l_host, l_port))
        LOG.info("Started {} Onkyo devices".format(l_count))

    def SaveXml(self, _p_xml):
        l_xml = XML.write_onkyo_section_xml(self.m_pyhouse_obj)
        LOG.info("Saved Onkyo XML.")
        return l_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
