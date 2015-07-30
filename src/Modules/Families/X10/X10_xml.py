"""
-*- test-case-name: PyHouse.src.Modules.Families.X10.test.test_X10_xml -*-

@name:      PyHouse/src/Modules/Families/X10/X10_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@note:      Created on Aug 6, 2014
@license:   MIT License
@summary:   This module is for Insteon/X10

"""

# Import system type stuff

# Import PyMh files
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.X10_xml      ')


class Xml(object):

    @staticmethod
    def ReadXml(p_device_obj, p_in_xml):
        pass

    @staticmethod
    def WriteXml(p_out_xml, p_device_obj):
        return p_out_xml

# ## END DBK
