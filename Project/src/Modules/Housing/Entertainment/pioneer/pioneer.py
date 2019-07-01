"""
@name:      PyHouse.src.Modules.Housing.Entertainment.pioneer.pioneer.py
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

See: pioneer/__init__.py for documentation.

"""

__updated__ = '2019-06-30'
__version_info__ = (19, 5, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import os
import yaml
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.error import ConnectionDone
from twisted.conch.telnet import StatefulTelnetProtocol
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Core.Utilities import extract_tools
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
from Modules.Core.Utilities.convert import long_to_str
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Housing.Entertainment.samsung.samsung import SamsungDeviceData
from Modules.Housing.Entertainment.entertainment_data import EntertainmentDeviceInformation
from Modules.Housing.Entertainment.entertainment_xml import XML as entertainmentXML

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Pioneer        ')

SECTION = 'pioneer'
DISCONNECT_TIMER = 30  # Seconds
XML_PATH = 'HouseDivision/EntertainmentSection/PioneerSection'

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


class PioneerDeviceData(EntertainmentDeviceInformation):
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
        self._isControlling = False
        self._isRunning = False


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
        l_xml = XmlConfigTools.find_xml_section(p_pyhouse_obj, 'HouseDivision/EntertainmentSection/PioneerSection')
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
                l_plugin_obj.DeviceCount = l_count
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

    m_transport = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _find_device(self, p_family, p_model):
        # l_pandora = self.m_pyhouse_obj.House.Entertainment.Plugins['pandora'].Devices
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
        l_device_obj = self._find_device(l_family, l_model)
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


class PioneerProtocol(StatefulTelnetProtocol):
    """ There is an instance of this for every pioneer device that we are controlling.

    Each protocol instance is mapped to a Pioneer Device (and visa  versa)
    """

    def __init__(self, p_pyhouse_obj, p_device_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_pioneer_device_obj = p_device_obj
        # LOG.debug('Factory init for {}'.format(PrettyFormatAny.form(self.m_pioneer_device_obj, 'PioneerFactory-')))
        LOG.info('Protocol Init - Version:{}'.format(__version__))

    def _get_status(self):
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

    def __init__(self, p_pyhouse_obj, p_device_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_pioneer_device_obj = p_device_obj

    def send_command(self, p_device_obj, p_command):
        LOG.info('Send command {}'.format(p_command))
        try:
            l_host = p_device_obj._Connector.host
            p_device_obj._Transport.write(p_command + b'\r\n')
            LOG.info('Send TCP command:{} to {}'.format(p_command, l_host))
        except AttributeError as e_err:
            LOG.error("Tried to call send_command without a pioneer device configured.\n\tError:{}".format(e_err))


class PioneerFactory(ClientFactory):
    """
    This is a factory which produces protocols.
    By default, buildProtocol will create a protocol of the class given in self.protocol.
    """

    def __init__(self, p_pyhouse_obj, p_device_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_pioneer_device_obj = p_device_obj
        LOG.info('Init - Version:{}'.format(__version__))

    def startedConnecting(self, p_connector):
        """ *1
        Called when we are connecting to the device.
        Provides access to the connector.
        """
        self.m_pioneer_device_obj._Connector = p_connector

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


class API(MqttActions, PioneerClient):
    """This interfaces to all of PyHouse.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("API Initialized - Version:{}".format(__version__))

    def _read_yaml(self, p_device):
        """
        This needs to be more generic and for all devices configs.
        This is the start.
        """
        l_name = SECTION + '_' + p_device.Model + '.yaml'
        l_filename = os.path.join(self.m_pyhouse_obj.Yaml.YamlConfigDir, l_name)
        with open(l_filename) as l_file:
            l_yaml = yaml.safe_load(l_file)
            p_device._Yaml = l_yaml
        LOG.info('Loaded {} '.format(l_filename))
        return l_yaml

    def _find_device(self, _p_family, p_model):
        l_pioneer = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices
        for l_device in l_pioneer.values():
            if l_device.Model.lower() == p_model.lower():
                LOG.debug("found device")
                return l_device
        LOG.error('No such device as "{}"'.format(p_model))
        return None

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

    def LoadXml(self, p_pyhouse_obj):
        """ Read the XML for all Pioneer devices.
        """
        self.m_started = False
        l_device_obj = p_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        self._read_yaml(l_device_obj)
        LOG.info("Loaded Pioneer Device(s) - Version:{}".format(__version__))
        return l_device_obj

    def Start(self):
        """ Start all the Pioneer factories if we have any Pioneer devices.
        """
        LOG.info('Starting...')
        l_count = 0
        l_devices = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Devices
        for l_device_obj in l_devices.values():
            l_count += 1
            if not l_device_obj.Active:
                continue
            if l_device_obj._isRunning:
                LOG.info('Pioneer device {} is already running.'.format(l_device_obj.Name))
            l_host = long_to_str(l_device_obj.IPv4)
            l_port = l_device_obj.Port
            l_factory = PioneerFactory(self.m_pyhouse_obj, l_device_obj)
            l_connector = self.m_pyhouse_obj._Twisted.Reactor.connectTCP(l_host, l_port, l_factory)
            l_device_obj._Factory = l_factory
            l_device_obj._Connector = l_connector
            l_device_obj._isRunning = True
            self.m_pioneer_device_obj = l_device_obj
            LOG.info("Started Pioneer Device: '{}'; IP:{}; Port:{};".format(l_device_obj.Name, l_host, l_port))
        LOG.info("Started {} Pioneer device(s).".format(l_count))

    def SaveXml(self, _p_xml):
        l_xml = XML().write_pioneer_section_xml(self.m_pyhouse_obj)
        LOG.info("Saved Pioneer XML.")
        return l_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
