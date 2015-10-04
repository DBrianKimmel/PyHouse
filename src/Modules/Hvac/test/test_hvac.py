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
from Modules.Hvac.hvac import API as hvacAPI
from Modules.Hvac import thermostats
from Modules.Families import family
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        # self.m_pyhouse_obj.House.FamilyData = family.API().build_lighting_family_info()
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = hvacAPI(self.m_pyhouse_obj)
        self.m_thermostat_obj = ThermostatData()


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        self.assertEqual(self.m_pyhouse_obj.House.Hvac, None)
        # print(PrettyFormatAny.form(self.m_xml.thermostat_sect, 'Thermostat'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'Family'))

    def test_02_Load(self):
        """
        """
        l_obj = self.m_api.LoadXml(self.m_pyhouse_obj)
        print(PrettyFormatAny.form(l_obj[0], 'Loaded'))

# ## END DBK
