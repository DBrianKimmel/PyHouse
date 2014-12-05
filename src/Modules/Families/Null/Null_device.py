"""
-*- test-case-name: PyHouse.src.Modules.families.Null.test.test_Null_device -*-

@name: PyHouse/src/Modules/families/Null/Null_device.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Aug 6, 2014
@summary: Used when no valid family exists

"""

# Import system type stuff

# Import PyMh files
from Modules.Computer import logging_pyh as Logger

g_debug = 1
LOG = Logger.getLogger('PyHouse.Null_device ')


class API(object):
    """
    """

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def ReadXml(self, p_obj, p_xml):
        pass

    def SaveXml(self, p_xml):
        pass

    def WriteXml(self, p_out_xml, p_device):
        pass

# ## END DBK
