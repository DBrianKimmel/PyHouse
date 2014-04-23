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
import logging
# import xml.etree.ElementTree as ET
# from src.entertain import pandora

g_debug = 0

g_logger = logging.getLogger('PyMh.Entertainment')
g_upnp = None

Entertainment_Data = {}


class EntertainmentAPI(object):
    """
    """

    def get_all_entertainment_slots(self):
        """
        """
        self.m_logger.info("Retrieving Entertainment Info")
        return self.Entertainment_Data


class API(object):
    def __init__(self):
        # self.m_pandora = pandora.API()
        g_logger.info("Initialized.")

    def Start(self, p_pyhouses_obj):
        # self.m_pandora.Start(p_pyhouses_obj)
        g_logger.info("Started.")

    def Stop(self, p_xml):
        # self.m_pandora.Stop()
        g_logger.info("Stopped.")

# ## END DBK
