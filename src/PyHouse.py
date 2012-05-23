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

#from tools import Lister


m_debug = None
m_logger = None

g_configure = None
g_house = None
g_logging = None
g_reactor = None
g_schedule = None
g_web_server = None


class MainProgram(object):
    """The main program for PyMh.
    This creates the initial run environment and allows for reloads.
    """

    def __init__(self):
        """The constructor for the class.
        Establish all pointers needed.
        """
        if platform.uname()[0] != 'Windows':
            signal.signal(signal.SIGHUP, self.SigHupHandler)
        signal.signal(signal.SIGINT, self.SigIntHandler)

        self.print_license()
        # These need to be first and in this order
        self.g_configure = configure_mh.ConfigureMain()
        self.g_configure.load_config()
        log.LoggingMain()
        # 2nd. Now the logging will be set up and work properly
        self.m_logger = logging.getLogger('PyHouse')
        self.m_logger.info("Initializing.")
        # 3rd. Now the rest of the system will be set up
        house.HouseMain()
        self.g_schedule = schedule.ScheduleMain()
        self.g_web_server = web_server.Web_ServerMain()
        self.m_logger.info("Initialized.\n")

    def configure(self):
        """For some needed modules, run the configuration code.
        """
        self.m_logger.info("Configuring.")
        self.g_web_server.configure()
        self.m_logger.info("Configured.\n")

    def start(self):
        """Put twisted setup functions in here.
        After they are all set-up we will start the reactor process.
        Every thing that is to run must be in the main reactor event loop as reactor.run() does not return.
        """
        self.m_logger.info("Starting.")
        self.g_schedule.start(reactor)
        #self.g_web_server.start(reactor)
        self.m_logger.info("Started.\n")
        reactor.run()

    def stop(self):
        """Stop twisted in preparation to exit PyMh.
        """
        reactor.stop()
        self.m_logger.info("Stopped.\n")
        log.LoggingMain().stop()

    def restart(self):
        """Allow for a running restart of PyMh.
        """
        self.stop()
        self.configure()
        self.start()

    def SigHupHandler(self, signum, _stackframe):
        print 'Hup Signal handler called with signal', signum
        self.restart()

    def SigIntHandler(self, signum, _stackframe):
        print 'Signal handler called with signal', signum
        self.stop()
        exit


    def print_license(self):
        #print "License printed here !!!\n"
        #return
        print """
    This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""


if __name__ == "__main__":
    mp = MainProgram()
    mp.configure()
    mp.start()

### END
