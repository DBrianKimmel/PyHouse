"""
-*- test-case-name: PyHouse.Modules.computer.test.test_computer -*-

@name:      PyHouse/src/Modules/computer/computer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@note:      Created on Jun 24, 2014
@license:   MIT License
@summary:   Handle the computer information.

This handles the Computer part of the node.  (The other part is "house").

This takes care of starting all the computer modules (In Order).
    Logging
    Mqtt Broker(s)
    Nodes
    Internet Connection(s)
    Web Server(s)

"""

# Import system type stuff
import platform
from xml.etree import ElementTree as ET

# Import PyHouse files
from Modules.Core.data_objects import CompAPIs, ComputerInformation, NodeData, MqttBrokerData
from Modules.Computer import logging_pyh as Logger
from Modules.Computer.Mqtt import broker
from Modules.Computer.Nodes import nodes
from Modules.Computer.Internet import internet
from Modules.Web import web_server
from Modules.Utilities.xml_tools import XmlConfigTools
from Modules.Utilities import uuid_tools
# from Modules.Utilities.tools import PrettyPrintAny

LOG = Logger.getLogger('PyHouse.Computer       ')

MODULES = ['Communication', 'Mqtt', 'Internet' , 'Node', 'Weather', 'Web']


class ReadWriteConfigXml(XmlConfigTools):
    """
    """

    def _read_computer_base_xml(self, p_xml):
        l_xml = ComputerInformation()
        self.read_base_object_xml(l_xml, p_xml)
        l_xml.Active = True
        l_xml.Name = platform.node()
        l_xml.UUID = uuid_tools.get_uuid(l_xml.UUID)
        return l_xml

    def read_computer_xml(self, p_pyhouse_obj):
        l_xml = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
        l_comp = self._read_computer_base_xml(l_xml)
        return l_comp

    def _write_computer_base_xml(self, p_computer_obj):
        l_xml = self.write_base_object_xml('ComputerDivision', p_computer_obj)
        return l_xml

    def write_computer_xml(self, p_pyhouse_obj):
        l_xml = self._write_computer_base_xml(p_pyhouse_obj.Computer)
        return  l_xml


class Utility(ReadWriteConfigXml):
    """
    """

    m_pyhouse_obj = None

    def add_api_references(self, p_pyhouse_obj):
        p_pyhouse_obj.APIs.Comp = CompAPIs()
        p_pyhouse_obj.APIs.Comp.ComputerAPI = self
        p_pyhouse_obj.APIs.Comp.MqttAPI = broker.API()
        p_pyhouse_obj.APIs.Comp.CommunicationsAPI = None
        p_pyhouse_obj.APIs.Comp.EmailAPI = None
        p_pyhouse_obj.APIs.Comp.InternetAPI = internet.API()
        p_pyhouse_obj.APIs.Comp.NodesAPI = nodes.API()
        p_pyhouse_obj.APIs.Comp.WeatherAPI = web_server.API()
        p_pyhouse_obj.APIs.Comp.WebAPI = web_server.API()

    def update_data_structures(self, p_pyhouse_obj):
        p_pyhouse_obj.Computer = ComputerInformation()
        p_pyhouse_obj.Computer.Mqtt[0] = MqttBrokerData()
        p_pyhouse_obj.Computer.Nodes[0] = NodeData()

    def start_component_apis(self, p_pyhouse_obj):
        p_pyhouse_obj.APIs.Comp.MqttAPI.Start(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Comp.InternetAPI.Start(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Comp.NodesAPI.Start(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Comp.WebAPI.Start(p_pyhouse_obj)

    def stop_component_apis(self, p_pyhouse_obj):
        p_pyhouse_obj.APIs.Comp.MqttAPI.Stop()
        p_pyhouse_obj.APIs.Comp.InternetAPI.Stop()
        p_pyhouse_obj.APIs.Comp.NodesAPI.Stop()
        p_pyhouse_obj.APIs.Comp.WebAPI.Stop()

    def save_component_apis(self, p_pyhouse_obj):
        l_xml = self.write_computer_xml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Comp.MqttAPI.SaveXml(l_xml)
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
        LOG.info('Starting')
        self.update_data_structures(p_pyhouse_obj)
        self.m_pyhouse_obj = p_pyhouse_obj
        self.add_api_references(p_pyhouse_obj)
        p_pyhouse_obj.Computer = self.read_computer_xml(p_pyhouse_obj)
        self.start_component_apis(p_pyhouse_obj)
        LOG.info('Started')

    def Stop(self):
        """
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
        LOG.info("Saved XML.")

# ## END DBK
