"""
@name:      Modules/House/Entertainment/samsung/samsung.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2019 by D. Brian Kimmel
@note:      Created on Jul 11, 2016
@license:   MIT License
@summary:



src     = '192.168.100.25'      # ip of remote (Indigo Server)
mac     = '00-15-17-F3-C0-B8'     # mac of remote
remote  = 'Indigo'                    # remote name
dst     = '192.168.100.51'      # ip of tv
app     = 'python'              # iphone..iapp.samsung
tv      = 'UE32ES6800'          # iphone.UE32ES6800.iapp.samsung

def push(key):
  new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  new.connect((dst, 55000))
  msg = chr(0x64) + chr(0x00) +\
        chr(len(base64.b64encode(src)))    + chr(0x00) + base64.b64encode(src) +\
        chr(len(base64.b64encode(mac)))    + chr(0x00) + base64.b64encode(mac) +\
        chr(len(base64.b64encode(remote))) + chr(0x00) + base64.b64encode(remote)
  pkt = chr(0x00) +\
        chr(len(app)) + chr(0x00) + app +\
        chr(len(msg)) + chr(0x00) + msg
  new.send(pkt)
  msg = chr(0x00) + chr(0x00) + chr(0x00) +\
        chr(len(base64.b64encode(key))) + chr(0x00) + base64.b64encode(key)
  pkt = chr(0x00) +\
        chr(len(tv))  + chr(0x00) + tv +\
        chr(len(msg)) + chr(0x00) + msg
  new.send(pkt)
  new.close()
  time.sleep(0.1)

while True:
  push("KEY_POWEROFF")
  break




    http://sc0ty.pl/2012/02/samsung-tv-network-remote-control-protocol/
    https://gist.github.com/danielfaust/998441
    https://github.com/Bntdumas/SamsungIPRemote
    https://github.com/kyleaa/homebridge-samsungtv2016

"""

__updated__ = '2019-12-23'
__version_info__ = (19, 11, 2)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
import base64
from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import clientFromString
from twisted.application.internet import ClientService
from twisted.internet import error

#  Import PyMh files and modules.
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.Utilities import extract_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.House.Entertainment.entertainment_data import EntertainmentDeviceInformation, EntertainmentPluginInformation

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Samsung        ')

SAMSUNG_ADDRESS = '192.168.1.100'
SAMSUNG_PORT = 55000
SAMSUNG_PORT2 = 8001
CONFIG_NAME = 'samsung'


class SamsungPluginInformation(EntertainmentPluginInformation):
    """
    """

    def __init__(self):
        super(SamsungPluginInformation, self).__init__()


class SamsungDeviceInformation(EntertainmentDeviceInformation):
    """ A superet that contains some samsung specific fields
    """

    def __init__(self):
        super(SamsungDeviceInformation, self).__init__()
        self.Room = None
        self.Type = None
        self.Volume = None


class SamsungDeviceData(EntertainmentDeviceInformation):

    def __init__(self):
        super(SamsungDeviceData, self).__init__()
        self.IPv4 = None
        self.Model = None
        self.Port = None
        self.Room = None
        self.Type = None
        self.Volume = None


