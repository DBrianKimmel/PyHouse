#!/usr/bin/env python

""" config_xml

Notice that there  is no logging in this module.
The logging file location is read in as a part of the configuration.
All errors are printed out.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from src.utils import xml_tools


g_debug = 0
g_xmltree = ''
g_logger = None

class ReadConfig(object):
    """
    """

    m_filename = None

    def __init__(self):
        """Open the xml config file.

        If the file is missing, an empty minimal skeleton is created.
        """
        global g_xmltree
        self.m_filename = xml_tools.open_config_file()
        try:
            g_xmltree = ET.parse(self.m_filename)
        except SyntaxError:
            xml_tools.ConfigFile().create_empty_config_file(self.m_filename)
            g_xmltree = ET.parse(self.m_filename)
        self.m_root = g_xmltree.getroot()


class WriteConfig(object):
    """Use the internal data to write an updated config file.

    This is called from the web interface or the GUI when the data has been changed.
    """

    m_filename = None
    m_root = None

    def __init__(self):
        global g_xmltree
        self.m_filename = xml_tools.open_config_file()
        try:
            g_xmltree = ET.parse(self.m_filename)
        except SyntaxError:
            xml_tools.ConfigFile().create_empty_config_file(self.m_filename)
            g_xmltree = ET.parse(self.m_filename)
        self.m_root = g_xmltree.getroot()



class API(ReadConfig, WriteConfig):

    def __init__(self, p_file):
        print "ERROR config_xml.API() should not be used"

# ## END DBK
