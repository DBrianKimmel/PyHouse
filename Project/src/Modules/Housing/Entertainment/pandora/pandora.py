"""
@name: PyHouse/Project/src/Modules/Housing/Entertainment/pandora/pandora.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: (c)2014-2019 by D. Brian Kimmel
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

__updated__ = '2019-06-08'
__version_info__ = (19, 6, 1)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
# import xml.etree.ElementTree as ET
from twisted.internet import protocol
from _datetime import datetime  # , time
from pathlib import Path

#  Import PyMh files and modules.
from Modules.Housing.Entertainment.pandora.pandora_xml import XML as pandoraXML
from Modules.Core.Utilities import extract_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities.extract_tools import extract_quoted
# from Modules.Core.Utilities.json_tools import encode_json
# from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML
from Modules.Housing.Entertainment.entertainment_data import \
        EntertainmentDeviceControl, \
        EntertainmentPluginData, \
        EntertainmentServiceControl, \
        EntertainmentServiceStatus, \
        EntertainmentServiceData
# from Modules.Housing.Entertainment.entertainment_xml import XML as entertainmentXML

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Pandora        ')

PIANOBAR_LOCATION = '/usr/bin/pianobar'
SECTION = 'pandora'

#  (i) Control fifo at /home/briank/.config/pianobar/ctl opened


class PandoraPluginData(EntertainmentPluginData):
    """
    """

    def __init__(self):
        super(PandoraPluginData, self).__init__()
        self._OpenSessions = 0


class PandoraServiceData(EntertainmentServiceData):

    def __init__(self):
        super(PandoraServiceData, self).__init__()
        self._Buffer = bytes(0)


class PandoraServiceStatusData(EntertainmentServiceStatus):

    def __init__(self):
        super(PandoraServiceStatusData, self).__init__()
        self.Album = None
        self.Artist = None
        self.DateTimePlayed = None
        # self.DateTimeStarted = None
        self.Error = None  # If some error occurred
        self.From = None  # This host id to identify where it came from
        self.inUseDevice = None
        self.Likability = None
        self.PlayingTime = None
        self.Song = None
        self.Station = None
        self.Status = 'Idle'  # Device if service is in use.
        self.TimeTotal = None
        self.TimeLeft = None


class PandoraServiceControlData(EntertainmentServiceControl):
    """ Node-red interface allows some control of Pandora and hence the playback.
    This is it.
    """

    def __init__(self):
        super(PandoraServiceControlData, self).__init__()
        self.Like = None
        self.Dislike = None
        self.Skip = None


class PandoraDeviceControlData(EntertainmentDeviceControl):
    """ Pandora needs to control A/V devices.
    This is it.
    """

    def __init__(self):
        super(PandoraDeviceControlData, self).__init__()
        self.Power = None
        self.Input = None
        self.Volume = None
        self.Zone = None


class MqttActions():
    """ Process messages to and from this module.
    Output Control messages use Mqtt to send messages to control the amplifier type device attached to the raspberry pi computer.
    Input Control messages come from a node red computer and are the listener (user) commands for their listening experience.
    """

    m_API = None
    m_transport = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def send_mqtt_status_msg(self, p_message):
        l_topic = 'house/entertainment/pandora/status'
        self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, p_message)

    def _send_control(self, p_family, p_message):
        l_topic = 'house/entertainment/{}/control'.format(p_family)
        LOG.debug('Sending control message to A/V Device\n\t{}\n\t{}'.format(l_topic, p_message))
        self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, p_message)

    def _decode_status(self, _p_topic, _p_message):
        l_logmsg = '\tPandora Status'
        return l_logmsg

    def _decode_control(self, p_topic, p_message):
        """ Decode the Pandora Control message we just received.
         Someone (web page via node-red) wants to control pandora in some manner.

         ServiceName must match one of the Pandora services on this node.

        ==>
            Topic: pyhouse/<house name>/house/entertainment/pandora/control
            Msg:{   'Time':   '2019-05-07T22:19:19.536Z',
                    'Sender': 'pi-04-pp',
                    'Status': 'On'}


        We may need to issue a message to control connected audio devices.
                    Zone:  0,1 ...
                    Power: On, Off
                    Input: Tv, Game
                    Volume: 0..100
        As a side effect, we need to control Pandora ( PianoBar ) via the control socket
                    Like:
                    Dislike:
                    Skip:
        """
        l_logmsg = '\tPandora Control'
        l_service_name = extract_tools.get_mqtt_field(p_message, 'Name')
        l_zone = extract_tools.get_mqtt_field(p_message, 'Zone')
        l_input = extract_tools.get_mqtt_field(p_message, 'Input')
        l_power = extract_tools.get_mqtt_field(p_message, 'Power')
        l_volume = extract_tools.get_mqtt_field(p_message, 'Volume')
        l_like = extract_tools.get_mqtt_field(p_message, 'Like')
        # l_dislike = extract_tools.get_mqtt_field(p_message, 'Dislike')
        l_skip = extract_tools.get_mqtt_field(p_message, 'Skip')
        if l_zone == None:
            l_zone = 0
        LOG.debug('{} {}'.format(p_topic, p_message))

        # These directly control pianobar(pandora)
        if l_power == 'On':
            l_logmsg += ' Turn On '
            PandoraControl(self.m_pyhouse_obj)._start_pandora(p_message)
            A_V_Control(self.m_pyhouse_obj).ChangeAVDevice(l_zone, l_power, l_input, l_volume)
            return l_logmsg
        elif l_power == 'Off':
            l_logmsg += ' Turn Off '
            PandoraControl(self.m_pyhouse_obj)._halt_pandora(p_message)
            A_V_Control(self.m_pyhouse_obj).ChangeAVDevice(l_zone, l_power, l_input, l_volume)
            return l_logmsg
        elif l_volume != None:
            l_logmsg += ' Volume to: {}'.format(l_volume)
            A_V_Control(self.m_pyhouse_obj).ChangeAVDevice(l_zone, l_power, l_input, l_volume)
            return l_logmsg
        elif l_like == 'LikeYes':
            l_logmsg += ' Like '
            l_like = 'Yes'
        elif l_like == 'LikeNo':
            l_logmsg += ' Dislike '
            l_like = 'No'
        elif l_skip == 'SkipYes':
            l_logmsg += ' Skip '
            l_skip = 'Yes'
        else:
            l_logmsg += ' Unknown Pandora Control Message {} {}'.format(p_topic, p_message)
        return l_logmsg

    def decode(self, p_topic, p_message):
        """ Decode the Mqtt message
        We currently handle only control messages for Pandora.
        We are not interested in other module's status.

        ==> pyhouse/<house name>/entertainment/pandora/<Action>
            where: <action> = control, status

        @param p_topic: is the topic after ',,,/pandora/'
        @return: the log message with information stuck in there.

        """
        l_logmsg = ' Pandora '
        LOG.debug('{} {}'.format(p_topic, p_message))
        if p_topic[0].lower() == 'control':
            l_logmsg += '\tControl: {}\n'.format(self._decode_control(p_topic, p_message))
        elif p_topic[0].lower() == 'status':
            l_logmsg += '\tStatus: {}\n'.format(self._decode_status(p_topic, p_message))
        else:
            l_logmsg += '\tUnknown Pandora sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Entertainment msg', 160))
            LOG.warn('Unknown Pandora Topic: {}'.format(p_topic[0]))
        return l_logmsg


class ExtractPianobar():
    """
    This handles the information coming back from pianobar concerning the playing song.
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_buffer = bytes()

    def _extract_like(self, p_line):
        """ The like info comes back as a '<' in the now-playing info.
        """
        l_ix = p_line.find(b'<')
        if l_ix > 0:
            l_like = p_line[l_ix + 1:l_ix + 2].decode('utf-8')
            l_remain = p_line[:l_ix] + p_line[l_ix + 3:]
        else:
            l_like = ''
            l_remain = p_line
        return l_like, l_remain

    def _extract_station(self, p_line):
        """ Extract the station information from the now-playing message.
        """
        l_ix = p_line.find(b'@')
        l_sta = p_line[l_ix + 1:].decode('utf-8').strip()
        l_remain = p_line[:l_ix]
        return l_sta, l_remain

    def _extract_nowplaying(self, p_obj, p_line):
        """
        """
        p_line = p_line[2:]
        try:
            p_obj.From = self.m_pyhouse_obj.Computer.Name
            p_obj.DateTimePlayed = '{:%H:%M:%S}'.format(datetime.now())
            p_obj.Song, p_line = extract_quoted(p_line, b'\"')
            p_obj.Artist, p_line = extract_quoted(p_line)
            p_obj.Album, p_line = extract_quoted(p_line)
            p_obj.Likability, p_line = self._extract_like(p_line)
            p_obj.Station, p_line = self._extract_station(p_line)
            p_obj.Status = 'Playing'
        except:
            pass
        return p_obj

    def _extract_playtime(self, p_obj, p_line):
        """
        b'#   -03:00/03:00\r'
        b'#   -02:29/03:21'
        """
        p_line = p_line[1:]
        l_line = p_line.strip()
        l_ix = l_line.find(b'/')
        try:
            p_obj.TimeLeft = l_line[l_ix - 5:l_ix].decode('utf-8')
            p_obj.TimeTotal = l_line[l_ix + 1:].decode('utf-8')
            p_obj.PlayingTime = l_line[l_ix + 1:].decode('utf-8')
        except:
            pass
        return p_obj

    def _extract_errors(self, p_playline):
        """
        """
        # l_title = extract_quoted(p_playline, b'\"')
        pass

    def extract_line(self, p_line, p_hold):
        """
        b'\x1b[2K|>  Station "QuickMix" (1608513919875785623)\n\x1b[2K(i) Receiving new playlist...'
        strippping off the esc sequence ...
        b'|>  Station "QuickMix" (1608513919875785623)\n\x1b[2K(i) Receiving new playlist...'
        b'|>  "Mississippi Blues" by "Tim Sparks" on "Sidewalk Blues" <3 @ Acoustic Blues Radio\n'
        b'#   -02:29/03:09\r'
        b'  "Carroll County Blues" by "Bryan Sutton" on "Not Too Far From The Tree" @ Bluegrass Radio'
        b'  "Love Is On The Way" by "Dave Koz" on "Greatest Hits" <3 @ Smooth Jazz Radio'
        """
        if len(p_line) < 5:
            return None
        # <ESC>[2K  Ansi esc sequence needs stripped off first.
        if p_line[0] == 0x1B:
            p_line = p_line[4:]
        #
        if p_line.startswith(b'Welcome') or p_line.startswith(b'Press ? for') or p_line.startswith(b'Ok.'):
            LOG.info(p_line)
            return None
        # Housekeeping messages Login, Rx Stations, Rx playlists, ...
        elif p_line.startswith(b'(i)'):
            LOG.info(p_line)
            return None
        #
        if p_line[0] == b'q':
            LOG.info('Quitting Pandora')
            return 'Quit'

        # We gather the play data here
        # We do not send the message yet but will wait for the first time to arrive. ???
        l_now_playing = PandoraServiceStatusData()
        if p_line.startswith(b'|>'):  # This is
            LOG.info("Playing: {}".format(p_line))
            self._extract_nowplaying(l_now_playing, p_line)
            MqttActions(self.m_pyhouse_obj).send_mqtt_status_msg(l_now_playing)
            return l_now_playing
        # get the time and then send the message of now-playing
        if p_line.startswith(b'#'):
            l_now_playing = p_hold
            self._extract_playtime(l_now_playing, p_line)
            if l_now_playing.TimeTotal == l_now_playing.TimeLeft or \
                l_now_playing.TimeLeft.endswith('00'):
                LOG.info(p_line)
                MqttActions(self.m_pyhouse_obj).send_mqtt_status_msg(l_now_playing)
            return l_now_playing

        if p_line.startswith(b'Network'):  # A network error has occurred, restart
            LOG.info(p_line)
            PandoraControl(self.m_pyhouse_obj)._halt_pandora('Network Error')
            PandoraControl(self.m_pyhouse_obj)._start_pandora('Restarting')
            return 'Restarted'

        LOG.debug("Data = {}".format(p_line))
        return None


