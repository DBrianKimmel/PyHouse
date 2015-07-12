"""
-*- test-case-name: PyHouse.src.Modules.Drivers.Erhernet.test.test_ethernet_xml -*-

@name:      PyHouse/src/Modules/Drivers/Ethernet/ethernet_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 29, 2014
@summary:   Read and write USB xml

"""

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import EthernetControllerData
from Modules.Utilities.xml_tools import PutGetXML


class Xml(object):
    """Read and write the interface information based in the interface type.
    """

    @staticmethod
    def read_interface_xml(p_controller_xml):
        l_ethernet = EthernetControllerData()
        l_ethernet.PortNumber = PutGetXML.get_int_from_xml(p_controller_xml, 'PortNumber')
        l_ethernet.Protocol = PutGetXML.get_text_from_xml(p_controller_xml, 'Protocol')
        return l_ethernet

    @staticmethod
    def write_interface_xml(p_xml, p_controller_obj):
        PutGetXML.put_int_element(p_xml, 'PortNumber', p_controller_obj.PortNumber)
        PutGetXML.put_text_element(p_xml, 'Protocol', p_controller_obj.Protocol)
        return p_xml

# ## END DBK
