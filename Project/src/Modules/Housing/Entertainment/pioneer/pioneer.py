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

__updated__ = '2018-10-09'
__version_info__ = (18, 10, 1)
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

SECTION = 'pioneer'
XML_PATH = 'HouseDivision/EntertainmentSection/PioneerSection'

VSX822K = {
    'PowerQuery':       b'?P',
    'PowerOn':          b'PN',
    'PowerOff':         b'PF',
    'VolumeQuery':      b'?V',
    'VolmeUp':          b'VU',
    'VolumeDown':       b'VN',
    'MuteQuery':        b'?M',
    'FunctionQuery':    b'?F',
    'FunctionPandora':  b'01FN'
    }


class PioneerDeviceData(EntertainmentDeviceData):
    """
    """

    def __init__(self):
        super(PioneerDeviceData, self).__init__()
        self.CommandSet = None  # Command sets change over the years.
        self.IPv4 = None
        self.Port = None
        self.RoomName = None
        self.RoomUUID = None
        self.Type = None
        self.Volume = None
        self.isRunning = False


class XML:
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
        l_device.CommandSet = PutGetXML.get_text_from_xml(p_xml, 'CommandSet')
        l_device.IPv4 = PutGetXML.get_ip_from_xml(p_xml, 'IPv4')
        l_device.Port = PutGetXML.get_int_from_xml(p_xml, 'Port')
        l_device.RoomName = PutGetXML.get_text_from_xml(p_xml, 'RoomName')
        l_device.RoomUUID = PutGetXML.get_uuid_from_xml(p_xml, 'RoomUUID')
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
        PutGetXML().put_text_element(l_xml, 'CommandSet', p_obj.CommandSet)
        PutGetXML().put_ip_element(l_xml, 'IPv4', p_obj.IPv4)
        PutGetXML().put_int_element(l_xml, 'Port', p_obj.Port)
        PutGetXML().put_text_element(l_xml, 'RoomName', p_obj.RoomName)
        PutGetXML().put_uuid_element(l_xml, 'RoomUUID', p_obj.RoomUUID)
        PutGetXML().put_text_element(l_xml, 'Type', p_obj.Type)
        PutGetXML().put_int_element(l_xml, 'Volume', p_obj.Volume)
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
        LOG.info('Loaded {} {} Device(s).'.format(l_count, SECTION))
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
        for l_obj in l_plugin_obj.Devices.values():
            l_dev_xml = XML._write_device(l_obj)
            l_xml.append(l_dev_xml)
            l_count += 1
        LOG.info('Saved {} Pioneer device(s) XML'.format(l_count))
        return l_xml


class MqttActions:
    """
    """

    # m_API = None
    m_transport = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _get_field(self, p_message, p_field):
        try:
            l_ret = p_message[p_field]
        except KeyError:
            l_ret = 'The "{}" field was missing in the MQTT Message.'.format(p_field)
            LOG.error(l_ret)
        return l_ret

    def _decode_control(self, _p_topic, p_message):
        """ Decode the message.
        As a side effect - control pioneer.

        @param p_message: is the payload used to control
        """
        LOG.debug('Decode-Control called:\n\tTopic:{}\n\tMessage:{}'.format(_p_topic, p_message))
        l_family = self._get_field(p_message, 'Family')
        l_device = self._get_field(p_message, 'Device')
        l_power = self._get_field(p_message, 'Power')
        l_volume = self._get_field(p_message, 'Volume')
        l_input = self._get_field(p_message, 'Input')
        l_logmsg = '\tPioneer Control:\n\t\tDevice:{}-{}\n\t\tPower:{}\n\t\tVolume:{}\n\t\tInput:{}'.format(l_family, l_device, l_power, l_volume, l_input)
        #
        if l_power != None:
            l_logmsg += ' Turn power {} to {}.'.format(l_power, l_device)
            self._pioneer_power(l_family, l_device, l_power)
        #
        if l_input != None:
            l_logmsg += ' Turn input to {}.'.format(l_input)
            self._pioneer_input(l_family, l_device, l_input)
        #
        if l_volume != None:
            l_logmsg += ' Change volume {}.'.format(l_volume)
            self._pioneer_volume(l_family, l_device, l_volume)
        #
        return l_logmsg

    def _decode_status(self, _p_topic, p_message):
        """ Decode the message.
        As a side effect - control pioneer.

        @param p_message: is the payload used to control
        """
        l_family = self._get_field(p_message, 'Family')
        l_device = self._get_field(p_message, 'Device')
        l_power = self._get_field(p_message, 'Power')
        l_volume = self._get_field(p_message, 'Volume')
        l_input = self._get_field(p_message, 'Input')
        l_logmsg = '\tPioneer Status: Power:{}\tVolume:{}\tInput:{}'.format(l_power, l_volume, l_input)
        return l_logmsg

    def decode(self, p_topic, p_message):
        """ Decode the Mqtt message
        ==> pyhouse/<house name>/entertainment/pioneer/<type>/<Name>/...
        <type> = ?

        @param p_topic: is the topic with pyhouse/housename/entertainment/pioneer stripped off.
        """
        # LOG.debug('Decode called:\n\tTopic:{}\n\tMessage:{}'.format(p_topic, p_message))
        l_logmsg = ' Pioneer-{}'.format(p_topic[0])
        if p_topic[0].lower() == 'control':
            l_logmsg += '\tPioneer: {}\n'.format(self._decode_control(p_topic, p_message))
        # elif p_topic[0].lower() == 'status':
        #    l_logmsg += '\tPioneer: {}\n'.format(self._decode_status(p_topic, p_message))
        else:
            l_logmsg += '\tUnknown Pioneer sub-topic: {}  Message: {}'.format(p_topic, PrettyFormatAny.form(p_message, 'Entertainment msg', 160))
        return l_logmsg


