#!/usr/bin/env python
"""
-*- test-case-name: PyHouse.src.Modules.test.test_PyHouse -*-

@name: PyHouse/src/Modules/Pyhouse.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2010-2014 by D. Brian Kimmel
@license: MIT License
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
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


                  cp   /c/Users/briank/Documents/GitHub/PyHouse/admin/config/cannontrail_master.xml   /c/etc//pyhouse//master.xml

                  > error ; > debug ; clear ; tail -f debug

Uses I{Epytext} mark-up for documentation.

see C{Modules.__init__.py} for Core documentation.

During development this is run by hand.
It is, however, planned to be a daemon that is kicked off on system start-up.
It is intended to run on everything from a small, low power bare bones system to a server running multiple
 houses in several, widespread locations.
It now (2013) runs on Raspberry Pi so that is the primary target.


The system is controlled via a browser connecting to a web server that will be integrated into PyHouse.

@TODO:
        Find proper ports for controllers
        set proper permissions on controller devices
        Add interfaces, move interface code out of controllers
        Setup to allow house add rooms lights etc
        Save house info for 'new' house.
"""

__author__ = "D. Brian Kimmel"
__copyright__ = "2010-2014 by D. Brian Kimmel"
__version_info__ = (1, 4, 0)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
import errno
import os
import platform
import signal
from twisted.internet import reactor
from twisted.application.service import Application

# Import PyMh files and modules.
from Modules.Core import data_objects
from Modules.Core import setup
from Modules.Computer import logging_pyh as Logger

g_debug = 0
g_API = None
LOG = Logger.getLogger('PyHouse                ')


def daemonize():
    """Taken from twisted.scripts._twistd_unix.py
    """
    if g_debug >= 1:
        LOG.debug("PyHouse is making itself into a daemon !!")
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


def SigHupHandler(signum, _stackframe):
    """
    """
    # if g_debug >= 1:
    LOG.debug('Hup Signal handler called with signal {0:}'.format(signum))
    g_API.Stop()
    g_API.Start()


def SigIntHandler(signum, _stackframe):
    """interrupt character (probably Ctrl-C)
    """
    # if g_debug >= 1:
    LOG.debug('SigInt - Signal handler called with signal {0:}'.format(signum))
    LOG.info("Interrupted.\n\n\n")
    g_API.Stop()
    g_API.Quit()
    exit

def SigKillHandler(signum, _stackframe):
    """
    """
    LOG.debug('SigInt - Signal handler called with signal {0:}'.format(signum))
    LOG.info('SigKill \n')
    exit


class Utilities(object):
    """
    """

    def do_daemon_stuff(self):
        handle_signals()
        pass


class API(Utilities):
    """
    """
    m_pyhouse_obj = data_objects.PyHouseData()

    def _setup_apis(self):
        self.m_pyhouse_obj.APIs.Comp = data_objects.CompAPIs()
        self.m_pyhouse_obj.APIs.House = data_objects.HouseAPIs()
        self.m_pyhouse_obj.APIs.PyHouseAPI = self
        self.m_pyhouse_obj.APIs.CoreSetupAPI = setup.API()
        return self.m_pyhouse_obj

    def _create_pyhouse_obj(self):
        self.m_pyhouse_obj = data_objects.PyHouseData()
        self.m_pyhouse_obj.APIs = data_objects.PyHouseAPIs()
        self.m_pyhouse_obj.Computer = data_objects.ComputerInformation()
        self.m_pyhouse_obj.House = data_objects.HouseInformation()
        self.m_pyhouse_obj.Services = data_objects.CoreServicesInformation()
        self.m_pyhouse_obj.Twisted = data_objects.TwistedInformation()
        self.m_pyhouse_obj.Xml = data_objects.XmlInformation()
        #
        self.m_pyhouse_obj.Twisted.Reactor = reactor
        self.m_pyhouse_obj.Twisted.Application = Application('PyHouse')
        self.m_pyhouse_obj.Xml.XmlFileName = '/etc/pyhouse/master.xml'
        return self.m_pyhouse_obj


    def __init__(self):
        """This is the startup of the entire system.
        All permanent services are started here.
        These Core routines are an integral part of the daemon process.

        Notice that the reactor starts here as the very last step here and that
        call never returns until the reactor is stopped (permanent stoppage).
        """
        self.do_daemon_stuff()
        global g_API
        g_API = self
        self._create_pyhouse_obj()
        self._setup_apis()
        self.m_pyhouse_obj.Twisted.Reactor.callWhenRunning(self.Start)
        self.m_pyhouse_obj.Twisted.Reactor.run()  # reactor never returns so must be last - Event loop will now run
        #  When the reactor stops we continue here
        LOG.info("PyHouse says Bye Now.\n")
        raise SystemExit("PyHouse says Bye Now.")

    def Start(self):
        """This is automatically invoked when the reactor starts from API().
        """
        self.m_pyhouse_obj.APIs.CoreSetupAPI.Start(self.m_pyhouse_obj)

    def Stop(self):
        """Stop various modules to prepare for restarting them.
        """
        self.m_pyhouse_obj.APIs.CoreSetupAPI.Stop()
        LOG.info("Stopped.\n")

    def SaveXml(self, _p_pyhouse_obj):
        """Update XML file with current info.
        Keep on running after the snapshot.
        """
        LOG.info("Saving XML")
        self.m_pyhouse_obj.APIs.CoreSetupAPI.WriteXml()
        LOG.info("Saved XML.\n")

    def Quit(self):
        """Prepare to exit all of PyHouse.
        """
        self.Stop()
        self.m_pyhouse_obj.Twisted.Reactor.stop()


if __name__ == "__main__":
    API()

# ## END DBK
