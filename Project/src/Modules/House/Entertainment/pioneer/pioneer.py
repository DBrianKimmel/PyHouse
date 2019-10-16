"""
@name:      Modules/House/Entertainment/pioneer/pioneer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2019 by D. Brian Kimmel
@note:      Created on Jul 10, 2016
@license:   MIT License
@summary:

Control of pioneer home entertainment devices'.
First is an A/V receiver VSX-822-K.

Listen to Mqtt message to control device
==> pyhouse/<house name>/house/entertain/<device>/<function>

    <device> = receiver, tv, etc...
    <function> = control, status
    <value> = on, off, 0-100, zone#, input#

"""

__updated__ = '2019-10-15'
__version_info__ = (19, 10, 4)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.internet.error import ConnectionDone
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.conch.telnet import StatefulTelnetProtocol
from queue import Queue

#  Import PyMh files and modules.
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.Utilities import extract_tools
from Modules.House.Entertainment.entertainment_data import EntertainmentDeviceInformation, EntertainmentDeviceStatus
from Modules.House.Entertainment.entertainment import EntertainmentPluginInformation

from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Pioneer        ')

SECTION = 'pioneer'
DISCONNECT_TIMER = 30  # Seconds
CONFIG_NAME = 'pioneer'

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


class PioneerPluginInformation(EntertainmentPluginInformation):
    """
    """

    def __init__(self):
        super(PioneerPluginInformation, self).__init__()


class PioneerDeviceInformation(EntertainmentDeviceInformation):
    """
    """

    def __init__(self):
        super(PioneerDeviceInformation, self).__init__()
        self.CommandSet = None  # Command sets change over the years.
        self.RoomName = None
        self.Type = None
        self.Volume = None
        self._isControlling = False
        self._isRunning = False


class PioneerDeviceStatus(EntertainmentDeviceStatus):
    """
    The device family is part of the topic.
    """

    def __init__(self):
        super(PioneerDeviceStatus, self).__init__()


