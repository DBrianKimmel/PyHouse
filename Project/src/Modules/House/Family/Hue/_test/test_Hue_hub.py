"""
@name:      Modules/House/Family/Hue/_test/test_Hue_hub.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2020 by D. Brian Kimmel
@note:      Created on Jan 2, 2018
@license:   MIT License
@summary:

Passed all 11 tests - DBK - 2019-03-16

"""

__updated__ = '2020-02-14'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.House import HouseInformation
from Modules.House.Family.Hue.hue_hub import HueHub

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """ Set up pyhouse object
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_version = '1.4.0'


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_Hue_hub')


class B1_Body(SetupMixin, unittest.TestCase):
    """ This section tests the setup
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_device = None

    def test_01_Light(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_ctl = LightControlInformation()
        # print(PrettyFormatAny.form(l_ctl, 'B1-01-A - LightControlInformation'))
        l_res = Hue_hub.generate_light_body_json(l_ctl)
        print(PrettyFormatAny.form(l_res, 'B1-01-B - Json'))

    def test_02_Light(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_ctl = LightControlInformation()
        l_ctl.BrightnessPct = 50
        # print(PrettyFormatAny.form(l_ctl, 'B1-02-A - LightControlInformation'))
        l_res = Hue_hub.generate_light_body_json(l_ctl)
        print(PrettyFormatAny.form(l_res, 'B1-02-B - Json'))

    def test_03_Light(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_ctl = LightControlInformation()
        l_ctl.BrightnessPct = 99
        # print(PrettyFormatAny.form(l_ctl, 'B1-03-A - LightControlInformation'))
        l_res = Hue_hub.generate_light_body_json(l_ctl)
        print(PrettyFormatAny.form(l_res, 'B1-03-B - Json'))

    def test_04_Light(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_ctl = LightControlInformation()
        l_ctl.BrightnessPct = 100
        # print(PrettyFormatAny.form(l_ctl, 'B1-04-A - LightControlInformation'))
        l_res = Hue_hub.generate_light_body_json(l_ctl)
        print(PrettyFormatAny.form(l_res, 'B1-04-B - Json'))


class B2_Prep(SetupMixin, unittest.TestCase):
    """ This section tests the setup
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_device = None

    def test_01_PyHouse(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        self.assertIsInstance(self.m_pyhouse_obj.House, HouseInformation)

    def test_03_House(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        l_url = HueHub(self.m_pyhouse_obj)._build_uri(b'/config')
        print(PrettyFormatAny.form(l_url, '1-03-A - Url'))
        pass

    def test_04_Objs(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        pass

    def test_05_XML(self):
        """ Did we get everything set up for the rest of the tests of this class.
        """
        pass

    def test_06_Device(self):
        """ Be sure that the XML contains the right stuff.
        """
        pass

# ## END DBK
