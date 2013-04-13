'''
Created on Apr 10, 2013

@author: briank
'''

import xml.etree.ElementTree as ET
from twisted.trial import unittest

from drivers import interface
from housing.house import HouseData
from lights.lighting_controllers import ControllerData


XML = """
<House Name='abc' Key='0' Active='True'>
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
    </Controllers>
</House>
"""

class Test(unittest.TestCase):

    def _get_xml(self):
        l_xml = ET.fromstring(XML)
        return l_xml

    def _get_attrs(self, p_obj):
        l_attrs = filter(lambda aname: not aname.startswith('__'), dir(p_obj))
        return l_attrs

    def _create_interface(self):
        int_obj = interface.SerialData()
        int_obj.BaudRate = 1234
        int_obj.ByteSize = 11
        int_obj.DsrDtr = False
        int_obj.InterCharTimeout = 0.24
        int_obj.Parity = 'N'
        int_obj.RtsCts = False
        int_obj.StopBits = 1.0
        int_obj.Timeout = None
        int_obj.WriteTimeout = None
        int_obj.XonXoff = False
        return int_obj

    def _create_controller(self, p_name, p_key):
        ctl_obj = ControllerData()
        ctl_obj.Name = p_name
        ctl_obj.Active = True
        ctl_obj.Key = p_key
        ctl_obj.Interface = 'Serial'
        l_obj = self._create_interface()
        l_attrs = self._get_attrs(l_obj)
        for l_attr in l_attrs:
            setattr(ctl_obj, l_attr, getattr(l_obj, l_attr))
        return ctl_obj

    def _create_house(self, p_name = 'Test House'):
        house_obj = HouseData()
        house_obj.Name = p_name
        house_obj.Active = True
        house_obj.Controllers = {}
        house_obj.Controllers[0] = self._create_controller('Ser 1', 0)
        return house_obj

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_001_create_house(self):
        house_obj = self._create_house()
        self.assertEqual(house_obj.Name, 'Test House')

    def test_002_read_xml(self):
        house_obj = self._create_house()
        interface.ReadWriteConfig().extract_serial_xml(house_obj, self._get_xml())
        self.assertEqual(house_obj.Controllers[0].BaudRate, 9600)

### END
