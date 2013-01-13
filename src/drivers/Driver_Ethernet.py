#!/usr/bin/python

"""Driver_Ethernet.py - Ethernet Driver module.

This will interface various PyHouse modules to an ethernet connected controller device.

This may be instanced as many times as there are serial devices to control.

This should also allow control of many different houses.
"""


# Import system type stuff
import logging

# Import PyHouse modules


g_debug = 1
g_logger = None

def Init():
    """
    @param p_obj: is the Controller_Data object we are using.
    """
    if g_debug > 0:
        print "Driver_Ethernet.Init()"
    global g_logger
    g_logger = logging.getLogger('PyHouse.USBDriver')
    g_logger.info(" Initializing Ethernet port.")
    return None

def Start(p_obj):
    if g_debug > 0:
        print "Driver_Ethernet.Start()"
    g_logger.info("Starting Ethernet port.")
    return None

def Stop():
    if g_debug > 0:
        print "Driver_Ethernet.Stop()"

# ## END
