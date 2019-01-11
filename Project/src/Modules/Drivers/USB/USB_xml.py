"""
-*- test-case-name: PyHouse.src.Modules.Drivers.USB.test.test_usb_xml -*-

@name:      PyHouse/src/Modules/Drivers/USB/usb_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 29, 2014
@summary:   Read and write USB xml

"""

__updated__ = '2019-01-10'

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import USBControllerData
from Modules.Core.Utilities.xml_tools import PutGetXML
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.UsbXml      ')


class XML(object):
    """Read and write the interface information based in the interface type.
    """

    @staticmethod
    def read_interface_xml(p_controller_xml):
        l_xml = p_controller_xml.find('USB')
        l_usb = USBControllerData()
        try:
            l_usb.Product = PutGetXML.get_int_from_xml(l_xml, 'Product')
            l_usb.Vendor = PutGetXML.get_int_from_xml(l_xml, 'Vendor')
        except Exception as e_err:
            LOG.error('Read Interface - {}'.format(e_err))
        return l_usb

    @staticmethod
    def write_interface_xml(p_controller_obj):
        l_xml = ET.Element('USB')
        try:
            PutGetXML.put_int_element(l_xml, 'Product', p_controller_obj.Product)
            PutGetXML.put_int_element(l_xml, 'Vendor', p_controller_obj.Vendor)
        except Exception:
            pass
        return l_xml

# ## END DBK
