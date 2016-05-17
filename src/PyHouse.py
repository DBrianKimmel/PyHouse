#!/usr/bin/env python
"""
-*- test-case-name: PyHouse.src.test.test_PyHouse -*-

@name:      PyHouse/src/Pyhouse.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2016 by D. Brian Kimmel
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
        APIs            Internal
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
        Add interfaces, move interface code out of controllers
        Setup to allow house add rooms lights etc
        Save house info for 'new' house.
"""

#  Import system type stuff
import errno
import os
import platform
import signal
#  from twisted.application.service import Application
from twisted.internet import reactor

from Modules.Computer import logging_pyh as Logger
from Modules.Core import setup_pyhouse
from Modules.Core.data_objects import PyHouseData, PyHouseAPIs, TwistedInformation, CoreServicesInformation, XmlInformation

__author__ = "D. Brian Kimmel"
__copyright__ = "(c) 2010-2016 by D. Brian Kimmel"
__version_info__ = (1, 7, 2)
__version__ = '.'.join(map(str, __version_info__))


#  Import PyMh files and modules.
g_API = None
LOG = Logger.getLogger('PyHouse                ')


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
    """
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
    """interrupt character (probably Ctrl-C)
    """
    LOG.debug('SigInt - Signal handler called with signal {}'.format(signum))
    LOG.info("Interrupted.\n\n\n")
    g_API.Quit()
    exit


def SigTermHandler(signum, _stackframe):
    """
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


class Utilities(object):
    """
    """

    #  @staticmethod
    #  def do_setup_stuff(p_self):
    #    if platform.uname()[0] == 'Windows':
    #        from Modules.Core import setup_windows
    #        pass
    #    else:
    #        from Modules.Core.setup_linux import Linux
    #        l_linux = Linux()
    #    handle_signals()

    @staticmethod
    def _create_pyhouse_obj():
        l_pyhouse_obj = PyHouseData()
        l_pyhouse_obj.APIs = PyHouseAPIs()
        l_pyhouse_obj.Services = CoreServicesInformation()
        l_pyhouse_obj.Xml = XmlInformation()
        l_pyhouse_obj.Twisted = TwistedInformation()
        l_pyhouse_obj.Twisted.Reactor = reactor
        #  l_pyhouse_obj.Twisted.Application = Application('PyHouse')
        return l_pyhouse_obj


class API(object):
    """
    """

    def __init__(self):
        """This is the startup of the entire system.
        All permanent services are started here.
        These Core routines are an integral part of the daemon process.

        Notice that the reactor starts here as the very last step here and that
        call never returns until the reactor is stopped (permanent stoppage).
        """
        global g_API
        g_API = self
        #  Utilities.do_setup_stuff(self)
        p_pyhouse_obj = Utilities._create_pyhouse_obj()
        self.m_pyhouse_obj = p_pyhouse_obj
        print('PyHouse.API()')  # For development - so we  an see when we get to this point...
        p_pyhouse_obj.APIs.PyHouseMainAPI = self
        p_pyhouse_obj.APIs.CoreSetupAPI = setup_pyhouse.API(p_pyhouse_obj)
        p_pyhouse_obj.Twisted.Reactor.callWhenRunning(self.LoadXml, p_pyhouse_obj)
        p_pyhouse_obj.Twisted.Reactor.run()  # reactor never returns so must be last - Event loop will now run
        #
        #  When the reactor stops we continue here
        #
        LOG.info("PyHouse says Bye Now.\n")
        raise SystemExit("PyHouse says Bye Now.")

    def LoadXml(self, p_pyhouse_obj):
        """ This is automatically invoked when the reactor starts from API().
        """
        LOG.info('Loading XML')
        p_pyhouse_obj.APIs.CoreSetupAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj.Twisted.Reactor.callLater(10, self.Start)
        LOG.info('Loaded XML\n-----------------------------------------\n')

    def Start(self):
        """ This is automatically invoked when the reactor starts from API().
        """
        LOG.info('Starting')
        self.m_pyhouse_obj.APIs.CoreSetupAPI.Start()
        LOG.info('Everything has been started\n-----------------------------------------\n')

    def SaveXml(self, _p_pyhouse_obj):
        """Update XML file with current info.
        Keep on running after the snapshot.
        """
        LOG.info("Saving XML")
        self.m_pyhouse_obj.APIs.CoreSetupAPI.SaveXml()
        LOG.info("Saved XML.\n")

    def Stop(self):
        """Stop various modules to prepare for restarting them.
        """
        self.m_pyhouse_obj.APIs.CoreSetupAPI.Stop()
        LOG.info("Stopped.\n")

    def Quit(self):
        """Prepare to exit all of PyHouse.
        """
        LOG.debug('Running Quit now.')
        self.Stop()
        self.m_pyhouse_obj.Twisted.Reactor.stop()


if __name__ == "__main__":
    API()

#  ## END DBK
