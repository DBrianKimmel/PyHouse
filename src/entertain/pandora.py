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

from src.utils.tools import PrintBytes

g_debug = 0
g_logger = logging.getLogger('PyHouse.Pandora     ')

PB_LOC = '/usr/bin/pianobar'

#  (i) Control fifo at /home/briank/.config/pianobar/ctl opened


class PianobarControlProtocol(protocol.Protocol):
    pass


class BarProcessControl(protocol.ProcessProtocol):

    def __init__(self):
        self.m_count = 0
        pass

    def connectionMade(self):
        """Write to stdin.
        """
        # self.transport.write('')
        # self.transport.closeStdin()
        pass

    def outReceived(self, p_data):
        """Data received from stdout.

        Note: Strings seem to begin with an ansi sequence  <esc>[xxx
        # incremental time
        """
        self.m_count += 1
        l_data = p_data.rstrip('\r\n')
        l_data = l_data.lstrip(' \t')
        if l_data[0] == chr(0x1B):
            l_data = l_data[2:]
        g_logger.debug(PrintBytes(l_data))
        if l_data.startswith('2K'):  # <ESC>[2K = erase
            l_data = l_data[2:]
        if l_data[0] == '#':  # The line is a timestamp - every second
            return
        if l_data.startswith('(i)'):  # This is an information message - Login, new playlist, etc.
            # g_logger.info("Pianobar Info = {0:}, {1:}".format(l_data, self.m_count))
            return
        if l_data.startswith('|>'):  # This is selection information
            # g_logger.info("Pianobar Info = {0:}, {1:}".format(l_data, self.m_count))
            return
        g_logger.debug("Data = {0:}, {1:} - Data".format(l_data, self.m_count))

    def errReceived(self, p_data):
        g_logger.warn("StdErr received - {0:}".format(p_data))


class API(object):

    def __init__(self):
        self.m_transport = None
        g_logger.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        """Start the Pandora player when we receive an IR signal to play music.
        This will open the socket for control
        """
        if self.m_transport == None:  # Do not start a second pianobar
            self.m_processProtocol = BarProcessControl()
            self.m_processProtocol.deferred = BarProcessControl()
            l_executable = '/usr/bin/pianobar'
            l_args = ('pianobar',)
            l_env = None  # this will pass <os.environ>
            self.m_transport = p_pyhouses_obj.Reactor.spawnProcess(self.m_processProtocol, l_executable, l_args, l_env)
            g_logger.info("Started.")

    def Stop(self):
        """Stop the Pandora player when we receive an IR signal to play some other thing.
        """
        self.m_transport.write('q')
        self.m_transport.closeStdin()
        g_logger.info("Stopped.")

# ## END DBK
