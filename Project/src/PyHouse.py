#!/usr/bin/env python3
"""
@name:      Pyhouse.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2020 by D. Brian Kimmel
@note:      Created on Mar 1, 2014
@license:   MIT License
@summary:   This is the core of the PyHouse daemon.

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights2
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.


PyHouse.
        Computer        Configuration File
        House           Configuration File
        Services        Internal
        Twisted         Internal
        Xml             Internal

Uses I{Epytext} mark-up for documentation.

see C{Modules.__init__.py} for Core documentation.

During development this is run by hand.
It is, however, planned to be a daemon that is kicked off on system start-up.
It now (2013) runs on Raspberry Pi so that is the primary target.

There are two components of this software.
The first is "computer' and is started first.
The second is 'house' and is started second.
See those modules to find out what each does.

Idea Links:
  https://github.com/TheThingSystem/home-controller forked from automategreen/home-controller
  https://github.com/zonyl/pytomation
  https://github.com/king-dopey/pytomation forked from zonyl/pytomation
  http://leftovercode.info/smartlinc.php
  https://github.com/hollie/misterhouse/
  https://github.com/hollie/misterhouse/blob/master/lib/Insteon/AllLinkDatabase.pm

    SmartHome Wiki: Using Custom Commands in SmartLinc
    SmartHome Forum: SmartLinc Direct Command for Light Status?
    SmartHome Forum: Custom Screens on the SmartLinc
    SmartHome Wiki: Insteon Command Table
    Smarthome Forum: SmartLinc web automation solved
    SmartHome Forum: 2412N Insteon Central Controller - Software
    Ramp Rate
    Insteon Commands


"""

__updated__ = '2020-02-17'
__version_info__ = (20, 2, 4)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import errno
import fcntl
import os
import platform
import signal
import sys

#  Import PyHouse files and modules.
from Modules.Core.setup_config import CheckInitialSetup
from Modules.Core import core

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse                ')

LOCK_PATH = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "lock")
g_Api = None


class Singleton:
    """ Set up the singleton pattern.
    This prevents more than one instance of PyHouse running on this computer.
    It is the very first action taken when starting PyHouse to run.
    """

    def __init__(self):
        self.fh = None
        self.is_running = False
        self.do_magic()

    def do_magic(self):
        try:
            self.fh = open(LOCK_PATH, 'w')
            fcntl.lockf(self.fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except EnvironmentError:
            if self.fh is not None:
                self.is_running = True
            else:
                raise

    def clean_up(self):
        try:
            if self.fh is not None:
                fcntl.lockf(self.fh, fcntl.LOCK_UN)
                self.fh.close()  # ???
                os.unlink(LOCK_PATH)
        except Exception as e_err:
            LOG.exception(e_err)
            raise  # for debugging purposes, do not raise it on production


def daemonize():
    """Taken from twisted.scripts._twistd_unix.py
    """
    if os.fork():  # launch child and...
        os._exit(0)  # kill off parent
    os.setsid()
    if os.fork():  # launch child and...
        os._exit(0)  # kill off parent again.
    os.umask(127)
    null = os.open('/dev/null', os.O_RDWR)
    for i in range(3):
        try:
            os.dup2(null, i)
        except OSError as e:
            if e.errno != errno.EBADF:
                raise
    os.close(null)


def handle_signals():
    """Handle Signals

    typing the interrupt character (probably Ctrl-C) causes SIGINT to be sent
    typing the quit character (probably Ctrl-\) sends SIGQUIT.
    hanging up the phone (modem) sends SIGHUP
    typing the stop character (probably Ctrl-Z) sends SIGSTOP.
    """
    LOG.info('Setting up signal handlers.')
    if platform.uname()[0] != 'Windows':
        signal.signal(signal.SIGHUP, SigHupHandler)
    signal.signal(signal.SIGINT, SigIntHandler)
    signal.signal(signal.SIGTERM, SigTermHandler)


def SigHupHandler(signum, _stackframe):
    """
    """
    LOG.debug('Hup Signal handler called with signal {}'.format(signum))
    g_Api.Stop()
    g_Api.Start()


def SigIntHandler(signum, _stackframe):
    """ SigInt
    interrupt character (probably Ctrl-C)
    """
    LOG.debug('SigInt - Signal handler called with signal {}'.format(signum))
    LOG.info("Interrupted.\n\n\n")
    g_Api.Quit()
    exit


def SigTermHandler(signum, _stackframe):
    """SigTerm
    """
    LOG.debug('SigTerm - Signal handler called with signal {}'.format(signum))
    LOG.info('SigTerm \n')
    exit


def SigKillHandler(signum, _stackframe):
    """
    """
    LOG.debug('SigKill - Signal handler called with signal {}'.format(signum))
    LOG.info('SigKill \n')
    exit


class Api:
    """
    """

    m_core = None
    m_pyhouse_obj = {}

    def __init__(self):
        """ This is the startup of the entire system.
        All permanent services are started here.
        These Core routines are an integral part of the daemon process.

        Notice that the reactor starts here as the very last step here and that
        call never returns until the reactor is stopped (permanent stoppage).
        """
        global g_Api
        g_Api = self
        self.m_core = core.Api()
        self.m_core._init_core()
        LOG.info('Initialized.\n==================================================================\n')

    def LoadConfig(self):
        """ This loads all the configuration.
        """
        self.m_core.LoadConfig()
        self.m_pyhouse_obj._Twisted.Reactor.callLater(3, self.Start)
        LOG.info("Loaded Config - Version:{}\n======================== Loaded Config Files ========================\n".format(__version__))
        pass

    def Start(self):
        """ This is automatically invoked when the reactor starts from Api().
        """
        print('Reactor is now running.')
        LOG.info('Starting - Reactor is now running.')
        self.m_core.Start()
        LOG.info('Everything has been started\n-----------------------------------------\n')

    def Stop(self):
        """Stop various modules to prepare for restarting them.
        """
        self.m_core.Stop()
        LOG.info("Stopped.\n")

    def Quit(self):
        """Prepare to exit all of PyHouse.
        """
        LOG.debug('Running Quit now.')
        self.Stop()
        self.m_pyhouse_obj._Twisted.Reactor.stop()


class BeforeReactor(Api):
    """ This class is for initialization before the reactor starts.
    It is run right after Singleton protection is invoked.
    """

    m_pyhouse_obj = None

    def start_setup(self):
        """
        Notice that the reactor starts here as the very last step here and that
        call never returns until the reactor is stopped (permanent stoppage).
        """
        print('PyHouse.BeforeReactor()')  # For development - so we can see when we get to this point...
        CheckInitialSetup()
        core.Api()
        #
        #  When the reactor stops we continue here
        #
        LOG.info("PyHouse says Bye Now.\n")
        print('PyHouse is exiting.')
        raise SystemExit("PyHouse says Bye Now.")


if __name__ == "__main__":
    si = Singleton()
    try:
        if si.is_running:
            sys.exit("This app is already running!")
        BeforeReactor().start_setup()
    finally:
        si.clean_up()

#  ## END DBK
