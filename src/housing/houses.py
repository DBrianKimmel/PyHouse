#!/usr/bin/python

"""Handle all the house(s) information.

main/houses.py

This module is a singleton called from PyHouse.
Its main purpose is to initiate the configuration system and then call
the other packages and set up the whole system based on the config read in.


Rooms and lights and HVAC are associated with a particular house.
"""

# Import system type stuff
import logging
import xml.etree.ElementTree as ET

# Import PyMh files
from src.housing import house
from src.utils import xml_tools


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 - Config file handling
# 4 = Access housing info
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.Houses      ')

Singletons = {}


class HousesData(object):
    """This class holds the data about all houses defined in xml.
    """

    def __init__(self):
        """Houses.
        """
        self.Name = None
        self.Key = 0
        self.Active = False
        self.HouseAPI = None
        self.HouseObject = {}

    def __str__(self):
        l_ret = "Houses:: "
        l_ret += "Name:{0:}, ".format(self.Name)
        l_ret += "Key:{0:}, ".format(self.Key)
        l_ret += "Active:{0:}, ".format(self.Active)
        l_ret += "HouseAPI:{0:}, ".format(self.HouseAPI)
        l_ret += "\nHouseObject:{0:}".format(self.HouseObject)
        return l_ret

    def reprJSON(self):
        """Houses.
        """
        return dict(
            Active = self.Active, Key = self.Key, Name = self.Name
            )


class HouseReadWriteConfig(xml_tools.ConfigFile):

    m_xml_filename = None
    m_xmltree_root = None

    def __init__(self):
        """Open the xml config file.
        If the file is missing, an empty minimal skeleton is created.
        """
        pass

    def get_xml_root(self):
        return self.m_xmltree_root


class LoadSaveAPI(HouseReadWriteConfig):
    """
    """

    def load_all_houses(self):
        """Load all the house info.
        """
        self.l_rwc = HouseReadWriteConfig()
        return self.l_rwc.get_xml_root()

    def get_house_info(self, p_house_xml, p_count):
        """Build up one entry for m_houses_data
        """
        l_houses_obj = HousesData()
        l_houses_obj.Key = p_count
        l_houses_obj.HouseAPI = house.API()
        l_houses_obj.HouseObject = l_houses_obj.HouseAPI.Start(p_house_xml)
        l_houses_obj.Name = l_houses_obj.HouseObject.Name
        return l_houses_obj

    def read_xml_config_houses(self, p_pyhouses_obj):
        """
        @return: iterable list of all houses defined.
        """
        l_xml_root = p_pyhouses_obj.XmlRoot
        self.m_xmltree_root = self.load_all_houses()
        #
        try:
            l_sect = l_xml_root.find('Houses')
            l_list = l_sect.iterfind('House')  # use l_sect to force error if it is missing
        except AttributeError:
            g_logger.warn("Warning - in read_house XML - Adding 'Houses' section")
            l_sect = ET.SubElement(l_xml_root, 'Houses')
            l_list = l_sect.iterfind('House')
        return l_list


class API(LoadSaveAPI):
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
        g_logger.info("Initialized all houses.\n\n")
        return self

    def __init__(self):
        pass

    def Start(self, p_pyhouses_obj):
        """Start processing for all things houses
        .
        May be stopped and then started anew to force reloading info.
        Invoked once no matter how many houses defined in the XML file.
        """
        l_count = 0
        for l_house_xml in self.read_xml_config_houses(p_pyhouses_obj):
            self.m_houses_data[l_count] = self.get_house_info(l_house_xml, l_count)
            l_count += 1
        g_logger.info("Started.")
        return self.m_houses_data

    def Stop(self, p_xml):
        """Close down everything we started.
        Each stopped instance returns an up-to-date XML subtree to be written out.
        """
        g_logger.info("Stopping.")
        l_houses_xml = ET.Element('Houses')
        for l_house in self.m_houses_data.itervalues():
            try:
                l_xml = l_house.HouseAPI.Stop(l_houses_xml, l_house.HouseObject)
            except AttributeError:  # New house being added has no existing API
                l_xml = house.API().Stop(l_houses_xml, l_house.HouseObject)
            # l_houses_xml.append(l_xml)  # append to the xml tree
        g_logger.info("XML appended.")
        p_xml.append(l_houses_xml)
        g_logger.info("Stopped.")
        # return p_xml

    def get_houses_obj(self):
        return self.m_houses_data

# ##  END DBK
