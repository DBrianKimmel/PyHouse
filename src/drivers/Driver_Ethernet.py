#!/usr/bin/python

"""Driver_Ethernet.py - Ethernet Driver module.

This will interface various PyHouse modules to an ethernet connected controller device.

This may be instanced as many times as there are serial devices to control.

This should also allow control of many different houses.
"""


# Import system type stuff
import logging

# Import PyHouse modules


g_debug = 0
g_logger = logging.getLogger('PyHouse.USBDriver')

class API(object):

    def __init__(self):
        """
        @param p_obj: is the Controller_Data object we are using.
        """
        if g_debug > 0:
            print "Driver_Ethernet.Init()"
        g_logger.info(" Initializing Ethernet port.")
        return None

    def Start(self, p_obj):
        if g_debug > 0:
            print "Driver_Ethernet.Start()"
        g_logger.info("Starting Ethernet port.")
        return None

    def Stop(self):
        if g_debug > 0:
            print "Driver_Ethernet.Stop()"

# ## END
