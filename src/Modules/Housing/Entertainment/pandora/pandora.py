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

When "pandora" button is pressed on a web page, pianobar is fired up as a process.

Further Mqtt messages control the pianobar process as needed, volume, next station etc.

When the stop button is pressed on a web page, pianobar is terminated and
this module goes back to its initial state ready for another session.

Now (2018) works with MQTT messages to control Pandora via PioanBar and PatioBar.
"""

__updated__ = '2018-08-22'
__version_info__ = (18, 8, 0)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.internet import protocol

#  Import PyMh files and modules.
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
from Modules.Housing.Entertainment.entertainment_data import \
        EntertainmentDeviceControl, EntertainmentDeviceData, EntertainmentPluginData
from Modules.Computer import logging_pyh as Logger
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.Pandora        ')

PIANOBAR_LOCATION = '/usr/bin/pianobar'
SECTION = 'pandora'

#  (i) Control fifo at /home/briank/.config/pianobar/ctl opened


class PandoraDeviceData(EntertainmentDeviceData):

    def __init__(self):
        super(PandoraDeviceData, self).__init__()
        self.Host = '1.2.3.4'
        self.ConnectionName = None  # pioneer, Onkyo
        self.InputName = None
        self.InputCode = None
        self.Volume = 0  # Default volume
        self.MaxPlayTime = 12 * 60 * 60  # Seconds


class XML:
    """
    """

    @staticmethod
    def _read_device(p_entry_xml):
        """
        @param p_entry_xml: Element <Device> within <PandoraSection>
        @return: a PandoraDeviceData object
        """
        l_obj = PandoraDeviceData()
        XmlConfigTools.read_base_object_xml(l_obj, p_entry_xml)
        l_obj.Host = PutGetXML.get_ip_from_xml(p_entry_xml, 'Host')
        l_obj.ConnectionName = PutGetXML.get_text_from_xml(p_entry_xml, 'ConnectionName')
        l_obj.InputName = PutGetXML.get_text_from_xml(p_entry_xml, 'InputName')
        l_obj.InputCode = PutGetXML.get_text_from_xml(p_entry_xml, 'InputCode')
        l_obj.MaxPlayTime = PutGetXML.get_int_from_xml(p_entry_xml, 'MaxPlayTime')
        l_obj.Volume = PutGetXML.get_int_from_xml(p_entry_xml, 'Volume')
        return l_obj

    @staticmethod
    def _write_device(p_obj):
        """
        @param p_obj: a filled in PandorDeviceData object
        @return: An XML element for <Device> to be appended to <PandoraSection> Element
        """

        l_xml = XmlConfigTools.write_base_object_xml('Device', p_obj)
        # PutGetXML().put_text_element(l_xml, 'Comment', p_obj.Comment)
        PutGetXML.put_ip_element(l_xml, 'Host', p_obj.Host)
        PutGetXML.put_text_element(l_xml, 'ConnectionName', p_obj.ConnectionName)
        PutGetXML.put_text_element(l_xml, 'InputName', p_obj.InputName)
        PutGetXML.put_text_element(l_xml, 'InputCode', p_obj.InputCode)
        PutGetXML.put_text_element(l_xml, 'MaxPlayTime', p_obj.MaxPlayTime)
        PutGetXML.put_int_element(l_xml, 'Volume', p_obj.Volume)
        return l_xml

    @staticmethod
    def read_pandora_section_xml(p_pyhouse_obj):
        """
        This has to:
            Fill in an entry in Entertainment Plugins

        @param p_pyhouse_obj: containing an XML Element for the <PandoraSection>
        @return: a EntertainmentPluginData object filled in.
        """
        l_xml = XmlConfigTools.find_section(p_pyhouse_obj, 'HouseDivision/EntertainmentSection/PandoraSection')
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
                l_plugin_obj.Count = l_count
        except AttributeError as e_err:
            LOG.error('ERROR if getting {} Device Data - {}'.format(SECTION, e_err))
        p_pyhouse_obj.House.Entertainment.Plugins[SECTION] = l_plugin_obj
        LOG.info('Loaded {} {}Devices.'.format(l_count, SECTION))
        return l_plugin_obj

    @staticmethod
    def write_pandora_section_xml(p_pyhouse_obj):
        """ Create the <PandoraSection> portion of the <EntertainmentSection>

        @param p_pyhouse_obj: containing an object with pandora data filled in.
        @return: An Element of the tree which can be appended to the EntertainmentSection
        """
        l_entertain_obj = p_pyhouse_obj.House.Entertainment
        l_plugin_obj = l_entertain_obj.Plugins[SECTION]
        l_active = l_plugin_obj.Active
        l_xml = ET.Element('PandoraSection', attrib={'Active': str(l_active)})
        PutGetXML.put_text_element(l_xml, 'Type', l_plugin_obj.Type)
        l_count = 0

        # print(PrettyFormatAny.form(l_entertain_obj, 'Wr-1 Pandora', 180))
        # print(PrettyFormatAny.form(l_entertain_obj.Plugins, 'Wr-2 Pandora Plugins', 180))
        # print(PrettyFormatAny.form(l_entertain_obj.Plugins[SECTION], 'Wr-3 Pandora Plugin', 180))
        # print(PrettyFormatAny.form(l_entertain_obj.Plugins[SECTION].Devices, 'Wr-4 Pandora Devices', 180))

        for l_pandora_object in l_plugin_obj.Devices.values():
            l_pandora_object.Key = l_count
            l_entry = XML._write_device(l_pandora_object)
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
        ==> pyhouse/<house name>/entertainment/pandora/control/<do-this>
        <do-this> = On, Off, VolUp1, VolDown1, VolUp5, VolDown5, Like, Dislike
        """
        l_logmsg = '\tControl: '
        l_control = self._get_field(p_message, 'Control')
        if l_control == 'On':
            l_logmsg += ' Turn On '
            self.m_API._play_pandora()
        elif l_control == 'Off':
            l_logmsg += ' Turn Off '
            self.m_API._halt_pandora()

        elif l_control == 'VolUp1':
            l_logmsg += ' Volume Up 1 '
        else:
            l_logmsg += ' Unknown Pandora Control Message {} {}'.format(p_topic, p_message)
        return l_logmsg

    def decode(self, p_topic, p_message):
        """ Decode the Mqtt message
        ==> pyhouse/<house name>/entertainment/pandora/<Action>/...
        <action> = control, status
        """
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
        """ Do the housekeeping for the pandora plugin.
        """
        # print(PrettyFormatAny.form(p_pyhouse_obj.House, 'Pandora.API() House'))
        # print(PrettyFormatAny.form(p_pyhouse_obj.House.Entertainment, 'Pandora.API() Entertainment'))
        p_pyhouse_obj.House.Entertainment.Plugins[SECTION] = EntertainmentPluginData()
        p_pyhouse_obj.House.Entertainment.Plugins[SECTION].Name = SECTION
        self.m_started = None
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadXml(self, p_pyhouse_obj):
        """ Read the XML for pandora.
        """
        l_obj = XML.read_pandora_section_xml(p_pyhouse_obj)
        LOG.info("Loaded Pandora XML.")
        return l_obj

    def Start(self):
        """ Start the Pandora plugin since we have it configured in the XML.
        This does not start playing pandora.  That takes a control message to play.
        """
        # LOG.info("Starting")
        if not self.m_started:
            pass
        LOG.info("Started.")

    def SaveXml(self, _p_xml):
        """
        """
        l_xml = XML.write_pandora_section_xml(self.m_pyhouse_obj)
        LOG.info("Saved Pandora XML.")
        return l_xml

    def Stop(self):
        """Stop the Pandora player when we receive an IR signal to play some other thing.
        """
        self.m_started = False
        self.m_transport.write(b'q')
        self.m_transport.closeStdin()
        LOG.info("Stopped.")

    def _play_pandora(self):
        """ When we receive a proper Mqtt message to start (power on) the pandora player.
        We need to issue Mqtt messages to power on the sound system, set inputs, and a default volume.

        TODO:    Allow for multiple pandora players within one house.time
                 Allow one pandora player to drive multiple amps to have whole house music.
                 Implement max play
        """
        self.m_processProtocol = BarProcessControl()
        self.m_processProtocol.deferred = BarProcessControl()
        l_executable = PIANOBAR_LOCATION
        l_args = ('pianobar',)
        l_env = None  # this will pass <os.environ>
        self.m_transport = self.m_pyhouse_obj.Twisted.Reactor.spawnProcess(self.m_processProtocol, l_executable, l_args, l_env)
        self.m_started = True

        # self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, 'On')
        l_obj = EntertainmentDeviceControl()
        l_obj.Power = "On"
        l_obj.Channel = '01'
        LOG.info('Sending power on')
        l_topic = 'entertainment/pioneer/control'
        self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_obj)

    def _halt_pandora(self):
        """ We have received a control message and therefore we stop the pandora player.
        This control message may come from a control screen or from a timer.
        """
        self.m_started = False
        self.m_transport.write(b'q')
        self.m_transport.closeStdin()
        LOG.info("Stopped Pandora.")

# ## END DBK
