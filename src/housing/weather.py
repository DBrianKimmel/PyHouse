#!/usr/bin/env python

"""Get the weather and make reports available for web interface.
"""

# Import system type stuff
import logging


g_debug = 0
g_logger = logging.getLogger('PyHouse.Weather    ')


class API(object):
    def __init__(self):
        g_logger.info("Initializing.")
        g_logger.info("Initialized.")

    def Start(self):
        pass

    def Stop(self, p_xml):
        return p_xml

# ## END DBK
