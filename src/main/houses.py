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
from house import house
from configure import xml_tools
from main import internet
from main import weather

g_debug = 3
m_logger = None

Singletons = {}
Houses_Data = {}
HouseCount = 0


class HousesData(object):
    """This class holds the data about all houses defined in xml.
    """

    def __init__(self):
        self.Key = 0
        self.Name = None
        self.HouseAPI = None
        self.Object = {}

    def __str__(self):
        return "Houses:: Name:{0:} ".format(self.Name)


class HouseReadWriteConfig(xml_tools.ConfigFile, HousesData):

    m_filename = None
    m_root = None
    m_xmltree = None

    def __init__(self):
        """Open the xml config file.

        If the file is missing, an empty minimal skeleton is created.
        """
        self.m_filename = xml_tools.open_config()
        try:
            self.m_xmltree = ET.parse(self.m_filename)
        except SyntaxError:
            xml_tools.ConfigFile().create_empty_config_file(self.m_filename)
            self.m_xmltree = ET.parse(self.m_filename)
        self.m_root = self.m_xmltree.getroot()

    def get_tree(self):
        return self.m_xmltree

    def get_root(self):
        return self.m_root

    def write_create_empty(self, p_name):
        """Create an empty XML section to be filled in.

        @param p_name: is the name of the xml section to be written.
        @return: the e-tree section to be used.
        """
        l_sect = self.m_root.find(p_name)
        try:
            l_sect.clear()
        except AttributeError:
            print "Creating a new sub-element named ", p_name
            l_sect = ET.SubElement(self.m_root, p_name)
        return l_sect

    def write_houses(self):
        """Replace the data in the 'Houses' section with the current data.
        """
        if g_debug > 2:
            print "houses.write_house() - Writing xml file to:{0:}".format(self.m_filename)
        self.m_root = self.m_xmltree.getroot()
        print " tree ", self.m_root
        # for l_elem in self.m_xmltree.iter():
        #    print "  tree "
        # print " ", xml_tools.prettify(self.m_root)
        self.write_file(self.m_xmltree, self.m_filename)


class LoadSaveAPI(HouseReadWriteConfig):
    """
    """

    def load_all_houses(self):
        """Load all the house info.
        """
        if g_debug > 1:
            print "houses.load_all_houses()"
        self.l_rwc = HouseReadWriteConfig()
        return self.l_rwc.get_root(), self.l_rwc.get_tree()

    def save_all_houses(self):
        if g_debug > 1:
            print "houses.save_all_houses()"
        self.l_rwc.write_houses()


class API(LoadSaveAPI):
    """
    """

    m_schedules = []

    def __new__(cls, *args, **kwargs):
        """This is for all houses.
        Set up the common / global things in this singleton.
        """
        if cls in Singletons:
            return Singletons[cls]
        if g_debug > 0:
            print "houses.__new__()"
        self = object.__new__(cls)
        cls.__init__(self, *args, **kwargs)
        Singletons[cls] = self
        #
        self.m_logger = logging.getLogger('PyHouse.Houses')
        self.m_logger.info("Initializing all houses.")
        internet.Init()
        weather.Init()
        self.m_logger.info("Initialized.")
        if g_debug > 0:
            print "houses.__new__() all houses initialized now."
        #
        return self

    def __init__(self):
        if g_debug > 0:
            print "houses.__init__()"
            print

    def Start(self):
        """Start processing for all things house.
        May be stopped and then started anew to force reloading info.
        Invoked once no matter how many houses defined.
        """
        if g_debug > 0:
            print "houses.API.Start() - Singleton"
        self.m_logger.info("Starting.")
        l_count = 0
        self.m_root, _l_tree = self.load_all_houses()
        #
        try:
            l_sect = self.m_root.find('Houses')
            l_list = l_sect.iterfind('House')  # use l_sect to force error if it is missing
        except AttributeError:
            print "Warning - in read_house - Adding 'Houses' section"
            l_sect = ET.SubElement(self.m_root, 'Houses')
            l_list = l_sect.iterfind('House')
        for l_house_xml in l_list:
            print "\nCreating a new house named:{0:}".format(l_house_xml.get('Name'))
            l_houses_obj = HousesData()
            l_houses_obj.HouseAPI = house.API()
            l_houses_obj.Key = l_count
            l_house_obj = l_houses_obj.HouseAPI.Start(l_houses_obj, l_house_xml)
            l_houses_obj.Object = l_house_obj
            l_houses_obj.Name = l_house_obj.Name
            Houses_Data[l_count] = l_houses_obj
            l_count += 1
        if g_debug > 0:
            print "houses.API.Start() - {0:} houses all started.".format(l_count)
        internet.Start()
        weather.Start()
        self.m_logger.info("Started.")


    def Stop(self):
        """Close down everything we started.
        Each stopped instance returns an up-to-date XML subtree to be written out.
        """
        if g_debug > 0:
            print "houses.API.Stop()"
        self.m_logger.info("Stopping.")
        l_houses_xml = self.m_root.find('Houses')
        try:
            l_houses_xml.clear()
        except AttributeError:
            print "Creating a new sub-element named 'Houses'"
            l_houses_xml = ET.SubElement(self.m_root, 'Houses')
        for l_house in Houses_Data.itervalues():
            if g_debug > 1:
                print "houses.API.Stop() - Working on house:{0:}".format(l_house.Name)
            l_xml = l_house.HouseAPI.Stop(l_houses_xml)
            print "  Done with house..."
        internet.Stop()
        weather.Stop()
        self.save_all_houses()
        self.m_logger.info("Stopped.")

# ##  END
