"""
-*- test-case-name: PyHouse.src.Modules.entertain.test.test_pandora -*-

@name: PyHouse/src/Modules/entertain/pandora.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
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
"""

# Import system type stuff
from twisted.internet import protocol

# from Modules.utils.tools import PrintBytes
from Modules.utils import pyh_log

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.Pandora     ')

PB_LOC = '/usr/bin/pianobar'

#  (i) Control fifo at /home/briank/.config/pianobar/ctl opened


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
        l_data = p_data.rstrip('\r\n')
        l_data = l_data.lstrip(' \t')
        if l_data[0] == chr(0x1B):
            l_data = l_data[2:]
        if l_data[1] == 'K':  # <ESC>[nK = erase something
            l_data = l_data[2:]
        if l_data[0] == '#'or l_data.startswith('(i)'):
            return
        if l_data.startswith('Welcome to pianobar') or l_data.startswith('Press ? for') or l_data.startswith('Ok.'):
            return
        if l_data.startswith('|>'):  # This is selection information
            LOG.info("Info = {0:}".format(l_data))
            return
        LOG.debug("Data = {0:}".format(l_data))

    def errReceived(self, p_data):
        LOG.warning("StdErr received - {0:}".format(p_data))


class API(object):

    m_started = False

    def __init__(self):
        self.m_started = None
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
            self.m_transport = p_pyhouse_obj.Reactor.spawnProcess(self.m_processProtocol, l_executable, l_args, l_env)
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
