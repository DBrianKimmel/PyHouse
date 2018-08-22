"""
-*- test-case-name: src/Modules/Housing/Entertainment/pioneer/test/test_pioneer.py -*-

@name:      PyHouse.src.Modules.Housing.Entertainment.pioneer.pioneer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2018 by D. Brian Kimmel
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

__updated__ = '2018-08-22'
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
from Modules.Housing.Entertainment.entertainment_data import EntertainmentDeviceData
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
from Modules.Core.Utilities.convert import long_to_str
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Pioneer        ')
# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

PORT = 8102
IP = '192.168.9.121'
SECTION = 'pioneer'

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


class PioneerDeviceData(EntertainmentDeviceData):

    def __init__(self):
        super(PioneerDeviceData, self).__init__()
        self.CommandSet = None
        self.IPv4 = None
        self.Port = None
        self.RoomName = None
        self.RoomUUID = None
        self.Type = None
        self.Volume = None


class XML(object):
    """
    """

    @staticmethod
    def _read_device(p_xml):
        """
        @param p_entry_xml: Element <Device> within <PandoraSection>
        @return: a PandoraDeviceData object
        """
        l_device = PioneerDeviceData()
        XmlConfigTools().read_base_UUID_object_xml(l_device, p_xml)
        # l_device.Name = PutGetXML.get_text_from_xml(p_xml, 'Name')
        # l_device.Active = PutGetXML.get_bool_from_xml(p_xml, 'Active')
        # l_device.Key = PutGetXML.get_int_from_xml(p_xml, 'Key')
        # l_device.UUID = PutGetXML.get_uuid_from_xml(p_xml, 'UUID')
        # l_device.Comment = PutGetXML.get_text_from_xml(p_xml, 'Comment')
        l_device.CommandSet = PutGetXML.get_text_from_xml(p_xml, 'CommandSet')
        l_device.IPv4 = PutGetXML.get_ip_from_xml(p_xml, 'IPv4')
        l_device.Port = PutGetXML.get_int_from_xml(p_xml, 'Port')
        l_device.RoomName = PutGetXML.get_text_from_xml(p_xml, 'RoomName')
        l_device.RoomUUID = PutGetXML.get_uuid_from_xml(p_xml, 'RoomUUID')
        # l_device.Status = PutGetXML.get_text_from_xml(p_xml, 'Status')
        l_device.Type = PutGetXML.get_text_from_xml(p_xml, 'Type')
        l_device.Volume = PutGetXML.get_int_from_xml(p_xml, 'Volume')
        return l_device

    @staticmethod
    def _write_device(p_obj):
        """
        @param p_obj: is a PioneerDeviceData
        @return: a xml element for the device
        """
        l_xml = XmlConfigTools().write_base_UUID_object_xml('Device', p_obj)
        PutGetXML().put_text_element(l_xml, 'Comment', p_obj.Comment)
        PutGetXML().put_text_element(l_xml, 'CommandSet', p_obj.CommandSet)
        PutGetXML().put_ip_element(l_xml, 'IPv4', p_obj.IPv4)
        PutGetXML().put_int_element(l_xml, 'Port', p_obj.Port)
        PutGetXML().put_int_element(l_xml, 'Port', p_obj.Port)
        PutGetXML().put_text_element(l_xml, 'Type', p_obj.Type)
        return l_xml

    @staticmethod
    def read_pioneer_section_xml(p_pyhouse_obj):
        """ Get the entire PioneerDeviceData object from the xml.
        """
        l_xml = XmlConfigTools.find_section(p_pyhouse_obj, 'HouseDivision/EntertainmentSection/PioneerSection')
        l_entertain_obj = p_pyhouse_obj.House.Entertainment
        l_plugin_obj = l_entertain_obj.Plugins[SECTION]
        l_plugin_obj.Name = SECTION
        l_plugin_obj.Active = PutGetXML.get_bool_from_xml(l_xml, 'Active')
        l_count = 0
        if l_xml is None:
            return l_plugin_obj
        try:
            l_plugin_obj.Type = PutGetXML.get_text_from_xml(l_xml, 'Type')
            for l_device_xml in l_xml.iterfind('Device'):
                l_device_obj = XML._read_device(l_device_xml)
                l_device_obj.Key = l_count
                l_plugin_obj.Devices[l_count] = l_device_obj
                LOG.info('Loaded {} Device {}'.format(SECTION, l_plugin_obj.Name))
                l_count += 1
                l_plugin_obj.Count = l_count
        except AttributeError as e_err:
            LOG.error('ERROR if getting {} Device Data - {}'.format(SECTION, e_err))
        p_pyhouse_obj.House.Entertainment.Plugins[SECTION] = l_plugin_obj
        LOG.info('Loaded {} {}Devices.'.format(l_count, SECTION))
        return l_plugin_obj

    @staticmethod
    def write_pioneer_section_xml(p_pyhouse_obj):
        """ Create the entire PioneerSection of the XML.
        """
        l_entertain_obj = p_pyhouse_obj.House.Entertainment
        l_plugin_obj = l_entertain_obj.Plugins[SECTION]
        l_active = l_plugin_obj.Active
        l_xml = ET.Element('PioneerSection', attrib={'Active': str(l_active)})
        PutGetXML.put_text_element(l_xml, 'Type', l_plugin_obj.Type)
        l_count = 0

        # print(PrettyFormatAny.form(l_entertain_obj, 'Wr-1 Pioneer', 180))
        # print(PrettyFormatAny.form(l_entertain_obj.Plugins, 'Wr-2 Pioneer', 180))
        # print(PrettyFormatAny.form(l_entertain_obj.Plugins[SECTION], 'Wr-3 Pioneer', 180))
        # print(PrettyFormatAny.form(l_entertain_obj.Plugins[SECTION].Devices, 'Wr-4 Pioneer', 180))

        for l_obj in l_plugin_obj.Devices.values():
            l_dev_xml = XML._write_device(l_obj)
            l_xml.append(l_dev_xml)
            l_count += 1
        LOG.info('Saved {} Pioneer device(s) XML'.format(l_count))
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
        As a side effect - control pioneer.
        """
        l_logmsg = '\tControl: '
        l_control = self._get_field(p_message, 'Control')
        l_power = self._get_field(p_message, 'Power')
        l_volume = self._get_field(p_message, 'Volume')
        l_input = self._get_field(p_message, 'Input')
        if l_control == 'On':
            l_logmsg += ' Turn On '
            self.m_API.Start()
        elif l_control == 'Off':
            l_logmsg += ' Turn Off '
            self.m_API.Stop()
        elif l_power == 'On':
            pass
        elif l_control == 'VolUp1':
            l_logmsg += ' Volume Up 1 '
        else:
            l_logmsg += ' Unknown pioneer Control Message {} {}'.format(p_topic, p_message)
        return l_logmsg

    def decode(self, p_topic, p_message):
        """ Decode the Mqtt message
        ==> pyhouse/<house name>/entertainment/pioneer/<type>/<Name>/...
        <type> = ?
        """
        if self.m_API == None:
            # LOG.debug('Decoding initializing')
            self.m_API = API(self.m_pyhouse_obj)

        l_logmsg = ''
        if p_topic[2] == 'control':
            l_logmsg += '\tPioneer: {}\n'.format(self._decode_control(p_topic, p_message))
        else:
            l_logmsg += '\tUnknown Pioneer sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Entertainment msg', 160))
        return l_logmsg


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


class API(MqttActions):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def _playPioneer(self):
        pass

    def LoadXml(self, p_pyhouse_obj):
        """ Read the XML for all Pioneer devices.
        """
        l_pioneer_obj = XML.read_pioneer_section_xml(p_pyhouse_obj)
        # p_pyhouse_obj.House.Entertainment.Plugins[SECTION] = l_pioneer_obj
        LOG.info("Loaded Pioneer Device(s).")
        return l_pioneer_obj

    def Start(self):
        """ Start all the Pioneer factories if we have any Pioneer devices.
        """
        return
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
        l_xml = XML().write_pioneer_section_xml(self.m_pyhouse_obj)
        # p_xml.append(l_xml)
        LOG.info("Saved Pioneer XML.")
        return l_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
