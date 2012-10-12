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
import logging
import platform
import signal
from twisted.internet import reactor

# Import PyMh files and modules.
import configure
import configure.config_xml as config_xml
import log
import house
import schedule.schedule as schedule
import weather
#import upnp

g_debug = True
g_logger = None

def Init():
    if g_debug: print "PyHouse.Init()"
    if platform.uname()[0] != 'Windows':
        signal.signal(signal.SIGHUP, SigHupHandler)
    signal.signal(signal.SIGINT, SigIntHandler)

    global g_logger
    # These need to be first and in this order
    #configure_mh.ConfigureMain() # Temp till xml fully functional.
    config_xml.read_config()
    log.LoggingMain()
    # 2nd. Now the logging will be set up and work properly
    g_logger = logging.getLogger('PyHouse')
    g_logger.info("Initializing - Starting PyHouse.")
    # Now everything else.
    house.Init()
    weather.Init()
    schedule.Init()
    #upnp.core.Init()
    #web_server.Init()
    configure.gui.Init()
    g_logger.info("Initialized.\n")

def Start():
    """Put twisted setup functions in here.
    After they are all set-up we will start the reactor process.
    Every thing that is to run must be in the main reactor event loop as reactor.run() does not return.
    """
    if g_debug: print "PyHouse.Start()"
    g_logger.info("Starting.")
    house.Start(reactor)
    schedule.Start(reactor)
    #upnp.core.Start()
    #web_server.Start(reactor)
    g_logger.info("Started.\n")
    # reactor never returns so must be last - Event loop will now run
    reactor.run()

def Stop(p_tag = None):
    """Stop twisted in preparation to exit PyMh.
    """
    if g_debug: print "PyHouse.Stop()"
    config_xml.write_config()
#    UPnP_core.Stop()
    if p_tag != 'Gui':
        configure.gui.Stop()
    schedule.Stop()
    #web_server.Stop()
    try:
        g_logger.info("Stopped.\n")
    except AttributeError:
        pass
    log.LoggingMain().stop()
    reactor.stop()
    raise SystemExit, "PyHouse says Bye Now."


def Restart():
    """Allow for a running restart of PyMh.
    """
    Stop()
    Start()

def SigHupHandler(signum, _stackframe):
    if g_debug: print 'Hup Signal handler called with signal', signum
    Restart()

def SigIntHandler(signum, _stackframe):
    if g_debug: print 'Signal handler called with signal', signum
    Stop()
    exit


if __name__ == "__main__":
    #print "MAIN"
    Init()
    Start()

### END
