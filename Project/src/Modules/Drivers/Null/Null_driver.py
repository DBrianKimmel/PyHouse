"""
Created on Aug 23, 2014

@author: briank
"""

# Import system type stuff

# Import PyHouse Modules
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.NullDriver     ')


class API(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info(" Initializing Null Driver.")

    def Start(self, p_pyhouse_obj, p_controller_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_controller_obj = p_controller_obj

    def Stop(self):
        pass

    def Read(self):
        l_ret = ''
        return l_ret

    def Write(self, p_message):
        pass

# ## END DBK
