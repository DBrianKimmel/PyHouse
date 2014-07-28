"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/families/Insteon/test/test_decoder.py
@author: briank
@contact: <d.briankimmel@gmail.com>
@Copyright: (c)  2014 by briank
@license: MIT License
@note: Created on Jul 18, 2014
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files
# from Modules.lights.lighting import LightData
from Modules.Core.data_objects import PyHouseData, ControllerData
from Modules.families.Insteon import decoder
from Modules.families.Insteon import Insteon_PLM
from Modules.housing import house
from Modules.utils.tools import PrettyPrintAny
from Modules.Core import setup
from test import xml_data


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = setup.build_pyhouse_obj(self)
        self.m_pyhouse_obj.Xml.XmlRoot = self.m_root_xml
        #
        self.m_api = decoder.Utility()
        self.m_house_api = house.API()
        self.m_pyhouse_obj = self.m_house_api.update_pyhouse_obj(self.m_pyhouse_obj)
        return self.m_pyhouse_obj


class Test_01(SetupMixin, unittest.TestCase):

    def setUp(self):
        self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        SetupMixin.setUp(self)

    def test_0101_FindAddress(self):
        l_obj = self.m_api._find_addr(self.m_pyhouse_obj.House.OBJs.Controllers, 'A1.B2.C3')
        PrettyPrintAny(l_obj, 'Found Object', 120)

# ## END DBK
