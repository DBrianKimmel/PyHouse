"""
@name:      PyHouse/src/Modules/Computer/Web/test/test_web_house.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 21, 2014
@Summary:

Passed all 3 tests - DBK - 2016-11-21

"""
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2017-01-19'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Computer.Web import web_house
from Modules.Computer.Web.web import WorkspaceData


class Workspace(object):
    def __init__(self):
        self.m_pyhouse_obj = None


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_web_house')


class B1_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_workspace = WorkspaceData
        self.m_workspace.m_pyhouse_obj = self.m_pyhouse_obj

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection')
        self.assertEqual(self.m_xml.controller.tag, 'Controller')

    def test_02_Json(self):
        l_api = web_house.HouseElement(self.m_workspace)
        l_json = l_api.getHouseData()
        # print(PrettyFormatAny.form(l_json, 'B1-02-A - JSON'))

# ## END DBK
