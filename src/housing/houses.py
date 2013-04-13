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
from housing import house
from utils import xml_tools

g_debug = 9
# 0 = off
# 1 = major routine entry
# 2 = get/put xml config info
# 3 = Access housing info

Singletons = {}


class HousesData(object):
    """This class holds the data about all houses defined in xml.
    """

    def __init__(self):
        self.Key = 0
        self.Name = None
        self.HouseAPI = None
        self.Object = {}

    def __str__(self):
        return "Houses:: Name:{0:}, Key:{1:}".format(self.Name, self.Key)


class HouseReadWriteConfig(xml_tools.ConfigFile):

    m_xml_filename = None
    m_xmltree_root = None

    def __init__(self):
        """Open the xml config file.
        If the file is missing, an empty minimal skeleton is created.
        """
        if g_debug >= 2:
            print "houses.HouseReadWriteConfig.__init__()"
        self.m_xml_filename = self.find_config_file_name()
        self.parse_xml()

    def parse_xml(self):
        if g_debug >= 2:
            print "houses.parse_xml()"
        try:
            self.m_xmltree = ET.parse(self.m_xml_filename)
        except SyntaxError:
            self.create_empty_config_file(self.m_xml_filename)
            self.m_xmltree = ET.parse(self.m_xml_filename)
        self.m_xmltree_root = self.m_xmltree.getroot()

    def find_config_file_name(self):
        if g_debug >= 2:
            print "houses.find_config_file_name()"
        l_xml_filename = xml_tools.open_config_file()
        return l_xml_filename

    def get_xml_root(self):
        return self.m_xmltree_root

    def write_config_file(self, p_xml):
        """Replace the data in the 'Houses' section with the current data.
        """
        if g_debug >= 2:
            print "houses.write_config_file() - Writing xml file to:{0:}".format(self.m_xml_filename)
        self.m_xmltree_root = self.m_xmltree.getroot()
        self.m_xmltree_root = p_xml
        self.write_xml_file(self.m_xmltree, self.m_xml_filename)


class LoadSaveAPI(HouseReadWriteConfig):
    """
    """

    def load_all_houses(self):
        """Load all the house info.
        """
        if g_debug >= 3:
            print "houses.load_all_houses()"
        self.l_rwc = HouseReadWriteConfig()
        return self.l_rwc.get_xml_root()

    def save_all_houses(self, p_xml):
        if g_debug >= 3:
            print "\nhouses.save_all_houses()"
        self.l_rwc.write_config_file(p_xml)

    def get_house_info(self, p_house_xml, p_count):
        """Build up one entry for m_houses_data
        """
        if g_debug >= 3:
            print "\nhouses.get_house_info() - Creating a new house named:{0:}".format(p_house_xml.get('Name'))
        l_houses_obj = HousesData()
        l_houses_obj.Key = p_count
        l_houses_obj.HouseAPI = house.API()
        l_houses_obj.Object = l_houses_obj.HouseAPI.Start(l_houses_obj, p_house_xml)
        l_houses_obj.Name = l_houses_obj.Object.Name
        return l_houses_obj

    def get_houses_xml(self):
        """
        @return: iterable list of all houses defined.
        """
        if g_debug >= 3:
            print "houses.get_houses_xml()"
        self.m_xmltree_root = self.load_all_houses()
        #
        try:
            l_sect = self.m_xmltree_root.find('Houses')
            l_list = l_sect.iterfind('House')  # use l_sect to force error if it is missing
        except AttributeError:
            print "Warning - in read_house - Adding 'Houses' section"
            l_sect = ET.SubElement(self.m_xmltree_root, 'Houses')
            l_list = l_sect.iterfind('House')
        return l_list


class API(LoadSaveAPI):
    """
    """

    m_schedules = []
    m_houses_data = {}

    def __new__(cls, *args, **kwargs):
        """This is for all houses.
        Set up the common / global things in this singleton.
        """
        if cls in Singletons:
            return Singletons[cls]
        if g_debug >= 1:
            print "houses.__new__()"
        self = object.__new__(cls)
        cls.__init__(self, *args, **kwargs)
        Singletons[cls] = self
        self.m_logger = logging.getLogger('PyHouse.Houses')
        self.m_logger.info("Initializing all houses.")
        self.m_logger.info("Initialized.")
        return self

    def __init__(self):
        if g_debug >= 1:
            print "houses.__init__()"

    def Start(self):
        """Start processing for all things house.
        May be stopped and then started anew to force reloading info.
        Invoked once no matter how many houses defined.
        """
        if g_debug >= 1:
            print "houses.API.Start() - Singleton"
        self.m_logger.info("Starting.")
        l_count = 0
        for l_house_xml in self.get_houses_xml():
            self.m_houses_data[l_count] = self.get_house_info(l_house_xml, l_count)
            l_count += 1
        if g_debug >= 1:
            print "houses.API.Start() - {0:} houses all started.".format(l_count)
        self.m_logger.info("Started.")


    def Stop(self):
        """Close down everything we started.
        Each stopped instance returns an up-to-date XML subtree to be written out.
        """
        if g_debug >= 1:
            print "houses.API.Stop()"
        self.m_logger.info("Stopping.")
        l_houses_xml = self.create_empty_xml_section(self.m_xmltree_root, 'Houses')
        for l_house in self.m_houses_data.itervalues():
            l_houses_xml.append(l_house.HouseAPI.Stop(l_houses_xml))  # append to the xml tree
        self.save_all_houses(l_houses_xml)
        self.m_logger.info("Stopped.")

    def get_houses_obj(self):
        return self.m_houses_data

# ##  END
