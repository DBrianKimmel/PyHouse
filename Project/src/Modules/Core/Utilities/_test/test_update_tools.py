"""
@name:      Modules/Core/Utilities/_test/test_update_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jan 11, 2019
@summary:   Test

"""

__updated__ = '2019-07-31'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest
from datetime import datetime

# Import PyMh files
from test.xml_data import XML_LONG, TESTING_VERSION, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.House.test.xml_housing import TESTING_HOUSE_DIVISION
from Modules.House.Entertainment.pandora.test.xml_pandora import \
    XML_PANDORA_SECTION, \
    L_PANDORA_SECTION_START, \
    TESTING_PANDORA_SECTION
from Modules.Core.Utilities import update_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Core.data_objects import DeviceInformation, LoginData

DATE_1 = datetime(2001, 1, 2)
DATE_2 = datetime(2099, 12, 30)


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):

    def setUp(self):
        pass

    def test_00_Print(self):
        print('Id: test_update_tools')


class A1_XML(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules._test.xml_data' file is correct
    and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly.
        """
        l_xml = self.m_xml.entertainment_sect
        # print(PrettyFormatAny.form(l_xml, 'A1-01-A - Entertainment XML'))

    def test_02_XmlTags(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'A1-02-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)


class A2_SetupXml(SetupMixin, unittest.TestCase):
    """ Test that the XML contains no syntax errors.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_PANDORA_SECTION
        # print('A2-01-A - Raw\n{}'.format(l_raw))
        self.assertEqual(l_raw[:16], L_PANDORA_SECTION_START[:16])

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_PANDORA_SECTION)
        print('A2-02-A - Parsed\n{}'.format(PrettyFormatAny.form(l_xml, 'A2-02-A - Parsed')))
        self.assertEqual(l_xml.tag, TESTING_PANDORA_SECTION)


class B1_Dates(SetupMixin, unittest.TestCase):
    """
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Missing(self):
        l_date = datetime.now()
        l_ok = update_tools.is_update_needed(None, None)
        self.assertEqual(l_ok, False)
        l_ok = update_tools.is_update_needed(None, l_date)
        self.assertEqual(l_ok, False)
        l_ok = update_tools.is_update_needed(l_date, None)
        self.assertEqual(l_ok, False)

    def test_02_NotObj(self):
        l_date = datetime.now()
        print(l_date)
        l_ok = update_tools.is_update_needed(l_date, l_date)
        self.assertEqual(l_ok, False)

    def test_03_Equal(self):
        l_obj = DeviceInformation()
        l_date = datetime.now()
        l_obj.LastUpdate = l_date
        l_ok = update_tools.is_update_needed(l_obj, l_obj)
        self.assertEqual(l_ok, True)

    def test_04_Older(self):
        """
        now > 2001
        """
        l_local = DeviceInformation()
        l_remote = LoginData()
        l_date = datetime.now()
        l_local.LastUpdate = l_date
        l_remote.LastUpdate = DATE_1
        l_ok = update_tools.is_update_needed(l_local, l_remote)
        self.assertEqual(l_ok, False)

    def test_05_Newer(self):
        """
        now < 2099
        """
        l_local = DeviceInformation()
        l_remote = LoginData()
        l_date = datetime.now()
        l_local.LastUpdate = l_date
        l_remote.LastUpdate = DATE_2
        l_ok = update_tools.is_update_needed(l_local, l_remote)
        self.assertEqual(l_ok, True)

    def test_06_Older(self):
        """
        2001 < Now
        """
        l_local = DeviceInformation()
        l_remote = LoginData()
        l_date = datetime.now()
        l_local.LastUpdate = DATE_1
        l_remote.LastUpdate = l_date
        l_ok = update_tools.is_update_needed(l_local, l_remote)
        self.assertEqual(l_ok, True)

    def test_07_Older(self):
        """
        2099 > Now
        """
        l_local = DeviceInformation()
        l_remote = LoginData()
        l_date = datetime.now()
        l_local.LastUpdate = DATE_2
        l_remote.LastUpdate = l_date
        l_ok = update_tools.is_update_needed(l_local, l_remote)
        self.assertEqual(l_ok, False)

# ## END DBK
