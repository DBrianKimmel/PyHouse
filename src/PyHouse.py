#!/usr/bin/env python
"""
-*- test-case-name: PyHouse.src.Modules.test.test_PyHouse -*-

@name: PyHouse/src/Modules/Pyhouse.py

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
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
__version_info__ = (1, 2, 0)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
import errno
import os
import platform
import signal
from twisted.internet import reactor
from twisted.application.service import Application
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import PyHouseData, PyHouseAPIs, ComputerData, CoreServicesData, HouseInformation, TwistedInfo, XmlData
from Modules.Core import setup
from Modules.utils import pyh_log
from Modules.utils import xml_tools
# from Modules.utils.tools import PrettyPrintAny

g_debug = 0
LOG = pyh_log.getLogger('PyHouse             ')


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
    os.umask(077)
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

    def read_xml_config_info(self, p_pyhouse_obj):
        """This will read the XML config file(s).
        This puts the XML tree and file name in the pyhouse object for use by various modules.
        """
        if g_debug >= 1:
            LOG.debug("Utilities.read_xml_config_info()")
        p_pyhouse_obj.Xml.XmlFileName = xml_tools.open_config_file()
        try:
            l_xmltree = ET.parse(p_pyhouse_obj.Xml.XmlFileName)
        except SyntaxError:
            xml_tools.ConfigFile().create_empty_config_file(p_pyhouse_obj.Xml.XmlFileName)
            l_xmltree = ET.parse(p_pyhouse_obj.Xml.XmlFileName)
        p_pyhouse_obj.Xml.XmlRoot = l_xmltree.getroot()
        p_pyhouse_obj.Xml.XmlParsed = p_pyhouse_obj.Xml.XmlRoot

    def build_twisted_info(self, _p_pyhouse_obj):
        l_ret = TwistedInfo()
        l_ret.Reactor = reactor
        l_ret.Application = Application('PyHouse')
        return l_ret

    def build_pyhouse_obj(self):
        l_pyhouse_obj = PyHouseData()
        l_pyhouse_obj.Computer = ComputerData()
        l_pyhouse_obj.House = HouseInformation()
        l_pyhouse_obj.Services = CoreServicesData()
        l_pyhouse_obj.Twisted = self.build_twisted_info(l_pyhouse_obj)
        l_pyhouse_obj.Xml = XmlData()
        #
        l_pyhouse_obj.House.APIs = PyHouseAPIs()
        return l_pyhouse_obj


class API(Utilities):
    """
    """
    m_pyhouse_obj = PyHouseData()

    def __init__(self):
        """This is the startup of the entire system.
        All permanent services are started here.
        These Core routines are an integral part of the daemon process.

        Notice that the reactor starts here as the very last step here and that
        call never returns until the reactor is stopped (permanent stoppage).
        """
        print('PyHouse Start Initializing')
        self.m_pyhouse_obj = self.build_pyhouse_obj()
        self.m_pyhouse_obj.House.APIs.PyHouseAPI = self  # Only used by web server to reload - Do we need this?
        global g_API
        g_API = self
        handle_signals()
        self.read_xml_config_info(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.APIs.LogsAPI = pyh_log.API()
        self.m_pyhouse_obj.House.APIs.LogsAPI.Start(self.m_pyhouse_obj)
        # PrettyPrintAny(self.m_pyhouse_obj, 'PyHouse 1')
        LOG.info("Initializing PyHouse.\n\n")
        #
        self.m_pyhouse_obj.House.APIs.CoreAPI = setup.API()
        self.m_pyhouse_obj.Twisted.Reactor.callWhenRunning(self.Start)

        LOG.info("Initialized.\n")
        self.m_pyhouse_obj.Twisted.Reactor.run()  # reactor never returns so must be last - Event loop will now run
        LOG.info("PyHouse says Bye Now.\n")
        raise SystemExit, "PyHouse says Bye Now."

    def Start(self):
        """This is automatically invoked when the reactor starts from API().
        """
        self.m_pyhouse_obj.House.APIs.CoreAPI.Start(self.m_pyhouse_obj)
        LOG.info("Started.\n")

    def Stop(self):
        """Stop various modules to prepare for restarting them.
        """
        LOG.info("Saving all data to XML file.")
        l_xml = ET.Element("PyHouse")
        self.m_pyhouse_obj.House.APIs.CoreAPI.Stop(l_xml)
        self.m_pyhouse_obj.House.APIs.LogsAPI.Stop(l_xml)
        xml_tools.write_xml_file(l_xml, self.m_pyhouse_obj.Xml.XmlFileName)

    def Reload(self, _p_pyhouses_obj):
        """Update XML file with current info.
        """
        self.Stop()
        self.Start()
        LOG.info("Reloaded.\n\n\n")

    def Quit(self):
        """Prepare to exit all of pyhouse
        """
        self.Stop()
        self.m_pyhouse_obj.Twisted.Reactor.stop()


if __name__ == "__main__":
    API()

# ## END DBK
