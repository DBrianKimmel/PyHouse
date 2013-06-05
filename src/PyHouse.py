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

"""

# Import system type stuff
import errno
import logging
import optparse
import os
import platform
import signal
import sys
from twisted.internet import reactor
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
# from src.configure import gui
from src.utils import log
from src.utils import xml_tools
from src.housing import houses
from src.web import web_server


g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 - Config file handling

g_logger = None


callWhenRunning = reactor.callWhenRunning
reactorrun = reactor.run
reactorstop = reactor.stop


class PyHouseData(object):
    """The master object, contains all other 'configuration' objects.
    """

    def __init__(self):
        self.Api = None
        self.WebData = None
        self.WebApi = None
        self.LogsData = None
        self.LogsApi = None
        self.HousesData = None9
        self.HousesApi = None
        self.XmlRoot = None


class OptionParser(optparse.OptionParser):
    """
    Simple wrapper to add list of available plugins to help
    message, but only if help message is really printed
    """
    def print_help(self, p_file = None):
        sys.argv = sys.argv[:1]
        optparse.OptionParser.print_help(self, p_file)


class ConfigFileHandler(xml_tools.ConfigFile):
    """Initial read and final write of the config file.
    """

    m_xml_filename = None
    m_xmltree_root = None

    def __init__(self):
        """Open the xml config file.

        If the file is missing, an empty minimal skeleton is created.
        """
        if g_debug >= 2:
            print "PyHouse.ConfigFileHandler.__init__()"
        self._find_config_file_name()

    def _find_config_file_name(self):
        if g_debug >= 2:
            print "PyHouse._find_config_file_name()"
        self.m_xml_filename = xml_tools.open_config_file()

    def parse_xml(self):
        if g_debug >= 2:
            print "PyHouse._parse_xml()"
        try:
            self.m_xmltree = ET.parse(self.m_xml_filename)
        except SyntaxError:
            self.create_empty_config_file(self.m_xml_filename)
            self.m_xmltree = ET.parse(self.m_xml_filename)
        self.m_xmltree_root = self.m_xmltree.getroot()
        return self.m_xmltree_root

    def read_xml_config_file(self):
        pass

    def write_xml_config_file(self, p_xml):
        """Replace the data in the 'Houses' section with the current data.
        """
        if g_debug >= 2:
            print "houses.write_xml_config_file() - Writing xml file to:{0:}".format(self.m_xml_filename)
        self.m_xmltree_root = self.m_xmltree.getroot()
        self.m_xmltree_root = p_xml
        self.write_xml_file(self.m_xmltree, self.m_xml_filename)


def daemonize():
    """Taken from twisted.scripts._twistd_unix.py
    """
    if g_debug >= 1:
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

def __opt_option(_option, _opt, value, parser):
    try:
        key, val = value.split(':', 1)
    except KeyError:
        key = value
        val = ''
    parser.values.options[key] = val

def setConfigFile():
    def findConfigDir():
        try:
            configDir = os.path.expanduser('~')
        except TypeError:
            configDir = os.getcwd()
        return configDir
    return os.path.join(findConfigDir(), '.PyHouse/PyHouse.xml')

def handle_signals():
    if platform.uname()[0] != 'Windows':
        signal.signal(signal.SIGHUP, SigHupHandler)
    signal.signal(signal.SIGINT, SigIntHandler)

def SigHupHandler(signum, _stackframe):
    if g_debug >= 1:
        print 'Hup Signal handler called with signal', signum
    API().Stop()
    API().Start()

def SigIntHandler(signum, _stackframe):
    if g_debug >= 1:
        print 'Signal handler called with signal', signum
    API().Stop()
    exit


class API(object):
    """
    """

    def __init__(self):
        """This is the startup of the entire system.
        All permanent services are started here.
        These core routines are an integral part of the daemon process.

        Notice that the reactor starts here as the very last step and that
        call never returns until the reactor is stopped (permanent stoppage).
        """
        if g_debug >= 1:
            print "\nPyHouse.API.__init__() - very beginning..."
        handle_signals()
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.Api = self
        l_cfg = ConfigFileHandler()
        self.m_pyhouses_obj.XmlRoot = l_cfg.parse_xml()
        self.m_pyhouses_obj.LogsApi = log.API()
        self.m_pyhouses_obj.LogsData = self.m_pyhouses_obj.LogsApi.Start(self.m_pyhouses_obj)

        global g_logger
        g_logger = logging.getLogger('PyHouse         ')
        g_logger.info("Initializing.\n")

        self.m_pyhouses_obj.HousesApi = houses.API()
        self.m_pyhouses_obj.WebApi = web_server.API(self)
        callWhenRunning(self.Start)
        g_logger.info("Initialized.\n")
        # reactor never returns so must be last - Event loop will now run
        reactorrun()
        raise SystemExit, "PyHouse says Bye Now."

    def Start(self):
        """New.  This will start all non-core services.
        This may be called multiple times along with stop to rerun various modules
        it is automatically invoked when the reactor starts from API().
        """
        if g_debug >= 1:
            print "\nPyHouse.Start()"
        g_logger.info("Starting.")
        self.m_pyhouses_obj.HousesData = self.m_pyhouses_obj.HousesApi.Start(self.m_pyhouses_obj)
        self.m_pyhouses_obj.WebData = self.m_pyhouses_obj.WebApi.Start(self.m_pyhouses_obj)
        g_logger.info("Started.\n")
        if g_debug >= 1:
            print "PyHouse all is started and running now.\n"

    def Stop(self):
        """Stop various modules to prepare for restarting them.
        """
        if g_debug >= 1:
            print "\nPyHouse.Stop()"
        global g_logger
        g_logger = logging.getLogger('PyHouse')
        g_logger.info("Stopping has begun.\n")
        self.m_pyhouses_obj.HousesApi.Stop()
        self.m_pyhouses_obj.WebApi.Stop()
        try:
            g_logger.info("Stopped.\n\n\n")
        except AttributeError, emsg:
            print "Got attribute error while trying to log 'Stopped' from PyHouse. ", emsg

    def Quit(self):
        """Prepare to exit all of pyhouse
        """
        if g_debug >= 1:
            print "\nPyHouse.Quit()"
        self.Stop()
        self.m_pyhouses_obj.LogsApi.Stop()
        reactorstop()


if __name__ == "__main__":

    if g_debug >= 1:
        print "MAIN"
    API()

# ## END DBK
