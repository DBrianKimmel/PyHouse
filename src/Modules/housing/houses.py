"""
-*- test-case-name: PyHouse.src.Modules.housing.test.test_houses -*-

@name: PyHouse/src/Modules/housing/houses.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2010-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jan 20, 2010
@summary: Handle all of the information for all houses.


This module is a singleton called from PyHouse.
It initiates an instance of house for each house defined in XML.

Perhaps it is no longer necessary (with multiple Raspberry Pis) to have more than a single house in the XML file.

Its initiates the configuration system and then calls the other packages and sets up the whole system.

"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import HousesData
from Modules.housing import house
from Modules.utils import pyh_log

g_debug = 1
LOG = pyh_log.getLogger('PyHouse.Houses      ')

Singletons = {}


class Utilities(object):

    def start_all_houses(self, p_pyhouses_obj):
        """Find all houses in the XML file and start a house instance for each one.
        """
        l_count = 0
        for l_house_xml in self.get_house_list(p_pyhouses_obj):
            p_pyhouses_obj.HousesData[l_count] = self.start_house_instance(p_pyhouses_obj, l_house_xml, l_count)
            l_count += 1
        return l_count

    def start_house_instance(self, p_pyhouses_obj, p_house_xml, p_index):
        """Build up one entry for m_houses_data
        """
        l_houses_obj = HousesData()
        l_houses_obj.Key = p_index
        l_houses_obj.HouseAPI = house.API(p_index)
        l_houses_obj.HouseObject = l_houses_obj.HouseAPI.Start(p_pyhouses_obj, p_house_xml)
        l_houses_obj.Name = l_houses_obj.HouseObject.Name
        return l_houses_obj

    def get_house_list(self, p_pyhouses_obj):
        """
        Find all the different houses in the XML configuration file.
        Each will have a 'house' sub-tree of elements under that house.
        When we first start configuring, there are no houses defined - so we need to create an empty house.

        @return: iterable list of all houses defined.
        """
        l_xml_root = p_pyhouses_obj.XmlRoot
        try:
            l_sect = l_xml_root.find('Houses')
            l_list = l_sect.iterfind('House')  # use l_sect to force error if it is missing
        except AttributeError:
            LOG.warning("Warning - in read_house XML - Adding 'Houses' section")
            l_sect = ET.SubElement(l_xml_root, 'Houses')
            l_list = l_sect.iterfind('House')
        return l_list


class API(Utilities):
    """
    """

    m_houses_data = {}

    def __new__(cls, *args, **kwargs):
        """This is for all houses.
        Set up the common / global things in this singleton.
        """
        if cls in Singletons:
            return Singletons[cls]
        self = object.__new__(cls)
        cls.__init__(self, *args, **kwargs)
        Singletons[cls] = self
        if g_debug >= 1:
            LOG.info("Initialized all houses.")
        return self

    def __init__(self):
        pass

    def Start(self, p_pyhouses_obj):
        """Start processing for all things houses
        .
        May be stopped and then started anew to force reloading info.
        Invoked once no matter how many houses defined in the XML file.
        """
        self.m_pyhouses_obj = p_pyhouses_obj
        l_count = self.start_all_houses(p_pyhouses_obj)
        if g_debug >= 1:
            LOG.info("Started {0:} house(s).".format(l_count))

    def Stop(self, p_xml):
        """Close down everything we started.
        Each stopped instance returns an up-to-date XML subtree to be written out.
        """
        if g_debug >= 1:
            LOG.info("Stopping.")
        l_houses_xml = ET.Element('Houses')
        for l_house in self.m_houses_data.itervalues():
            try:
                l_house.HouseAPI.Stop(l_houses_xml, l_house.HouseObject)
            except AttributeError:  # New house being added has no existing API
                house.API().Stop(l_houses_xml, l_house.HouseObject)
        if g_debug >= 1:
            LOG.info("XML appended.")
        p_xml.append(l_houses_xml)

    def get_houses_obj(self):
        return self.m_houses_data

# ##  END DBK
