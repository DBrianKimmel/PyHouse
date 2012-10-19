#!/usr/bin/python

"""This module will create UPnP light xml files for each light etc in the config file.

It will only be run at startup/restart time.

The goal is to allow a UPnP lighting control be interfaced so when a light is turned on
either manually or via a PyHouse schedule, the information is updated on all Control Points
in the network.  It will also allow control points to set any of the lights to a new value.
Also, scenes can be invoked from the control point.
"""

from lighting import lighting

Light_Data = lighting.Light_Data

class XmlFile(object):
    pass


class ConfigFile(object):
    pass


class BuildLights(object):
    """
    """

    def __init__(self):
        pass

    def create_xml(self):
        for l_obj in Light_Data.itervalues():
            l_file = XmlFile()
            pass


### END
