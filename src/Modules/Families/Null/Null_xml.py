"""
-*- test-case-name: PyHouse.src.Modules.families.Null.test.test_Null_xml -*-

@name:      PyHouse/src/Modules/families/Null/Null_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 9, 2014
@summary:   This module is for communicating with invalid controllers.

"""

# Import system type stuff

# Import PyMh files
# from Modules.Families.Null.Null_data import NullData
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Null_xml    ')


class Xml(object):

    @staticmethod
    def ReadXml(p_device_obj, _p_entry_xml):
        return p_device_obj

    @staticmethod
    def WriteXml(p_entry_xml, p_device_obj):
        pass

# ## END DBK