class PianobarProtocol(protocol.ProcessProtocol):
    """
    OutReceived - Some data was received from stdout.
    ErrReceived - Some data was received from stderr.
    ProcessExited - This will be called when the subprocess exits.
    ProcessEnded - Called when the child process exits and all file descriptors associated with it have been closed.
    """

    m_buffer = bytes()
    m_hold = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_buffer = bytes()

    def _get_line(self, p_buffer):
        """ Get a single line from the buffer.
        Remove the first line from the buffer.

        """
        p_buffer = p_buffer.lstrip()
        l_ix = p_buffer.find(b'\r')
        l_line = p_buffer[:l_ix]
        p_buffer = p_buffer[l_ix:]
        return p_buffer, l_line

    def _process_buffer(self):
        """
        """
        self.m_buffer = self.m_buffer.lstrip()

        while self.m_buffer:
            self.m_hold = PandoraServiceStatusData()
            self.m_buffer, l_line = self._get_line(self.m_buffer)
            l_ret = ExtractPianobar(self.m_pyhouse_obj).extract_line(l_line, self.m_hold)
            if l_ret == 'Quit':
                return
            elif l_ret == None:
                continue
            else:
                # self.m_hold = l_ret
                pass
            continue

    def connectionMade(self):
        """ Write to stdin.
        We do not have to do any initialization here.
        When we connect, the data flow from pianobar begins,
        """
        LOG.info("Connection to PianoBar Made.")

    def outReceived(self, p_data):
        """Data received from stdout.

        Note: Strings seem to begin with an ansi sequence  <esc>[xxx
        #        The line is a timestamp - every second
        (i)      This is an information message - Login, new playlist, etc.
        """
        self.m_buffer += p_data
        self._process_buffer()

    def errReceived(self, p_data):
        """ Data received from StdErr.
        """
        LOG.warning("StdErr received - {}".format(p_data))

    def ProcessEnded(self, p_reason):
        """
        """
        LOG.info("PianoBar closed. {}".format(p_reason))


