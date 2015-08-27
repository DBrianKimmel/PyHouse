"""
-*- test-case-name: PyHouse.src.Modules.Drivers.USB.test.test_usb_xml -*-

@name:      PyHouse/src/Modules/Drivers/USB/usb_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 29, 2014
@summary:   Read and write USB xml

"""

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import USBControllerData
from Modules.Utilities.xml_tools import PutGetXML
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.UsbXml      ')


class XML(object):
    """Read and write the interface information based in the interface type.
    """

    @staticmethod
    def read_interface_xml(p_controller_xml):
        l_usb = USBControllerData()
        try:
            l_usb.Product = PutGetXML.get_int_from_xml(p_controller_xml, 'Product')
            l_usb.Vendor = PutGetXML.get_int_from_xml(p_controller_xml, 'Vendor')
        except Exception as e_err:
            LOG.error('Read Interface - {0:}'.format(e_err))
        return l_usb

    @staticmethod
    def write_interface_xml(p_xml, p_controller_obj):
        try:
            PutGetXML.put_int_element(p_xml, 'Product', p_controller_obj.Product)
            PutGetXML.put_int_element(p_xml, 'Vendor', p_controller_obj.Vendor)
        except Exception:
            pass
        return p_xml

# ## END DBK
