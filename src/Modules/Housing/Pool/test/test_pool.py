"""
@name:      PyHouse/src/Modules/Housing/Pool/test/test_pool.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 27, 2015
@Summary:

Passed all 11 tests - DBK - 2017-01-12

"""
from Modules.Housing.test.xml_housing import TESTING_HOUSE_DIVISION

__updated__ = '2017-01-18'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG, TESTING_PYHOUSE
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import PoolData
from Modules.Housing.Pool.pool import Xml as poolXml
from Modules.Housing.Pool.test.xml_pool import \
        XML_POOL, \
        TESTING_POOL_NAME_0, \
        TESTING_POOL_KEY_0, \
        TESTING_POOL_ACTIVE_0, \
        TESTING_POOL_COMMENT_0, \
        TESTING_POOL_TYPE_0, \
        TESTING_POOL_NAME_1, \
        TESTING_POOL_KEY_1, \
        TESTING_POOL_ACTIVE_1, \
        TESTING_POOL_COMMENT_1, \
        TESTING_POOL_UUID_0, \
        TESTING_POOL_SECTION
# from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_pool_obj = PoolData()


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_pool')


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouse(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_pyhouse_obj.House.Pools, {})

    def test_02_FindXML(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, TESTING_PYHOUSE)
        self.assertEqual(self.m_xml.house_div.tag, TESTING_HOUSE_DIVISION)
        self.assertEqual(self.m_xml.pool_sect.tag, TESTING_POOL_SECTION)

    def test_03_XML(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml.pool_sect, 'Pool'))
        self.assertEqual(self.m_xml.pool.tag, 'Pool')

    def test_04_Pools(self):
        """ Be sure that the XML contains the Pool Info.
        """
        self.m_pyhouse_obj.House.Pools = poolXml.read_all_pools_xml(self.m_pyhouse_obj)
        l_pools = self.m_pyhouse_obj.House.Pools
        # print(PrettyFormatAny.form(l_pools, 'Pools'))
        self.assertEqual(len(l_pools), 2)


class A2_Xml(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring('<x />'))
        pass

    def test_01_Raw(self):
        l_raw = XML_POOL
        print(l_raw)
        self.assertEqual(l_raw[:13], '<PoolSection>')

    def test_02_Parsed(self):
        l_xml = ET.fromstring(XML_POOL)
        # print(l_xml)
        self.assertEqual(l_xml.tag, TESTING_POOL_SECTION)


class B1_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        # self.m_pyhouse_obj.House.Pools = poolXml.read_all_pools_xml(self.m_pyhouse_obj)

    def test_01_Base(self):
        """ Read the base Pool Info
        """
        l_pool = poolXml._read_base(self.m_xml.pool)
        # print(PrettyFormatAny.form(l_pool, 'B1-01-A - Pool'))
        self.assertEqual(l_pool.Name, TESTING_POOL_NAME_0)
        self.assertEqual(l_pool.Key, int(TESTING_POOL_KEY_0))
        self.assertEqual(str(l_pool.Active), TESTING_POOL_ACTIVE_0)
        self.assertEqual(l_pool.UUID, TESTING_POOL_UUID_0)
        l_pool = poolXml._read_base(self.m_xml.pool_sect[1])
        # print(PrettyFormatAny.form(l_pool, B1-01-B - 'Pool'))
        self.assertEqual(l_pool.Name, TESTING_POOL_NAME_1)
        self.assertEqual(l_pool.Key, int(TESTING_POOL_KEY_1))
        self.assertEqual(l_pool.Active, bool(TESTING_POOL_ACTIVE_1))

    def test_02_OnePool(self):
        """ Read one entire pool
        """
        l_pool = poolXml._read_one_pool(self.m_xml.pool)
        # print(PrettyFormatAny.form(l_pool, 'B1-02-A - Pool'))
        self.assertEqual(l_pool.Name, TESTING_POOL_NAME_0)
        self.assertEqual(l_pool.Key, int(TESTING_POOL_KEY_0))
        self.assertEqual(l_pool.Active, bool(TESTING_POOL_ACTIVE_0))
        self.assertEqual(l_pool.Comment, TESTING_POOL_COMMENT_0)
        self.assertEqual(l_pool.PoolType, TESTING_POOL_TYPE_0)

    def test_03_AllPools(self):
        """ Read all pool info
        """
        l_obj = poolXml.read_all_pools_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_obj, 'B1-03-A - Pool'))
        self.assertEqual(len(l_obj), 2)


class B2_Write(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_pools = poolXml.read_all_pools_xml(self.m_pyhouse_obj)

    def test_01_Base(self):
        """ Write pool base info
        """
        # print(PrettyFormatAny.form(self.m_pools[0], 'Pools'))
        l_xml = poolXml._write_base(self.m_pools[0])
        # print(PrettyFormatAny.form(l_xml, 'Pool'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_POOL_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_POOL_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_POOL_ACTIVE_0)

    def test_02_OnePool(self):
        """ Write one entire pool XML
        """
        l_xml = poolXml._write_one_pool(self.m_pools[0])
        # print(PrettyFormatAny.form(l_xml, 'Pool'))
        self.assertEqual(l_xml.attrib['Name'], TESTING_POOL_NAME_0)
        self.assertEqual(l_xml.attrib['Key'], TESTING_POOL_KEY_0)
        self.assertEqual(l_xml.attrib['Active'], TESTING_POOL_ACTIVE_0)
        self.assertEqual(l_xml.find('Comment').text, TESTING_POOL_COMMENT_0)

    def test_03_AllPools(self):
        """ Write Pool Section with all pools.
        """
        l_xml = poolXml.write_all_pools_xml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_xml, 'Pool'))
        # l_xml1 = l_xml.find('Pool')
        l_xml2 = l_xml[1]
        self.assertEqual(l_xml2.attrib['Name'], TESTING_POOL_NAME_1)
        self.assertEqual(l_xml2.attrib['Key'], TESTING_POOL_KEY_1)
        self.assertEqual(l_xml2.attrib['Active'], TESTING_POOL_ACTIVE_1)
        self.assertEqual(l_xml2.find('Comment').text, TESTING_POOL_COMMENT_1)

# ## END DBK
