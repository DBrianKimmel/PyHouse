"""
-*- test-case-name: Pyhouse.src.Modules.Communication.test.test-communication -*-

@name:      Pyhouse/Project/src/Modules/Communication/communication.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Jan 9, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2019-07-04'

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Communication  ')


class Utility(object):

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


class API(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def LoadXml(self, p_pyhouse_obj):
        """
        """
        LOG.info('Loaded XML.')

    def Start(self):
        pass

    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        l_xml = ET.Element('CommunicationSection')
        p_xml.append(l_xml)
        LOG.info("Saved Communication XML.")
        return p_xml

# ## END DBK
