"""
-*- test-case-name: PyHouse.src.Modules.Drivers.Erhernet.test.test_ethernet_xml -*-

@name:      PyHouse/src/Modules/Drivers/Ethernet/ethernet_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 29, 2014
@summary:   Read and write USB xml

"""

__updated__ = '2019-01-10'

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import EthernetControllerData
from Modules.Core.Utilities.xml_tools import PutGetXML


class XML(object):
    """Read and write the interface information based in the interface type.
    """

    @staticmethod
    def read_interface_xml(p_controller_xml):
        l_ethernet = EthernetControllerData()
        l_ethernet.PortNumber = PutGetXML.get_int_from_xml(p_controller_xml, 'PortNumber')
        l_ethernet.Protocol = PutGetXML.get_text_from_xml(p_controller_xml, 'Protocol')
        return l_ethernet

    @staticmethod
    def write_interface_xml(p_controller_obj):
        l_xml = ET.Element('Ethernet')
        try:
            PutGetXML.put_int_element(l_xml, 'PortNumber', p_controller_obj.PortNumber)
            PutGetXML.put_text_element(l_xml, 'Protocol', p_controller_obj.Protocol)
        except Exception:
            pass
        return l_xml

# ## END DBK
