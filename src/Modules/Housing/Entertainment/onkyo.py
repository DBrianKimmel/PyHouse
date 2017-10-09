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

__updated__ = '2017-07-24'

#  Import system type stuff
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.error import ConnectionDone
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Core.data_objects import BaseUUIDObject
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Onkyo          ')



DEFAULT_EISCP_IPV4 = '192.168.1.138'
DEFAULT_EISCP_PORT = 60128


class OnkyoData(object):
    def __init__(self):
        self.DeviceCount = 0
        self.Devices = {}  # OnkyoDeviceData()


class OnkyoDeviceData(BaseUUIDObject):

    def __init__(self):
        super(OnkyoDeviceData, self).__init__()
        self.Comment = None
        self.IPv4 = None
        self.Port = None
        self.RoomCoords = None
        self.RoomName = None
        self.RoomUUID = None
        self.Status = None
        self.Type = None
        self.Volume = None
        self._Factory = None


class XML(object):
    """
    """

    @staticmethod
    def _read_device(p_xml):
        l_device = OnkyoDeviceData()
        XmlConfigTools().read_base_UUID_object_xml(l_device, p_xml)
        l_device.Comment = PutGetXML.get_text_from_xml(p_xml, 'Comment')
        l_device.IPv4 = PutGetXML.get_ip_from_xml(p_xml, 'IPv4')
        l_device.Port = PutGetXML.get_int_from_xml(p_xml, 'Port')
        l_device.Type = PutGetXML.get_text_from_xml(p_xml, 'Type')
        return l_device

    @staticmethod
    def _write_device(p_obj):
        l_xml = XmlConfigTools().write_base_UUID_object_xml('Device', p_obj)
        PutGetXML().put_text_element(l_xml, 'Comment', p_obj.Comment)
        PutGetXML().put_ip_element(l_xml, 'IPv4', p_obj.IPv4)
        PutGetXML().put_int_element(l_xml, 'Port', p_obj.Port)
        PutGetXML().put_text_element(l_xml, 'Type', p_obj.Type)
        return l_xml

    @staticmethod
    def _read_one(p_xml):
        """ Read in one entire OnkyoDeviceData
        """
        l_obj = XML._read_device(p_xml)
        l_obj.Status = 'off'
        l_obj.Type = 'Receiver'
        l_obj.Volume = 0
        return l_obj

    @staticmethod
    def _write_one(_p_pyhouse_obj, p_obj):
        """ Create the complete Device XML for one Onkyo device.
        """
        l_xml = XML._write_device(p_obj)
        PutGetXML.put_text_element(l_xml, 'Volume', p_obj.Volume)
        return l_xml

    @staticmethod
    def read_all(p_pyhouse_obj):
        """ Get the entire OnkyoData object from the xml.
        """
        l_dict = {}
        l_count = 0
        l_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
        if l_xml == None:
            return l_dict
        l_xml = l_xml.find('EntertainmentSection')
        if l_xml == None:
            return l_dict
        l_xml = l_xml.find('OnkyoSection')
        if l_xml == None:
            return l_dict
        for l_dev_xml in l_xml.iterfind('Device'):
            l_dict[l_count] = XML._read_one(l_dev_xml)
            LOG.info('Loaded Onkyo device {}'.format(l_dict[l_count]))
            l_count += 1
        LOG.info('Loaded {} Onkyo Devices.'.format(l_count))
        return l_dict, l_count

    @staticmethod
    def write_all(p_pyhouse_obj):
        """ Create the entire OnkyoSection of the XML.
        """
        l_xml = ET.Element('OnkyoSection')
        l_count = 0
        for l_obj in p_pyhouse_obj.House.Entertainment.Onkyo.values():
            l_xml.append(XML._write_one(p_pyhouse_obj, l_obj))
            l_count += 1
        LOG.info('Saved {} Onkyo devices XML'.format(l_count))
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
        LOG.info("Initialized")

    def LoadXml(self, p_pyhouse_obj):
        """ Read the XML for all Onkyo devices.
        """
        p_pyhouse_obj.House.Entertainment.Onkyo = OnkyoData()  # Clear before loading
        l_onkyo_obj, _l_count = XML().read_all(p_pyhouse_obj)
        p_pyhouse_obj.House.Entertainment.Onkyo = l_onkyo_obj
        LOG.info("Loaded XML")
        return l_onkyo_obj

    def Start(self):
        """ Start all the Onkyo factories if we have any Onkyo devices.
        """
        l_count = 0
        for l_onkyo_obj in self.m_pyhouse_obj.House.Entertainment.Onkyo.values():
            l_host = l_onkyo_obj.IPv4
            l_port = l_onkyo_obj.Port
            l_onkyo_obj.Factory = OnkyoFactory(self.m_pyhouse_obj, l_onkyo_obj)
            _l_connector = self.m_pyhouse_obj.Twisted.Reactor.connectTCP(l_host, l_port, l_onkyo_obj.Factory)
            LOG.info("Started Onkyo {} {}".format(l_host, l_port))
        LOG.info("Started {} Onkyo devices".format(l_count))

    def SaveXml(self, p_xml):
        l_xml = XML().write_all(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Saved Onkyo XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
