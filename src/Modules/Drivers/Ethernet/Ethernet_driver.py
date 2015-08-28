"""Ethernet_driver.py - Ethernet Driver module.

This will interface various PyHouse modules to an ethernet connected controller device.

This may be instanced as many times as there are serial devices to control.

This should also allow control of many different houses.
"""


# Import system type stuff

# Import PyHouse modules
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.USBDriver')

class API(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info(" Initializing Ethernet Driver.")

    def Start(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj
        LOG.info("Starting Ethernet port.")
        return None

    def Stop(self):
        pass

# ## END
