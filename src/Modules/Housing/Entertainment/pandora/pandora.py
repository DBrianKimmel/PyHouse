"""
-*- test-case-name: PyHouse.src.Modules.entertain.test.test_pandora -*-

@name: PyHouse/src/Modules/entertain/pandora.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: (c)2014-2018 by D. Brian Kimmel
@note: Created on Feb 27, 2014
@license: MIT License
@summary: Controls pandora playback thru pianobar.

When PyHouse starts initially, Pandora is inactive.

My (briank) system is controlled by an IR signal coming from an attached Pifacecad module vi lircd.

When a signal is recieved indicate the "pandora" button was pressed on a remote control,
 pianobar is fires up as a process.

Further IR signals control the pianobar process as needed, volume, next station etc.

When the remotes switches to another device (TV, BluRay, Tuner etc.), pianobar is terminated and
this module goes back to its initial state ready for another session.

Now (2018) will also work with MQTT messages to control Pandora via PioanBar and PatioBar.
"""
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML

__updated__ = '2018-08-08'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.internet import protocol

#  Import PyMh files and modules.
from Modules.Core.data_objects import BaseObject
from Modules.Housing.Entertainment.entertainment_data import EntertainmentDeviceControl
from Modules.Computer import logging_pyh as Logger
# from Modules.Core.Utilities.debug_tools import FormatBytes
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.Pandora     ')

PIANOBAR_LOC = '/usr/bin/pianobar'

#  (i) Control fifo at /home/briank/.config/pianobar/ctl opened


class PandoraData:

    def __init__(self):
        self.Active = False
        self.DeviceCount = 0
        self.Devices = {}  # PandoraDeviceData()


class DeviceControl:
    """ Standardized control message for Entertainment devices
    """

    def __init__(self):
        self.Channel = '01'
        self.Input = '1'
        self.Power = 'Off'
        self.Volume = '50'
        self.Zone = '1'


class PandoraDeviceData(BaseObject):

    def __init__(self):
        self.Active = False
        self.DeviceCount = 0
        self.Factory = None
        self.Api = None
        self.IPv4 = None
        self.Port = None


class XML:
    """
    """

    @staticmethod
    def _read_one_entry(p_entry_xml):
        l_obj = PandoraDeviceData()
        XmlConfigTools.read_base_object_xml(l_obj, p_entry_xml)
        l_obj.IPv4 = PutGetXML.get_ip_from_xml(p_entry_xml, 'IPv4')
        return l_obj

    @staticmethod
    def _write_one_entry():
        pass

    @staticmethod
    def read_pandora_section_xml(p_pyhouse_obj):
        l_ret = {}
        l_count = 0
        l_xml = p_pyhouse_obj.Xml.XmlRoot
        l_xml = l_xml.find('HouseDivision')
        if l_xml is None:
            return l_ret, l_count
        l_xml = l_xml.find('EntertainmentSection')
        if l_xml is None:
            return l_ret, l_count
        l_xml = l_xml.find('PandoraSection')
        if l_xml is None:
            return l_ret, l_count
        try:
            for l_entry_xml in l_xml.iterfind('Device'):
                l_entry_obj = XML._read_one_entry(l_entry_xml)
                l_entry_obj.Key = l_count
                l_ret[l_count] = l_entry_obj
                LOG.info('Loaded Pandora Device {}'.format(l_entry_obj.Name))
                l_count += 1
        except AttributeError as e_err:
            LOG.error('ERROR if getting Pandora Device Data - {}'.format(e_err))
        LOG.info('Loaded {} Pandora Devices.'.format(l_count))
        return l_ret, l_count

    @staticmethod
    def write_pandora_section_xml(p_pyhouse_obj):
        l_xml = ET.Element('PandoraSection')
        l_count = 0
        l_obj = p_pyhouse_obj.House.Entertainment.Pandora
        for l_pandora_object in l_obj.values():
            l_pandora_object.Key = l_count
            l_entry = XML._write_one_entry(l_pandora_object)
            l_xml.append(l_entry)
            l_count += 1
        LOG.info('Saved {} Pandora device(s) XML'.format(l_count))
        return l_xml