class A_V_Control():
    """ Control the A/V device that pandora plays thru.
    """

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj

    def ChangeAVDevice(self, p_zone, p_power, p_input, p_volume):
        """ Build the control message for the A/V device.
        Fill in only what is necessary
        """
        l_pandora_plugin = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]  # PandoraPluginData()
        for l_service in l_pandora_plugin.Services.values():
            l_service_control_obj = PandoraDeviceControlData()  # Use the base control structure
            l_service_control_obj.Family = l_family = l_service.ConnectionFamily
            l_service_control_obj.Model = l_service.ConnectionModel
            l_service_control_obj.From = SECTION
            l_service_control_obj.InputName = p_input
            l_service_control_obj.Power = p_power
            l_service_control_obj.Volume = p_volume
            l_service_control_obj.Zone = p_zone
            # LOG.debug(PrettyFormatAny.form(l_service_control_obj, 'Obj', 190))
            # l_json = encode_json(l_service_control_obj)
            # LOG.debug(PrettyFormatAny.form(l_json, 'Json', 190))
            MqttActions(self.m_pyhouse_obj)._send_control(l_family, l_service_control_obj)


class PandoraControl(A_V_Control):
    """ This section starts and stops pandora.
    It also sends control messages to the connected A/V device
    """
    m_session_count = 0
    m_transport = None

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_session_count = 0

    def _start_pianobar(self):
        """ Start the pianobar process.
        Ensure that only 1 instance is running.
        """
        LOG.info('Start Pianobar.')
        l_pandora_plugin_obj = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        if l_pandora_plugin_obj._OpenSessions > 0:
            LOG.warn('multiple pianobar start attempts')
            return
        l_pandora_plugin_obj._OpenSessions += 1
        self.m_processProtocol = PianobarProtocol(self.m_pyhouse_obj)
        self.m_processProtocol.deferred = PianobarProtocol(self.m_pyhouse_obj)
        l_executable = PIANOBAR_LOCATION
        l_args = ('pianobar',)
        l_env = None  # this will pass <os.environ>
        self.m_transport = self.m_pyhouse_obj.Twisted.Reactor.spawnProcess(self.m_processProtocol, l_executable, l_args, l_env)

    def _stop_pianobar(self):
        """ Stop the pianobar process
        Clean up  and prepare for starting again.
        """
        LOG.info('Halt Pianobar')
        self.m_transport.write(b'q')
        self.m_transport.loseConnection()
        # l_pandora_plugin_obj = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]

    def is_pianobar_installed(self, p_pyhouse_obj):
        """ Check this node to see if pianobar is installed.
        If it is, assume we are the player and connect to the A/V equipment to play
        """
        l_file = Path(PIANOBAR_LOCATION)
        if l_file.is_file():
            return True
        p_pyhouse_obj.House.Entertainment.Plugins[SECTION].Active = False
        return False

    def _clear_status_fields(self):
        """
        Send message to Node-Red to update the status.
        All the fields used in node-red must be defined.
        """
        l_msg = PandoraServiceStatusData()
        l_msg.Status = ''
        l_msg.Album = ''
        l_msg.Artist = ''
        l_msg.Song = ''
        l_msg.Station = ''
        l_msg.Likability = ''
        l_msg.PlayingTime = ''
        l_msg.TimeLeft = ''
        l_msg.TimeTotal = ''
        l_date_time = datetime.now()
        l_msg.DateTimePlayed = '{:%H:%M:%S}'.format(l_date_time)
        return l_msg

    def issue_pandora_stopped_status(self):
        """
        Send message to Node-Red to update the status.
        """
        l_msg = self._clear_status_fields()
        l_msg.Status = 'Stopped'
        MqttActions(self.m_pyhouse_obj).send_mqtt_status_msg(l_msg)

    def _pandora_starting(self):
        """
        Send message to Node-Red to update the status.
        """
        l_msg = self._clear_status_fields()
        l_msg.Status = 'Starting'
        MqttActions(self.m_pyhouse_obj).send_mqtt_status_msg(l_msg)

    def _start_pandora(self, p_message):
        """ Start playing pandora.
        When we receive a proper Mqtt message to start (power on) the pandora player we:
            start the pianobar service to play pandora,
            send a control message to entertainment device pandora is hooked to to start that device
        """
        LOG.info('Play Pandora - {}'.format(p_message))
        if not self.is_pianobar_installed(self.m_pyhouse_obj):
            LOG.warn('Pianobar is not installed yet pandora is configured.')
            return
        l_pandora_plugin_obj = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        if l_pandora_plugin_obj._OpenSessions > 0:
            LOG.warn('multiple pianobar start attempts')
            return
        self._pandora_starting()
        l_pandora_plugin_obj._OpenSessions += 1
        self.m_processProtocol = PianobarProtocol(self.m_pyhouse_obj)
        # self.m_processProtocol.deferred = PianobarProtocol(self.m_pyhouse_obj)
        l_executable = PIANOBAR_LOCATION
        l_args = ('pianobar',)
        l_env = None  # this will pass <os.environ>
        self.m_transport = self.m_pyhouse_obj.Twisted.Reactor.spawnProcess(self.m_processProtocol, l_executable, l_args, l_env)
        #
        for l_service in l_pandora_plugin_obj.Services.values():
            l_device_control_obj = EntertainmentDeviceControl()
            l_device_control_obj.Family = l_family = l_service.ConnectionFamily
            l_device_control_obj.Model = l_model = l_service.ConnectionModel
            l_device_control_obj.From = SECTION
            l_device_control_obj.Power = "On"
            l_device_control_obj.InputName = l_service.InputName
            # l_device_control_obj.Volume = l_service.Volume
            l_device_control_obj.Zone = '1'
            LOG.info('Sending control-command to {}-{}'.format(l_family, l_model))
            l_topic = 'house/entertainment/{}/control'.format(l_family)
            self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_device_control_obj)

    def build_av_control_msg(self, p_service):
        """
        """
        l_service_control_obj = PandoraServiceControlData()
        l_service_control_obj.Family = l_family = p_service.ConnectionFamily
        l_service_control_obj.Device = l_name = p_service.ConnectionModel
        l_service_control_obj.From = SECTION
        l_service_control_obj.Model = p_service.ConnectionModel
        l_service_control_obj.Power = "Off"
        l_service_control_obj.InputName = p_service.InputName
        l_service_control_obj.Volume = p_service.Volume
        l_service_control_obj.Zone = '0'
        LOG.info('Sending control-command to {}-{}'.format(l_family, l_name))
        l_topic = 'house/entertainment/{}/control'.format(l_family)
        self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_service_control_obj)

    def _halt_pandora(self, p_message):
        """ We have received a control message and therefore we stop the pandora player.
        This control message may come from a MQTT message or from a timer.
        """
        LOG.info('Halt Pandora - {}'.format(p_message))
        l_pandora_plugin_obj = self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION]
        l_pandora_plugin_obj._OpenSessions -= 1
        try:
            self.m_transport.write(b'q')
            self.m_transport.closeStdin()
        except:
            pass
        LOG.info('Service Stopped')
        for l_service in l_pandora_plugin_obj.Services.values():
            l_service_control_obj = PandoraServiceControlData()
            l_service_control_obj.Family = l_family = l_service.ConnectionFamily
            l_service_control_obj.Device = l_name = l_service.ConnectionModel
            l_service_control_obj.From = SECTION
            l_service_control_obj.Model = l_service.ConnectionModel
            l_service_control_obj.Power = "Off"
            l_service_control_obj.InputName = l_service.InputName
            l_service_control_obj.Volume = l_service.Volume
            l_service_control_obj.Zone = '1'
            LOG.info('Sending control-command to {}-{}'.format(l_family, l_name))
            l_topic = 'house/entertainment/{}/control'.format(l_family)
            self.m_pyhouse_obj.APIs.Computer.MqttAPI.MqttPublish(l_topic, l_service_control_obj)
        self.issue_pandora_stopped_status()

    def control_audio_device(self, p_audio_device, p_control):
        """
        """


