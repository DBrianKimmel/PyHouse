#!/usr/bin/env python3
"""
@name:      PyHouse/Project/src/Pyhouse.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2019 by D. Brian Kimmel
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
        _APIs           Internal
        Computer        Configuration File
        House           Configuration File
        Services        Internal
        Twisted         Internal
        Xml             Internal

Uses I{Epytext} mark-up for documentation.

see C{Modules.__init__.py} for Core documentation.

During development this is run by hand.
It is, however, planned to be a daemon that is kicked off on system start-up.
It is intended to run on everything from a small, low power bare bones system to a server running multiple
 houses in several, widespread locations.
It now (2013) runs on Raspberry Pi so that is the primary target.

The system is controlled via a browser connecting to a web server that is integrated into PyHouse.

There are two components of this software.
The first is "computer' and is started first.
The second is 'house' and is started second.
See those modules to find out what each does.

@TODO:
        Find proper ports for controllers
        set proper permissions on controller devices

Idea Links:
  https://github.com/TheThingSystem/home-controller forked from automategreen/home-controller
  https://github.com/zonyl/pytomation
  https://github.com/king-dopey/pytomation forked from zonyl/pytomation
  http://leftovercode.info/smartlinc.php
  http://misterhouse.sourceforge.net/lib/Insteon/AllLinkDatabase.html
  https://github.com/hollie/misterhouse/


    SmartHome Wiki: Using Custom Commands in SmartLinc
    SmartHome Forum: SmartLinc Direct Command for Light Status?
    SmartHome Forum: Custom Screens on the SmartLinc
    SmartHome Wiki: Insteon Command Table
    Smarthome Forum: SmartLinc web automation solved
    SmartHome Forum: 2412N Insteon Central Controller - Software
    Ramp Rate
    Insteon Commands


"""

__updated__ = '2019-07-07'
__version_info__ = (19, 6, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import errno
import fcntl
import os
import platform
import signal
import sys
from twisted.internet import reactor

#  Import PyHouse files and modules.
from Modules.Core import setup_pyhouse
from Modules.Core.data_objects import \
    UuidInformation, \
    PyHouseAPIs, \
    PyHouseInformation, \
    TwistedInformation, \
    UuidData, CoreAPIs
from Modules.Core.Utilities.config_tools import ConfigInformation
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse                ')

LOCK_PATH = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "lock")
g_API = None


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
    g_API.Stop()
    g_API.Start()


def SigIntHandler(signum, _stackframe):
    """ SigInt
    interrupt character (probably Ctrl-C)
    """
    LOG.debug('SigInt - Signal handler called with signal {}'.format(signum))
    LOG.info("Interrupted.\n\n\n")
    g_API.Quit()
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


class API:
    """
    """

    m_pyhouse_obj = {}

    def __init__(self):
        """ This is the startup of the entire system.
        All permanent services are started here.
        These Core routines are an integral part of the daemon process.

        Notice that the reactor starts here as the very last step here and that
        call never returns until the reactor is stopped (permanent stoppage).
        """
        global g_API
        g_API = self
        LOG.info('Initialized.\n==================================================================\n')

    def LoadConfig(self, p_pyhouse_obj: object):
        """ This loads all the configuration.
        """
        p_pyhouse_obj._APIs.Core.CoreSetupAPI.LoadConfig(p_pyhouse_obj)
        p_pyhouse_obj._Twisted.Reactor.callLater(3, self.Start)
        LOG.info("Loaded Config - Version:{}\n======================== Loaded Config Files ========================\n".format(__version__))
        pass

    def Start(self):
        """ This is automatically invoked when the reactor starts from API().
        """
        print('Reactor is now running.')
        LOG.info('Starting - Reactor is now running.')
        self.m_pyhouse_obj._APIs.Core.CoreSetupAPI.Start()
        LOG.info('Everything has been started\n-----------------------------------------\n')

    def SaveConfig(self, p_pyhouse_obj):
        """Update XML file with current info.
        Keep on running after the snapshot.
        """
        LOG.info("Saving Config")
        self.m_pyhouse_obj._APIs.Core.CoreSetupAPI.SaveConfig(p_pyhouse_obj)
        LOG.info("Saved Config.\n")

    def Stop(self):
        """Stop various modules to prepare for restarting them.
        """
        self.m_pyhouse_obj._APIs.Core.CoreSetupAPI.Stop()
        LOG.info("Stopped.\n")

    def Quit(self):
        """Prepare to exit all of PyHouse.
        """
        LOG.debug('Running Quit now.')
        self.Stop()
        self.m_pyhouse_obj._Twisted.Reactor.stop()


class BeforeReactor(API):
    """ This class is for initialization before the reactor starts.
    It is run right after Singleton protection is invoked.
    """

    def _create_pyhouse_obj(self):
        """ This creates the master PyHouse_Obj from scratch.
        """
        self.m_pyhouse_obj = PyHouseInformation()

    def _setup_APIs(self):
        """
        """
        self.m_pyhouse_obj._APIs = PyHouseAPIs()
        self.m_pyhouse_obj._APIs.Core = CoreAPIs()
        self.m_pyhouse_obj._APIs.Core.PyHouseMainAPI = self

    def _setup_Config(self):
        """
        """
        self.m_pyhouse_obj._Config = ConfigInformation()

    def _setup_Twisted(self):
        """
        """
        self.m_pyhouse_obj._Twisted = TwistedInformation()
        self.m_pyhouse_obj._Twisted.Reactor = reactor

    def _setup_Uuids(self):
        """
        """
        self.m_pyhouse_obj._Uuids = UuidInformation()
        self.m_pyhouse_obj._Uuids.All = UuidData()
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'SetupUuids-PyHouse', 190))

    def start_setup(self):
        """
        Notice that the reactor starts here as the very last step here and that
        call never returns until the reactor is stopped (permanent stoppage).
        """
        print('PyHouse.BeforeReactor()')  # For development - so we can see when we get to this point...
        self._create_pyhouse_obj()
        self._setup_APIs()
        self._setup_Config()
        # _Families are set up in ???
        # _Parameters are set up in ???
        self._setup_Twisted()
        self._setup_Uuids()
        #
        self.m_pyhouse_obj._APIs.Core.CoreSetupAPI = setup_pyhouse.API(self.m_pyhouse_obj)
        #
        self.m_pyhouse_obj._Twisted.Reactor.callWhenRunning(self.LoadConfig, self.m_pyhouse_obj)
        LOG.info("Initialized - Version:{}\n======================== Initialized ========================\n".format(__version__))
        LOG.info('Starting Reactor...')
        self.m_pyhouse_obj._Twisted.Reactor.run()  # reactor never returns so must be last - Event loop will now run
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