class MqttActions:
    """
    """

    m_transport = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _find_device(self, p_family, p_model):
        # l_pioneer = self.m_pyhouse_obj.House.Entertainment.Plugins['pioneer'].Devices
        l_devices = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices
        for l_device in l_devices.values():
            if l_device.Name.lower() == p_model.lower():
                LOG.info("found model - {} {}".format(p_family, p_model))
                return l_device
        LOG.error('No such model as {}'.format(p_model))
        return None

    def _get_power(self, p_message):
        """
        force power to be None, 'On' or 'Off'
        """
        l_ret = extract_tools.get_mqtt_field(p_message, 'Power')
        if l_ret == None:
            return l_ret
        if l_ret == 'On':
            return 'On'
        return 'Off'

    def _decode_control(self, _p_topic, p_message):
        """ Decode the message.
        As a side effect - control pioneer.

        @param p_message: is the payload used to control
        """
        LOG.debug('Decode-Control called:\n\tTopic:{}\n\tMessage:{}'.format(_p_topic, p_message))
        l_family = extract_tools.get_mqtt_field(p_message, 'Family')
        if l_family == None:
            l_family = 'pioneer'
        l_model = extract_tools.get_mqtt_field(p_message, 'Model')
        # l_device_obj = self._find_device(l_family, l_model)
        l_power = self._get_power(p_message)
        l_input = extract_tools.get_mqtt_field(p_message, 'Input')
        l_volume = extract_tools.get_mqtt_field(p_message, 'Volume')
        l_logmsg = '\tPioneer Control:\n\t\tDevice:{}-{}\n\t\tPower:{}\n\t\tVolume:{}\n\t\tInput:{}'.format(l_family, l_model, l_power, l_volume, l_input)
        #
        if l_power != None:
            l_logmsg += ' Turn power {} to {}.'.format(l_power, l_model)
            self._pioneer_power(l_family, l_model, l_power)
        #
        if l_input != None:
            l_logmsg += ' Turn input to {}.'.format(l_input)
            self._pioneer_input(l_family, l_model, l_input)
        #
        if l_volume != None:
            l_logmsg += ' Change volume {}.'.format(l_volume)
            self._pioneer_volume(l_family, l_model, l_volume)
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


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def dump_struct(self):
        """
        """
        l_entertain = self.m_pyhouse_obj.House.Entertainment
        l_pioneer = l_entertain.Plugins['pioneer']
        LOG.debug(PrettyFormatAny.form(l_entertain, 'Entertainment'))
        LOG.debug(PrettyFormatAny.form(l_entertain.Plugins, 'Plugins'))
        LOG.debug(PrettyFormatAny.form(l_pioneer, 'Pioneer'))
        LOG.debug(PrettyFormatAny.form(l_pioneer.Services, 'Pandora'))
        #
        for l_service in l_pioneer.Services.values():
            LOG.debug(PrettyFormatAny.form(l_service, 'Service'))
            if hasattr(l_service, 'Connection'):
                LOG.debug(PrettyFormatAny.form(l_service.Connection, 'Connection'))
            if hasattr(l_service, 'Host'):
                LOG.debug(PrettyFormatAny.form(l_service.Host, 'Host'))
            if hasattr(l_service, 'Access'):
                LOG.debug(PrettyFormatAny.form(l_service.Access, 'Access'))

    def _extract_one_device(self, p_config):
        """
        """
        # self.dump_struct()
        l_required = ['Name', 'Type', 'Host']
        l_obj = PioneerDeviceInformation()
        for l_key, l_value in p_config.items():
            if l_key == 'Host':
                l_obj.Host = self.m_config.extract_host_group(l_value)
            else:
                setattr(l_obj, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('Pioneer Yaml is missing an entry for "{}"'.format(l_key))
        return l_obj  # For testing.

    def _extract_all_devices(self, p_config):
        """
        """
        l_dict = {}
        for l_ix, l_value in enumerate(p_config):
            l_device = self._extract_one_device(l_value)
            l_dict[l_ix] = l_device
        return l_dict

    def _extract_all_pioneer(self, p_config, p_api):
        """
        """
        # self.dump_struct()
        l_required = ['Name']
        l_obj = PioneerPluginInformation()
        l_obj._Api = p_api
        l_old = self.m_pyhouse_obj.House.Entertainment.Plugins['pioneer']
        l_obj._Api = l_old._Api
        l_obj._Module = l_old._Module
        for l_key, l_value in p_config.items():
            if l_key == 'Device':
                l_devices = self._extract_all_devices(l_value)
                l_obj.Devices = l_devices
                l_obj.DeviceCount = len(l_devices)
            else:
                setattr(l_obj, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warn('Pioneer Yaml is missing an entry for "{}"'.format(l_key))
        return l_obj  # For testing.

    def load_yaml_config(self, p_api):
        """ Read the pioneer.yaml file.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj.House.Rooms = None
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Pioneer']
        except:
            LOG.warn('The config file does not start with "Pioneer:"')
            return None
        l_pioneer = self._extract_all_pioneer(l_yaml, p_api)
        self.m_pyhouse_obj.House.Entertainment.Plugins['pioneer'] = l_pioneer
        return l_pioneer  # for testing purposes


class PioneerControl:
    """
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _get_endpoint(self, p_device_obj):
        """
        """
        l_reactor = self.m_pyhouse_obj._Twisted.Reactor
        l_host = p_device_obj.Host.Name
        l_port = p_device_obj.Host.Port
        l_endpoint = TCP4ClientEndpoint(l_reactor, l_host, l_port)
        return l_endpoint

    def pioneer_start_connecting(self, p_device_obj):
        """ Open connections to the various Pioneer devices we will communicate with.
        This will also publish a status message with controller info.

        @param p_device_obj: PioneerDeviceInformation()
        """

        def cb_got_protocol(p_protocol, p_device_obj, p_status):
            p_device_obj._Protocol = p_protocol
            p_device_obj._isRunning = True
            p_status.Type = 'Connected'
            p_status.Connected = True
            p_status.ControllingNode = self.m_pyhouse_obj.Computer.Name
            l_topic = 'house/entertainment/pioneer/status'
            self.m_pyhouse_obj._Apis.Core.MqttApi.MqttPublish(l_topic, p_status)

        def eb_got_protocol(p_reason, p_device_obj, p_status):
            p_device_obj._Protocol = None
            p_device_obj._isRunning = False
            p_status.Type = 'UnConnected'
            p_status.Connected = False
            l_topic = 'house/entertainment/pioneer/status'
            self.m_pyhouse_obj._Apis.Core.MqttApi.MqttPublish(l_topic, p_status)
            LOG.debug('Got an error connecting to Pioneer device - {}'.format(p_reason))
            LOG.debug(PrettyFormatAny.form(p_device_obj, 'Device'))
            LOG.debug(PrettyFormatAny.form(p_device_obj.Host, 'Host'))

        p_device_obj._Queue = Queue(32)
        l_status = PioneerDeviceStatus()
        l_status.Family = 'pioneer'
        l_status.Model = p_device_obj.Model
        l_status.Node = self.m_pyhouse_obj.Computer.Name
        l_endpoint = self._get_endpoint(p_device_obj)
        p_device_obj._Endpoint = l_endpoint
        LOG.debug(PrettyFormatAny.form(l_endpoint, 'Endpoint'))
        d_connector = l_endpoint.connect(PioneerFactory(self.m_pyhouse_obj, p_device_obj))
        d_connector.addCallback(cb_got_protocol, p_device_obj, l_status)
        d_connector.addErrback(eb_got_protocol, p_device_obj, l_status)
        p_device_obj._Connector = d_connector
        # self.m_device_lst.append(p_device_obj)


class PioneerProtocol(StatefulTelnetProtocol):
    """ There is an instance of this for every pioneer device that we are controlling.

    Each protocol instance is mapped to a Pioneer Device (and visa  versa)
    """

    m_pyhouse_obj = None
    m_pioneer_device_obj = None

    def __init__(self, p_pyhouse_obj, p_device_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_pioneer_device_obj = p_device_obj
        LOG.debug('Factory init for {}'.format(PrettyFormatAny.form(self.m_pioneer_device_obj, 'PioneerFactory-')))
        LOG.info('PioneerProtocol Init - Version:{}'.format(__version__))

    def _get_status(self):
        LOG.debug('Get Status')
        self.send_command(self.m_pioneer_device_obj, CONTROL_COMMANDS['PowerQuery'])  # Query Power
        self.send_command(self.m_pioneer_device_obj, CONTROL_COMMANDS['MuteQuery'])
        self.send_command(self.m_pioneer_device_obj, CONTROL_COMMANDS['VolumeQuery'])
        self.send_command(self.m_pioneer_device_obj, CONTROL_COMMANDS['FunctionQuery'])

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
        self._get_status()

    def connectionLost(self, reason=ConnectionDone):
        """ TearDown
        """
        Protocol.connectionLost(self, reason=reason)
        LOG.warn('Lost connection.\n\tReason:{}'.format(reason))


class PioneerClient(PioneerProtocol):
    """
    """

    m_pyhouse_obj = None
    m_pioneer_device_obj = None

    def __init__(self, p_pyhouse_obj, p_device_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_pioneer_device_obj = p_device_obj

    def send_command(self, p_device_obj, p_command):
        LOG.info('Send command {}'.format(p_command))
        try:
            l_host = p_device_obj.Host.Name
            p_device_obj._Transport.write(p_command + b'\r\n')
            LOG.info('Send TCP command:{} to {}'.format(p_command, l_host))
        except AttributeError as e_err:
            LOG.error("Tried to call send_command without a pioneer device configured.\n\tError:{}".format(e_err))


class PioneerFactory(ClientFactory):
    """
    This is a factory which produces protocols.
    By default, buildProtocol will create a protocol of the class given in self.protocol.
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj, p_device_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_pioneer_device_obj = p_device_obj
        LOG.debug(PrettyFormatAny.form(p_device_obj, 'Pioneer Device'))
        LOG.info('PioneerFactory Init - Version:{}'.format(__version__))

    def startedConnecting(self, p_connector):
        """ *1
        Called when we are connecting to the device.
        Provides access to the connector.
        """
        LOG.debug(PrettyFormatAny.form(p_connector, 'Connector'))
        self.m_pioneer_device_obj._Connector = p_connector

    def buildProtocol(self, p_addr):
        """ *2
        Create an instance of PioneerProtocol.

        @param p_addr: an object implementing twisted.internet.interfaces.IAddress
        @return:
        """
        self.protocol = PioneerProtocol(self.m_pyhouse_obj, self.m_pioneer_device_obj)
        l_client = PioneerClient(self.m_pyhouse_obj, self.m_pioneer_device_obj)
        LOG.info('BuildProtocol\n\tAddr = {};\n\tClient:{}'.format(p_addr, l_client))
        return l_client

    def clientConnectionLost(self, p_connector, p_reason):
        LOG.warn('Lost connection.\n\tReason:{}'.format(p_reason))
        ClientFactory.clientConnectionLost(self, p_connector, p_reason)

    def clientConnectionFailed(self, p_connector, p_reason):
        LOG.error('Connection failed.\n\tReason:{}'.format(p_reason))
        ClientFactory.clientConnectionFailed(self, p_connector, p_reason)

    def connectionLost(self, p_reason):
        """ This is required. """
        LOG.error('ConnectionLost.\n\tReason: {}'.format(p_reason))

    def makeConnection(self, p_transport):
        """ This is required. """
        LOG.warn('makeConnection - Transport: {}'.format(p_transport))


class Api(MqttActions, PioneerClient):
    """This interfaces to all of PyHouse.
    """

    m_local_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info("Api Initialized - Version:{}".format(__version__))

    def _pioneer_power(self, p_family, p_model, p_power):
        """
        @param p_power: 'On' or 'Off'
        """
        # Get the device_obj to control
        l_device_obj = self._find_device(p_family, p_model)
        if p_power == 'On':
            self.send_command(l_device_obj, CONTROL_COMMANDS['PowerOn'])  # Query Power
        else:
            pass
        LOG.debug('Change Power to {}'.format(p_power))

    def _pioneer_volume(self, p_family, p_model, p_volume):
        """
        @param p_volume: 'VolumeUp1', 'VolumeUp5', 'VolumeDown1' or 'VolumeDown5'
        """
        LOG.debug('Volume:{}'.format(p_volume))
        l_device_obj = self._find_device(p_family, p_model)
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

    def _pioneer_input(self, p_family, p_model, p_input):
        """
        @param p_input: Channel Code
        """
        l_device_obj = self._find_device(p_family, p_model)
        self.send_command(l_device_obj, b'01FN')
        LOG.debug('Change input channel to {}'.format(p_input))

    def LoadConfig(self):
        """ Read the XML for all Pioneer devices.
        """
        self.m_local_config.load_yaml_config(self)
        LOG.info("Loaded Pioneer Device(s) - Version:{}".format(__version__))

    def Start(self):
        """ Start all the Pioneer factories if we have any Pioneer devices.
        """
        LOG.info('Api Start...')
        l_count = 0
        l_devices = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices
        for l_device_obj in l_devices.values():
            # # Read Yaml here
            LOG.debug(PrettyFormatAny.form(l_device_obj, 'Device'))
            l_count += 1
            if l_device_obj._isRunning:
                LOG.info('Pioneer device {} is already running.'.format(l_device_obj.Name))
                continue
            PioneerControl(self.m_pyhouse_obj).pioneer_start_connecting(l_device_obj)
        LOG.info("Started {} Pioneer device(s).".format(l_count))

    def SaveConfig(self):
        LOG.info("Saved Pioneer Config.")

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
