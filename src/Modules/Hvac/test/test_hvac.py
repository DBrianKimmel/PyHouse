"""
@name:      PyHouse/src/Modules/Hvac/test/test_hvac.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 12, 2015
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest


# Import PyMh files and modules.
from Modules.Core.data_objects import ThermostatData
from Modules.Core import conversions
from Modules.Hvac import thermostats
from Modules.Families import family
from Modules.Web import web_utils
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = thermostats.API()
        self.m_thermostat_obj = ThermostatData()



class Test(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()

    def tearDown(self):
        pass

    def testName(self):
        pass

# ## END DBK
