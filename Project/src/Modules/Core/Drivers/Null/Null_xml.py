"""
@name:      Modules/Drivers/Null/Null_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 23, 2014
@summary:

"""

__updated__ = '2020-02-14'

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import NullControllerInformation


class XML(object):
    """Read and write the interface information based in the interface type.
    """

    @staticmethod
    def read_interface_xml(p_controller_entry):
        l_obj = NullControllerInformation()
        return l_obj

    @staticmethod
    def write_interface_xml(p_controller_obj):
        l_xml = ET.Element('Null')
        return l_xml

# ## END DBK
