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


g_debug = 4
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 - Config file handling
# 4 = Access housing info

g_logger = logging.getLogger('PyHouse.Houses  ')

Singletons = {}


class HousesData(object):
    """This class holds the data about all houses defined in xml.
    """

    def __init__(self):
        self.Name = None
        self.Key = 0
        self.Active = False
        self.HouseAPI = None
        self.Object = {}

    def __str__(self):
        return "Houses:: Name:{0:}, Key:{1:}, Object:{2:}, API:{3:}".format(self.Name, self.Key, self.Object, self.HouseAPI)

    def __repr__(self):
        l_ret = "{"
        l_ret += "'Name':'{0:}', ".format(self.Name)
        l_ret += "'Key':'{0:}', ".format(self.Key)
        l_ret += "'Active':'{0:}', ".format(self.Active)
        l_ret += "'HouseAPI':'{0:}', ".format(self.HouseAPI)
        l_ret += "'Object':'{0:}'".format(self.Object)
        l_ret += "}"
        return l_ret


class HouseReadWriteConfig(xml_tools.ConfigFile):

    m_xml_filename = None
    m_xmltree_root = None

    def __init__(self):
        """Open the xml config file.
        If the file is missing, an empty minimal skeleton is created.
        """
        if g_debug >= 3:
            print "houses.HouseReadWriteConfig()"

    def get_xml_root(self):
        return self.m_xmltree_root

    def write_config_file(self, p_xml):
        """Replace the data in the 'Houses' section with the current data.
        """
        if g_debug >= 3:
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
        if g_debug >= 4:
            print "houses.load_all_houses()"
        self.l_rwc = HouseReadWriteConfig()
        return self.l_rwc.get_xml_root()

    def save_all_houses(self, p_xml):
        if g_debug >= 4:
            print "\nhouses.save_all_houses()"
        self.l_rwc.write_config_file(p_xml)

    def get_house_info(self, p_house_xml, p_count):
        """Build up one entry for m_houses_data
        """
        if g_debug >= 4:
            print "\nhouses.get_house_info() - Creating a new house named:{0:}".format(p_house_xml.get('Name'))
        l_houses_obj = HousesData()
        l_houses_obj.Key = p_count
        l_houses_obj.HouseAPI = house.API()
        l_houses_obj.Object = l_houses_obj.HouseAPI.Start(l_houses_obj, p_house_xml)
        l_houses_obj.Name = l_houses_obj.Object.Name
        if g_debug >= 4:
            print "houses.get_house_info()", l_houses_obj
        return l_houses_obj

    def read_xml_config_houses(self, p_pyhouses_obj):
        """
        @return: iterable list of all houses defined.
        """
        l_xml_root = p_pyhouses_obj.XmlRoot
        if g_debug >= 4:
            print "houses.read_xml_config_houses()"
        self.m_xmltree_root = self.load_all_houses()
        #
        try:
            l_sect = l_xml_root.find('Houses')
            l_list = l_sect.iterfind('House')  # use l_sect to force error if it is missing
        except AttributeError:
            print "Warning - in read_house - Adding 'Houses' section"
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
        if g_debug >= 2:
            print "houses.__new__()"
        self = object.__new__(cls)
        cls.__init__(self, *args, **kwargs)
        Singletons[cls] = self
        g_logger.info("Initialized all houses.")
        return self

    def __init__(self):
        if g_debug >= 2:
            print "houses.__init__()"

    def Start(self, p_pyhouses_obj):
        """Start processing for all things houses
        .
        May be stopped and then started anew to force reloading info.
        Invoked once no matter how many houses defined.
        """
        if g_debug >= 2:
            print "houses.API.Start() - Singleton"
        g_logger.info("Starting.")
        l_count = 0
        for l_house_xml in self.read_xml_config_houses(p_pyhouses_obj):
            if g_debug >= 4:
                print "houses.API.Start() - ", l_house_xml
            self.m_houses_data[l_count] = self.get_house_info(l_house_xml, l_count)
            l_count += 1
        if g_debug >= 2:
            print "houses.API.Start() - {0:} houses loaded.".format(l_count)
        if g_debug >= 4:
            for l_entry in self.m_houses_data.itervalues():
                print "   ", l_entry
        g_logger.info("Started.")
        return self.m_houses_data

    def Stop(self):
        """Close down everything we started.
        Each stopped instance returns an up-to-date XML subtree to be written out.
        """
        if g_debug >= 2:
            print "\nhouses.API.Stop() - Count:{0:}".format(len(self.m_houses_data))
        g_logger.info("Stopping.")
        l_houses_xml = ET.Element('Houses')
        for l_house in self.m_houses_data.itervalues():
            if g_debug >= 4:
                print "houses.Stop() - House:{0:}, Key:{1:}".format(l_house.Name, l_house.Key), l_house.HouseAPI
            l_houses_xml.append(l_house.HouseAPI.Stop(l_houses_xml, l_house.Object))  # append to the xml tree
        self.save_all_houses(l_houses_xml)
        g_logger.info("Stopped.")

    def Reload(self, p_pyhouses_obj):
        if g_debug >= 2:
            print "houses.API.Reload()"
        l_houses_xml = ET.Element('Houses')
        for l_house in self.m_houses_data.itervalues():
            l_houses_xml.append(l_house.HouseAPI.Reload(l_house.Object))  # append to the xml tree
        self.save_all_houses(l_houses_xml)
        return l_houses_xml

    def get_houses_obj(self):
        return self.m_houses_data

# ##  END DBK
