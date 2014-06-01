'''
Created on Apr 10, 2013

@author: briank
'''

import xml.etree.ElementTree as ET
from twisted.trial import unittest

from Modules.drivers import interface
from Modules.utils import xml_tools
from src.test import xml_data

XML = xml_data.XML_LONG

class Test_01_XML(unittest.TestCase):

    def setUp(self):
        self.m_root_element = ET.fromstring(XML)
        self.m_util = xml_tools.PutGetXML()
        self.m_intf = interface.ReadWriteConfig()

    def tearDown(self):
        pass

    def test_0101_read_xml(self):
        l_pyhouse = self.m_root_element
        self.assertEqual(l_pyhouse.tag, 'PyHouse')

    def test_0102_find_node(self):
        l_node = self.m_root_element.find('Node')
        print('Node {0:}'.format(l_node))
        self.assertEqual(l_node.tag, 'Node')

    def test_002_xml_find_controllers(self):
        l_controllers = self.m_root_element.find('Controllers')
        l_list = l_controllers.findall('Controller')
        for l_controller in l_list:
            print("Controller {0:}".format(l_controller.get('Name')))

    def test_0103_xml_find_serial_1(self):
        l_controllers = self.m_root_element.find('Controllers')
        l_first = l_controllers.find('Controller')
        self.assertEqual(l_first.get('Name'), 'Serial_1')
        l_interf = l_first.find('Interface')
        self.assertEqual(l_interf.text, 'Serial')
        l_baud = l_first.find('BaudRate')
        self.assertEqual(l_baud.text, '19200')

    def test_004_extract_serial(self):
        l_controllers = self.m_root_element.find('Controllers')
        l_first = l_controllers.find('Controller')
        pass

# ## END
