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


"""

__updated__ = '2019-03-06'
__version_info__ = (18, 10, 0)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from twisted.internet import error

#  Import PyMh files and modules.
from Modules.Core.Utilities import extract_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
from Modules.Housing.Entertainment.entertainment_data import EntertainmentDeviceData
from Modules.Housing.Entertainment.entertainment_xml import XML as entertainmentXML

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Samsung        ')

SAMSUNG_ADDRESS = '192.168.1.103'
SAMSUNG_PORT = 55000
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
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadXml(self, p_pyhouse_obj):
        LOG.info('XML Loading')
        # l_samsung_obj = SamsungDeviceData()
        p_pyhouse_obj.House.Entertainment.Plugins[SECTION] = SamsungDeviceData()  # Clear before loading
        l_samsung_obj = XML.read_samsung_section_xml(p_pyhouse_obj)
        p_pyhouse_obj.House.Entertainment.Plugins[SECTION] = l_samsung_obj
        # l_host = SAMSUNG_ADDRESS
        # l_port = SAMSUNG_PORT
        # l_samsung_obj._Factory = SamsungFactory(p_pyhouse_obj, l_samsung_obj)
        # _l_connector = p_pyhouse_obj.Twisted.Reactor.connectTCP(l_host, l_port, l_samsung_obj._Factory)
        LOG.info('Loaded XML')

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
        LOG.info("Stopped.")

# ## END DBK
