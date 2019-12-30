"""
@name:      Modules/Housing/Security/_test/test_security.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 1, 2016
@summary:   Test

Passed all 13 tests - DBK - 2018-02-13

"""

__updated__ = '2019-12-29'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_security')


class A1(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-01-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.security_sect.tag, 'SecuritySection')
        self.assertEqual(self.m_xml.garagedoor_sect.tag, 'GarageDoorSection')
        self.assertEqual(self.m_xml.garagedoor.tag, 'GarageDoor')
        self.assertEqual(self.m_xml.motiondetector_sect.tag, 'MotionDetectorSection')
        self.assertEqual(self.m_xml.motiondetector.tag, 'Motion')

    def test_02_Xml(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj._Config.XmlRoot))
        pass

    def test_03_Family(self):
        self.assertEqual(self.m_family['Insteon'].Name, 'Insteon')

# ## END DBK
