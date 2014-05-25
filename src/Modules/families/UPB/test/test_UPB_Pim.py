"""
@name: PyHouse/Modules/Core/node_local.py

# -*- test-case-name: PyHouse.Modules.Core.test.test_node_local -*-

Created on Apr 8, 2013

@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@license: MIT License

@summary: Test the UPB controller.

"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.families.UPB import UPB_Pim
from Modules.lights import lighting_core
from test import xml_data
from Modules.Core.data_objects import PyHouseData, HouseData, ControllerData

XML = xml_data.XML_LONG


class Test(unittest.TestCase):


    def setUp(self):
        self.m_root_element = ET.fromstring(XML)
        self.m_house_obj = HouseData()
        self.m_controller = ControllerData()
        self.m_api = UPB_Pim.API()

    def tearDown(self):
        pass


    def test_001_load_xml(self):
        print("Root Element {0:}".format(self.m_root_element))
        self.m_api.Start(self.m_house_obj, self.m_controller)

# ## END DBK
