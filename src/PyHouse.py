#!/usr/bin/env python

""" PyHouse.py - Run the python version house automation.

During development this is run by hand.
It is, however, planned to be a daemon that is kicked off on system start-up.
It is intended to run on a small, low power barebones system.

Python modules used:
    Core python 2.7
    twisted
    nevow
    PySerial 2.6

Modules desired are:
    Web server - allow control over the internet by a browser
    Scheduler - kick off automation that follows a schedule
    Lighting - allow cautmation of home lighting systems
    Entertainment - allow control of tv, video systems, audio systems etc
    Surveillance - allow remote control ov video cameras etc.
"""

# Import system type stuff
import logging
import platform
import signal
from twisted.internet import reactor

# Import PyMh files and modules.
import configure_mh
import log
import house
import web_server
import schedule
import weather


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
    # 2nd. Now the logging will be set up and work properly
    g_logger = logging.getLogger('PyHouse')
    g_logger.info("Initializing - Starting PyHouse.")
    house.Init()
    weather.Init()
    schedule.Init()
    web_server.Init()
    g_logger.info("Initialized.\n")

def Start():
    """Put twisted setup functions in here.
    After they are all set-up we will start the reactor process.
    Every thing that is to run must be in the main reactor event loop as reactor.run() does not return.
    """
    global g_logger
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
