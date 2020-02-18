"""
@name:      PyHouse/src/Modules/House/Pool/pool.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 29, 2015
@Summary:

"""

__updated__ = '2020-02-14'

# Import system type stuff

# Import PyMh files

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Pool           ')


class Api(object):

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def LoadConfig(self):
        l_dict = {}
        # self.m_pyhouse_obj.House.Pools = l_dict
        return l_dict

    def Start(self):
        # self.LoadXml(self.m_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        LOG.info("Stopped.")

    def SaveConfig(self):
        pass

# ## END DBK
