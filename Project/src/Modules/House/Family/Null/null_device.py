"""
@name:      Modules/families/Null/Null_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 6, 2014
@summary:   Used when no valid family exists

"""

__updated__ = '2019-12-30'

# Import system type stuff

# Import PyMh files
from Modules.Core import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Null_device ')


class Api(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self):
        pass

    def SaveXml(self, p_xml):
        return p_xml

# ## END DBK
