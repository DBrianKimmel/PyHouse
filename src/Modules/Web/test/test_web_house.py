"""
@name:      PyHouse/src/Modules/Web/test/trst_web_house.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 21, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Web import web_house
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny



class Workspace(object):
    def __init__(self):
        self.m_pyhouse_obj = None



class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_workspace_obj.m_pyhouse_obj = self.m_pyhouse_obj



class C01_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        # self.m_pyhouse_obj.House.RefOBJs.FamilyData = family.API().build_lighting_family_info()
        # self.m_api = lighting_controllers.LCApi(self.m_pyhouse_obj)
        # self.m_controller_obj = ControllerData()

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouseData')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection', 'XML - No Controllers section')
        self.assertEqual(self.m_xml.controller.tag, 'Controller', 'XML - No Controller section')

    def test_02_Json(self):
        l_api = web_house.HouseElement(self.m_workspace_obj, None)
        l_json = l_api.getServerData()
        PrettyPrintAny(l_json, 'JSON', 70)

# ## END DBK