#!/usr/bin/env python

""" PyHouse.py - Run the python version house automation.

During development this is run by hand.
It is, however, planned to be a daemon that is kicked off on system start-up.
It is intended to run on everything from a small, low power bare bones system
to a server running multiple houses in several, widespread locations.

The system is controlled via a browser connecting to a web server that will
be either integrated or separate from PyHouse.

The highest level is the House/Location.  Every house has a location and
contains a number of rooms.
Each house must be unique and its name is used to qualify lower level rooms
and devices.

Each house may share a central schedule and also have a schedule that is only
for that house.  It is recommended that the schedule be mostly on a house by
house basis and only a very few actions are done on all houses.
Each house will need at least a small bare bone system to control all the USB
and Ethernet devices used to control the various devices in the house.

The next level is the room.  Rooms may be duplicated between houses but must
be unique within a single house.  Therefore you may not have 3 bedrooms named
'bedroom' and so on.

Python modules used:
    Core python 2.7
    Twisted
    zope.interface
    nevow
    PySerial
    PyUsb
    ConfigObj
    Pmw

also install:
    libusb

Modules desired are:
    Web server - allow control over the Internet by a browser
    Scheduler - kick off automation that follows a schedule
    Lighting - allow automation of home lighting systems
    Heating,
    Pool Control.
    Irrigation control.
    Entertainment - allow control of tv, video systems, audio systems etc
    Surveillance - allow remote control of video cameras etc.
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
import configure
import configure.config_etc as config_etc
import configure.config_xml as config_xml
import log
import house
import schedule.schedule as schedule
import weather

__version_info__ = (1, 0, 1)
__version__ = '.'.join(map(str, __version_info__))

g_debug = 0
g_logger = None

class OptionParser(optparse.OptionParser):
    """
    Simple wrapper to add list of available plugins to help
    message, but only if help message is really printed
    """
    def print_help(self, file = None):
        sys.argv = sys.argv[:1]
        optparse.OptionParser.print_help(self, file)



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

def __opt_option(option, opt, value, parser):
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


def parse_command_line():
    parser = OptionParser('%prog [options]', version = "Coherence version: %s" % __version__)
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

def Init():
    """This is the startup of the entire system.
    All permanent services are started here.
    These core routines are an integral part of the daemon process.

    Notice that the reactor starts here as the very last step and that
    call never returns.
    """
    if g_debug > 0:
        print "PyHouse.Init()"
    handle_signals()
    parse_command_line()
    l_config = config_etc.find_etc_config_file()
    config_xml.read_config()
    log.LoggingMain()
    # 2nd. Now the logging will be set up and work properly
    global g_logger
    g_logger = logging.getLogger('PyHouse')
    g_logger.info("Initializing - Starting PyHouse.")
    house.Init()
    weather.Init()
    schedule.Init()
    # web_server.Init()
    configure.gui.Init()
    g_logger.info("Initialized.\n")
    # reactor never returns so must be last - Event loop will now run
    reactor.run()

def Start():
    """New.  This will start all non-core services.
    This may be called multiple times along with stop to reerun various modules
    Every thing that is to run must be in the main reactor event loop as reactor.run() does not return.
    """
    if g_debug > 0:
        print "PyHouse.Start()"
    g_logger.info("Starting.")
    schedule.Start()
    # web_server.Start()
    g_logger.info("Started.\n")

def Stop(p_tag = None):
    """Stop twisted in preparation to exit PyMh.
    """
    print "PyHouse.Stop() - Tag: ", p_tag
    global g_logger
    g_logger = logging.getLogger('PyHouse')
    g_logger.info("Stopping has begun.\n")
    config_xml.write_config()
    if p_tag != 'Gui':
        configure.gui.Stop()
    schedule.Stop()
    # web_server.Stop()
    try:
        g_logger.info("Stopped.\n")
    except AttributeError, emsg:
        print "Got attribute error while trying to log 'Stopped' from PyHouse. ", emsg
    log.LoggingMain().stop()
    reactor.stop()
    raise SystemExit, "PyHouse says Bye Now."

def Restart():
    """Allow for a running restart of PyMh.
    """
    Stop()
    Start()

def SigHupHandler(signum, _stackframe):
    if g_debug > 0:
        print 'Hup Signal handler called with signal', signum
    Restart()

def SigIntHandler(signum, _stackframe):
    if g_debug > 0:
        print 'Signal handler called with signal', signum
    Stop()
    exit


if __name__ == "__main__":
    # print "MAIN"
    Init()
    Start()

# ## END
