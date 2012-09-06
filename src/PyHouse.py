#!/usr/bin/env python

""" PyHouse.py - Run the python version house automation.

During development this is run by hand.
It is, however, planned to be a daemon that is kicked off on system start-up.
It is intended to run on eveerything from a small, low power barebones system
to a server running multiple houses in several, sidespread locations.

The system is controlled via a browser connecting to a web server that will
be either integrated or seperate from PyHouse.

The highest level is the House/Location.  Every house has a location and
contains a number of rooms.
Each house must be unique and its name is used to qualify lower level rooms
and devices.

Each house may share a central schedule and also have a schedule that is only
for that house.  It is recommended that the schedule be mostly on a house by
house basis and only a very few actions are done on all houses.
Each house will need at least a small barebone system to control all the USB
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
    Web server - allow control over the internet by a browser
    Scheduler - kick off automation that follows a schedule
    Lighting - allow cautmation of home lighting systems
    Heating,
    Pool Contgrol.
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
import configure_mh
import config_xml
import log
import house
import gui
import web_server
import schedule
import weather
import UPnP_core


Configure_Data = configure_mh.Configure_Data


g_logger = None


def Init():
    global g_logger
    if platform.uname()[0] != 'Windows':
        signal.signal(signal.SIGHUP, SigHupHandler)
    signal.signal(signal.SIGINT, SigIntHandler)

    # These need to be first and in this order
    configure_mh.ConfigureMain()
    log.LoggingMain()
    config_xml.ReadConfig()
    # 2nd. Now the logging will be set up and work properly
    g_logger = logging.getLogger('PyHouse')
    g_logger.info("Initializing - Starting PyHouse.")
    house.Init()
    weather.Init()
    schedule.Init()
    UPnP_core.Init()
    web_server.Init()
    g_logger.info("Initialized.\n")

def Start():
    """Put twisted setup functions in here.
    After they are all set-up we will start the reactor process.
    Every thing that is to run must be in the main reactor event loop as reactor.run() does not return.
    """
    g_logger.info("Starting.")
    house.Start(reactor)
    schedule.Start(reactor)
    web_server.Start(reactor)
    g_logger.info("Started.\n")
    # reactor never returns so must be last - Event loop will now run
    reactor.run()

def Stop():
    """Stop twisted in preparation to exit PyMh.
    """
    reactor.stop()
    schedule.Stop()
    web_server.Stop()
    g_logger.info("Stopped.\n")
    log.LoggingMain().stop()

def Restart():
    """Allow for a running restart of PyMh.
    """
    Stop()
    Start()

def SigHupHandler(signum, _stackframe):
    print 'Hup Signal handler called with signal', signum
    Restart()

def SigIntHandler(signum, _stackframe):
    print 'Signal handler called with signal', signum
    Stop()
    exit


if __name__ == "__main__":
    Init()
    Start()

### END
