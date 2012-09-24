#!/usr/bin/python

"""Entertainment component access module.
This is a Main Module - always present.

Can act as a UPnP Control point

"""

# Import system type stuff
import logging

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
        pass

    def discover_all_media_servers(self):
        pass

    def discover_all_media_renderers(self):
        pass

    def locate_desired_content(self):
        pass

def Init():
    l_upnp = UPnPControlPoint()

### END
