#!/usr/bin/python

"""Entertainment component access module.
This is a Main Module - always present.

"""

# Import system type stuff
import logging
import time

# Import PyMh files


Entertainment_Data = {}


class EntertainmentAPI(object):
    """
    """

    def get_all_entertainment_slots(self):
        """
        """
        self.m_logger.info("Retrieving Entertainment Info")
        return self.Entertainment_Data


class EntertainmentMain(EntertainmentAPI):
    """
    """

    def __init__(self):
        """Constructor for the PLM.
        """
        self.m_logger = logging.getLogger('PyMh.Entertainment')
        self.m_logger.info("Initialized.")

### END
