"""
@name:       Modules/House/Entertainment/pandora/pandora.py
@author:     D. Brian Kimmel
@contact:    D.BrianKimmel@gmail.com
@copyright:  (c)2014-2020 by D. Brian Kimmel
@note:       Created on Feb 27, 2014
@license:    MIT License
@summary:    Controls pandora playback thru pianobar.

When PyHouse starts initially, Pandora is inactive.

When "pandora" button is pressed on a web page, pianobar is fired up as a process.

Further Mqtt messages control the pianobar process as needed, volume, next station etc.

When the stop button is pressed on a web page, pianobar is terminated and
this module goes back to its initial state ready for another session.

Now (2018) works with MQTT messages to control Pandora via PioanBar and PatioBar.
"""

__updated__ = '2020-02-17'
__version_info__ = (19, 10, 5)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
from twisted.internet import protocol
from _datetime import datetime  # , time
from pathlib import Path

#  Import PyMh files and modules.
from Modules.Core.Config.config_tools import Api as configApi
from Modules.Core.Utilities import extract_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.Utilities.extract_tools import extract_quoted
from Modules.House.Entertainment.Pandora import \
    PandoraPluginInformation, \
    PandoraServiceInformation, \
    PandoraDeviceConnectionInformation, \
    PandoraServiceControlInformation, \
    PandoraDeviceControl, \
    PandoraServiceStatus, \
    MOD_NAME

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Pandora        ')

PIANOBAR_LOCATION = '/usr/bin/pianobar'


class MqttActions:
    """ Process messages to and from this module.
    Output Control messages use Mqtt to send messages to control the amplifier type device attached to the raspberry pi computer.
    Input Control messages come from a node red computer and are the listener (user) commands for their listening experience.
    """

    m_api = None
    m_transport = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def send_mqtt_status_msg(self, p_message):
        l_topic = 'house/entertainment/pandora/status'
        self.m_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, p_message)

    def _send_control(self, p_family, p_message):
        l_topic = 'house/entertainment/{}/control'.format(p_family)
        LOG.debug('Sending control message to A/V Device\n\t{}\n\t{}'.format(l_topic, p_message))
        self.m_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, p_message)

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
        l_zone = extract_tools.get_mqtt_field(p_message, 'Zone')
        l_input = extract_tools.get_mqtt_field(p_message, 'Input')
        l_power = extract_tools.get_mqtt_field(p_message, 'Power')
        l_volume = extract_tools.get_mqtt_field(p_message, 'Volume')
        l_like = extract_tools.get_mqtt_field(p_message, 'Like')
        l_skip = extract_tools.get_mqtt_field(p_message, 'Skip')
        if l_zone == None:
            l_zone = 0
        LOG.debug('{} {}'.format(p_topic, p_message))

        # These directly control pianobar(pandora)
        if l_power == 'On':
            l_logmsg += ' Turn On '
            PandoraControl(self.m_pyhouse_obj)._start_pandora(p_message)
            A_V_Control(self.m_pyhouse_obj).change_av_device(l_zone, l_power, l_input, l_volume)
            return l_logmsg
        elif l_power == 'Off':
            l_logmsg += ' Turn Off '
            PandoraControl(self.m_pyhouse_obj)._halt_pandora(p_message)
            A_V_Control(self.m_pyhouse_obj).change_av_device(l_zone, l_power, l_input, l_volume)
            return l_logmsg
        elif l_volume != None:
            l_logmsg += ' Volume to: {}'.format(l_volume)
            A_V_Control(self.m_pyhouse_obj).change_av_device(l_zone, l_power, l_input, l_volume)
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

    def decode(self, p_msg):
        """ Decode the Mqtt message
        We currently handle only control messages for Pandora.
        We are not interested in other module's status.

        ==> pyhouse/<house name>/entertainment/pandora/<Action>
            where: <action> = control, status

        @param p_topic: is the topic after ',,,/pandora/'
        @return: the log message with information stuck in there.
        """
        l_topic = p_msg.UnprocessedTopic
        p_msg.UnprocessedTopic = p_msg.UnprocessedTopic[1:]
        p_msg.LogMessage += ' Pandora '
        LOG.debug('{} {}'.format(l_topic[0], p_msg.Payload))
        if l_topic[0].lower() == 'control':
            p_msg.LogMessage += '\tControl: {}\n'.format(self._decode_control(l_topic[0], p_msg.Payload))
        elif l_topic[0].lower() == 'status':
            p_msg.LogMessage += '\tStatus: {}\n'.format(self._decode_status(l_topic[0], p_msg.Payload))
        else:
            p_msg.LogMessage += '\tUnknown Pandora sub-topic {}'.format(PrettyFormatAny.form(p_msg.Payload, 'Entertainment msg', 160))
            LOG.warning('Unknown Pandora Topic: {}'.format(l_topic[0]))


