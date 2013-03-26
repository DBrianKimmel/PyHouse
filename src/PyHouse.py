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
        Add routines to update dynamic dns
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

# Import PyMh files and modules.
from configure import gui
from utils import log
from housing import houses
from web import web_server

g_debug = 0
g_logger = None

callWhenRunning = reactor.callWhenRunning
reactorrun = reactor.run
reactorstop = reactor.stop


class OptionParser(optparse.OptionParser):
    """
    Simple wrapper to add list of available plugins to help
    message, but only if help message is really printed
    """
    def print_help(self, p_file = None):
        sys.argv = sys.argv[:1]
        optparse.OptionParser.print_help(self, p_file)



def daemonize():
    """Taken from twisted.scripts._twistd_unix.py
    """
    if g_debug > 0:
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
    except:
        key = value
        val = ''
    parser.values.options[key] = val

def setConfigFile():
    def findConfigDir():
        try:
            configDir = os.path.expanduser('~')
        except:
            configDir = os.getcwd()
        return configDir
    return os.path.join(findConfigDir(), '.PyHouse/PyHouse.xml')


def XXparse_command_line():
    parser = OptionParser('%prog [options]')
    parser.add_option('-d', '--daemon', action = 'store_true', help = 'daemonize')
    parser.add_option('--noconfig', action = 'store_false', dest = 'configfile', help = 'ignore any configfile found')
    parser.add_option('-c', '--configfile', default = setConfigFile(), help = 'configfile to use, default: %default')
    parser.add_option('-l', '--logfile', help = 'logfile to use')
    parser.add_option('-o', '--option', action = 'callback', dest = 'options', metavar = 'NAME:VALUE', default = {}, callback = __opt_option, type = 'string',
                      help = "activate option (name and value separated by a colon (`:`), may be given multiple times)")
    parser.add_option('-p', '--plugins', action = 'append',
                      help = 'activate plugins (may be given multiple times) Example: --plugin=backend:FSStore,name:MyCoherence')
    options, args = parser.parse_args()
    if args:
        parser.error('takes no arguments')
    if options.daemon:
        try:
            daemonize()
        except:
            print "*** ERROR - Unable to daemonize!"
    config = {}
    config['logging'] = {}


def handle_signals():
    if platform.uname()[0] != 'Windows':
        signal.signal(signal.SIGHUP, SigHupHandler)
    signal.signal(signal.SIGINT, SigIntHandler)


def SigHupHandler(signum, _stackframe):
    if g_debug > 0:
        print 'Hup Signal handler called with signal', signum
    API().Stop()
    API().Start()

def SigIntHandler(signum, _stackframe):
    if g_debug > 0:
        print 'Signal handler called with signal', signum
    API().Stop()
    exit


class API(object):
    """
    """

    m_gui = None
    m_houses_api = None

    def __init__(self):
        """This is the startup of the entire system.
        All permanent services are started here.
        These core routines are an integral part of the daemon process.

        Notice that the reactor starts here as the very last step and that
        call never returns.
        """
        if g_debug > 0:
            print "\nPyHouse.API.__init__() - very beginning..."
        handle_signals()
        log.LoggingMain()
        global g_logger
        g_logger = logging.getLogger('PyHouse')
        g_logger.info("Initializing.\n")

        self.m_houses_api = houses.API()
        web_server.Init()
        self.m_gui = gui.API(self, self.m_houses_api)
        callWhenRunning(self.Start)
        g_logger.info("Initialized.\n")
        # reactor never returns so must be last - Event loop will now run
        reactorrun()
        raise SystemExit, "PyHouse says Bye Now."

    def Start(self):
        """New.  This will start all non-core services.
        This may be called multiple times along with stop to rerun various modules
        it is automatically invoked when the reactor starts from Init.
        """
        if g_debug > 0:
            print "\nPyHouse.Start()"
        g_logger.info("Starting.")
        self.m_houses_api.Start()
        web_server.Start()
        g_logger.info("Started.\n")
        if g_debug > 0:
            print "PyHouse all is started and running now.\n"

    def Stop(self):
        """Stop various modules to prepare for restarting them.
        """
        if g_debug > 0:
            print "\nPyHouse.Stop()"
        global g_logger
        g_logger = logging.getLogger('PyHouse')
        g_logger.info("Stopping has begun.\n")
        self.m_houses_api.Stop()
        web_server.Stop()
        try:
            g_logger.info("Stopped.\n")
        except AttributeError, emsg:
            print "Got attribute error while trying to log 'Stopped' from PyHouse. ", emsg

    def Quit(self):
        """Prepare to exit all of pyhouse
        """
        if g_debug > 0:
            print "\nPyHouse.Quit()"
        self.Stop()
        log.LoggingMain().stop()
        reactorstop()


if __name__ == "__main__":

    if g_debug > 0:
        print "MAIN"
    API()

# ## END
