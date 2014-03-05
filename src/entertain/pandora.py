"""
Created on Feb 27, 2014

@author: briank

Controls pandora playback thru pianobar.

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
from twisted.internet import reactor


g_debug = 0
g_logger = logging.getLogger('PyHouse.Pandora     ')

PB_LOC = '/usr/bin/pianobar'

#  (i) Control fifo at /home/briank/.config/pianobar/ctl opened


class BarProcessControl(protocol.ProcessProtocol):

    def __init__(self):
        pass

    def connectionMade(self):
        """Write to stdin.
        """
        self.transport.write('')
        self.transport.closeStdin()

    def outReceived(self, p_data):
        """Data received from stdout.
        """
        if p_data.startswith('(i) Control fifo at'):
            pass
        pass

    def errReceived(self, p_data):
        pass


class API(object):

    def __init__(self):
        g_logger.info("Initialized.")

    def Start(self, _p_pyhouses_obj):
        """Start the Pndora player when we receive an IR signal to play music.
        """
        self.m_pianobar = BarProcessControl()
        reactor.spawnProcess(self.m_pianobar, PB_LOC, [PB_LOC])
        g_logger.info("Started.")

    def Stop(self):
        """Stop the Pandora player when we receive an IR signal to play some other thing.
        """
        g_logger.info("Stopped.")

# ## END DBK