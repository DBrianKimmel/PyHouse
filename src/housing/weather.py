#!/usr/bin/env python

"""Get the weather and make reports available for web interface.
"""

# Import system type stuff

from src.utils import pyh_log

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.Weather    ')


class API(object):
    def __init__(self):
        LOG.info("Initializing.")
        LOG.info("Initialized.")

    def Start(self):
        pass

    def Stop(self, p_xml):
        return p_xml

# ## END DBK
