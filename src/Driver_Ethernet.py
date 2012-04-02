#!/usr/bin/python

"""Driver_Ethernet.py - Ethernet Driver module.

This will interface various PyHouse modules to an ethernet connected controller device.

This may be instanced as many times as there are serial devices to control.

This should also allow control of many different houses.
"""


# Import system type stuff
import logging

# Import PyHouse modules


class EthernetDriverMain(object):
    """
    """

    def __init__(self, p_obj):
        #print "--EthernetDriverMain.__init__()", p_obj
        self.m_logger = logging.getLogger('PyHouse.EthernetDriver')
        self.m_logger.info(" Initializing Ethernet port")

### END
