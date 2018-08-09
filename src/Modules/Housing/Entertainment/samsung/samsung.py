"""
-*- test-case-name: /home/briank/PyHouse/src/Modules/Entertainment/samsung.py -*-

@name:      src.Modules.Housing.Entertainment.samsung.samsung.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2018 by D. Brian Kimmel
@note:      Created on Jul 11, 2016
@license:   MIT License
@summary:

"""

__updated__ = '2018-08-08'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet import error

#  Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
from Modules.Core.data_objects import BaseUUIDObject
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
LOG = Logger.getLogger('PyHouse.Samsung        ')

SAMSUNG_ADDRESS = '192.168.1.103'
SAMSUNG_PORT = 55000


class SamsungData:

    def __init__(self):
        self.Active = False
        self.DeviceCount = 0
        self.Devices = {}  # SamsungDeviceData()


class SamsungDeviceData(BaseUUIDObject):

    def __init__(self):
        self.DeviceCount = 0
        self.Factory = None
        self.Api = None
        self.Installed = None
        self.IPv4 = None
        self.Model = None
        self.Port = None
        self.RoomName = None
        self.RoomUUID = None
        self.Type = None


class XML:
    """
    """

    @staticmethod
    def _read_one_device(p_xml):
        l_obj = SamsungDeviceData()
        XmlConfigTools.read_base_UUID_object_xml(l_obj, p_xml)
        l_obj.Installed = PutGetXML.get_text_from_xml(p_xml, 'Installed')
        l_obj.IPv4 = PutGetXML.get_ip_from_xml(p_xml, 'IPv4')
        l_obj.Model = PutGetXML.get_text_from_xml(p_xml, 'Model')
        l_obj.Port = PutGetXML.get_int_from_xml(p_xml, 'Port', 55000)
        l_obj.RoomName = PutGetXML.get_text_from_xml(p_xml, 'RoomName')
        l_obj.RoomUUID = PutGetXML.get_uuid_from_xml(p_xml, 'RoomUUID')
        l_obj.Type = PutGetXML.get_text_from_xml(p_xml, 'Type')
        return l_obj

    @staticmethod
    def read_samsung_section_xml(p_pyhouse_obj):
        l_ret = {}
        l_count = 0
        l_xml = p_pyhouse_obj.Xml.XmlRoot
        l_xml = l_xml.find('HouseDivision')
        if l_xml is None:
            return l_ret, l_count
        l_xml = l_xml.find('EntertainmentSection')
        if l_xml is None:
            return l_ret, l_count
        l_xml = l_xml.find('SamsungSection')
        if l_xml is None:
            return l_ret, l_count
        try:
            for l_device_xml in l_xml.iterfind('Device'):
                l_device_obj = XML._read_one_device(l_device_xml)
                l_device_obj.Key = l_count
                l_ret[l_count] = l_device_obj
                LOG.info('Loaded Samsung Device {}'.format(l_device_obj.Name))
                l_count += 1
        except AttributeError as e_err:
            LOG.error('ERROR if getting Samsung Device Data - {}'.format(e_err))
        p_pyhouse_obj.House.Entertainment.Samsung = l_ret
        LOG.info('Loaded {} Samsung Devices.'.format(l_count))
        return l_ret, l_count

    @staticmethod
    def _write_one_device(p_obj):
        l_xml = XmlConfigTools.write_base_UUID_object_xml('Device', p_obj)
        PutGetXML().put_text_element(l_xml, 'Comment', p_obj.Comment)
        return l_xml

    @staticmethod
    def write_samsung_section_xml(p_pyhouse_obj):
        l_xml = ET.Element('SamsungSection')
        l_count = 0
        l_obj = p_pyhouse_obj.House.Entertainment.Samsung
        for l_room_object in l_obj.values():
            l_room_object.Key = l_count
            l_entry = XML.write_one_device(l_room_object)
            l_xml.append(l_entry)
            l_count += 1
        LOG.info('Saved {} Samsung device(s) XML'.format(l_count))
        return l_xml


class MqttActions:
    """
    """

    m_API = None
    m_transport = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _get_field(self, p_message, p_field):
        try:
            l_ret = p_message[p_field]
        except KeyError:
            l_ret = 'The "{}" field was missing in the MQTT Message.'.format(p_field)
        return l_ret

    def _decode_control(self, p_topic, p_message):
        """ Decode the message.
        As a side effect - control samsung.
        """
        l_logmsg = '\tControl: '
        l_control = self._get_field(p_message, 'Control')
        if l_control == 'On':
            l_logmsg += ' Turn On '
            self.m_API.Start()
        elif l_control == 'Off':
            l_logmsg += ' Turn Off '
            self.m_API.Stop()

        elif l_control == 'VolUp1':
            l_logmsg += ' Volume Up 1 '
        else:
            l_logmsg += ' Unknown samsung Control Message {} {}'.format(p_topic, p_message)
        return l_logmsg

    def decode(self, p_topic, p_message):
        """ Decode the Mqtt message
        ==> pyhouse/<house name>/entertainment/samsung/<type>/<Name>/...
        <type> = ?
        """
        if self.m_API == None:
            # LOG.debug('Decoding initializing')
            self.m_API = API(self.m_pyhouse_obj)

        l_logmsg = ''
        if p_topic[2] == 'control':
            l_logmsg += '\tSamsung: {}\n'.format(self._decode_control(p_topic, p_message))
        else:
            l_logmsg += '\tUnknown Samsung sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Entertainment msg', 160))
        return l_logmsg


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

    def __init__(self, p_pyhouse_obj, _p_samsung_obj, _p_clientID=None):
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
        _l_msg = PrettyFormatAny.form(p_connector, 'Samsung Factory connector.')
        LOG.info('Started to connect. {}'.format(p_connector))

    def buildProtocol(self, p_addr):
        LOG.info('BuildProtocol - Addr = {}'.format(p_addr))
        _l_client = SamsungClient(self.m_pyhouse_obj, self.m_samsung_obj)
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
        # l_samsung_obj = SamsungDeviceData()
        p_pyhouse_obj.House.Entertainment.Samsung = SamsungDeviceData()  # Clear before loading
        l_samsung_obj, l_count = XML().read_samsung_section_xml(p_pyhouse_obj)
        p_pyhouse_obj.House.Entertainment.Samsung = l_samsung_obj
        # l_host = SAMSUNG_ADDRESS
        # l_port = SAMSUNG_PORT
        # l_samsung_obj.Factory = SamsungFactory(p_pyhouse_obj, l_samsung_obj)
        # _l_connector = p_pyhouse_obj.Twisted.Reactor.connectTCP(l_host, l_port, l_samsung_obj.Factory)
        LOG.info('Loaded {} XML'.format(l_count))

    def Start(self):
        LOG.info("Starting.")
        LOG.info("Started.")

    def SaveXml(self, p_xml):
        # LOG.info("Saving XML.")
        l_xml = XML().write_samsung_section_xml(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Saved XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopping.")
        LOG.info("Stopped.")

# ## END DBK