class PioneerProtocol(StatefulTelnetProtocol):
    """ There is an instance of this for every pioneer device that we are controlling.

    Each protocol instance is mapped to a Pioneer Device (and visa  versa)
    """

    def __init__(self, p_pyhouse_obj, p_pioneer_device_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_pioneer_device_obj = p_pioneer_device_obj
        # LOG.debug('Factory init for {}'.format(PrettyFormatAny.form(self.m_pioneer_device_obj, 'PioneerFactory-')))
        LOG.info('Protocol Init - Version:{}'.format(__version__))

    def dataReceived(self, p_data):
        """ This seems to be a line received function
        """
        Protocol.dataReceived(self, p_data)
        self.setLineMode()
        l_data = p_data[:-2]  # Drop the trailing CrLf
        if l_data == b'R':
            return
        LOG.info('Data Received.\n\tData:{}'.format(l_data))

    def lineReceived(self, p_line):
        StatefulTelnetProtocol.lineReceived(self, p_line)
        LOG.info('Line Received.\n\tData:{}'.format(p_line))

    def connectionMade(self):
        """ *3
        Setup
        We have connected - now get the initial conditions.
        """
        Protocol.connectionMade(self)
        self.setLineMode()
        LOG.info('Connection Made.')
        self.m_pioneer_device_obj._Transport = self.transport
        # LOG.debug('Connection Transport. {}'.format(PrettyFormatAny.form(self.transport, '_Transport', 180)))
        self.send_command(self.m_pioneer_device_obj, VSX822K['PowerQuery'])  # Query Power
        self.send_command(self.m_pioneer_device_obj, VSX822K['MuteQuery'])
        self.send_command(self.m_pioneer_device_obj, VSX822K['VolumeQuery'])
        self.send_command(self.m_pioneer_device_obj, VSX822K['FunctionQuery'])
        self.send_command(self.m_pioneer_device_obj, b'01FN')

    def connectionLost(self, reason=ConnectionDone):
        """ TearDown
        """
        Protocol.connectionLost(self, reason=reason)
        LOG.warn('Lost connection.\n\tReason:{}'.format(reason))


class PioneerClient(PioneerProtocol):
    """
    """

    def __init__(self, p_pyhouse_obj, p_pioneer_device_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_pioneer_device_obj = p_pioneer_device_obj
        # LOG.debug('PioneerClient init for {}'.format(PrettyFormatAny.form(self.m_pioneer_device_obj, 'PioneerClient Init-')))

    def send_command(self, p_device_obj, p_command):
        LOG.info('Send command {}'.format(p_command))
        try:
            l_host = p_device_obj._Connector.host
            p_device_obj._Transport.write(p_command + b'\r\n')
            LOG.info('Send TCP command:{} to {}'.format(p_command, l_host))
        except AttributeError as e_err:
            LOG.error("Tried to call send_command without a pioneer device configured.\n\tError:{}".format(e_err))


class PioneerFactory(ReconnectingClientFactory):
    """
    This is a factory which produces protocols.
    By default, buildProtocol will create a protocol of the class given in self.protocol.
    """

    def __init__(self, p_pyhouse_obj, p_pioneer_device_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_pioneer_device_obj = p_pioneer_device_obj
        # LOG.debug('Factory init for {}'.format(PrettyFormatAny.form(self.m_pioneer_device_obj, 'PioneerFactory-')))
        LOG.info('Init - Version:{}'.format(__version__))

    def startedConnecting(self, p_connector):
        """ *1
        Called when we are connecting to the device.
        Provides access to the connector.
        """
        self.m_pioneer_device_obj._Connector = p_connector
        # LOG.debug('Started to connect. {}'.format(PrettyFormatAny.form(p_connector, '_Connector', 180)))

    def buildProtocol(self, p_addr):
        """ *2
        Create an instance of PioneerProtocol.

        @param p_addr: an object implementing twisted.internet.interfaces.IAddress
        @return:
        """
        self.protocol = PioneerProtocol(self.m_pyhouse_obj, self.m_pioneer_device_obj)
        l_client = PioneerClient(self.m_pyhouse_obj, self.m_pioneer_device_obj)
        LOG.info('BuildProtocol - Addr = {}; Client:{}'.format(p_addr, l_client))
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


class API(MqttActions, PioneerClient):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("API Initialized - Version:{}".format(__version__))

    def _find_device(self, _p_family, p_device):
        l_pioneer = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices
        for l_device in l_pioneer.values():
            if l_device.Name == p_device:
                LOG.debug("found device")
                return l_device
        LOG.error('No such device')
        return None

    def _pioneer_power(self, p_family, p_device, p_power):
        """
        @param p_power: 'On' or 'Off'
        """
        # Get the device_obj to control
        l_device_obj = self._find_device(p_family, p_device)
        if p_power == 'On':
            self.send_command(l_device_obj, VSX822K['PowerOn'])  # Query Power
        else:
            # self.send_command(l_device_obj, VSX822K['PowerOff'])  # Query Power
            pass
        LOG.debug('Change Power to {}'.format(p_power))

    def _pioneer_volume(self, p_family, p_device, p_volume):
        """
        @param p_volume: 'Up1', 'Up5', 'Down1' or 'Down5'
        """
        LOG.debug('Volume:{}'.format(p_volume))
        l_device_obj = self._find_device(p_family, p_device)
        if p_volume == 'VolUp1':
            self.send_command(l_device_obj, VSX822K['VolumeUp'])
        elif p_volume == 'VolUp5':
            self.send_command(l_device_obj, VSX822K['VolumeUp'])
            self.send_command(l_device_obj, VSX822K['VolumeUp'])
            self.send_command(l_device_obj, VSX822K['VolumeUp'])
            self.send_command(l_device_obj, VSX822K['VolumeUp'])
            self.send_command(l_device_obj, VSX822K['VolumeUp'])
        elif p_volume == 'VolDown1':
            self.send_command(l_device_obj, VSX822K['VolumeDown'])
        elif p_volume == 'VolDown5':
            self.send_command(l_device_obj, VSX822K['VolumeDown'])
            self.send_command(l_device_obj, VSX822K['VolumeDown'])
            self.send_command(l_device_obj, VSX822K['VolumeDown'])
            self.send_command(l_device_obj, VSX822K['VolumeDown'])
            self.send_command(l_device_obj, VSX822K['VolumeDown'])
        else:
            pass
        LOG.debug('Change Volume to {}'.format(p_volume))

    def _pioneer_input(self, p_family, p_device, p_input):
        """
        @param p_input: Channel Code
        """
        l_device_obj = self._find_device(p_family, p_device)
        self.send_command(l_device_obj, b'01FN')  # Query Power
        LOG.debug('Change input channel to {}'.format(p_input))

    def LoadXml(self, p_pyhouse_obj):
        """ Read the XML for all Pioneer devices.
        """
        self.m_started = False
        l_pioneer_device_obj = XML.read_pioneer_section_xml(p_pyhouse_obj)
        LOG.info("Loaded Pioneer Device(s) - Version:{}".format(__version__))
        return l_pioneer_device_obj

    def Start(self):
        """ Start all the Pioneer factories if we have any Pioneer devices.
        """
        LOG.info('Starting...')
        l_count = 0
        for l_pioneer_device_obj in self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices.values():
            l_count += 1
            if not l_pioneer_device_obj.Active:
                continue
            if l_pioneer_device_obj.isRunning:
                LOG.info('Pioneer device {} is already running.'.format(l_pioneer_device_obj.Name))
            l_host = long_to_str(l_pioneer_device_obj.IPv4)
            l_port = l_pioneer_device_obj.Port
            l_factory = PioneerFactory(self.m_pyhouse_obj, l_pioneer_device_obj)
            l_connector = self.m_pyhouse_obj.Twisted.Reactor.connectTCP(l_host, l_port, l_factory)
            l_pioneer_device_obj._Factory = l_factory
            l_pioneer_device_obj._Connector = l_connector
            l_pioneer_device_obj.isRunning = True
            self.m_pioneer_device_obj = l_pioneer_device_obj
            # LOG.debug('Connection Factory. {}'.format(PrettyFormatAny.form(l_factory, '_Factory', 180)))
            # LOG.debug('Connection Connector. {}'.format(PrettyFormatAny.form(l_connector, '_Connector', 180)))
            LOG.info("Started Pioneer Device: '{}'; IP:{}; Port:{};".format(l_pioneer_device_obj.Name, l_host, l_port))
            # LOG.debug('Pioneer-Start {}'.format(PrettyFormatAny.form(self.m_pioneer_device_obj, 'PioneerStart-')))
        LOG.info("Started {} Pioneer device(s).".format(l_count))

    def SaveXml(self, _p_xml):
        l_xml = XML().write_pioneer_section_xml(self.m_pyhouse_obj)
        LOG.info("Saved Pioneer XML.")
        return l_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