class MqttActions:
    """
    """

    m_api = None
    m_transport = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _decode_control(self, p_topic, p_message):
        """ Decode the message.
        As a side effect - control samsung.
        """
        l_logmsg = '\tControl: '
        l_control = extract_tools.get_mqtt_field(p_message, 'Control')
        if l_control == 'On':
            l_logmsg += ' Turn On '
            self.m_api.Start()
        elif l_control == 'Off':
            l_logmsg += ' Turn Off '
            self.m_api.Stop()

        elif l_control == 'VolUp1':
            l_logmsg += ' Volume Up 1 '
        else:
            l_logmsg += ' Unknown samsung Control Message {} {}'.format(p_topic, p_message)
        return l_logmsg

    def decode(self, p_msg):
        """ Decode the Mqtt message
        ==> pyhouse/<house name>/entertainment/samsung/<type>/<Name>/...
        <type> = ?
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        p_msg.LogMessage += p_msg.Payload
        if l_topic[0] == 'control':
            p_msg.LogMessage += '\tSamsung: {}\n'.format(self._decode_control(p_msg.Topic, p_msg.Payload))
        else:
            p_msg.LogMessage += '\tUnknown Samsung sub-topic {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Entertainment msg', 160))


class SamsungProtocol(Protocol):
    """
    """

    def dataReceived(self, data):
        LOG.debug('data rxed. {}'.format(data))
        Protocol.dataReceived(self, data)

    def connectionMade(self, data):
        LOG.debug('Connection Made. {}'.format(data))
        Protocol.connectionMade(self)

    def connectionLost(self, reason=error.ConnectionDone):
        LOG.debug('Connection Lost. {}'.format(reason))
        Protocol.connectionLost(self, reason=reason)


class SamsungClient:
    """
    """

    def __init__(self, p_pyhouse_obj, _p_device_obj, _p_clientID=None):
        """
        At this point all config has been read in and Set-up
        """
        self.m_pyhouse_obj = p_pyhouse_obj


class Commands:
    """
    """

    def __init__(self, config):
        if not config["port"]:
            config["port"] = 55000
        """Make a new connection."""
        # self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if config["timeout"]:
            self.connection.settimeout(config["timeout"])
        self.connection.connect((config["host"], config["port"]))
        payload = b"\x64\x00" \
                  +self._serialize_string(config["description"]) \
                  +self._serialize_string(config["id"]) \
                  +self._serialize_string(config["name"])
        packet = b"\x00\x00\x00" + self._serialize_string(payload, True)
        LOG.info("Sending handshake.")
        self.connection.send(packet)
        self._read_response(True)

    def __enter__(self):
        return self

    # def __exit__(self, type, value, traceback):
    #    self.close()

    def close(self):
        """Close the connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            LOG.debug("Connection closed.")

    def control(self, key):
        """Send a control command."""
        if not self.connection:
            pass
        payload = b"\x00\x00\x00" + self._serialize_string(key)
        packet = b"\x00\x00\x00" + self._serialize_string(payload, True)
        LOG.info("Sending control command: %s", key)
        self.connection.send(packet)
        self._read_response()
        # time.sleep(self._key_interval)

    _key_interval = 0.2

    def _read_response(self, first_time=False):
        header = self.connection.recv(3)
        tv_name_len = int.from_bytes(header[1:3], byteorder="little")
        tv_name = self.connection.recv(tv_name_len)
        if first_time:
            LOG.debug("Connected to '%s'.", tv_name.decode())
        response_len = int.from_bytes(self.connection.recv(2), byteorder="little")
        response = self.connection.recv(response_len)
        if len(response) == 0:
            self.close()
        if response == b"\x64\x00\x01\x00":
            LOG.debug("Access granted.")
            return
        elif response == b"\x64\x00\x00\x00":
            pass
        elif response[0:1] == b"\x0a":
            if first_time:
                LOG.warning("Waiting for authorization...")
            return self._read_response()
        elif response[0:1] == b"\x65":
            LOG.warning("Authorization cancelled.")
        elif response == b"\x00\x00\x00\x00":
            LOG.debug("Control accepted.")
            return

    @staticmethod
    def _serialize_string(p_string, raw=False):
        if isinstance(p_string, str):
            p_string = str.encode(p_string)
        if not raw:
            p_string = base64.b64encode(p_string)
        return bytes([len(p_string)]) + b"\x00" + p_string


