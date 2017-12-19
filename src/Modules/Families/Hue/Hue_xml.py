"""
-*- test-case-name: /home/briank/workspace/PyHouse/src/Modules/Families/Hue/Hue_xml.py -*-

@name:      /home/briank/workspace/PyHouse/src/Modules/Families/Hue/Hue_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2017 by D. Brian Kimmel
@note:      Created on Dec 18, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2017-12-18'

# Import system type stuff

# Import PyMh files
# from Modules.Families.Null.Null_data import NullData
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Hue_xml    ')


class Xml(object):

    @staticmethod
    def ReadXml(p_device_obj, _p_entry_xml):
        return p_device_obj

    @staticmethod
    def WriteXml(p_entry_xml, p_device_obj):
        pass

# ## END DBK
