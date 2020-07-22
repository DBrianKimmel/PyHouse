"""
@name:      Modules/Core/Drivers/_test/test_Serial.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 30, 2015
@Summary:

"""

__updated__ = '2019-10-08'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import ControllerInformation
from Modules.Housing.Lighting.lighting_controllers import Api as controllerApi
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_controller_obj = ControllerInformation()
        self.m_ctlr_api = controllerApi()


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_Serial')


class A1_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Tags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))

    def test_01_Raw(self):
        l_raw = XML_SERIAL
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:8], '<Serial>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_SERIAL)
        print(PrettyFormatAny.form(l_xml, 'A2-02-A - Parsed\n'))
        self.assertEqual(l_xml.tag, "Serial")

    def test_03_Raw(self):
        l_raw = XML_USB
        # print('A2-03-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:5], '<USB>')

    def test_04_Parsed(self):
        l_xml = ET.fromstring(XML_USB)
        print(PrettyFormatAny.form(l_xml, 'A2-04-A Parsed'))
        self.assertEqual(l_xml.tag, "USB")

"""
class Z_Suite(unittest.TestCase):

    def setUp(self):
        self.m_test = runner.TestLoader()

    def test_Serial(self):
        l_package = runner.TestLoader().loadPackage(I_test)
        l_ret = reporter.Reporter()
        l_package.run(l_ret)
        l_ret.done()
        #
        print('\n====================\n*** test_Serial ***\n{}\n'.format(l_ret))
"""

# ## END DBK
