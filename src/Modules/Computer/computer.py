"""
-*- test-case-name: PyHouse.Modules.computer.test.test_computer -*-

@name: PyHouse/src/Modules/computer/computer.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Jun 24, 2014
@license: MIT License
@summary: Handle the computer information.

This handles the Computer part of the node.  (The other part is "house").

This takes care of starting all the computer modules.

"""

# Import system type stuff
from xml.etree import ElementTree as ET

# Import PyHouse files
from Modules.Core.data_objects import ComputerInformation
from Modules.Computer.Internet import internet
from Modules.Computer.Nodes import nodes
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.xml_tools import XmlConfigTools
from Modules.Web import web_server
# from Modules.Utilities.tools import PrettyPrintAny

LOG = Logger.getLogger('PyHouse.Computer       ')

MODULES = ['Communication', 'Internet' , 'Node', 'Weather', 'Web']


class ReadWriteConfigXml(XmlConfigTools):
    """
    """

    def read_computer_xml(self, p_pyhouse_obj):
        l_xml = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
        return l_xml

    def write_computer_xml(self):
        l_xml = ET.Element('ComputerDivision')
        return  l_xml


class Utility(ReadWriteConfigXml):
    """
    """

    def update_pyhouse_obj(self, p_pyhouse_obj):
        p_pyhouse_obj.Computer = ComputerInformation()

    def add_api_references(self, p_pyhouse_obj):
        p_pyhouse_obj.APIs.Comp.InternetAPI = internet.API()
        p_pyhouse_obj.APIs.Comp.NodesAPI = nodes.API()
        p_pyhouse_obj.APIs.Comp.WebAPI = web_server.API()

    def start_component_apis(self, p_pyhouse_obj):
        p_pyhouse_obj.APIs.Comp.InternetAPI.Start(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Comp.NodesAPI.Start(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Comp.WebAPI.Start(p_pyhouse_obj)

    def stop_component_apis(self, p_pyhouse_obj):
        p_pyhouse_obj.APIs.Comp.InternetAPI.Stop()
        p_pyhouse_obj.APIs.Comp.NodesAPI.Stop()
        p_pyhouse_obj.APIs.Comp.WebAPI.Stop()

    def save_component_apis(self, p_pyhouse_obj):
        l_xml = self.write_computer_xml()
        p_pyhouse_obj.APIs.Comp.InternetAPI.SaveXml(l_xml)
        p_pyhouse_obj.APIs.Comp.NodesAPI.SaveXml(l_xml)
        p_pyhouse_obj.APIs.Comp.WebAPI.SaveXml(l_xml)
        return l_xml


class API(Utility):
    """
    """

    def Start(self, p_pyhouse_obj):
        """
        Start processing
        """
        # LOG.info('Starting')
        self.m_pyhouse_obj = p_pyhouse_obj
        self.update_pyhouse_obj(p_pyhouse_obj)
        self.add_api_references(p_pyhouse_obj)
        self.read_computer_xml(p_pyhouse_obj)
        self.start_component_apis(p_pyhouse_obj)
        LOG.info('Started')

    def Stop(self):
        """Stop all houses.
        Append the house XML to the passed in xlm tree.
        """
        self.stop_component_apis(self.m_pyhouse_obj)
        LOG.info("Stopped.")

    def WriteXml(self, p_xml):
        """
        Take a snapshot of the current Configuration/Status and write out an XML file.
        """
        l_xml = self.save_component_apis(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        # LOG.info("Saved XML.")

# ## END DBK
