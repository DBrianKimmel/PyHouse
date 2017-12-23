"""
-*- test-case-name: /home/briank/workspace/PyHouse/src/Modules/Families/Hue/Hue_device.py -*-

@name:      /home/briank/workspace/PyHouse/src/Modules/Families/Hue/Hue_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2017 by D. Brian Kimmel
@note:      Created on Dec 18, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2017-12-20'

# Import system type stuff

# Import PyMh files
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Hue_device ')


class API(object):
    """
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def LoadXml(self, p_pyhouse_obj):
        """ Load the Schedule xml info.
        """

    def Start(self):
        pass

    def SaveXml(self, p_xml):
        return p_xml

# ## END DBK
