"""
-*- test-case-name: PyHouse.src.Modules.hvac.test.test_thermostat -*-

@name: PyHouse/src/Modules/hvac/thermostat.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Mar 27, 2013
@summary: This module is for testing local node data.

Created on Mar 27, 2013

@author: briank
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import ThermostatData
from Modules.utils import xml_tools
from Modules.utils import pyh_log

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.Thermostat  >>')


class ReadWriteConfigXml(xml_tools.XmlConfigTools):
    """
    """
    m_count = 0

    def read_one_thermostat(self, p_thermostat_element):
        l_thermostat_obj = ThermostatData()
        self.read_base_object_xml(l_thermostat_obj, p_thermostat_element)
        l_thermostat_obj.Key = self.m_count  # Renumber
        l_thermostat_obj.Comment = self.get_text_from_xml(p_thermostat_element, 'Comment')
        return l_thermostat_obj

    def read_all_thermostats(self, p_pyhouse_obj):
        """
        """
        l_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
        l_xml = l_xml.find('ThermostatSection')
        l_dict = {}
        return l_dict

    def write_one_thermostat(self, p_thermostat_obj):
        l_thermostat_xml = ET.Element('Thermostat')
        return l_thermostat_xml
        pass

    def write_all_thermostats(self, p_pyhouse_obj):
        """Create a sub tree for 'Internet' - the sub elements do not have to be present.
        @return: a sub tree ready to be appended to "something"
        """
        l_thermostat_xml = ET.Element('ThermostatSection')
        return l_thermostat_xml


class API(ReadWriteConfigXml):

    m_house_obj = None

    def __init__(self):
        LOG.info("Initialized.")

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.read_all_thermostats(p_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self, p_xml):
        l_xml = self.write_all_thermostats(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Stopped.")
        return l_xml

# ## END DBK
