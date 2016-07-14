"""
@name:      PyHouse/src/Modules/Security/security.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 29, 2015
@Summary:

"""

__updated__ = '2016-07-14'

# Import system type stuff

# Import PyMh files
from Modules.Housing.Security.pi_camera import API as cameraApi
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Security       ')


class API(object):
    """ Called from house.

    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_api = cameraApi(p_pyhouse_obj)
        LOG.info('Initialized')

    def LoadXml(self, p_pyhouse_obj):
        LOG.info('Loaded XML')

    def Start(self):
        self.m_api.Start()
        LOG.info("Started.")

    def SaveXml(self, p_xml):
        LOG.info("Saved XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
