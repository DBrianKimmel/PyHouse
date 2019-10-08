"""
@name:      PyHouse/Project/src/Modules/Entertainment/_test/test_entertainment.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 14, 2013
@summary:   Test

Passed all 13 tests - DBK - 2019-03-18

"""

__updated__ = '2019-10-08'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.Utilities.xml_tools import XmlConfigTools
from Modules.Housing.Entertainment.entertainment import Api as entertainmentApi
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = entertainmentApi(self.m_pyhouse_obj)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_entertainment')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_1_BuildObjects(self):
        """ Test to be sure the compound object was built correctly - Rooms is an empty dict.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Tags'))
        self.assertEqual(self.m_pyhouse_obj.House.Rooms, {})


class C1_Load(SetupMixin, unittest.TestCase):
    """ This will _test all of the sub modules ability to load their part of the XML file
            and this modules ability to put everything together in the structure
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_xml = XmlConfigTools.find_xml_section(self.m_pyhouse_obj, 'HouseDivision/EntertainmentSection')
        self.m_entertainment_obj = EntertainmentInformation()
        self.m_pyhouse_obj.House.Entertainment = EntertainmentInformation()  # Clear before loading

    def test_01_Setup(self):
        """
        """
        # print(PrettyFormatAny.form(self.m_xml, 'C1-01-A - Entertainment XML'))
        self.assertEqual(self.m_xml.tag, TESTING_ENTERTAINMENT_SECTION)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House.Entertainment, 'C1-01-B - Entertainment'))
        self.assertEqual(self.m_entertainment_obj.Active, False)
        self.assertEqual(self.m_entertainment_obj.PluginCount, 0)
        self.assertEqual(self.m_entertainment_obj.Plugins, {})

    def test_03_XML(self):
        """ Test
        """
        l_ret = self.m_api.LoadConfig(self.m_pyhouse_obj)
        l_entertain = self.m_pyhouse_obj.House.Entertainment
        # print(PrettyFormatAny.form(l_entertain, 'C1-01-A - Entertainment'))
        # print(PrettyFormatAny.form(l_entertain.Plugins, 'C1-01-B- Plugins'))
        # print(PrettyFormatAny.form(l_entertain.Plugins['onkyo'], 'C1-01-C - Plugins["onkyo"]'))
        # print(PrettyFormatAny.form(l_entertain.Plugins['panasonic'], 'C1-01-D - Plugins["panasonic"]'))
        # print(PrettyFormatAny.form(l_entertain.Plugins['pandora'], 'C1-01-E - Plugins["pandora"]'))
        # print(PrettyFormatAny.form(l_entertain.Plugins['pioneer'], 'C1-01-F - Plugins["pioneer"]'))
        # print(PrettyFormatAny.form(l_entertain.Plugins['samsung'], 'C1-01-G - Plugins["samsung"]'))


class D1_Save(SetupMixin, unittest.TestCase):
    """ Test writing of the entertainment XML.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Setup(self):
        """
        """
        l_xml = self.m_xml.entertainment_sect
        # print(PrettyFormatAny.form(l_xml, 'C1-01-A - Entertainment XML'))
        self.assertEqual(l_xml.tag, TESTING_ENTERTAINMENT_SECTION)

    def test_02_XML(self):
        """ Test
        """
        l_ret = entertainmentApi(self.m_pyhouse_obj).LoadConfig(self.m_pyhouse_obj)
        l_xml = ET.Element('HouseDivision')
        l_xml1 = entertainmentApi(self.m_pyhouse_obj).SaveXml(l_xml)
        l_ent = self.m_pyhouse_obj.House.Entertainment = l_ret
        # print(PrettyFormatAny.form(l_ret, 'D1-02-A - Ret'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.House, 'D1-02-B - HouseInformation()'))
        # print(PrettyFormatAny.form(l_ent, 'D1-02-C - Entertainment'))
        # print(PrettyFormatAny.form(l_ent.Plugins, 'D1-02-D- Plugins'))
        # print(PrettyFormatAny.form(l_ent.Plugins['onkyo'], 'D1-02-Onkyo - Plugins["onkyo"]'))
        # print(PrettyFormatAny.form(l_ent.Plugins['panasonic'], 'D1-02-Panasonic - Plugins["panasonic"]'))
        # print(PrettyFormatAny.form(l_ent.Plugins['pandora'], 'D1-02-Pandora - Plugins["pandora"]'))
        # print(PrettyFormatAny.form(l_ent.Plugins['pioneer'], 'D1-02-Pioneer - Plugins["pioneer"]'))
        # print(PrettyFormatAny.form(l_ent.Plugins['samsung'], 'D1-02-Samsung - Plugins["pioneer"]'))
        # print(PrettyFormatAny.form(l_ent.Plugins['pandora'].Api, 'D1-02-H - Plugins["pandora"].Api'))

    def test_03_XML(self):
        """ Test
        """
        l_ret = entertainmentApi(self.m_pyhouse_obj).LoadConfig(self.m_pyhouse_obj)
        l_xml = ET.Element('HouseDivision')
        l_xml1 = entertainmentApi(self.m_pyhouse_obj).SaveXml(l_xml)
        l_ent = self.m_pyhouse_obj.House.Entertainment = l_ret
        # print(PrettyFormatAny.form(l_ent.Plugins, 'D1-03-A- Plugins'))
        # print(PrettyFormatAny.form(l_ent.Plugins['pandora'], 'D1-03-Pandora - Plugins["pandora"]'))
        # print(PrettyFormatAny.form(l_ent.Plugins['pandora']._Api, 'D1-02-H - Plugins["pandora"].Api'))

# ## END DBK
