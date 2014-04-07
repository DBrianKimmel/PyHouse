"""
pandora.py

Created on Feb 27, 2014

@author: briank

@copyright: 2014 by D. Brian Kimmel

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
import logging
from twisted.internet import protocol

# from src.utils.tools import PrintBytes

g_debug = 0
g_logger = logging.getLogger('PyHouse.Pandora     ')

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
        g_logger.info("Connection Made.")

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
            g_logger.info("Info = {0:}".format(l_data))
            return
        g_logger.debug("Data = {0:}".format(l_data))

    def errReceived(self, p_data):
        g_logger.warn("StdErr received - {0:}".format(p_data))


class API(object):

    m_started = False

    def __init__(self):
        self.m_started = None
        g_logger.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        """Start the Pandora player when we receive an IR signal to play music.
        This will open the socket for control
        """
        g_logger.info("Starting")
        if not self.m_started:
            self.m_processProtocol = BarProcessControl()
            self.m_processProtocol.deferred = BarProcessControl()
            l_executable = '/usr/bin/pianobar'
            l_args = ('pianobar',)
            l_env = None  # this will pass <os.environ>
            self.m_transport = p_pyhouses_obj.Reactor.spawnProcess(self.m_processProtocol, l_executable, l_args, l_env)
            self.m_started = True
        g_logger.info("Started.")

    def Stop(self):
        """Stop the Pandora player when we receive an IR signal to play some other thing.
        """
        self.m_started = False
        self.m_transport.write('q')
        self.m_transport.closeStdin()
        g_logger.info("Stopped.")

# ## END DBK
