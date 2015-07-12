"""
@name:      PyHouse/src/Modules/Security/security.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 29, 2015
@Summary:

"""


# Import system type stuff

# Import PyMh files
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Security       ')


class API(object):

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self):
        LOG.info("Started.")

    def Stop(self):
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        LOG.info("Saved XML.")
        return p_xml


# ## END DBK
