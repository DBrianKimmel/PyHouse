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
from twisted.internet import reactor
# from twisted.internet.defer import Deferred


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
        if ord(l_data[0]) == 0x1b:
            l_data = l_data[1:]
        if l_data[0] < ' ' or l_data[0] > 0x7f:
            print('>>>{0:#x} {1:#x}'.format(ord(l_data[0]), ord(l_data[1])))
        l_data = l_data.lstrip('\r\n\t0x1B[ ')
        if l_data[0] == '#':
            return
        if l_data.startswith('(i)'):
            print("Pianobar Info = {0:}, {1:}".format(l_data, self.m_count))
            return
        print("Data = {0:}, {1:}".format(l_data, self.m_count))

    def errReceived(self, p_data):
        print("Err received - {0:}".format(p_data))


class API(object):

    def __init__(self):
        g_logger.info("Initialized.")

    def Start(self, _p_pyhouses_obj):
        """Start the Pndora player when we receive an IR signal to play music.
        This will open the socket for control
        """
        self.m_processProtocol = BarProcessControl()
        self.m_processProtocol.deferred = BarProcessControl()
        l_executable = '/usr/bin/pianobar'
        l_args = ('pianobar',)
        l_env = None  # this will pass <os.environ>
        self.m_transport = reactor.spawnProcess(self.m_processProtocol, l_executable, l_args, l_env)
        g_logger.info("Started.")

    def Stop(self):
        """Stop the Pandora player when we receive an IR signal to play some other thing.
        """
        self.m_transport.write('q')
        self.m_transport.closeStdin()
        g_logger.info("Stopped.")

# ## END DBK
