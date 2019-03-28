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

__updated__ = '2019-03-28'
__version_info__ = (19, 3, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.error import ConnectionDone
from twisted.internet.endpoints import clientFromString
from twisted.application.internet import ClientService

#  Import PyMh files and modules.
from Modules.Core.Utilities import extract_tools, convert
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Onkyo          ')

SECTION = 'onkyo'

# See https://tylerwatt12.com/vsx-822k-telnet-interface/
CONTROL_COMMANDS = {
    'PowerQuery':       b'?P',
    'PowerOn':          b'PN',
    'PowerOff':         b'PF',
    'VolumeQuery':      b'?V',
    'VolumeUp':         b'VU',
    'VolumeDown':       b'VD',
    'MuteQuery':        b'?M',
    'FunctionQuery':    b'?F',
    'FunctionPandora':  b'01FN'
    }


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _decode_control(self, _p_topic, p_message):
        """ Decode the message.
        As a side effect - control pioneer.

        @param p_message: is the payload used to control
        """
        LOG.debug('Decode-Control called:\n\tTopic:{}\n\tMessage:{}'.format(_p_topic, p_message))
        l_family = extract_tools.get_mqtt_field(p_message, 'Family')
        l_device = extract_tools.get_mqtt_field(p_message, 'Device')
        l_input = extract_tools.get_mqtt_field(p_message, 'Input')
        l_power = extract_tools.get_mqtt_field(p_message, 'Power')
        l_volume = extract_tools.get_mqtt_field(p_message, 'Volume')
        l_zone = extract_tools.get_mqtt_field(p_message, 'Zone')
        l_logmsg = '\tPioneer Control:\n\t\tDevice:{}-{}\n\t\tPower:{}\n\t\tVolume:{}\n\t\tInput:{}'.format(l_family, l_device, l_power, l_volume, l_input)
        #
        if l_input != None:
            l_logmsg += ' Turn input to {}.'.format(l_input)
            self._control_input(l_family, l_device, l_input)
        #
        if l_power != None:
            l_logmsg += ' Turn power {} to {}.'.format(l_power, l_device)
            self._control_power(l_family, l_device, l_power)
        #
        if l_volume != None:
            l_logmsg += ' Change volume {}.'.format(l_volume)
            self._control_volume(l_family, l_device, l_volume)
        #
        if l_zone != None:
            l_logmsg += ' Turn Zone to {}.'.format(l_zone)
            self._control_zone(l_family, l_device, l_zone)
        #
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
        elif p_topic[0].lower() == 'status':
            pass
        else:
            l_logmsg += '\tUnknown Pioneer sub-topic: {}  Message: {}'.format(p_topic, PrettyFormatAny.form(p_message, 'Entertainment msg', 160))
        return l_logmsg


class OnkyoProtocol(Protocol):
    """
    """

    def dataReceived(self, p_data):
        Protocol.dataReceived(self, p_data)
        LOG.info('Data Received.\n\tData:{}'.format(p_data))

    def connectionMade(self):
        """
        Called when a connection is made.

        This may be considered the initializer of the protocol, because
        it is called when the connection is completed.  For clients,
        this is called once the connection to the server has been
        established; for servers, this is called after an accept() call
        stops blocking and a socket has been received.  If you need to
        send any greeting or initial message, do it here.
        """
        Protocol.connectionMade(self)
        LOG.info('Connection Made')
        # OnkyoClient().send_command(p_device_obj, '1PWRQSTN')

    def connectionLost(self, reason=ConnectionDone):
        Protocol.connectionLost(self, reason=reason)
        LOG.warn('Lost connection.\n\tReason:{}'.format(reason))


class OnkyoClient:
    """
    """

    def send_command(self, p_device_obj, p_command):
        """
        @param p_command: is the comaand "!1PWR01"
        Gthis will add the rest of the ethernet framework
        """
        LOG.info('Send command {}'.format(p_command))
        l_command = b'IPCS' + b'/00/00/00/10' + b'/00/00/00/08' + b'/01' + b'/00/00/00' + p_command + b'/0d'
        try:
            l_host = p_device_obj._Connector.host
            p_device_obj._Transport.write(l_command)
            LOG.info('Send TCP command:{} to {}'.format(p_command, l_host))
        except AttributeError as e_err:
            LOG.error("Tried to call send_command without a onkyp device configured.\n\tError:{}".format(e_err))


class Connecting:

    def connect_onkyo(self, p_device_obj):
        """
        """
        l_reactor = self.m_pyhouse_obj.Twisted.Reactor
        try:
            # l_host = convert.long_to_str(p_device_obj.IPv4)
            l_host = 'onkyo'
            l_port = p_device_obj.Port
            l_endpoint_str = 'tcp:{}:port={}'.format(l_host, l_port)
            l_endpoint = clientFromString(l_reactor, l_endpoint_str)
            l_factory = Factory.forProtocol(OnkyoProtocol)
            l_ReconnectingService = ClientService(l_endpoint, l_factory)
            l_ReconnectingService.setName('Onkyo ')
            LOG.debug('Endpoint: {}'.format(l_endpoint_str))
            # LOG.debug('{}'.format(PrettyFormatAny.form(l_endpoint, 'Endpoint', 190)))
            # LOG.debug('{}'.format(PrettyFormatAny.form(l_factory, 'Factory', 190)))
            # LOG.debug('{}'.format(PrettyFormatAny.form(l_ReconnectingService, 'ReconnectService', 190)))

            waitForConnection = l_ReconnectingService.whenConnected(failAfterFailures=1)

            def cb_connectedNow(OnkyoClient):
                LOG.debug('Connected Now')
                # OnkyoClient().send_command(p_device_obj, '1PWRQSTN')

            def eb_failed(fail_reason):
                LOG.warn("initial Onkyo connection failed: {}".format(fail_reason))
                # now you should stop the service and report the error upwards

            waitForConnection.addCallbacks(cb_connectedNow, eb_failed)
            l_ReconnectingService.startService()
            p_device_obj._Endpoint = l_endpoint
            p_device_obj._Factory = l_factory
            p_device_obj._isRunning = True
            LOG.info("Started Onkyo - Host:{}; Port:{}".format(l_host, l_port))
        except Exception as e_err:
            LOG.error('Error found: {}'.format(e_err))


class API(Connecting, MqttActions):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadXml(self, p_pyhouse_obj):
        """ Read the XML for all Onkyo devices.
        """
        # l_onkyo_obj = XML.read_onkyo_section_xml(p_pyhouse_obj)
        l_onkyo_obj = p_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        LOG.info("Loaded Onkyo XML")
        return l_onkyo_obj

    def Start(self):
        """ Start all the Onkyo factories if we have any Onkyo devices.

        We have one or more Onkyo devices in this house to use/control.
        Connect to all of them.

        EntertainmentDeviceData()

        endpoint 'tcp:192.168.1.120:60128'
        """
        l_count = 0
        l_onkyo = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        # LOG.info(PrettyFormatAny.form(l_onkyo, 'onkyo.Start() Plugins'))
        for l_onkyo_obj in l_onkyo.Devices.values():
            LOG.info(PrettyFormatAny.form(l_onkyo_obj, 'Device'))
            if not l_onkyo_obj.Active:
                continue
            self.connect_onkyo(l_onkyo_obj)
            l_count += 1
        LOG.info("Started {} Onkyo devices".format(l_count))

    def SaveXml(self, p_xml):
        # LOG.info("Saved Onkyo XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopped.")

    def _change_input(self, p_family, p_device, p_input):
        """
        @param p_input: Channel Code
        """
        l_device_obj = self._find_device(p_family, p_device)
        self.send_command(l_device_obj, b'01FN')
        LOG.debug('Change input channel to {}'.format(p_input))

    def _change_power(self, p_family, p_device, p_power):
        """
        @param p_power: 'On' or 'Off'
        """
        # Get the device_obj to control
        l_device_obj = self._find_device(p_family, p_device)
        if p_power == 'On':
            self.send_command(l_device_obj, CONTROL_COMMANDS['PowerOn'])  # Query Power
        else:
            pass
        LOG.debug('Change Power to {}'.format(p_power))

    def _change_volume(self, p_family, p_device, p_volume):
        """
        @param p_volume: 'VolumeUp1', 'VolumeUp5', 'VolumeDown1' or 'VolumeDown5'
        """
        LOG.debug('Volume:{}'.format(p_volume))
        l_device_obj = self._find_device(p_family, p_device)
        if p_volume == 'VolumeUp1':
            self.send_command(l_device_obj, CONTROL_COMMANDS['VolumeUp'])
        elif p_volume == 'VolumeUp5':
            self.send_command(l_device_obj, b'VU')
            self.send_command(l_device_obj, CONTROL_COMMANDS['VolumeUp'])
            self.send_command(l_device_obj, CONTROL_COMMANDS['VolumeUp'])
            self.send_command(l_device_obj, CONTROL_COMMANDS['VolumeUp'])
            self.send_command(l_device_obj, CONTROL_COMMANDS['VolumeUp'])
        elif p_volume == 'VolumeDown1':
            self.send_command(l_device_obj, CONTROL_COMMANDS['VolumeDown'])
        elif p_volume == 'VolumeDown5':
            self.send_command(l_device_obj, CONTROL_COMMANDS['VolumeDown'])
            self.send_command(l_device_obj, CONTROL_COMMANDS['VolumeDown'])
            self.send_command(l_device_obj, CONTROL_COMMANDS['VolumeDown'])
            self.send_command(l_device_obj, CONTROL_COMMANDS['VolumeDown'])
            self.send_command(l_device_obj, CONTROL_COMMANDS['VolumeDown'])
        else:
            pass
        LOG.debug('Change Volume to {}'.format(p_volume))

    def _change_zone(self, p_family, p_device, p_input):
        """
        @param p_input: Channel Code
        """
        l_device_obj = self._find_device(p_family, p_device)
        self.send_command(l_device_obj, b'01FN')
        LOG.debug('Change input channel to {}'.format(p_input))

# ## END DBK
