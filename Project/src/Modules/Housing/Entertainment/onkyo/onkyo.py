"""
-*- test-case-name: PyHouse/Project/src/Modules/Entertainment/test_onkyo.py -*-

@name:      PyHouse/src/Modules/Entertainment/onkyo.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c)2016-2019 by D. Brian Kimmel
@note:      Created on Jul 9, 2016
@license:   MIT License
@summary:

"""

__updated__ = '2019-05-02'
__version_info__ = (19, 4, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from twisted.internet.protocol import Factory
from twisted.internet.error import ConnectionDone
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.protocols.basic import LineReceiver
from queue import Queue

#  Import PyMh files and modules.
from Modules.Housing.Entertainment.entertainment_data import EntertainmentDeviceData
from Modules.Core.Utilities import convert
from Modules.Core.Utilities import extract_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Onkyo          ')

SECTION = 'onkyo'

# See https://
CONTROL_COMMANDS = {
    'Power':            [b'PWR', b'PWZ'],
    'Volume':           [b'MVL', b'ZVL'],
    'Mute':             [b'AMT', b'ZMT'],
    'InputSelect':      [b'SLI', b'SLZ']
    }

CMD_01 = b'ISCP\x00\x00\x00\x10\x00\x00\x00\x0c\x01\x00\x00\x00!1PWRQSTN\x1a\n\r'

#  ==Endpoints==
# clientFromString
# serverFromString
# TCP4ServerEndpoint
# TCP6ServerEndpoint
# TCP4ClientEndpoint
# TCP6ClientEndpoint
# UNIXServerEndpoint
# UNIXClientEndpoint
# SSL4ServerEndpoint
# SSL4ClientEndpoint
# AdoptedStreamServerEndpoint
# StandardIOEndpoint
# ProcessEndpoint
# HostnameEndpoint
# StandardErrorBehavior
# connectProtocol
# wrapClientTLS


class OnkyoDeviceData(EntertainmentDeviceData):
    """
    """

    def __init__(self):
        super(OnkyoDeviceData, self).__init__()
        self._Queue = None


class QueueData:
    """
    """

    def __init__(self):
        self.Command = b'aaa'
        self.Args = b'01'
        self.isDone = False


class OnkyoResponses:
    """
    """

    m_buffer = bytearray(0)

    def _decode_message(self, p_msg):
        l_eq_type = p_msg[1:2]
        l_cmd = p_msg[2:5]
        l_args = p_msg[5:]
        LOG.info('Onkyo sent Eq:{} {} {}'.format(l_eq_type, l_cmd, l_args))

        if l_cmd == 'AEQ':
            LOG.info('AEQ ??? : {}'.format(l_args))  # Onkyo sent EqType:1 AEQ 01
        if l_cmd == 'AMT':
            LOG.info('AMT Auto Mute : {}'.format(l_args))  # Onkyo sent EqType:1 AMT 00
        if l_cmd == 'DIM':
            LOG.info('DIM Dimmer Level : {}'.format(l_args))  # Onkyo sent EqType:1 DIM 02
        if l_cmd == 'IFA':
            LOG.info('IFA Info Audio : {}'.format(l_args))
        if l_cmd == 'ITV':
            LOG.info('ITV ??? : {}'.format(l_args))  # Onkyo sent EqType:1 ITV 000
        if l_cmd == 'MVL':
            LOG.info('MVL Master Volume Level : {}'.format(l_args))  # Onkyo sent EqType:1 MVL 36
        if l_cmd == 'MOT':
            LOG.info('MOT Music Optimizer : {}'.format(l_args))  # Onkyo sent EqType:1 MOT 00
        if l_cmd == 'NAL':
            LOG.info('NAL Song from Album : {}'.format(l_args))  # Onkyo sent EqType:1 NAL Forever Changing - The Golden Age Of Elektra Records 1963-1973
        if l_cmd == 'NAT':
            LOG.info('NAT Song Artist : {}'.format(l_args))  # Onkyo sent EqType:1 NAT Judy Collins
        if l_cmd == 'NDS':
            LOG.info('NDS ??? : {}'.format(l_args))  # Onkyo sent EqType:1 NDS E-x
        if l_cmd == 'NJA':
            LOG.info('NJA Jacket-Art: {}'.format(l_args))  # Onkyo sent EqType:1 NJA 2-http://192.168.1.120/album_art.cgi
        if l_cmd == 'NLS':
            LOG.info('NLS USB List Info : {}'.format(l_args))  # Onkyo sent EqType:1 NLS C-P
        if l_cmd == 'NLT':
            LOG.info('NLT ??? : {}'.format(l_args))  # Onkyo sent EqType:1 NLT 0422000000000001000400
        if l_cmd == 'NMS':
            LOG.info('NMS ??? : {}'.format(l_args))  # Onkyo sent EqType:1 NMS M0C02x104
        if l_cmd == 'NTI':
            LOG.info('NTI Song Title : {}'.format(l_args))  # Onkyo sent EqType:1 NTI Tomorrow Is A Long Time
        if l_cmd == 'NTM':
            LOG.info('NTM Stream time : {}'.format(l_args))  # Onkyo sent EqType:1 NTM 00:02:46/00:02:57
        if l_cmd == 'NTR':
            LOG.info('NTR Time?? : {}'.format(l_args))  # Onkyo sent EqType:1 NTR ----/----
        if l_cmd == 'PCT':
            LOG.info('PCT Picture Control : {}'.format(l_args))  # Onkyo sent EqType:1 PCT 00
        if l_cmd == 'PWR':
            LOG.info('PWR Power : {}'.format(l_args))  # Onkyo sent EqType:1 PWR 01
        if l_cmd == 'RAS':
            LOG.info('RAS Re-Eq : {}'.format(l_args))  # Onkyo sent EqType:1 RAS 00
        if l_cmd == 'SLI':
            LOG.info('SLI Input Selector : {}'.format(l_args))  # Onkyo sent EqType:1 SLI 12
        if l_cmd == 'SLZ':
            LOG.info('SLZ Zone 2 Input Selector : {}'.format(l_args))  # Onkyo sent EqType:1 SLZ 2E
        if l_cmd == 'ZMT':
            LOG.info('ZMT Zone 2 Muting  : {}'.format(l_args))  # Onkyo sent EqType:1 ZMT 00
        if l_cmd == 'ZPW':
            LOG.info('ZPW Zone 2 Power : {}'.format(l_args))  # Onkyo sent EqType:1 ZPW 01
        if l_cmd == 'ZVL':
            LOG.info('ZVL Zone 2 Volume Level : {}'.format(l_args))  # Onkyo sent EqType:1 ZPW 01

    def _get_onkyo_message(self, p_msg):
        """
        """
        l_prefix = p_msg[0:4].decode('utf-8')
        if l_prefix != 'ISCP':
            LOG.warn('error in buffer: {} - {}'.format(l_prefix, PrettyFormatAny.form(self.m_buffer, 'Buffer', 150)))
            self.m_buffer = self.m_buffer[1:]
            return
        l_header_size = convert.bigend_2_int(p_msg[4:8])
        l_data_size = convert.bigend_2_int(p_msg[8:12])
        _l_version = convert.bigend_2_int(p_msg[12:13])
        # Note - there are possibly extra chars in the header
        l_total_size = l_header_size + l_data_size
        l_msg = p_msg[l_header_size:l_total_size]
        l_msg = l_msg.rstrip(b'\r\n\x1a').decode('utf-8')
        if l_msg[0:1] != '!':
            LOG.error('Invalid char found')
        self._decode_message(l_msg)
        # LOG.debug('Msg = "{}"'.format(l_msg))
        return l_total_size

    def _extract_message(self, p_buffer):
        """ Take the 1st message from the buffer and process it.
        Pop the message from the buffer.
        """
        l_len = self._get_onkyo_message(p_buffer)
        p_buffer = p_buffer[l_len:]
        return p_buffer


class OnkyoProtocol(LineReceiver, OnkyoResponses):
    """
    Each onkyo device can have only one connection.
    This may cause the tcp connection to fail.
    """

    def __init__(self, p_pyhouse_obj, p_device_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_device_obj = p_device_obj

    def dataReceived(self, p_data):
        """
        Called whenever data is received.
        """
        self.m_buffer += p_data
        while len(self.m_buffer) > 16:
            self.m_buffer = self._extract_message(self.m_buffer)

    def lineReceived(self, p_data):
        """
        Called whenever data is received.
        """
        self.m_buffer += p_data
        LOG.debug('LineReceived.\n\tData:{}'.format(p_data))
        while len(self.m_buffer) > 16:
            self.m_buffer = self._extract_message(self.m_buffer)

    def connectionMade(self):
        """
        Called when a connection is made.
        This may be considered the initializer of the protocol, because it is called when the connection is completed.
        For clients, this is called once the connection to the server has been established;
        for servers, this is called after an accept() call stops blocking and a socket has been received.
        If you need to send any greeting or initial message, do it here.
        """
        LOG.info('ConnectionMade')
        # Protocol.connectionMade(self)
        self.setLineMode()
        self.m_device_obj._Transport = self.transport
        # self._get_status()

    def connectionLost(self, reason=ConnectionDone):
        """
        Called when the connection is shut down.
        Clear any circular references here, and any external references to this Protocol.
        The connection has been closed.
        The reason Failure wraps a twisted.internet.error.ConnectionDone or twisted.internet.error.ConnectionLost instance (or a subclass of one of those).
        """
        # Protocol.connectionLost(self, reason=reason)
        LOG.warn('Lost connection.\n\tReason:{}'.format(reason))


class OnkyoFactory(Factory):
    """
    """
    protocol = OnkyoProtocol
    m_pyhouse_oj = None
    m_device_obj = None

    def __init__(self, p_pyhouse_obj, p_device_obj):
        """ Set up the persistent Data.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_device_obj = p_device_obj

    def startedConnecting(self, p_connector):
        LOG.debug('Started to connect.'.format(PrettyFormatAny.form(p_connector, 'Connector', 180)))

    def buildProtocol(self, _p_addr):
        LOG.debug('Build Protocol.')
        l_protocol = OnkyoProtocol(self.m_pyhouse_obj, self.m_device_obj)
        return l_protocol

    def clientConnectionLost(self, p_reason):
        LOG.debug('Lost connection. Reason: {}'.format(p_reason))

    def clientConnectionFailed(self, p_reason):
        LOG.debug('Connection failed. Reason:', p_reason)

    def makeConnection(self, transport):
        """
        Make a connection to a transport and a server.
        """
        # Protocol.makeConnection(self, transport)
        LOG.debug('MakeConnection {}'.format(PrettyFormatAny.form(transport, 'Transport', 180)))


class OnkyoClient(OnkyoProtocol):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def Xconnect(self, p_device_obj):
        l_host = p_device_obj.Host
        l_port = p_device_obj.Port
        l_factory = OnkyoFactory(self.m_pyhouse_obj, p_device_obj)
        l_connector = self.m_pyhouse_obj.Twisted.Reactor.connectTCP(l_host, l_port, l_factory)
        p_device_obj._Factory = l_factory
        p_device_obj._Connector = l_connector
        p_device_obj._isRunning = True
        self.m_device_obj = p_device_obj
        LOG.info("Started Onkyo Device: '{}'; Host:{}; Port:{};".format(p_device_obj.Name, l_host, l_port))

    def send_command(self, p_device_obj, p_command):
        """
        @param p_command: is the comaand b"!1PWR01"
        Gthis will add the rest of the ethernet framework
        """
        if p_device_obj == None:
            LOG.error('Sending a commant to None will never work!')
            return
        LOG.info('Send command {}'.format(p_command))
        # LOG.debug('Log send command {}'.format(PrettyFormatAny.form(p_device_obj, 'Device', 190)))
        l_len = len(p_command) + 3
        l_command = b'ISCP' + \
                convert.int_2_bigend(16, 4) + \
                convert.int_2_bigend(l_len, 4) + \
                b'\x01' + b'\x00\x00\x00' + p_command + b'\x1a\n\r'
        try:
            p_device_obj._Protocol.transport.write(l_command)
            LOG.info('Send TCP command: {} to {}'.format(l_command, p_device_obj.Name))
        except AttributeError as e_err:
            LOG.error("Tried to call send_command without a onkyo device configured.\n\tError:{}".format(e_err))


class OnkeoControl:
    """
    """

    def _list_devices(self, p_list):
        """ List the devices we have opened.  Mostly for debugging and testing.
        """
        for l_dev in p_list:
            LOG.debug('Onkyo Device {}'.format(PrettyFormatAny.form(l_dev, 'Device', 190)))

    def onkyo_start(self, p_pyhouse_obj, p_device_obj):
        """ Open connections to the various Onkyo devices we will communicate with.
        """

        def cb_got_protocol(p_protocol, p_device_obj):
            p_device_obj._Protocol = p_protocol
            l_topic = 'entertainment/onkyo/status'
            l_message = p_device_obj
            self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_message)

            # LOG.debug('Connected to Onkyo device {}'.format(PrettyFormatAny.form(p_protocol, 'Proto', 190)))
            # LOG.debug('Connected to Onkyo device {}'.format(PrettyFormatAny.form(p_device_obj, 'Device', 190)))
            p_protocol.transport.write(CMD_01)

        def eb_got_protocol(p_reason):
            LOG.debug('Got an error connecting to Onkyo device - {}'.format(p_reason))

        l_reactor = p_pyhouse_obj.Twisted.Reactor
        l_host = p_device_obj.Host
        l_port = p_device_obj.Port
        #
        l_endpoint = TCP4ClientEndpoint(l_reactor, l_host, l_port)
        d_connector = l_endpoint.connect(OnkyoFactory(p_pyhouse_obj, p_device_obj))
        d_connector.addCallback(cb_got_protocol, p_device_obj)
        d_connector.addErrback(eb_got_protocol)
        #
        p_device_obj._Endpoint = l_endpoint
        p_device_obj._isRunning = True
        p_device_obj._Queue = Queue(32)
        self.m_device_lst.append(p_device_obj)
        LOG.info("Started Onkyo Device: '{}'; IP:{}; Port:{};".format(p_device_obj.Name, l_host, l_port))

    def _control_input(self, p_family, p_device, _p_zone, p_input):
        """
        !1SLIxx
        xx = 02 Game
        @param p_input: Channel Code
        """
        LOG.inf0('controlInput')
        l_device_obj = self._find_device(p_family, p_device)
        l_cmd = b'!1MVLQSTN'
        self.queue_command(l_device_obj, l_cmd)
        LOG.info('Changed input channel to {}'.format(p_input))

    def _control_power(self, p_family, p_device, _p_zone, p_power):
        """
        !1PWR01 = On
        !1PWR00 = Standby (Off)
        @param p_power: 'On' or 'Off'
        """
        LOG.inf0('xxx2')
        l_device_obj = self._find_device(p_family, p_device)
        l_cmd = b'!1PWR01'
        if p_power == 'Off':
            l_cmd = b'!1PWR00'
        self.send_command(l_device_obj, l_cmd)
        LOG.info('Changed Power to {}'.format(p_power))

    def _control_volume(self, p_family, p_device, _p_zone, p_volume):
        """
        !1MLVxx where xx is in hex (00-64)
        @param p_family: "onkyo"
        @param p_device: is the device we are going to change (Tx-555)
        @param p_volume: % 0-100
        """
        LOG.info('xxx3')
        l_device_obj = self._find_device(p_family, p_device)
        l_cmd = '!1MVL' + '{:02X}'.format(p_volume)
        l_cmd = bytes(l_cmd, 'utf-8')
        # l_cmd = b'!1MVL38'
        LOG.debug('Vol command {}'.format(l_cmd))
        self.send_command(l_device_obj, l_cmd)
        LOG.info('Changed Volume to {} %'.format(p_volume))

    def queue_comand(self, p_device_obj, p_command, p_zone):
        """
        """


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _decode_control(self, _p_topic, p_message):
        """ Decode the message.

        @param p_message: is the payload used to control
        """
        LOG.info('Decode-Control called:\n\tTopic:{}\n\tMessage:{}'.format(_p_topic, p_message))
        l_family = extract_tools.get_mqtt_field(p_message, 'Family')
        l_device = extract_tools.get_mqtt_field(p_message, 'Device')
        l_input = extract_tools.get_mqtt_field(p_message, 'Input')
        l_power = extract_tools.get_mqtt_field(p_message, 'Power')
        l_volume = extract_tools.get_mqtt_field(p_message, 'Volume')
        l_zone = extract_tools.get_mqtt_field(p_message, 'Zone')
        if l_family == None:
            l_family = 'onkyo'
        #
        l_logmsg = '\tOnkyo Control:\n\tDevice:{}-{}\n\tPower:{}\n\tVolume:{}\n\tInput:{}'.format(l_family, l_device, l_power, l_volume, l_input)
        LOG.debug(l_logmsg)
        #
        if l_input != None:
            l_logmsg += ' Turn input to {}.'.format(l_input)
            self._control_input(l_family, l_device, l_input)
        else:
            LOG.warn('No Input')
        #
        if l_volume != None:
            LOG.warn('Vol')
            l_logmsg += ' Change volume {}.'.format(l_volume)
            self._control_volume(l_family, l_device, l_volume)
        else:
            LOG.warn('No Vol')
        #
        if l_power != None:
            LOG.warn('Power')
            l_logmsg += ' Turn power {} to {}.'.format(l_power, l_device)
            self._control_power(l_family, l_device, l_power)
        else:
            LOG.warn('No Power')
        #
        if l_zone != None:
            l_logmsg += ' Turn Zone to {}.'.format(l_zone)
            self._control_zone(l_family, l_device, l_zone)
        else:
            LOG.warn('No Zone')
        #
        LOG.info('Decode-Control 2 called:\n\tTopic:{}\n\tMessage:{}'.format(_p_topic, p_message))
        return l_logmsg

    def decode(self, p_topic, p_message):
        """ Decode the Mqtt message
        ==> pyhouse/<house name>/entertainment/onkyo/<type>/<Name>/...
        <type> = ?

        @param p_topic: is the topic with pyhouse/housename/entertainment/onkyo stripped off.
        """
        # LOG.debug('Decode called:\n\tTopic:{}\n\tMessage:{}'.format(p_topic, p_message))
        l_logmsg = ' Onkyo-{}'.format(p_topic[0])
        if p_topic[0].lower() == 'control':
            l_logmsg += '\tControl: {}\n'.format(self._decode_control(p_topic, p_message))
        elif p_topic[0].lower() == 'status':
            l_logmsg += '\tStatus:'
        else:
            l_logmsg += '\tUnknown Onkyo sub-topic: {}  Message: {}'.format(p_topic, PrettyFormatAny.form(p_message, 'Entertainment msg', 160))
        return l_logmsg


class API(MqttActions, OnkyoClient, OnkeoControl):
    """This interfaces to all of PyHouse.
    """

    m_device_lst = []

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def _find_device(self, p_family, p_device):
        # l_pandora = self.m_pyhouse_obj.House.Entertainment.Plugins['pandora'].Devices
        l_devices = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices
        for l_device in l_devices.values():
            if l_device.Name == p_device:
                LOG.info("found device - {} {}".format(p_family, p_device))
                return l_device
        LOG.error('No such device as {}'.format(p_device))
        return None

    def LoadXml(self, p_pyhouse_obj):
        """ Read the XML for all Onkyo devices.
        """

        # l_device_obj = XML.read_onkyo_section_xml(p_pyhouse_obj)
        l_device_obj = p_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        LOG.info("Loaded Onkyo XML")
        return l_device_obj

    def Start(self):
        """ Start all the Onkyo factories if we have any Onkyo devices.

        We have one or more Onkyo devices in this house to use/control.
        Connect to all of them.

        EntertainmentDeviceData()

        """
        LOG.info('Start Onkyo.')
        l_count = 0
        l_devices = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices
        for l_device_obj in l_devices.values():
            if not l_device_obj.Active:
                continue
            if l_device_obj._isRunning:
                LOG.info('Onkyo device {} is already running.'.format(l_device_obj.Name))
                continue
            l_count += 1
            self.onkyo_start(self.m_pyhouse_obj, l_device_obj)
            self.m_device_lst.append(l_device_obj)
        LOG.info("Started {} Onkyo devices".format(l_count))

    def SaveXml(self, p_xml):
        # LOG.info("Saved Onkyo XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
