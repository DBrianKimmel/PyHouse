"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_setup -*-

@name: PyHouse/src/Modules/Core/setup.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Mar 1, 2014
@license: MIT License
@summary: This module sets up the Core part of PyHouse.


This will set up this node and then find all other nodes in the same domain (House).

Then start the House and all the sub systems.
"""

# Import system type stuff
import datetime
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import CoreServicesInformation, XmlInformation
from Modules.Comps import computer
# from Modules.entertain import entertainment
from Modules.housing import house
from Modules.utils import pyh_log
from Modules.utils import xml_tools
from Modules.utils.xml_tools import XmlConfigTools
from Modules.utils.tools import PrettyPrintAny

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.CoreSetup   ')

INTER_NODE = 'tcp:port=8581'
INTRA_NODE = 'unix:path=/var/run/pyhouse/node:lockfile=1'


class ReadWriteConfigXml(XmlConfigTools):
    """Use the internal data to read / write an updated XML config file.
    """

    def read_xml_config_info(self, p_pyhouse_obj):
        """This will read the XML config file(s).
        This puts the XML tree and file name in the pyhouse object for use by various modules.
        """
        p_pyhouse_obj.Xml.XmlFileName = l_name = xml_tools.open_config_file()
        try:
            l_xmltree = ET.parse(l_name)
            # print('Setup-XML file {0:} parsed OK.'.format(l_name))
        except SyntaxError as e_error:
            print('Setup-XML file ERROR - {0:} - {1:}'.format(e_error, l_name))
            xml_tools.ConfigFile().create_empty_config_file(l_name)
            l_xmltree = ET.parse(p_pyhouse_obj.Xml.XmlFileName)
        p_pyhouse_obj.Xml.XmlRoot = l_xmltree.getroot()

    def write_xml_config_file(self):
        LOG.info("Saving all data to XML file.")
        l_xml = ET.Element("PyHouse")
        xml_tools.PutGetXML().put_text_attribute(l_xml, 'Version', self.m_pyhouse_obj.Xml.XmlVersion)
        l_xml.append(ET.Comment('Updated by PyHouse {0:}'.format(datetime.datetime.now())))
        self.m_pyhouse_obj.APIs.ComputerAPI.Stop(l_xml)
        self.m_pyhouse_obj.APIs.HouseAPI.Stop(l_xml)
        xml_tools.write_xml_file(l_xml, self.m_pyhouse_obj.Xml.XmlFileName)


class Utility(ReadWriteConfigXml):
    """
    """

    def log_start(self, p_pyhouse_obj):
        """Logging is the very first thing we start so we can see errors in the starting process
        """
        l_log = pyh_log.API()
        l_log.Start(p_pyhouse_obj)
        LOG.info("\n------------------------------------------------------------------\n\n")


class API(Utility):

    def __init__(self, p_pyhouse_obj):
        """
        This runs before the reactor has started - Be Careful!
        """
        p_pyhouse_obj.Services = CoreServicesInformation()
        p_pyhouse_obj.Xml = XmlInformation()
        p_pyhouse_obj.APIs.ComputerAPI = computer.API()
        p_pyhouse_obj.APIs.HouseAPI = house.API()
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self, p_pyhouse_obj):
        """The reactor is now running.
        """
        self.read_xml_config_info(self.m_pyhouse_obj)
        self.log_start(p_pyhouse_obj)
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.APIs.ComputerAPI.Start(p_pyhouse_obj)  # Logs now started
        p_pyhouse_obj.APIs.HouseAPI.Start(p_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        self.write_xml_config_file()
        LOG.info("Stopped.")

    def Reload(self):
        self.write_xml_config_file()
        LOG.info("Reloaded.")

# ## END DBK