class Connecting:

    def connect_samsung(self, p_device_obj):

        def cb_connectedNow(SamsungClient):
            LOG.debug('Connected Now')
            SamsungClient.send_command('1PWRQSTN')

        def eb_failed(fail_reason):
            LOG.warning("initial Samsung connection failed: {}".format(fail_reason))
            l_ReconnectingService.stopService()

        l_reactor = self.m_pyhouse_obj._Twisted.Reactor
        try:
            # l_host = convert.long_to_str(p_device_obj.IPv4)
            l_host = 'samsung-tv'
            l_port = p_device_obj.Port
            l_endpoint_str = 'tcp:{}:port={}'.format(l_host, l_port)
            l_endpoint = clientFromString(l_reactor, l_endpoint_str)
            l_factory = Factory.forProtocol(SamsungProtocol)
            l_ReconnectingService = ClientService(l_endpoint, l_factory)
            l_ReconnectingService.setName('Samsung ')
            waitForConnection = l_ReconnectingService.whenConnected(failAfterFailures=1)
            LOG.debug('Endpoint: {}'.format(l_endpoint_str))
            LOG.debug('{}'.format(PrettyFormatAny.form(l_endpoint, 'Endpoint', 190)))
            LOG.debug('{}'.format(PrettyFormatAny.form(l_factory, 'Factory', 190)))
            LOG.debug('{}'.format(PrettyFormatAny.form(l_ReconnectingService, 'ReconnectService', 190)))

            waitForConnection.addCallbacks(cb_connectedNow, eb_failed)
            l_ReconnectingService.startService()
            p_device_obj._Endpoint = l_endpoint
            p_device_obj._Factory = l_factory
            p_device_obj._isRunning = True
            LOG.info("Started Samsung - Host:{}; Port:{}".format(l_host, l_port))
        except Exception as e_err:
            LOG.error('Error found: {}'.format(e_err))
        pass


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
        l_entertain = self.m_pyhouse_obj.House.Entertainment['samsung']
        LOG.debug(PrettyFormatAny.form(l_entertain, 'Entertainment'))

        return

        for _l_key, l_service in l_samsung.Services.items():
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
        l_obj = SamsungDeviceInformation()
        for l_key, l_value in p_config.items():
            if l_key == 'Host':
                l_obj.Host = self.m_config.extract_host_group(l_value)
            else:
                setattr(l_obj, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('samsung Yaml is missing an entry for "{}"'.format(l_key))
        return l_obj  # For testing.

    def _extract_all_devices(self, p_config):
        """
        """
        l_dict = {}
        for l_ix, l_value in enumerate(p_config):
            l_device = self._extract_one_device(l_value)
            l_dict[l_ix] = l_device
        return l_dict

    def _extract_all_samsung(self, p_config, p_api):
        """
        """
        # self.dump_struct()
        l_required = ['Name']
        l_obj = SamsungPluginInformation()
        l_obj._Api = p_api
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
                LOG.warning('samsung Yaml is missing an entry for "{}"'.format(l_key))
        return l_obj  # For testing.

    def load_yaml_config(self, p_api):
        """ Read the samsung.yaml file.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        self.m_pyhouse_obj.House.Entertainment['samsung'] = None
        l_yaml = self.m_config.read_config(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Samsung']
        except:
            LOG.warning('The config file does not start with "Samsung:"')
            return None
        l_samsung = self._extract_all_samsung(l_yaml, p_api)
        self.m_pyhouse_obj.House.Entertainment['samsung'] = l_samsung
        # self.dump_struct()
        return l_samsung  # for testing purposes


class Api(Connecting):

    m_pyhouse_obj = None
    m_local_config = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self):
        self.m_local_config.load_yaml_config(self)
        LOG.info('Loaded Config')

    def Start(self):
        LOG.info("Starting.")
        l_count = 0
        for l_samsung_device_obj in self.m_pyhouse_obj.House.Entertainment['samsung'].Devices.values():
            l_count += 1
            # if not l_samsung_device_obj.Active:
            #    continue
            self.connect_samsung(l_samsung_device_obj)
        LOG.info("Started {} Samsung Devices.".format(l_count))

    def SaveConfig(self):
        # LOG.info("Saving XML.")
        # l_xml = XML().write_samsung_section_xml(self.m_pyhouse_obj)
        # p_xml.append(l_xml)
        LOG.info("Saved XML.")

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
