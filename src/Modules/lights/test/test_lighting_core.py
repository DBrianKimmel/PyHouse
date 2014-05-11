"""
PyHouse/Modules/lights/test/test_lighting_core.py

Created on May 4, 2014

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License

@summary: This module is for testing lighting Core.
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.lights import lighting_core
from test import xml_data
from Modules.Core.data_objects import PyHouseData, BaseLightingData

XML = xml_data.XML


class Test_02_ReadXML(unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        self.m_pyhouses_obj = PyHouseData()
        self.m_pyhouses_obj.XmlRoot = ET.fromstring(XML)
        self.m_api = lighting_core.CoreAPI()

    def test_0201_read_xml(self):
        self.m_api.read_light_common(p_entry_xml, p_device_obj, p_house_obj)(self.m_pyhouses_obj)
        self.assertEqual(self.m_pyhouses_obj.LogsData.Debug, '/var/log/pyhouse/debug')
        self.assertEqual(self.m_pyhouses_obj.LogsData.Error, '/var/log/pyhouse/error')

# ## END DBK
