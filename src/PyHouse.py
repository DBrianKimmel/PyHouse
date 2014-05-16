#!/usr/bin/env python

"""
-*- test-case-name: PyHouse.Modules.test.test_PyHouse -*-

@name: PyHouse/Modules/Pyhouse.py
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
from Modules.Core.data_objects import PyHouseData
from Modules.Core import setup
from Modules.utils import pyh_log
from Modules.utils import xml_tools

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

def SigHupHandler(signum, _stackframe):
    """
    """
    if g_debug >= 1:
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


class Utilities(object):

    def read_xml_config_info(self, p_pyhouses_obj):
        """This will read the XML config file(s).
        There may be a device config file.
        This puts the XML tree and file name in the pyhouses object for use by various modules.
        """
        if g_debug >= 1:
            LOG.debug("Utilities.read_xml_config_info()")
        p_pyhouses_obj.XmlFileName = xml_tools.open_config_file()
        try:
            l_xmltree = ET.parse(p_pyhouses_obj.XmlFileName)
        except SyntaxError:
            xml_tools.ConfigFile().create_empty_config_file(p_pyhouses_obj.XmlFileName)
            l_xmltree = ET.parse(p_pyhouses_obj.XmlFileName)
        p_pyhouses_obj.XmlRoot = l_xmltree.getroot()


class API(Utilities):
    """
    """
    m_pyhouses_obj = PyHouseData()

    def __init__(self):
        """This is the startup of the entire system.
        All permanent services are started here.
        These Core routines are an integral part of the daemon process.

        Notice that the reactor starts here as the very last step here and that
        call never returns until the reactor is stopped (permanent stoppage).
        """
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.Reactor = reactor
        self.m_pyhouses_obj.Application = Application('PyHouse')
        self.m_pyhouses_obj.API = self  # Only used by web server to reload - Do we need this?
        global g_API
        g_API = self
        handle_signals()
        self.read_xml_config_info(self.m_pyhouses_obj)
        self.m_pyhouses_obj.LogsAPI = l_logs = pyh_log.API()
        l_logs.Start(self.m_pyhouses_obj)
        # global LOG
        LOG.info("Initializing PyHouse.\n\n")
        #
        self.m_pyhouses_obj.CoreAPI = setup.API()
        self.m_pyhouses_obj.Reactor.callWhenRunning(self.Start)
        LOG.info("Initialized.\n")
        self.m_pyhouses_obj.Reactor.run()  # reactor never returns so must be last - Event loop will now run
        LOG.info("PyHouse says Bye Now.\n")
        raise SystemExit, "PyHouse says Bye Now."

    def Start(self):
        """This is automatically invoked when the reactor starts from API().
        """
        self.m_pyhouses_obj.CoreAPI.Start(self.m_pyhouses_obj)
        self.m_pyhouses_obj.HousesAPI.Start(self.m_pyhouses_obj)
        self.m_pyhouses_obj.WebAPI.Start(self.m_pyhouses_obj)
        LOG.info("Started.\n")

    def Stop(self):
        """Stop various modules to prepare for restarting them.
        """
        LOG.info("Saving all data to XML file.")
        l_xml = ET.Element("PyHouse")
        self.m_pyhouses_obj.WebAPI.Stop(l_xml)
        self.m_pyhouses_obj.LogsAPI.Stop(l_xml)
        self.m_pyhouses_obj.HousesAPI.Stop(l_xml)
        self.m_pyhouses_obj.CoreAPI.Stop(l_xml)
        xml_tools.write_xml_file(l_xml, self.m_pyhouses_obj.XmlFileName)
        LOG.info("XML file has been updated.")
        LOG.info("Stopped.\n\n")

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
        LOG.info("Quit.\n\n\n")
        self.m_pyhouses_obj.Reactor.stop()


if __name__ == "__main__":
    API()

# ## END DBK
