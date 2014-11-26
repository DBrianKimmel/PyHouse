#!/usr/bin/env python

"""Get the weather and make reports available for web interface.
"""

# Import system type stuff

from Modules.Computer import logging_pyh as Logger

g_debug = 0
LOG = Logger.getLogger('PyHouse.Weather    ')


class API(object):
    def __init__(self):
        LOG.info("Initializing.")
        LOG.info("Initialized.")

    def Start(self):
        pass

    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        LOG.info('Saved XML.')
        return p_xml

# ## END DBK
