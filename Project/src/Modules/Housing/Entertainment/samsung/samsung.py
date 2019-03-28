"""
-*- test-case-name: /home/briank/PyHouse/src/Modules/Entertainment/samsung.py -*-

@name:      src.Modules.Housing.Entertainment.samsung.samsung.py
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

__updated__ = '2019-03-28'
__version_info__ = (19, 3, 0)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
import base64
import xml.etree.ElementTree as ET
from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import clientFromString
from twisted.application.internet import ClientService
from twisted.internet import error

#  Import PyMh files and modules.
from Modules.Core.Utilities import extract_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
# from Modules.Core.Utilities.convert import long_to_str
from Modules.Housing.Entertainment.entertainment_data import EntertainmentDeviceData
from Modules.Housing.Entertainment.entertainment_xml import XML as entertainmentXML

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Samsung        ')

SAMSUNG_ADDRESS = '192.168.1.100'
SAMSUNG_PORT = 55000
SAMSUNG_PORT2 = 8001
SECTION = 'samsung'


class SamsungDeviceData(EntertainmentDeviceData):

    def __init__(self):
        super(SamsungDeviceData, self).__init__()
        self.IPv4 = None
        self.Model = None
        self.Port = None
        self.RoomName = None
        self.RoomUUID = None
        self.Type = None
        self.Volume = None


class XML:
    """
    """

    @staticmethod
    def _read_device(p_xml):
        l_obj = SamsungDeviceData()
        l_device = entertainmentXML().read_entertainment_device(p_xml, l_obj)
        return l_device

    @staticmethod
    def _write_device(p_obj):
        l_xml = entertainmentXML().write_entertainment_device(p_obj)
        return l_xml

    @staticmethod
    def read_samsung_section_xml(p_pyhouse_obj):
        l_xml = XmlConfigTools.find_section(p_pyhouse_obj, 'HouseDivision/EntertainmentSection/SamsungSection')
        l_entertain_obj = p_pyhouse_obj.House.Entertainment
        l_plugin_obj = l_entertain_obj.Plugins[SECTION]
        l_plugin_obj.Name = SECTION
        l_plugin_obj.Active = PutGetXML.get_bool_from_xml(l_xml, 'Active')
        l_plugin_obj.DeviceCount = l_count = 0
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
                l_plugin_obj.DeviceCount = l_count
        except AttributeError as e_err:
            LOG.error('ERROR if getting {} Device Data - {}'.format(SECTION, e_err))
        p_pyhouse_obj.House.Entertainment.Plugins[SECTION] = l_plugin_obj
        LOG.info('Loaded {} {} Device(s).'.format(l_count, SECTION))
        return l_plugin_obj

    @staticmethod
    def write_samsung_section_xml(p_pyhouse_obj):
        """
        """
        l_entertain_obj = p_pyhouse_obj.House.Entertainment
        l_plugin_obj = l_entertain_obj.Plugins[SECTION]
        l_active = l_plugin_obj.Active
        l_xml = ET.Element('SamsungSection', attrib={'Active': str(l_active)})
        l_count = 0
        for l_obj in l_plugin_obj.Devices.values():
            l_dev_xml = XML._write_device(l_obj)
            l_xml.append(l_dev_xml)
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

    def _decode_control(self, p_topic, p_message):
        """ Decode the message.
        As a side effect - control samsung.
        """
        l_logmsg = '\tControl: '
        l_control = extract_tools.get_mqtt_field(p_message, 'Control')
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
        LOG.debug('data rxed. {}'.format(data))
        Protocol.dataReceived(self, data)

    def connectionMade(self, data):
        LOG.debug('Connection Made. {}'.format(data))
        Protocol.connectionMade(self)

    def connectionLost(self, reason=error.ConnectionDone):
        LOG.debug('Connection Lost. {}'.format(reason))
        Protocol.connectionLost(self, reason=reason)


class SamsungClient(SamsungProtocol):
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
        l_reactor = self.m_pyhouse_obj.Twisted.Reactor
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

            def cb_connectedNow(OnkyoClient):
                LOG.debug('Connected Now')
                OnkyoClient.send_command('1PWRQSTN')

            def eb_failed(fail_reason):
                LOG.warn("initial Samsung connection failed: {}".format(fail_reason))
                l_ReconnectingService.stopService()

            waitForConnection.addCallbacks(cb_connectedNow, eb_failed)
            l_ReconnectingService.startService()
            p_device_obj._Endpoint = l_endpoint
            p_device_obj._Factory = l_factory
            p_device_obj._isRunning = True
            LOG.info("Started Samsung - Host:{}; Port:{}".format(l_host, l_port))
        except Exception as e_err:
            LOG.error('Error found: {}'.format(e_err))
        pass


class API(Connecting):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadXml(self, p_pyhouse_obj):
        LOG.info('XML Loading')
        # l_samsung_obj = SamsungDeviceData()
        p_pyhouse_obj.House.Entertainment.Plugins[SECTION] = SamsungDeviceData()  # Clear before loading
        l_samsung_obj = XML.read_samsung_section_xml(p_pyhouse_obj)
        p_pyhouse_obj.House.Entertainment.Plugins[SECTION] = l_samsung_obj
        LOG.info('Loaded XML')

    def Start(self):
        LOG.info("Starting.")
        l_count = 0
        for l_samsung_device_obj in self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices.values():
            l_count += 1
            if not l_samsung_device_obj.Active:
                continue
            self.connect_samsung(l_samsung_device_obj)
        LOG.info("Started {} Samsung Devices.".format(l_count))

    def SaveXml(self, p_xml):
        # LOG.info("Saving XML.")
        l_xml = XML().write_samsung_section_xml(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Saved XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
