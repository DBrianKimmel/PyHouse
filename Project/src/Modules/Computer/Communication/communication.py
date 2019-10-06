"""
@name:      Modules/Communication/communication.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Jan 9, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2019-10-06'

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Communication  ')


class lightingUtility(object):

    def read_xml(self, p_pyhouse_obj):
        """Read all the information.
        """
        self.m_count = 0
        l_dict = {}
        try:
            _l_xml = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision').find('CommunicationSection')
        except AttributeError as e_err:
            LOG.error('ERROR in read_xml() - {}'.format(e_err))
        return l_dict


class Api(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def LoadConfig(self):
        """
        """
        LOG.info('Loaded Communication Config.')

    def Start(self):
        pass

    def Stop(self):
        pass

    def SaveConfig(self):
        LOG.info("Saved Communication Config.")

# ## END DBK
