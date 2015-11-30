"""
@name:      PyHouse/src/Modules/Web/test/test_web_rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Oct 20, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Web import web_rooms
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj


class Workspace(object):
    def __init__(self):
        self.m_pyhouse_obj = None



class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_workspace_obj = Workspace()
        self.m_workspace_obj.m_pyhouse_obj = self.m_pyhouse_obj



class C01_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        # self.m_pyhouse_obj.House.FamilyData = family.API().build_lighting_family_info()
        # self.m_controller_obj = ControllerData()

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection', 'XML - No Controllers section')
        self.assertEqual(self.m_xml.controller.tag, 'Controller', 'XML - No Controller section')

    def test_02_Json(self):
        l_api = web_rooms.RoomsElement(self.m_workspace_obj, None)
        l_json = l_api.getServerData()

# ## END DBK
