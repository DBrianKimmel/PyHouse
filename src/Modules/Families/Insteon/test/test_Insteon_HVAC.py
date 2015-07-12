"""
@name:      PyHouse/src/Modules/Families/Insteon/test/test_Insteon_HVAC.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 6, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Core.data_objects import PyHouseData, ControllerData
from Modules.Families.Insteon import Insteon_HVAC
from Modules.Families import family
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny



class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()



class C01_Util(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_Class(self):
        Insteon_HVAC.Util().get_device_obj(self.m_pyhouse_obj, 'xxx')

# ## END DBK
