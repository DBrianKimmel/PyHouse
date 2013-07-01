#!/usr/bin/env python

""" PyHouse.py - Run the python version house automation.

see main.__init__.py for core documentation.

During development this is run by hand.
It is, however, planned to be a daemon that is kicked off on system start-up.
It is intended to run on everything from a small, low power bare bones system
to a server running multiple houses in several, widespread locations.

The system is controlled via a browser connecting to a web server that will
be either integrated or separate from PyHouse.

TODO:
        Find proper ports for controllers
        set proper permissions on controller devices
        Add DynDns to gui for house
        Add interfaces, move interface code out of controllers
        Enter key save in gui
        Set focus in each gui
        Setup to allow house add rooms lights etc seem ok
        Save house info for 'new' house


MIT License

Copyright (c) 2010-2013 by D. Brian Kimmel

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

"""

__author__ = "D. Brian Kimmel"
__copyright__ = "2010-2013 by D. Brian Kimmel"
__version_info__ = (1, 0, 0)
__version__ = '.'.join(map(str, __version_info__))


# Import system type stuff
import errno
import logging
import os
import platform
import signal
from twisted.internet import reactor
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from src.utils import log
from src.utils import xml_tools
from src.housing import houses
from src.web import web_server


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# + = NOT USED HERE
g_logger = None


callWhenRunning = reactor.callWhenRunning
reactorrun = reactor.run
reactorstop = reactor.stop


class PyHouseData(object):
    """The master object, contains all other 'configuration' objects.
    """

    def __init__(self):
        self.API = None
        self.WebData = None
        self.WebAPI = None
        self.LogsData = None
        self.LogsAPI = None
        self.HousesData = None
        self.HousesAPI = None
        self.XmlRoot = None
        self.XmlFileName = ''

    def __str__(self):
        l_ret = "PyHouseData:: "
        l_ret += "WebData:{0:}".format(self.WebData)
        l_ret += "WebAPI:{0:}".format(self.WebAPI)
        l_ret += "LogsData:{0:}".format(self.LogsData)
        l_ret += "LogsAPI:{0:}".format(self.LogsAPI)
        l_ret += "HousesData:{0:}".format(self.HousesData)
        l_ret += "HousesAPI:{0:}".format(self.HousesAPI)
        l_ret += "XmlRoot:{0:}".format(self.XmlRoot)
        l_ret += "XmlFileName:{0:}".format(self.XmlFileName)
        return l_ret

    def __repr__(self):
        l_ret = "{"
        l_ret += "'WebData':'{0:}', ".format(self.WebData)
        l_ret += "'LogsData':'{0:}', ".format(self.LogsData)
        l_ret += "'HousesData':'{0:}', ".format(self.HousesData)
        l_ret += "'XmlFileName':'{0:}'".format(self.XmlFileName)
        l_ret += "}"
        return l_ret


def daemonize():
    """Taken from twisted.scripts._twistd_unix.py
    """
    if g_debug >= 2:
        print "PyHouse is making itself into a daemon !!"
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
        except OSError, e:
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
    if g_debug >= 3:
        print 'Hup Signal handler called with signal', signum
    API().Stop()
    API().Start()

def SigIntHandler(signum, _stackframe):
    """interrupt character (probably Ctrl-C)
    """
    if g_debug >= 3:
        print 'SigInt - Signal handler called with signal', signum
    g_logger.info("Interrupted.\n\n\n")
    reactorstop()
    print "Interrupted."
    exit


