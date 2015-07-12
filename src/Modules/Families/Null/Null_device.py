"""
-*- test-case-name: PyHouse.src.Modules.families.Null.test.test_Null_device -*-

@name:      PyHouse/src/Modules/families/Null/Null_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 6, 2014
@summary:   Used when no valid family exists

"""

# Import system type stuff

# Import PyMh files
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Null_device ')


class API(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self):
        pass

    def SaveXml(self, p_xml):
        return p_xml

# ## END DBK
