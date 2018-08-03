"""
-*- test-case-name: src/Modules/Entertainment/pioneer/test/test_pioneer.py -*-

@name:      src.Modules.Entertainment.pioneer.pioneer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2017 by D. Brian Kimmel
@note:      Created on Jul 10, 2016
@license:   MIT License
@summary:

Control of pioneer home entertainment devices'.
First is an A/V receiver VSX-822-K.

Listen to Mqtt message to control device
==> pyhouse/<house name>/entertain/<device>/<function>/<value>

    <device> = receiver, tv, etc...
    <function> = power, zone, volume, input
    <value> = on, off, 0-100, zone#, input#

See: pioneer/__init__.py for documentation.

"""

from Modules.Core.Utilities.convert import long_to_str

__updated__ = '2018-08-02'
__version_info__ = (18, 7, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.error import ConnectionDone
from twisted.conch.telnet import StatefulTelnetProtocol
# from twisted.protocols import basic
# from twisted.internet import defer
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Core.data_objects import BaseUUIDObject
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Pioneer        ')
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

PORT = 8102
IP = '192.168.9.121'

VSX822K = {
    'PowerQuery':       b'?P\r\n',
    'PowerOn':          b'PO\r\n',
    'PowerOff':         b'PF\r\n',
    'VolumeQuery':      b'?V\r\n',
    'VolmeUp':          b'VU\r\n',
    'VolumeDown':       b'VN\r\n',
    'MuteQuery':        b'?M\r\n',
    'FunctionQuery':    b'?F\r\n',
    'FunctionPandora':  b'01FN\r\n'
    }


class PioneerData:

    def __init__(self):
        self.DeviceCount = 0
        self.Devices = {}  # PioneerDeviceData()


class PioneerDeviceData(BaseUUIDObject):

    def __init__(self):
        super(PioneerDeviceData, self).__init__()
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
        l_device = PioneerDeviceData()
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
        """ Read in one entire PioneerDeviceData
        """
        l_obj = XML._read_device(p_xml)
        l_obj.Status = 'off'
        l_obj.Type = 'Receiver'
        l_obj.Volume = 0
        return l_obj

    @staticmethod
    def _write_one(_p_pyhouse_obj, p_obj):
        """ Create the complete Device XML for one Pioneer device.
        """
        l_xml = XML._write_device(p_obj)
        PutGetXML.put_text_element(l_xml, 'Volume', p_obj.Volume)
        return l_xml

    @staticmethod
    def read_all(p_pyhouse_obj):
        """ Get the entire PioneerData object from the xml.
        """
        l_dict = {}
        l_count = 0
        l_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
        if l_xml == None:
            return l_dict, l_count
        l_xml = l_xml.find('EntertainmentSection')
        if l_xml == None:
            return l_dict, l_count
        l_xml = l_xml.find('PioneerSection')
        if l_xml == None:
            return l_dict, l_count
        for l_dev_xml in l_xml.iterfind('Device'):
            l_dict[l_count] = XML._read_one(l_dev_xml)
            LOG.info('Loaded Pioneer device {}'.format(l_dict[l_count].Name))
            l_count += 1
        # LOG.info('Loaded {} Pioneer Device(s).'.format(l_count))
        return l_dict, l_count

    @staticmethod
    def write_all(p_pyhouse_obj):
        """ Create the entire PioneerSection of the XML.
        """
        l_xml = ET.Element('PioneerSection')
        l_count = 0
        for l_obj in p_pyhouse_obj.House.Entertainment.Pioneer.values():
            l_xml.append(XML._write_one(p_pyhouse_obj, l_obj))
            l_count += 1
        LOG.info('Saved {} Pioneer device(s) XML'.format(l_count))
        return l_xml


class Commands(object):
    """
    """

    def __init__(self):
        pass

    def send_command(self, p_command):
        LOG.info('Send command {}'.format(p_command))
        self.transport.write(p_command)


class PioneerProtocol(StatefulTelnetProtocol, Commands):
    """
    """

    def dataReceived(self, p_data):
        """ This seems to be a line received function
        """
        Protocol.dataReceived(self, p_data)
        self.setLineMode()
        l_data = p_data[:-2]
        if l_data == b'R':
            return
        LOG.info('Data Received.\n\tData:{}'.format(l_data))

    def lineReceived(self, p_line):
        StatefulTelnetProtocol.lineReceived(self, p_line)
        LOG.info('Line Received.\n\tData:{}'.format(p_line))

    def connectionMade(self):
        """ We have connected - now get the initial conditions.
        """
        Protocol.connectionMade(self)
        self.setLineMode()
        LOG.info('Connection Made.')
        self.send_command(b'?P\r\n')  # Query Power
        self.send_command(b'?M\r\n')
        self.send_command(b'?V\r\n')
        self.send_command(b'?F\r\n')
        self.send_command(b'01FN\r\n')

    def connectionLost(self, reason=ConnectionDone):
        Protocol.connectionLost(self, reason=reason)
        LOG.warn('Lost connection.\n\tReason:{}'.format(reason))


class PioneerClient(PioneerProtocol):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        # self.m_pioneer_obj = p_pioneer_obj


class PioneerFactory(ReconnectingClientFactory):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        # self.m_pioneer_obj = p_pioneer_obj
        # LOG.debug('Factory init for {}'.format(PrettyFormatAny.form(self.m_pioneer_obj, 'Pioneer')))

    def startedConnecting(self, p_connector):
        # ReconnectingClientFactory.startedConnecting(self, p_connector)
        LOG.info('Started to connect. {}'.format(p_connector))

    def buildProtocol(self, p_addr):
        _protocol = PioneerProtocol()
        LOG.info('BuildProtocol - Addr = {}'.format(p_addr))
        l_client = PioneerClient(self.m_pyhouse_obj)
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
        """ Read the XML for all Pioneer devices.
        """
        p_pyhouse_obj.House.Entertainment.Pioneer = PioneerData()  # Clear before loading
        l_pioneer_obj, l_count = XML().read_all(p_pyhouse_obj)
        p_pyhouse_obj.House.Entertainment.Pioneer = l_pioneer_obj
        LOG.info("Loaded {} Pioneer Device(s).".format(l_count))
        return l_pioneer_obj

    def Start(self):
        """ Start all the Pioneer factories if we have any Pioneer devices.
        """
        l_count = 0
        for l_pioneer_obj in self.m_pyhouse_obj.House.Entertainment.Pioneer.values():
            l_count += 1
            # LOG.debug('Working on device {}.'.format(l_pioneer_obj.Name))
            if not l_pioneer_obj.Active:
                continue
            l_host = long_to_str(l_pioneer_obj.IPv4)
            l_port = l_pioneer_obj.Port
            # LOG.debug("Started Pioneer Host:{}; Port:{}.".format(l_host, l_port))
            l_factory = PioneerFactory(self.m_pyhouse_obj)
            l_pioneer_obj._Factory = l_factory
            # LOG.debug('Factory {}'.format(PrettyFormatAny.form(l_factory, 'Factory')))
            _l_connector = self.m_pyhouse_obj.Twisted.Reactor.connectTCP(l_host, l_port, l_pioneer_obj._Factory)
            # LOG.debug('Connector {}'.format(PrettyFormatAny.form(l_connector, 'Connector')))
            LOG.info("Started Pioneer {} {}.".format(l_host, l_port))
        LOG.info("Started {} Pioneer device(s).".format(l_count))

    def SaveXml(self, p_xml):
        l_xml = XML().write_all(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Saved Pioneer XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
