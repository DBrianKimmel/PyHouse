"""
-*- test-case-name: PyHouse.Modules.computer.test.test_computer -*-

@name: PyHouse/src/Modules/computer/computer.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Jun 24, 2014
@license: MIT License
@summary: Handle the computer information.

"""

# Import system type stuff
from xml.etree import ElementTree as ET

# Import PyHouse files
from Modules.Core.data_objects import ComputerInformation
import internet
from Modules.Core import nodes
from Modules.utils import pyh_log
from Modules.utils.xml_tools import XmlConfigTools
from Modules.web import web_server
# from Modules.utils.tools import PrettyPrintAny

g_debug = 9
LOG = pyh_log.getLogger('PyHouse.Computer    ')


class ReadWriteConfigXml(XmlConfigTools):
    """
    """

    def read_computer_xml(self):
        pass

    def write_computer_xml(self):
        """Replace the data in the 'ComputerDivision' section with the current data.
        """
        l_xml = ET.Element('ComputerDivision')
        return l_xml


class Utility(ReadWriteConfigXml):
    """
    """


class API(Utility):
    """
    """

    def __init__(self):
        """
        """

    def Start(self, p_pyhouse_obj):
        """
        Start processing
        """
        LOG.info('Starting')
        p_pyhouse_obj.Computer = ComputerInformation()
        p_pyhouse_obj.APIs.InternetAPI = internet.API()
        p_pyhouse_obj.APIs.LogsAPI = pyh_log.API()
        p_pyhouse_obj.APIs.NodesAPI = nodes.API()
        p_pyhouse_obj.APIs.WebAPI = web_server.API()
        self.m_pyhouse_obj = p_pyhouse_obj
        #
        p_pyhouse_obj.APIs.InternetAPI.Start(p_pyhouse_obj)
        p_pyhouse_obj.APIs.LogsAPI.Start(p_pyhouse_obj)
        p_pyhouse_obj.APIs.NodesAPI.Start(p_pyhouse_obj)
        p_pyhouse_obj.APIs.WebAPI.Start(p_pyhouse_obj)
        # PrettyPrintAny(p_pyhouse_obj.Computer, 'Computer - Start - PyHouse.Computer ')
        LOG.info('Started')

    def Stop(self, p_xml):
        """Stop all houses.
        Append the house XML to the passed in xlm tree.
        """
        LOG.info("Stopping Computer.")
        l_xml = self.write_computer_xml()
        self.m_pyhouse_obj.APIs.InternetAPI.Stop(l_xml)
        self.m_pyhouse_obj.APIs.LogsAPI.Stop(l_xml)
        self.m_pyhouse_obj.APIs.NodesAPI.Stop(l_xml)
        self.m_pyhouse_obj.APIs.WebAPI.Stop(l_xml)
        p_xml.append(l_xml)
        LOG.info("Stopped.")

# ## END DBK
