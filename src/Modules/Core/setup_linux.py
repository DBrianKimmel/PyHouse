"""
@name:      PyHouse/src/Modules/Core/setup_linux.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Oct 21, 2015
@Summary:

"""

# Import system type stuff
import errno
import os
import platform
import signal
from twisted.internet import reactor
from twisted.application.service import Application

# Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.LinuxSetup     ')


class Linux(object):
    """
    """

    def __init__(self):
        pass

    def handle_signals(self):
        """
        typing the interrupt character (probably Ctrl-C) causes SIGINT to be sent
        typing the quit character (probably Ctrl-\) sends SIGQUIT.
        hanging up the phone (modem) sends SIGHUP
        typing the stop character (probably Ctrl-Z) sends SIGSTOP.
        """
        if platform.uname()[0] != 'Windows':
            signal.signal(signal.SIGHUP, SigHupHandler)
        signal.signal(signal.SIGINT, SigIntHandler)
        signal.signal(signal.SIGTERM, SigKillHandler)


    def SigHupHandler(self, signum, _stackframe):
        """
        """
        # if g_debug >= 1:
        LOG.debug('Hup Signal handler called with signal {}'.format(signum))
        g_API.Stop()
        g_API.Start()


    def SigIntHandler(signum, _stackframe):
        """interrupt character (probably Ctrl-C)
        """
        # if g_debug >= 1:
        LOG.debug('SigInt - Signal handler called with signal {}'.format(signum))
        LOG.info("Interrupted.\n\n\n")
        g_API.Stop()
        g_API.Quit()
        exit

    def SigKillHandler(signum, _stackframe):
        """
        """
        LOG.debug('SigInt - Signal handler called with signal {}'.format(signum))
        LOG.info('SigKill \n')
        exit



# ## END DBK