class ExtractPianobar:
    """
    This handles the information coming back from pianobar concerning the playing song.
    """

    m_pyhouse_obj = None
    m_now_playing = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_buffer = bytes()
        self.m_now_playing = PandoraServiceStatus()

    def _extract_like(self, p_line):
        """ The like info comes back as a '<' in the now-playing info.
        """
        l_ix = p_line.find(b'<')
        if l_ix > 0:
            l_like = p_line[l_ix + 1:l_ix + 2].decode('utf-8')
            l_remain = p_line[:l_ix] + p_line[l_ix + 3:].strip()
        else:
            l_like = ''
            l_remain = p_line.strip()
        return l_like, l_remain

    def _extract_station(self, p_line):
        """ Extract the station information from the now-playing message.
        """
        l_ix = p_line.find(b'@')
        l_sta = p_line[l_ix + 1:].decode('utf-8').strip()
        l_remain = p_line[:l_ix].strip()
        return l_sta, l_remain

    def _extract_nowplaying(self, p_obj, p_line):
        """
        @param p_obj: is the status
        @param p_line: is the line from pianobar
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
            l_left = l_line[l_ix - 5:l_ix].decode('utf-8')
            l_total = l_line[l_ix + 1:].decode('utf-8')
        except:
            l_left = '01:23'
            l_left = '06:54'
        p_obj.TimeLeft = l_left
        p_obj.TimeTotal = l_total
        return p_obj

    def _extract_errors(self, p_playline):
        """
        """
        pass

    def extract_line(self, p_line):
        """
        b'\x1b[2K|>  Station "QuickMix" (1608513919875785623)\n\x1b[2K(i) Receiving new playlist...'

        After breaking into lines and strippping off the esc sequence we have ...

        b'|>  Station "QuickMix" (1608513919875785623)\n\x1b[2K(i) Receiving new playlist...'
        b'|>  "Mississippi Blues" by "Tim Sparks" on "Sidewalk Blues" <3 @ Acoustic Blues Radio\n'
        b'#   -02:29/03:09\r'
        b'  "Carroll County Blues" by "Bryan Sutton" on "Not Too Far From The Tree" @ Bluegrass Radio'
        b'  "Love Is On The Way" by "Dave Koz" on "Greatest Hits" <3 @ Smooth Jazz Radio'

        @param p_line: is an input line from pianobar.
        """
        if len(p_line) < 5:
            return None
        # <ESC>[2K  Ansi esc sequence needs stripped off first.
        if p_line[0] == 0x1B:
            p_line = p_line[4:]
        if p_line.startswith(b'Welcome') or \
           p_line.startswith(b'Press ? for') or \
           p_line.startswith(b'Ok.') or \
           p_line.startswith(b'(i)'):
            LOG.info(p_line)
            return None
        if p_line[0] == b'q':
            LOG.info('Quitting Pandora')
            return 'Quit'
        # We gather the play data here
        # We do not send the message yet but will wait for the first time to arrive.
        if p_line.startswith(b'|>'):  # This is a new playing selection line.
            self.m_now_playing = PandoraServiceStatus()
            LOG.info("Playing: {}".format(p_line))
            self.m_now_playing = self._extract_nowplaying(self.m_now_playing, p_line)
            self.m_now_playing.Error = None
            MqttActions(self.m_pyhouse_obj).send_mqtt_status_msg(self.m_now_playing)
            return self.m_now_playing
        # get the time and then send the message of now-playing
        if p_line.startswith(b'#'):
            self._extract_playtime(self.m_now_playing, p_line)
            if self.m_now_playing.TimeTotal == self.m_now_playing.TimeLeft or \
                self.m_now_playing.TimeLeft.endswith('00'):
                LOG.info(p_line)
                MqttActions(self.m_pyhouse_obj).send_mqtt_status_msg(self.m_now_playing)
            return self.m_now_playing
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

    m_pyhouse_obj = None
    m_buffer = bytes()
    m_extract = None
    m_hold = None  # Playing info

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_buffer = bytes()
        self.m_hold = PandoraServiceStatus()  # Clear playing info
        self.m_extract = ExtractPianobar(self.m_pyhouse_obj)

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
        """ Process the entire buffer - perhaps several, in extract_line
        """
        self.m_buffer = self.m_buffer.lstrip()
        while self.m_buffer:
            self.m_buffer, l_line = self._get_line(self.m_buffer)
            l_ret = self.m_extract.extract_line(l_line)
            if l_ret == 'Quit':
                return
            elif l_ret == None:
                continue
            else:
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


class A_V_Control:
    """ Control the A/V device that pandora plays thru.
    """

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj

    def change_av_device(self, p_zone, p_power, p_input, p_volume):
        """ Build the control message for the A/V device.
        Fill in only what is necessary
        """
        l_pandora_plugin = self.m_pyhouse_obj.House.Entertainment[MOD_NAME]  # PandoraPluginData()
        for l_service in l_pandora_plugin.Services.values():
            l_service_control_obj = PandoraDeviceControl()  # Use the base control structure
            l_service_control_obj.Family = l_family = l_service.ConnectionFamily
            l_service_control_obj.Model = l_service.ConnectionModel
            l_service_control_obj.From = MOD_NAME
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
        l_pandora_plugin_obj = self.m_pyhouse_obj.House.Entertainment[MOD_NAME]
        if l_pandora_plugin_obj._OpenSessions > 0:
            LOG.warning('multiple pianobar start attempts')
            return
        l_pandora_plugin_obj._OpenSessions += 1
        self.m_processProtocol = PianobarProtocol(self.m_pyhouse_obj)
        self.m_processProtocol.deferred = PianobarProtocol(self.m_pyhouse_obj)
        #
        l_executable = PIANOBAR_LOCATION
        l_args = ('pianobar',)
        l_env = None  # this will pass <os.environ>
        self.m_transport = self.m_pyhouse_obj._Twisted.Reactor.spawnProcess(self.m_processProtocol, l_executable, l_args, l_env)

    def _stop_pianobar(self):
        """ Stop the pianobar process
        Clean up  and prepare for starting again.
        """
        LOG.info('Halt Pianobar')
        self.m_transport.write(b'q')
        self.m_transport.loseConnection()

    def is_pianobar_installed(self, _p_pyhouse_obj):
        """ Check this node to see if pianobar is installed.
        If it is, assume we are the player and connect to the A/V equipment to play
        """
        l_file = Path(PIANOBAR_LOCATION)
        if l_file.is_file():
            return True
        return False

    def _clear_status_fields(self):
        """
        Send message to Node-Red to update the status.
        All the fields used in node-red must be defined.
        """
        l_msg = PandoraServiceStatus()
        l_msg.Likability = ''
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
            LOG.warning('Pianobar is not installed yet pandora is configured.')
            return
        l_pandora_plugin_obj = self.m_pyhouse_obj.House.Entertainment[MOD_NAME]
        if l_pandora_plugin_obj._OpenSessions > 0:
            LOG.warning('multiple pianobar start attempts')
            return
        self._pandora_starting()
        l_pandora_plugin_obj._OpenSessions += 1
        self.m_processProtocol = PianobarProtocol(self.m_pyhouse_obj)
        l_executable = PIANOBAR_LOCATION
        l_args = ('pianobar',)
        l_env = None  # this will pass <os.environ>
        self.m_transport = self.m_pyhouse_obj._Twisted.Reactor.spawnProcess(self.m_processProtocol, l_executable, l_args, l_env)
        #
        for l_service in l_pandora_plugin_obj.Services.values():
            l_device_control_obj = PandoraDeviceControl()
            l_device_control_obj.Family = l_family = l_service.ConnectionFamily
            l_device_control_obj.Model = l_model = l_service.ConnectionModel
            l_device_control_obj.From = MOD_NAME
            l_device_control_obj.Power = "On"
            l_device_control_obj.InputName = l_service.InputName
            l_device_control_obj.Zone = '1'
            LOG.info('Sending control-command to {}-{}'.format(l_family, l_model))
            l_topic = 'house/entertainment/{}/control'.format(l_family)
            self.m_pyhouse_obj.Core.NqttApi.MqttPublish(l_topic, l_device_control_obj)

    def build_av_control_msg(self, p_service):
        """
        """
        l_service_control_obj = PandoraServiceControlInformation()
        l_service_control_obj.Family = l_family = p_service.ConnectionFamily
        l_service_control_obj.Device = l_name = p_service.ConnectionModel
        l_service_control_obj.From = MOD_NAME
        l_service_control_obj.Model = p_service.ConnectionModel
        l_service_control_obj.Power = "Off"
        l_service_control_obj.InputName = p_service.InputName
        l_service_control_obj.Volume = p_service.Volume
        l_service_control_obj.Zone = '0'
        LOG.info('Sending control-command to {}-{}'.format(l_family, l_name))
        l_topic = 'house/entertainment/{}/control'.format(l_family)
        self.m_pyhouse_obj.Core.NqttApi.MqttPublish(l_topic, l_service_control_obj)

    def _halt_pandora(self, p_message):
        """ We have received a control message and therefore we stop the pandora player.
        This control message may come from a MQTT message or from a timer.
        """
        LOG.info('Halt Pandora - {}'.format(p_message))
        l_pandora_plugin_obj = self.m_pyhouse_obj.House.Entertainment[MOD_NAME]
        l_pandora_plugin_obj._OpenSessions -= 1
        try:
            self.m_transport.write(b'q')
            self.m_transport.closeStdin()
        except Exception as e_err:
            LOG.warning('Could not close pianobar - {}'.format(e_err))
            pass
        LOG.info('Service Stopped')
        for l_service in l_pandora_plugin_obj.Services.values():
            l_service_control_obj = PandoraDeviceControl()
            l_service_control_obj.Family = l_family = l_service.Connection.Family
            l_service_control_obj.Device = l_name = l_service.Connection.Model
            l_service_control_obj.From = MOD_NAME
            l_service_control_obj.Model = l_service.Connection.Model
            l_service_control_obj.Power = "Off"
            l_service_control_obj.InputName = l_service.Connection.Input
            l_service_control_obj.Volume = l_service.Volume
            l_service_control_obj.Zone = '1'
            LOG.info('Sending control-command to {}-{}'.format(l_family, l_name))
            l_topic = 'house/entertainment/{}/control'.format(l_family)
            self.m_pyhouse_obj.Core.MqttApi.MqttPublish(l_topic, l_service_control_obj)
        self.issue_pandora_stopped_status()

    def control_audio_device(self, p_audio_device, p_control):
        """
        """


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
        l_pandora = l_entertain[MOD_NAME]
        LOG.debug(PrettyFormatAny.form(l_entertain, 'Entertainment'))
        LOG.debug(PrettyFormatAny.form(l_pandora, 'Pandora'))
        LOG.debug(PrettyFormatAny.form(l_pandora.Services, 'Pandora'))
        #
        for _l_key, l_service in l_pandora.Services.items():
            LOG.debug(PrettyFormatAny.form(l_service, 'Service'))
            if hasattr(l_service, 'Connection'):
                LOG.debug(PrettyFormatAny.form(l_service.Connection, 'Connection'))
            if hasattr(l_service, 'Host'):
                LOG.debug(PrettyFormatAny.form(l_service.Host, 'Host'))
            if hasattr(l_service, 'Access'):
                LOG.debug(PrettyFormatAny.form(l_service.Access, 'Access'))

    def _extract_connection_group(self, p_config):
        """
        """
        l_obj = PandoraDeviceConnectionInformation()
        try:
            for l_key, l_value in p_config.items():
                # LOG.debug('Connection Key:{}; Value:{}'.format(l_key, l_value))
                setattr(l_obj, l_key, l_value)
            return l_obj
        except:
            l_obj.Name = p_config
        l_ret = None
        return l_ret

    def _extract_one_service(self, p_config):
        """
        """
        # self.dump_struct()
        l_required = ['Name', 'Host', 'Connection', 'Access']
        l_obj = PandoraServiceInformation()
        for l_key, l_value in p_config.items():
            if l_key == 'Host':
                l_obj.Host = self.m_config.extract_host_group(l_value)
            elif l_key == 'Connection':
                l_ret = self._extract_connection_group(l_value)
                l_obj.Connection = l_ret
            elif l_key == 'Access':
                l_obj.Access = self.m_config.extract_access_group(l_value)
            else:
                setattr(l_obj, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('Pandora Yaml is missing an entry for "{}"'.format(l_key))
        return l_obj  # For testing.

    def _extract_all_services(self, p_config):
        """
        """
        l_dict = {}
        for l_ix, l_value in enumerate(p_config):
            l_service = self._extract_one_service(l_value)
            l_dict[l_ix] = l_service
        return l_dict

    def _extract_all_pandora(self, p_config):
        """
        """
        # self.dump_struct()
        l_required = ['Name']
        l_obj = PandoraPluginInformation()
        for l_key, l_value in p_config.items():
            if l_key == 'Service':
                l_services = self._extract_all_services(l_value)
                l_obj.Services = l_services
                l_obj.ServiceCount = len(l_services)
            else:
                setattr(l_obj, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('Pandora Yaml is missing an entry for "{}"'.format(l_key))
        return l_obj  # For testing.

    def load_yaml_config(self):
        """ Read the pandora.yaml file.
        """
        LOG.info('Loading Config - Version:{}'.format(__version__))
        l_yaml = self.m_config.read_config_file(MOD_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(MOD_NAME))
            return None
        try:
            l_yaml = l_yaml['Pandora']
        except:
            LOG.warning('The config file does not start with "Pandora:"')
            return None
        l_pandora = self._extract_all_pandora(l_yaml)
        self.m_pyhouse_obj.House.Entertainment['pandora'] = l_pandora
        # self.dump_struct()
        return l_pandora  # for testing purposes


class Api(MqttActions):

    m_pyhouse_obj = None
    m_local_config = None

    def __init__(self, p_pyhouse_obj):
        """ Do the housekeeping for the Pandora plugin.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_api = self
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info("Api Initialized - Version:{}".format(__version__))
        self.m_pandora_control_api = PandoraControl(p_pyhouse_obj)

    def _add_storage(self):
        self.m_pyhouse_obj.House.Entertainment['Pandora'] = {}

    def LoadConfig(self):
        """ Read the Config for pandora.
        """
        LOG.info("Loading Config - Version:{}".format(__version__))
        if self.m_pandora_control_api.is_pianobar_installed(self.m_pyhouse_obj):
            LOG.info('Pianobar present')
            self.m_pyhouse_obj.House.Entertainment['Pandora'] = self.m_local_config.load_yaml_config()
        else:
            LOG.warning('Pianobar Missing')

    def Start(self):
        """ Start the Pandora plugin since we have it configured.

        This does not start playing pandora.  That takes a control message to play.
        The control message comes from some external source (Alexa, WebPage, SmartPhone) etc.
        """
        self.m_pandora_control_api.issue_pandora_stopped_status()
        LOG.info("Started - Version:{}".format(__version__))

    def SaveConfig(self):
        """
        """

    def Stop(self):
        """ Stop the Pandora player when we receive a signal to play some other thing.
        """
        self.m_transport.write(b'q')
        self.m_transport.closeStdin()
        LOG.info("Stopped.")

# ## END DBK
