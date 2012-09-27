#!/usr/bin/python

"""Entertainment component access module.
This is a Main Module - always present.

Can act as a UPnP Control point

"""

# Import system type stuff
import logging

# Import PyMh files
import upnp.UPnP_core
from upnp.UPnP_core import g_uuid

Entertainment_Data = {}
g_logger = None
g_upnp = None

class EntertainmentAPI(object):
    """
    """

    def get_all_entertainment_slots(self):
        """
        """
        self.m_logger.info("Retrieving Entertainment Info")
        return self.Entertainment_Data


class UPnPControlPoint(object):
    """
    0.  Addressing - not needed since we already have an IP address.
    1.  Discovery - Using SSDP to advertise and discover other UPnP thingies.
    2.  Description - XML queries back and forth to provide details of UPnP workings.
    3.  Control - A UPnP control point controls UPnP devices.
    4.  Eventing - How a device gets notified about happenings in the UPnP network.
    5.  Presentation - How to retrieve content from a UPnP device.
    """

    def __init__(self):
        print "entertainment.UPnPControlPoint.__init__()"
        upnp.UPnP_core.Init()
        upnp.UPnP_core.Start()

    def discover_all_media_servers(self):
        pass

    def discover_all_media_renderers(self):
        pass

    def locate_desired_content(self):
        pass

def Init():
    global g_logger, g_upnp
    print "Entertainment.Init()"
    g_logger = logging.getLogger('PyMh.Entertainment')
    g_logger.info("Initializing.")
    g_upnp = UPnPControlPoint()
    g_logger.info("Initialized.")
    
def Start():
    pass

def Stop():
    pass

### END
