"""
@name:      Modules/House/Entertainment/Onkyo/onkyo_protocol.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 24, 2019
@summary:
"""

__updated__ = '2020-02-17'
__version_info__ = (19, 12, 2)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from twisted.protocols.basic import LineReceiver
from twisted.internet.error import ConnectionDone
from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ClientEndpoint
from queue import Queue

#  Import PyMh files and modules.
from Modules.Core.Utilities import convert
from Modules.House.Entertainment import EntertainmentDeviceStatus

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Onkyo          ')


class OnkyoDeviceStatus(EntertainmentDeviceStatus):
    """
    The device family is part of the topic.
    """

    def __init__(self):
        super(OnkyoDeviceStatus, self).__init__()
        pass


class OnkyoResponses():
    """
    """

    m_buffer = bytearray(0)

    def _decode_message(self, p_msg):
        l_eq_type = p_msg[1:2]
        l_cmd = p_msg[2:5]
        l_args = p_msg[5:]
        LOG.info('Onkyo sent Eq:{} {} {}'.format(l_eq_type, l_cmd, l_args))
        # Volume - Send feedback to service controlling this device.
        if l_cmd == 'MVL':
            _l_zone = 0
            _l_volume = l_args
            LOG.info('MVL Master Volume Level : {}'.format(l_args))  # Onkyo sent EqType:1 MVL 36
        elif l_cmd == 'ZVL':
            _l_zone = 1
            _l_volume = l_args
            LOG.info('ZVL Zone 2 Volume Level : {}'.format(l_args))  # Onkyo sent EqType:1 ZPW 01

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

    def _get_onkyo_message(self, p_msg):
        """
        """
        l_prefix = p_msg[0:4].decode('utf-8')
        if l_prefix != 'ISCP':
            LOG.warning('error in buffer: {} - {}'.format(l_prefix, PrettyFormatAny.form(self.m_buffer, 'Buffer', 150)))
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

    Other nodes may silently steal the connection.
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
        self.setLineMode()
        self.m_device_obj._Transport = self.transport

    def connectionLost(self, reason=ConnectionDone):
        """
        Called when the connection is shut down.
        Clear any circular references here, and any external references to this Protocol.
        The connection has been closed.
        The reason Failure wraps a twisted.internet.error.ConnectionDone or twisted.internet.error.ConnectionLost instance (or a subclass of one of those).
        """
        # Protocol.connectionLost(self, reason=reason)
        LOG.warning('Lost connection.\n\tReason:{}'.format(reason))


