"""

@name:      PyHouse/src/Modules/Entertainment/entertainment.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2013
@summary:   Entertainment component access module.

Depending on node type, start up entertainment systems.

Pandora (via pianobar) is one of the systems.

"""

# Import system type stuff
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Entertainment  ')


class Utility(object):

    def get_all_entertainment_slots(self):
        """
        """
        self.m_logger.info("Retrieving Entertainment Info")
        return self.Entertainment_Data


class API(Utility):
    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def Start(self):
        LOG.info("Started.")

    def Stop(self):
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        LOG.info("Saved XML.")
        return p_xml

# ## END DBK
