"""
-*- test-case-name: PyHouse.src.Modules.families.Null.test.test_Null_xml -*-

@name:      PyHouse/src/Modules/families/Null/Null_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 9, 2014
@summary:   This module is for communicating with invalid controllers.

"""

# Import system type stuff

# Import PyMh files
from Modules.Families.Null.Null_data import NullData
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Null_xml    ')

class API(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def ReadXml(self, p_device_obj, _p_entry_xml):
        return p_device_obj

    def WriteXml(self, p_entry_xml, p_device_obj):
        pass

# ## END DBK