class MqttActions:
    """
    """

    m_API = None
    m_transport = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _get_field(self, p_message, p_field):
        try:
            l_ret = p_message[p_field]
        except KeyError:
            l_ret = 'The "{}" field was missing in the MQTT Message.'.format(p_field)
        return l_ret

    def _decode_control(self, p_topic, p_message):
        """ Decode the message.
        As a side effect - control Pandora ( PianoBar ) via the control socket
        """
        l_logmsg = '\tControl: '
        l_control = self._get_field(p_message, 'Control')
        if l_control == 'On':
            l_logmsg += ' Turn On '
            self.m_API.Start()
        elif l_control == 'Off':
            l_logmsg += ' Turn Off '
            self.m_API.Stop()

        elif l_control == 'VolUp1':
            l_logmsg += ' Volume Up 1 '
        else:
            l_logmsg += ' Unknown Pandora Control Message {} {}'.format(p_topic, p_message)
        return l_logmsg

    def decode(self, p_topic, p_message):
        """ Decode the Mqtt message
        ==> pyhouse/<house name>/hvac/<type>/<Name>/...
        <type> = thermostat, ...
        """
        if self.m_API == None:
            # LOG.debug('Decoding initializing')
            self.m_API = API(self.m_pyhouse_obj)

        l_logmsg = ''
        if p_topic[2] == 'control':
            l_logmsg += '\tPandora: {}\n'.format(self._decode_control(p_topic, p_message))
        else:
            l_logmsg += '\tUnknown Pandora sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Entertainment msg', 160))
        return l_logmsg


class PianobarControlProtocol(protocol.Protocol):
    pass


class BarProcessControl(protocol.ProcessProtocol):

    m_buffer = bytes()

    def __init__(self):
        self.m_buffer = bytes()

    def _extract_line(self, p_line):
        """
        """
        if p_line[0] == b'q':
            LOG.info('Quitting Pandora')
            return
        if p_line.startswith(b'Welcome'):
            LOG.info(p_line)
            return
        if p_line.startswith(b'Press ? for'):
            # LOG.debug('found Press')
            return
        if p_line.startswith(b'Ok.'):
            LOG.info(p_line)
            return
        # <ESC>[
        if p_line[0] == 0x1B:
            # LOG.debug('found esc sequence')
            p_line = p_line[4:]
        #
        if p_line.startswith(b'#'):
            # LOG.debug('found # {}'.format(p_line))
            return
        if p_line.startswith(b'(i)'):
            LOG.info(p_line)
            return
        if p_line.startswith(b'|>'):  # This is selection information
            LOG.info("Playing: {}".format(p_line[2:]))
            return
        LOG.debug("Data = {}".format(p_line))
        pass

    def connectionMade(self):
        """Write to stdin.
        """
        LOG.info("Connection Made.")

    def outReceived(self, p_data):
        """Data received from stdout.

        Note: Strings seem to begin with an ansi sequence  <esc>[xxx
        #        The line is a timestamp - every second
        (i)      This is an information message - Login, new playlist, etc.
        """
        # LOG.debug('PB Data-1 {}'.format(p_data))
        self.m_buffer += p_data
        while self.m_buffer[0] == b'\n' or self.m_buffer[0] == b'\r':  # Strip off all leading newlines
            self.m_buffer = self.m_buffer[1:]
        # LOG.debug('PB Data-2 {}'.format(self.m_buffer))
        while len(self.m_buffer) > 0:
            l_ix = self.m_buffer.find(b'\n')
            if l_ix > 0:
                l_line = self.m_buffer[:l_ix]
                # LOG.debug('PB Data-3 {}'.format(l_line))
                self.m_buffer = self.m_buffer[l_ix + 1:]
                self._extract_line(l_line)
                continue
            else:
                l_line = self.m_buffer
                # LOG.debug('PB Data-4 {}'.format(l_line))
                self._extract_line(l_line)
                self.m_buffer = bytes()

    def errReceived(self, p_data):
        """ Data received from StdErr.
        """
        LOG.warning("StdErr received - {}".format(p_data))


class API(MqttActions):

    m_started = False

    def __init__(self, p_pyhouse_obj):
        self.m_started = None
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def Start(self):
        """Start the Pandora player when we receive an IR signal to play music.
        This will open the socket for control
        """
        # LOG.info("Starting")
        l_topic = 'entertainment/pioneer/control'
        l_obj = EntertainmentDeviceControl()
        if not self.m_started:
            self.m_processProtocol = BarProcessControl()
            self.m_processProtocol.deferred = BarProcessControl()
            l_executable = '/usr/bin/pianobar'
            l_args = ('pianobar',)
            l_env = None  # this will pass <os.environ>
            self.m_transport = self.m_pyhouse_obj.Twisted.Reactor.spawnProcess(self.m_processProtocol, l_executable, l_args, l_env)
            self.m_started = True

            # self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, 'On')
            l_obj.Power = "On"
            l_obj.Channel = '01'
            self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_obj)

        LOG.info("Started.")

    def Stop(self):
        """Stop the Pandora player when we receive an IR signal to play some other thing.
        """
        self.m_started = False
        self.m_transport.write(b'q')
        self.m_transport.closeStdin()
        LOG.info("Stopped.")

# ## END DBK