class OnkyoFactory(Factory):
    """
    """
    protocol = OnkyoProtocol
    m_pyhouse_obj = None
    m_device_obj = None

    def __init__(self, p_pyhouse_obj, p_device_obj):
        """ Set up the persistent Data.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_device_obj = p_device_obj

    def startedConnecting(self, p_connector):
        LOG.debug('Started to connect. {}'.format(PrettyFormatAny.form(p_connector, 'Connector', 180)))

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

    def _build_header(self):
        """
        """

    def _build_volume(self, p_yaml, p_queue_entry):
        """ Internally, volume is a percent 0 to 100
        My onkyo receiver uses hex 00 to 64 for the value.
        """
        l_zone = int(p_queue_entry.Zone)
        l_command = p_queue_entry.Command
        l_arg = '{:02X}'.format(int(p_queue_entry.Args))
        l_unit = p_yaml['UnitType']
        l_code = p_yaml['ControlCommands'][l_command][l_zone]
        l_ret = b'!' + str(l_unit).encode('utf-8') + l_code.encode('utf-8') + str(l_arg).encode('utf-8')
        return l_ret

    def _build_comand(self, p_queue_entry, p_device_obj):
        """
        Build '!1PWRQSTN' or similar command
        """
        # LOG.debug('Building:\n\t{}\n\t{}'.format(PrettyFormatAny.form(p_queue_entry, 'QueueEntry', 190), PrettyFormatAny.form(p_device_obj, 'Device', 190)))
        l_zone = int(p_queue_entry.Zone)
        l_command = p_queue_entry.Command
        l_args = p_queue_entry.Args
        l_yaml = p_device_obj._Yaml
        l_unit = l_yaml['UnitType']
        #
        if l_command == 'Volume':
            l_ret = self._build_volume(l_yaml, p_queue_entry)
            return l_ret
        # LOG.debug('Unit:{}'.format(l_unit))
        l_code = l_yaml['ControlCommands'][l_command][l_zone]
        # LOG.debug('Code:{}'.format(l_code))
        l_arg = l_yaml['Arguments'][l_command][l_args]
        # LOG.debug('Arg:{}'.format(l_arg))
        l_ret = b'!'
        l_ret += str(l_unit).encode('utf-8')
        l_ret += l_code.encode('utf-8')
        l_ret += l_arg.encode('utf-8')
        return l_ret

    def send_command(self, p_device_obj, p_queue_entry):
        """
        @param p_command: is the comand b"!1PWR01"
        Gthis will add the rest of the ethernet framework
        """
        if p_device_obj == None:
            LOG.error('Sending a command to None will never work!')
            return
        # LOG.debug(PrettyFormatAny.form(p_device_obj, 'Device', 190))
        l_cmd = self._build_comand(p_queue_entry, p_device_obj)
        l_cmd += b'\x1a\n\r'
        l_len = len(l_cmd)
        l_ret = b'ISCP' + \
                convert.int_2_bigend(16, 4) + \
                convert.int_2_bigend(l_len, 4) + \
                b'\x01' + \
                b'\x00\x00\x00' + \
                l_cmd
        # LOG.debug('Command {}'.format(l_ret))
        try:
            p_device_obj._Protocol.transport.write(l_ret)
            LOG.info('Send TCP command: {} to {}'.format(l_ret, p_device_obj.Name))
        except AttributeError as e_err:
            LOG.error("Tried to call send_command without a onkyo device configured.\n\tError:{}".format(e_err))


class OnkeoControl:
    """
    """

    def _get_endpoint(self, p_pyhouse_obj, p_device_obj):
        """
        """
        l_reactor = p_pyhouse_obj._Twisted.Reactor
        l_host = p_device_obj.Host
        l_port = p_device_obj.Port
        l_endpoint = TCP4ClientEndpoint(l_reactor, l_host, l_port)
        return l_endpoint

    def onkyo_start_connecting(self, p_pyhouse_obj, p_device_obj):
        """ Open connections to the various Onkyo devices we will communicate with.
        This will also publish a status message with controller info.

        @param p_device_obj: OnkyoDeviceInformation()
        """

        def cb_got_protocol(p_protocol, p_device_obj, p_status):
            p_device_obj._Protocol = p_protocol
            p_device_obj._isRunning = True
            p_status.Type = 'Connected'
            p_status.Connected = True
            p_status.ControllingNode = self.m_pyhouse_obj.Computer.Name
            l_topic = 'house/entertainment/onkyo/status'
            self.m_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, p_status)

        def eb_got_protocol(p_reason, p_device_obj, p_status):
            p_device_obj._Protocol = None
            p_device_obj._isRunning = False
            p_status.Type = 'UnConnected'
            p_status.Connected = False
            l_topic = 'house/entertainment/onkyo/status'
            self.m_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, p_status)
            LOG.debug('Got an error connecting to Onkyo device - {}'.format(p_reason))

        p_device_obj._Queue = Queue(32)
        l_status = OnkyoDeviceStatus()
        l_status.Family = 'onkyo'
        l_status.Model = p_device_obj.Model
        l_status.Node = p_pyhouse_obj.Computer.Name
        l_endpoint = self._get_endpoint(p_pyhouse_obj, p_device_obj)
        d_connector = l_endpoint.connect(OnkyoFactory(p_pyhouse_obj, p_device_obj))
        d_connector.addCallback(cb_got_protocol, p_device_obj, l_status)
        d_connector.addErrback(eb_got_protocol, p_device_obj, l_status)
        # self.m_device_lst.append(p_device_obj)

# ## END DBK
