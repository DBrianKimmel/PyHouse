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

__updated__ = '2019-01-24'
__version_info__ = (19, 1, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet.error import ConnectionDone
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Housing.Entertainment.entertainment_data import EntertainmentDeviceData
from Modules.Housing.Entertainment.entertainment_xml import XML as entertainmentXML
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Onkyo          ')

DEFAULT_EISCP_IPV4 = '192.168.1.138'
DEFAULT_EISCP_PORT = 60128
SECTION = 'onkyo'

DISCONNECT_TIMER = 30  # Seconds
XML_PATH = 'HouseDivision/EntertainmentSection/OnkyoSection'

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
        l_input = self._get_field(p_message, 'Input')
        l_power = self._get_field(p_message, 'Power')
        l_volume = self._get_field(p_message, 'Volume')
        l_zone = self._get_field(p_message, 'Zone')
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
        self.m_onkyo_obj._Transport = p_transport


class Utility(object):
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

    def LoadXml(self, p_pyhouse_obj):
        """ Read the XML for all Onkyo devices.
        """
        # l_onkyo_obj = XML.read_onkyo_section_xml(p_pyhouse_obj)
        l_onkyo_obj = p_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        LOG.info("Loaded Onkyo XML")
        return l_onkyo_obj

    def Start(self):
        """ Start all the Onkyo factories if we have any Onkyo devices.
        """
        l_count = 0
        l_mfg = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        LOG.info(PrettyFormatAny.form(l_mfg, 'onkyo.Start() Plugins'))
        for l_onkyo_obj in l_mfg.Devices.values():
            if not l_onkyo_obj.Active:
                continue
            try:
                l_host = l_onkyo_obj.IPv4
                l_port = l_onkyo_obj.Port
                l_onkyo_obj._Factory = OnkyoFactory(self.m_pyhouse_obj, l_onkyo_obj)
                _l_connector = self.m_pyhouse_obj.Twisted.Reactor.connectTCP(l_host, l_port, l_onkyo_obj._Factory)
                LOG.info("Started Onkyo {} {}".format(l_host, l_port))
            except Exception as e_err:
                LOG.error('Error found: {}'.format(e_err))
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
