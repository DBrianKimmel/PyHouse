"""
@name:      PyHouse/src/Modules/Utilities/test/test_uuid_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 22, 2015
@Summary:

Passed all 7 tests - DBK - 2016-11-16

"""
from Modules.Computer.test.xml_computer import TESTING_COMPUTER_DIV_START
from Modules.Computer.Nodes.test.xml_nodes import TESTING_NODE_SECTION_START

__updated__ = '2017-01-11'

#  Import system type stuff
from twisted.trial import unittest
import xml.etree.ElementTree as ET

#  Import PyMh files
from Modules.Core.data_objects import UuidData
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Utilities.uuid_tools import Uuid, FileUuid
from test.testing_mixin import SetupPyHouseObj
from test.xml_data import XML_LONG


#  Import PyMh files and modules.
class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_uuid_tools')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the test
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_PyHouseObj(self):
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Xml, 'A1-01-A - PyHouse.Xml'))
        self.assertNotEqual(self.m_pyhouse_obj.Xml, None)

    def test_02_Tags(self):
        # print(PrettyFormatAny.form(self.m_xml, 'A1-02-A - Tags'))
        self.assertEqual(self.m_xml.root.tag, 'PyHouse')
        self.assertEqual(self.m_xml.computer_div.tag, TESTING_COMPUTER_DIV_START)
        self.assertEqual(self.m_xml.node_sect.tag, TESTING_NODE_SECTION_START)


class A2_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Nodes(self):
        """ Be sure that the XML contains the right stuff.
        """
        print(PrettyFormatAny.form(self.m_xml.node_sect, 'A2-01-A - Light'))
        pass

    def test_02_Uuids(self):
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Uuids, 'UUIDS'))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Uuids.All, 'All'))


class B1_UUID(SetupMixin, unittest.TestCase):
    """
    This series tests the complex PutGetXML class methods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_None(self):
        l_test = None
        l_uuid = Uuid.make_valid(l_test)
        #  print('UUID = {}'.format(l_uuid))
        self.assertNotEqual(l_uuid, l_test)

    def test_02_Invalid(self):
        l_test = '123456'
        l_uuid = Uuid.make_valid(l_test)
        #  print('UUID = {}'.format(l_uuid))
        self.assertNotEqual(l_uuid, l_test)

    def test_03_Valid(self):
        l_test = '12345678-dead-beef-dead-fedcba987654'
        l_uuid = Uuid.make_valid(l_test)
        #  print('UUID = {}'.format(l_uuid))
        self.assertEqual(l_uuid, l_test)

    def test_04_Add(self):
        l_obj_0 = UuidData()
        l_obj_0.UUID = '12345678-dead-beef-dead-fedcba987654'
        l_obj_0.UuidType = 'House'
        Uuid.add_uuid(self.m_pyhouse_obj, l_obj_0)
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Uuids, 'B1-4-A - one'))
        self.assertEqual(self.m_pyhouse_obj.Uuids.All[l_obj_0.UUID].UuidType, l_obj_0.UuidType)
        #
        l_obj_1 = UuidData()
        l_obj_1.UUID = '01234567-dead-beef-dead-fedcba987654'
        l_obj_1.UuidType = 'Room'
        Uuid.add_uuid(self.m_pyhouse_obj, l_obj_1)
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Uuids.All, 'B1-4-B - two'))
        self.assertEqual(self.m_pyhouse_obj.Uuids.All[l_obj_1.UUID].UuidType, l_obj_1.UuidType)


class B2_File(SetupMixin, unittest.TestCase):
    """This tests reading and writing of uuid files in the /etc/pyhouse directory
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))

    def test_01_Read(self):
        FileUuid().XXXread_file('Computer')

    def test_02_Write(self):
        # FileUuid().XXXwrite_file('Computer')
        pass

#  ## END DBK
