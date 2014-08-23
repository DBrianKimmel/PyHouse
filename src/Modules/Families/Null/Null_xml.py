"""
-*- test-case-name: PyHouse.src.Modules.families.Null.test.test_Null_xml -*-

@name: PyHouse/src/Modules/families/Null/Null_xml.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Aug 9, 2014
@summary: This module is for communicating with invalid controllers.

"""

# Import system type stuff

# Import PyMh files
from Modules.Families.Null.Null_data import NullData
from Modules.Utilities.xml_tools import stuff_new_attrs
from Modules.Computer import logging_pyh as Logger

g_debug = 9
LOG = Logger.getLogger('PyHouse.Null_xml    ')


def ReadXml(p_device_obj, _p_entry_xml):
    """
    @param p_entry_xml: is the e-tree XML house object
    @param p_house: is the text name of the House.
    @return: a dict of the entry to be attached to a house object.
    """
    l_obj = NullData()
    stuff_new_attrs(p_device_obj, l_obj)
    return p_device_obj

def WriteXml(p_entry_xml, p_device_obj):
    pass

# ## END DBK
