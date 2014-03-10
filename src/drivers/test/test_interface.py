'''
Created on Apr 10, 2013

@author: briank
'''

import xml.etree.ElementTree as ET
from twisted.trial import unittest

from drivers import interface
from src.lights import lighting_controllers
from src.utils import xml_tools


XML = """
<House Name='House_1' Key='0' Active='True'>
    <Controllers>
        <Controller Name='Serial_1' Key='0' Active='True'>
            <Interface>Serial</Interface>
            <BaudRate>19200</BaudRate>
            <ByteSize>8</ByteSize>
            <DsrDtr>False</DsrDtr>
            <Parity>N</Parity>
            <RtsCts>False</RtsCts>
            <StopBits>1.0</StopBits>
            <Timeout>0</Timeout>
            <XonXoff>False</XonXoff>
        </Controller>
        <Controller Name='USB_1' Key='1' Active='True'>
            <Interface>USB</Interface>
            <Vendor>12345</Vendor>
            <Product>9876</Product>
        </Controller>
    </Controllers>
</House>
"""

class Test(unittest.TestCase):

    def setUp(self):
        self.m_root_element = ET.fromstring(XML)
        self.m_util = xml_tools.PutGetXML()
        self.m_intf = interface.ReadWriteConfig()

    def tearDown(self):
        pass

    def test_001_xml_find_house(self):
        l_name = self.m_root_element.get('Name')
        self.assertEqual(l_name, 'House_1')

    def test_002_xml_find_controllers(self):
        l_controllers = self.m_root_element.find('Controllers')
        l_list = l_controllers.findall('Controller')
        for l_controller in l_list:
            print("Controller {0:}".format(l_controller.get('Name')))

    def test_003_xml_find_serial_1(self):
        l_controllers = self.m_root_element.find('Controllers')
        l_first = l_controllers.find('Controller')
        self.assertEqual(l_first.get('Name'), 'Serial_1')
        l_interf = l_first.find('Interface')
        self.assertEqual(l_interf.text, 'Serial')
        l_baud = l_first.find('BaudRate')
        self.assertEqual(l_baud.text, '19200')

    def test_004_extracr_serial(self):
        l_controllers = self.m_root_element.find('Controllers')
        l_first = l_controllers.find('Controller')
        pass

# ## END