class Utilities(object):
    """
    """

    def import_config_info(self, p_pyhouses_obj):
        if g_debug >= 3:
            print "PyHouse.Utilities.import_config_info()"
        p_pyhouses_obj.XmlFileName = xml_tools.open_config_file()
        try:
            l_xmltree = ET.parse(p_pyhouses_obj.XmlFileName)
        except SyntaxError:
            self.create_empty_config_file(p_pyhouses_obj.XmlFileName)
            l_xmltree = ET.parse(p_pyhouses_obj.XmlFileName)
        p_pyhouses_obj.XmlRoot = l_xmltree.getroot()

    def export_config_info(self, p_pyhouses_obj):
        """Replace the data in the xml file with the current data.
        """
        if g_debug >= 3:
            print "PyHouse.export_config_info() - Writing XML file to:{0:}".format(p_pyhouses_obj.XmlFileName)
        self.m_xmltree_root = p_pyhouses_obj.XmlRoot
        xml_tools.write_xml_file(p_pyhouses_obj.XmlRoot, p_pyhouses_obj.XmlFileName)

    def init_logs(self, p_pyhouses_obj):
        p_pyhouses_obj.LogsAPI = log.API()
        p_pyhouses_obj.LogsData = p_pyhouses_obj.LogsAPI.Start(p_pyhouses_obj)


class API(Utilities):
    """
    """

    def __init__(self):
        """This is the startup of the entire system.
        All permanent services are started here.
        These core routines are an integral part of the daemon process.

        Notice that the reactor starts here as the very last step and that
        call never returns until the reactor is stopped (permanent stoppage).
        """
        if g_debug >= 2:
            print "\nPyHouse.API()"
            import sys
            print "  SYS.Path =", sys.path
            print "---\n\n"
        handle_signals()
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.API = self
        self.import_config_info(self.m_pyhouses_obj)
        self.init_logs(self.m_pyhouses_obj)
        global g_logger
        g_logger = logging.getLogger('PyHouse         ')
        g_logger.info("Initializing PyHouse.\n")
        if g_debug >= 1:
            g_logger.info("Logging level is {0:}".format(g_debug))
        self.m_pyhouses_obj.HousesAPI = houses.API()
        self.m_pyhouses_obj.WebAPI = web_server.API()
        callWhenRunning(self.Start)
        g_logger.info("Initialized.\n")
        if g_debug >= 1:
            g_logger.info("PyHouseData:{0:}\n".format(self.m_pyhouses_obj))
        # reactor never returns so must be last - Event loop will now run
        reactorrun()
        raise SystemExit, "PyHouse says Bye Now."

    def Start(self):
        """This is automatically invoked when the reactor starts from API().
        """
        if g_debug >= 2:
            print "\nPyHouse.API.Start() - Starting"
        self.m_pyhouses_obj.HousesData = self.m_pyhouses_obj.HousesAPI.Start(self.m_pyhouses_obj)
        self.m_pyhouses_obj.WebData = self.m_pyhouses_obj.WebAPI.Start(self.m_pyhouses_obj)
        g_logger.info("Started.\n")
        if g_debug >= 2:
            print "    PyHouse all is started and running now.\n"

    def Stop(self):
        """Stop various modules to prepare for restarting them.
        """
        if g_debug >= 2:
            print "\nPyHouse.API.Stop() - Stopping."
        self.m_pyhouses_obj.HousesAPI.Stop()
        self.m_pyhouses_obj.WebAPI.Stop()
        self.export_config_info(self.m_pyhouses_obj)
        g_logger.info("Stopped.\n\n\n")

    def Reload(self, p_pyhouses_obj):
        """Update XML file with current info.
        """
        if g_debug >= 2:
            print "\nPyHouse.API.Reload() - Reloading"
        l_root_xml = ET.Element("PyHouse")
        l_root_xml.append(p_pyhouses_obj.HousesAPI.Reload(p_pyhouses_obj))
        p_pyhouses_obj.WebAPI.Reload(p_pyhouses_obj)
        self.export_config_info(p_pyhouses_obj)
        g_logger.info("Reloaded.\n\n\n")

    def Quit(self):
        """Prepare to exit all of pyhouse
        """
        if g_debug >= 2:
            print "\nPyHouse.API.Quit() - Quitting"
        self.Stop()
        g_logger.info("Quit.\n\n\n")
        reactorstop()


if __name__ == "__main__":
    API()

# ## END DBK