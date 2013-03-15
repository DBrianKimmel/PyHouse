#!/usr/bin/env python

"""Get the internet address and make reports available for web interface.
"""

# Import system type stuff
import logging


g_debug = 0
g_logger = None


class API(object):
    def __init__(self):
        if g_debug > 0:
            print "internet.Init()"
        global g_logger
        g_logger = logging.getLogger('PyHouse.Internet')
        g_logger.info("Initializing.")
        g_logger.info("Initialized.")

    def Start(self):
        if g_debug > 0:
            print "internet.Start()"

    def Stop(self, p_xml):
        if g_debug > 0:
            print "internet.Stop()"
        return p_xml

# ## END