class API(MqttActions):

    def __init__(self, p_pyhouse_obj):
        """ Do the housekeeping for the Pandora plugin.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_API = self
        LOG.info("API Initialized - Version:{}".format(__version__))
        self.m_pandora_control_api = PandoraControl(p_pyhouse_obj)

    def LoadXml(self, p_pyhouse_obj):
        """ Read the XML for pandora.
        """
        LOG.info("Loading XML - Version:{}".format(__version__))
        l_obj = pandoraXML().read_pandora_section_xml(p_pyhouse_obj)
        LOG.info("Loaded Pandora XML - Version:{}".format(__version__))
        if self.m_pandora_control_api.is_pianobar_installed(self.m_pyhouse_obj):
            self.m_pyhouse_obj.House.Entertainment.Plugins[SECTION].Active = False
            l_obj.Active = False
        return l_obj

    def Start(self):
        """ Start the Pandora plugin since we have it configured in the XML.

        This does not start playing pandora.  That takes a control message to play.
        The control message comes from some external source (Alexa, WebPage, SmartPhone) etc.
        """
        self.m_pandora_control_api.issue_pandora_stopped_status()
        LOG.info("Started - Version:{}".format(__version__))

    def SaveXml(self, _p_xml):
        """
        """
        l_xml = pandoraXML().write_pandora_section_xml(self.m_pyhouse_obj)
        LOG.info("Saved Pandora XML.")
        return l_xml

    def Stop(self):
        """ Stop the Pandora player when we receive a signal to play some other thing.
        """
        self.m_transport.write(b'q')
        self.m_transport.closeStdin()
        LOG.info("Stopped.")

# ## END DBK
