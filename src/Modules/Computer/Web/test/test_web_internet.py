"""
@name:      PyHouse/src/Modules/Computer/Web/test/test_web_internet.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 20, 2014
@Summary:

Passed all 3 tests - DBK - 2016-11-21

"""
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2017-01-19'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Computer.Web import web_internet
from Modules.Computer.Web.web import WorkspaceData
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_web_internet')


class A1_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.internet_sect.tag, 'InternetSection')


class B1_Data(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_workspace = WorkspaceData
        self.m_workspace.m_pyhouse_obj = self.m_pyhouse_obj

    def test_01_Get(self):
        """ Be sure that the XML contains the right stuff.
        """
        l_comp = web_internet.InternetElement(self.m_workspace, None).getInternetData()
        # print(PrettyFormatAny.form(l_comp, 'B1-01-A - Data'))

# ## END DBK
