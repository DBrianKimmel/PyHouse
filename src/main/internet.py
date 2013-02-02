#!/usr/bin/env python

"""Get the internet address and make reports available for web interface.
"""

# Import system type stuff
import logging


g_debug = 0
g_logger = None


def Init():
    if g_debug > 0:
        print "internet.Init()"
    global g_logger
    g_logger = logging.getLogger('PyHouse.Internet')
    g_logger.info("Initializing.")
    g_logger.info("Initialized.")

def Start():
    if g_debug > 0:
        print "internet.Start()"

def Stop():
    if g_debug > 0:
        print "internet.Stop()"

# ## END
