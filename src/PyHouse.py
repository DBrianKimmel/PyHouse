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


g_debug = 3
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 - Config file handling

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
        l_ret = "PyHouseData(str):: "
        l_ret += "WebData:{0:}".format(self.WebData)
        return l_ret

    def __repr__(self):
        l_ret = "{"
        l_ret += "'WebData':'{0:}', ".format(self.WebData)
        l_ret += "'LogsData':'{0:}', ".format(self.LogsData)
        l_ret += "'HousesData':'{0:}', ".format(self.HousesData)
        l_ret += "'XmlFileName':'{0:}'".format(self.XmlFileName)
        l_ret += "}"
        return l_ret


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

    def __init__(self, p_pyhouses_obj):
        """Open the xml config file.

        If the file is missing, an empty minimal skeleton is created.
        """
        if g_debug >= 3:
            print "PyHouse.ConfigFileHandler()"
        self.m_pyhouses_obj = p_pyhouses_obj
        self.m_pyhouses_obj.XmlFileName = self._find_config_file_name()

    def _find_config_file_name(self):
        if g_debug >= 3:
            print "PyHouse._find_config_file_name()"
        l_filename = xml_tools.open_config_file()
        return l_filename

    def parse_xml(self):
        if g_debug >= 3:
            print "PyHouse.parse_xml()"
        try:
            self.m_xmltree = ET.parse(self.m_pyhouses_obj.XmlFileName)
        except SyntaxError:
            self.create_empty_config_file(self.m_pyhouses_obj.XmlFileName)
            self.m_xmltree = ET.parse(self.m_pyhouses_obj.XmlFileName)
        self.m_xmltree_root = self.m_xmltree.getroot()
        return self.m_xmltree_root

    def read_xml_config_file(self):
        pass

    def write_xml_config_file(self, p_pyhouses_obj):
        """Replace the data in the 'Houses' section with the current data.
        """
        if g_debug >= 3:
            print "houses.write_xml_config_file() - Writing xml file to:{0:}".format(p_pyhouses_obj.XmlFileName)
        self.m_xmltree_root = p_pyhouses_obj.XmlRoot
        self.write_xml_file(self.m_xmltree, p_pyhouses_obj.XmlFileName)


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
    if g_debug >= 3:
        print 'Hup Signal handler called with signal', signum
    API().Stop()
    API().Start()

def SigIntHandler(signum, _stackframe):
    if g_debug >= 3:
        print 'Signal handler called with signal', signum
    API().Stop()
    exit


class Utils(object):
    """
    """

    def init_log(self):
        self.m_cfg = ConfigFileHandler(self.m_pyhouses_obj)
        self.m_pyhouses_obj.XmlRoot = self.m_cfg.parse_xml()
        self.m_pyhouses_obj.LogsAPI = log.API()
        self.m_pyhouses_obj.LogsData = self.m_pyhouses_obj.LogsAPI.Start(self.m_pyhouses_obj)


class API(Utils):
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
        handle_signals()
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.API = self
        self.init_log()
        global g_logger
        g_logger = logging.getLogger('PyHouse         ')
        g_logger.info("Initializing.\n")
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
            print "PyHouse.API.Start()"
        self.m_pyhouses_obj.HousesData = self.m_pyhouses_obj.HousesAPI.Start(self.m_pyhouses_obj)
        self.m_pyhouses_obj.WebData = self.m_pyhouses_obj.WebAPI.Start(self.m_pyhouses_obj)
        g_logger.info("Started.\n")
        if g_debug >= 2:
            print "PyHouse all is started and running now.\n"

    def Stop(self):
        """Stop various modules to prepare for restarting them.
        """
        if g_debug >= 2:
            print "PyHouse.API.Stop()"
        self.m_pyhouses_obj.HousesAPI.Stop()
        self.m_pyhouses_obj.WebAPI.Stop()
        g_logger.info("Stopped.\n\n\n")

    def Reload(self, p_pyhouses_obj):
        """Update XML file with current info.
        """
        if g_debug >= 2:
            print "PyHouse.API.Reload()"
        l_root_xml = ET.Element("PyHouse")
        l_root_xml.append(p_pyhouses_obj.HousesAPI.Reload(p_pyhouses_obj))
        p_pyhouses_obj.WebAPI.Reload(p_pyhouses_obj)
        self.m_cfg.write_xml_config_file(p_pyhouses_obj)

    def Quit(self):
        """Prepare to exit all of pyhouse
        """
        if g_debug >= 2:
            print "\nPyHouse.Quit()"
        self.Stop()
        reactorstop()


if __name__ == "__main__":
    API()

# ## END DBK
