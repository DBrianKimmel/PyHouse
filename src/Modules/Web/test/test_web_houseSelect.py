"""
@name:      PyHouse/src/Modules/web/test/test_web_houseSelect.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by briank
@license:   MIT License
@note:      Created on Jun 6, 2014
@Summary:

"""

# Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Web import web_houseSelect
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_10(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = web_houseSelect.HouseSelectElement(None)

    def tearDown(self):
        pass

    def test_1011_getHousesToSelect(self):
        l_json = self.m_api.getHousesToSelect(None)
        PrettyPrintAny(l_json, 'Houses to select')

    def test_1012_getSelectedHouseData(self):
        pass

# ## END DBK
