"""
-*- test-case-name: PyHouse.src.Modules.Drivers.Null.test.test_Null_xml -*-

@name:      PyHouse/src/Modules/Drivers/Null/Null_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 23, 2014
@summary:

"""

__updated__ = '2017-01-20'


# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import NullControllerData
# from Modules.Core.Utilities.xml_tools import PutGetXML


class XML(object):
    """Read and write the interface information based in the interface type.
    """

    @staticmethod
    def read_interface_xml(p_controller_entry):
        l_obj = NullControllerData()
        return l_obj

    @staticmethod
    def write_interface_xml(p_xml, p_controller_obj):
        return p_xml

# ## END DBK
