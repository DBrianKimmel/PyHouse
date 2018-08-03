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
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2018-08-03'

# Import system type stuff
from twisted.internet import protocol

#  Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Pandora     ')

PIANOBAR_LOC = '/usr/bin/pianobar'

#  (i) Control fifo at /home/briank/.config/pianobar/ctl opened


class MqttActions:
    """
    """

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
            API.Start(self.m_pyhouse_obj)
        elif l_control == 'Off':
            l_logmsg += ' Turn Off '
            API.Stop()
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
        l_logmsg = ''
        if p_topic[2] == 'control':
            l_logmsg += '\tPandora: {}\n'.format(self._decode_control(p_topic, p_message))
        else:
            l_logmsg += '\tUnknown Pandora sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Entertainment msg', 160))
        return l_logmsg


class PianobarControlProtocol(protocol.Protocol):
    pass


class BarProcessControl(protocol.ProcessProtocol):

    def __init__(self):
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
        l_data = p_data.rstrip(b'\r\n')
        l_data = l_data.lstrip(b' \t')
        if l_data[0] == chr(0x1B):
            l_data = l_data[2:]
        if l_data[1] == 'K':  # <ESC>[nK = erase something
            l_data = l_data[2:]
        if l_data[0] == '#'or l_data.startswith(b'(i)'):
            return
        if l_data.startswith(b'Welcome to pianobar') or l_data.startswith(b'Press ? for') or l_data.startswith(b'Ok.'):
            return
        if l_data.startswith(b'|>'):  # This is selection information
            LOG.info("Info = {}".format(l_data))
            return
        LOG.debug("Data = {}".format(l_data))

    def errReceived(self, p_data):
        LOG.warning("StdErr received - {}".format(p_data))


class API(MqttActions):

    m_started = False

    def __init__(self, p_pyhouse_obj):
        self.m_started = None
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def Start(self, p_pyhouse_obj):
        """Start the Pandora player when we receive an IR signal to play music.
        This will open the socket for control
        """
        LOG.info("Starting")
        if not self.m_started:
            self.m_processProtocol = BarProcessControl()
            self.m_processProtocol.deferred = BarProcessControl()
            l_executable = '/usr/bin/pianobar'
            l_args = ('pianobar',)
            l_env = None  # this will pass <os.environ>
            self.m_transport = p_pyhouse_obj.Twisted.Reactor.spawnProcess(self.m_processProtocol, l_executable, l_args, l_env)
            self.m_started = True
        LOG.info("Started.")

    def Stop(self):
        """Stop the Pandora player when we receive an IR signal to play some other thing.
        """
        self.m_started = False
        self.m_transport.write('q')
        self.m_transport.closeStdin()
        LOG.info("Stopped.")

# ## END DBK
