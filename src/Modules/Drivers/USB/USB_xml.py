"""
-*- test-case-name: PyHouse.src.Modules.Drivers.USB.test.test_usb_xml -*-

@name: PyHouse/src/Modules/Drivers/USB/usb_xml.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jul 29, 2014
@summary: Read and write USB xml

"""

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import USBControllerData
from Modules.Utilities import xml_tools
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.UsbXml      ')


class ReadWriteConfigXml(xml_tools.XmlConfigTools):
    """Read and write the interface information based in the interface type.
    """

    def read_interface_xml(self, p_controller_xml):
        l_usb = USBControllerData()
        try:
            l_usb.Product = self.get_int_from_xml(p_controller_xml, 'Product')
            l_usb.Vendor = self.get_int_from_xml(p_controller_xml, 'Vendor')
        except Exception as e_err:
            LOG.error('Read Interface - {0:}'.format(e_err))
        return l_usb

    def write_interface_xml(self, p_xml, p_controller_obj):
        self.put_int_element(p_xml, 'Product', p_controller_obj.Product)
        self.put_int_element(p_xml, 'Vendor', p_controller_obj.Vendor)
        return p_xml

# ## END DBK
