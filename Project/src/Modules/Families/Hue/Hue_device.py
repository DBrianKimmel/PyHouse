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

__updated__ = '2019-02-27'

# Import system type stuff

# Import PyMh files
from Modules.Families.Hue.Hue_hub import HueHub
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Hue_device     ')


class API(object):
    """
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized')

    def LoadXml(self, p_pyhouse_obj):
        """ Reading the xml has already happened - handled by Bridges.
        Now we set up the rest client
        """
        LOG.info('Loading')
        HueHub(self.m_pyhouse_obj).Start(self.m_pyhouse_obj)

    def Start(self):
        """
        """
        # if self.m_pyhouse_obj.Computer != {}:
        # HueHub(self.m_pyhouse_obj).Start(self.m_pyhouse_obj)
        LOG.info('Started')
        pass

    def SaveXml(self, p_xml):
        """ Handled by Bridges
        """
        return p_xml

# ## END DBK
