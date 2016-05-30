"""
-*- test-case-name: PyHouse.src.Modules.Communications.test.test_twitter -*-

@name:      PyHouse/src/Modules/Communication/twitter.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 27, 2016
@summary:   Allow PyHouse to send tweets.


"""

#  Import system type stuff


#  Import PyMh files
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Twitter        ')


class API(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def LoadXml(self, p_pyhouse_obj):
        # p_pyhouse_obj.Computer.Communication = Utility().read_xml(p_pyhouse_obj)
        pass

    def Start(self):
        pass

    def SaveXml(self, p_xml):
        LOG.info("Saved XML.")
        return p_xml

    def Stop(self):
        pass

# ## END DBK
