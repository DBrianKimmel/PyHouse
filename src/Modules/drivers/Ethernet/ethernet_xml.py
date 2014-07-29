"""
-*- test-case-name: PyHouse.src.Modules.drivers.Erhernet.test.test_ethernet_xml -*-

@name: PyHouse/src/Modules/drivers/Ethernet/ethernet_xml.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jul 29, 2014
@summary: Read and write USB xml

"""

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import EthernetControllerData
from Modules.utils import xml_tools


class ReadWriteConfigXml(xml_tools.XmlConfigTools):
    """Read and write the interface information based in the interface type.
    """

    def read_interface_xml(self, p_controller_xml):
        l_ethernet = EthernetControllerData()
        l_ethernet.PortNumber = self.get_int_from_xml(p_controller_xml, 'PortNumber')
        l_ethernet.Protocol = self.get_text_from_xml(p_controller_xml, 'Protocol')
        return l_ethernet

    def write_interface_xml(self, p_xml, p_controller_obj):
        self.put_int_element(p_xml, 'PortNumber', p_controller_obj.PortNumber)
        self.put_text_element(p_xml, 'Protocol', p_controller_obj.Protocol)
        return p_xml

# ## END DBK
