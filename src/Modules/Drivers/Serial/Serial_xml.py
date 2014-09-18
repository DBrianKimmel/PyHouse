"""
-*- test-case-name: PyHouse.src.Modules.Drivers.Serial.test.test_Serial_xml -*-

@name: PyHouse/src/Modules/Drivers/Serial/serial_xml.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jul 29, 2014
@summary: Read and write USB xml

"""

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import SerialControllerData
from Modules.Utilities import xml_tools


class ReadWriteConfigXml(xml_tools.XmlConfigTools):
    """Read and write the interface information based in the interface type.
    """

    def read_interface_xml(self, p_controller_entry):
        l_serial = SerialControllerData()
        l_serial.BaudRate = self.get_int_from_xml(p_controller_entry, 'BaudRate', 19200)
        l_serial.ByteSize = self.get_int_from_xml(p_controller_entry, 'ByteSize', 8)
        l_serial.DsrDtr = self.get_bool_from_xml(p_controller_entry, 'DsrDtr', False)
        l_serial.Parity = self.get_text_from_xml(p_controller_entry, 'Parity', 'N')
        l_serial.RtsCts = self.get_bool_from_xml(p_controller_entry, 'RtsCts', False)
        l_serial.StopBits = self.get_float_from_xml(p_controller_entry, 'StopBits', 1.0)
        l_serial.Timeout = self.get_float_from_xml(p_controller_entry, 'Timeout', 1.0)
        l_serial.XonXoff = self.get_bool_from_xml(p_controller_entry, 'XonXoff', False)
        return l_serial

    def write_interface_xml(self, p_xml, p_controller_obj):
        self.put_int_element(p_xml, 'BaudRate', p_controller_obj.BaudRate)
        self.put_int_element(p_xml, 'ByteSize', p_controller_obj.ByteSize)
        self.put_bool_element(p_xml, 'DsrDtr', p_controller_obj.DsrDtr)
        self.put_text_element(p_xml, 'Parity', p_controller_obj.Parity)
        self.put_bool_element(p_xml, 'RtsCts', p_controller_obj.RtsCts)
        self.put_float_element(p_xml, 'StopBits', p_controller_obj.StopBits)
        self.put_float_element(p_xml, 'Timeout', p_controller_obj.Timeout)
        self.put_bool_element(p_xml, 'XonXoff', p_controller_obj.XonXoff)
        return p_xml

# ## END DBK
