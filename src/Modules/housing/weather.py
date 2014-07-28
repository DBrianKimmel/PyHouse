#!/usr/bin/env python

"""Get the weather and make reports available for web interface.
"""

# Import system type stuff

from Modules.utils import pyh_log

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.Weather    ')


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
