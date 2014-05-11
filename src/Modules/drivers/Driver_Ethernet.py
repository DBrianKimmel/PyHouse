#!/usr/bin/python

"""Driver_Ethernet.py - Ethernet Driver module.

This will interface various PyHouse modules to an ethernet connected controller device.

This may be instanced as many times as there are serial devices to control.

This should also allow control of many different houses.
"""


# Import system type stuff

# Import PyHouse modules
from Modules.utils import pyh_log

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.USBDriver')

class API(object):

    def __init__(self):
        """
        @param p_obj: is the Controller_Data object we are using.
        """
        LOG.info(" Initializing Ethernet port.")
        return None

    def Start(self, p_obj):
        LOG.info("Starting Ethernet port.")
        return None

    def Stop(self):
        pass

# ## END
