"""
entertainment.py

@author: briank

@copyright: 2010 - 2014 by D. Brian Kimmel

@summary: Entertainment component access module.

This is a Main Module - always present.

Depending on node type, start up entertainment systems.

Pandora (via pianobar) is one of the systems.

"""

# Import system type stuff
# import xml.etree.ElementTree as ET
# from Modules.entertain import pandora
from Modules.Computer import logging_pyh as Logger

g_debug = 0

LOG = Logger.getLogger('PyMh.Entertainment')
g_upnp = None

Entertainment_Data = {}


class Utility(object):
    """
    """

    def get_all_entertainment_slots(self):
        """
        """
        self.m_logger.info("Retrieving Entertainment Info")
        return self.Entertainment_Data


class API(Utility):
    def __init__(self):
        # self.m_pandora = pandora.API()
        LOG.info("Initialized.")

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        # self.m_pandora.Start(p_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        # self.m_pandora.Stop()
        LOG.info("Stopped.")

    def SaveXml(self, _p_xml):
        # self.m_pandora.Stop()
        LOG.info("Saved XML.")

# ## END DBK
