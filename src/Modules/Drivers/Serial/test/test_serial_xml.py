"""
@name: PyHouse/src/Modules/drivers/Serial/test/test_serial_xml.py
@author: briank
@contact: <d.briankimmel@gmail.com>
@Copyright: (c)  2014 by briank
@license: MIT License
@note: Created on Aug 5, 2014
@Summary:

Passed 3 XML tests - DBK - 2014-08-05
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData
from Modules.drivers.Serial import serial_xml
from Modules.lights import lighting_controllers
from Modules.families import family
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.utils.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by lighting_controllers.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_pyhouse_obj.House.OBJs.FamilyData = family.API().build_lighting_family_info()
        self.m_api = serial_xml.ReadWriteConfigXml()
        self.m_controller_obj = ControllerData()

    def test_0202_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        PrettyPrintAny(self.m_pyhouse_obj, 'PyHouseData')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.controller_sect.tag, 'ControllerSection', 'XML - No Controllers section')
        self.assertEqual(self.m_xml.controller.tag, 'Controller', 'XML - No Controller section')

    def test_0221_ReadSerialXml(self):
        l_interface = self.m_api.read_interface_xml(self.m_xml.controller)
        self.assertEqual(l_interface.BaudRate, 19200, 'Bad Baud Rate')
        self.assertEqual(l_interface.ByteSize, 8, 'Bad ByteSize')
        self.assertEqual(l_interface.DsrDtr, False, 'Bad DsrDtr')
        self.assertEqual(l_interface.Parity, 'N', 'Bad Parity')
        self.assertEqual(l_interface.RtsCts, False, 'Bad RtsCts')
        self.assertEqual(l_interface.StopBits, 1.0, 'Bad StopBits')
        self.assertEqual(l_interface.Timeout, 1.0, 'Bad Timeout')
        self.assertEqual(l_interface.XonXoff, False, 'Bad XonXoff')
        PrettyPrintAny(l_interface, 'Read Interface', 100)

    def test_0241_WriteSerialXml(self):
        l_obj = lighting_controllers.ControllersAPI(self.m_pyhouse_obj).read_one_controller_xml(self.m_xml.controller)
        PrettyPrintAny(l_obj, 'Controller', 120)
        l_ret = self.m_api.write_interface_xml(self.m_xml.controller, l_obj)
        PrettyPrintAny(l_ret, 'Interface Xml', 120)

# ## END
