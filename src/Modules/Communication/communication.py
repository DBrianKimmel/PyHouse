"""
@name:      PyHouse/src/Modules/Communication/communication.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 28, 2015
@Summary:

"""


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
            l_xml = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision').find('CommunicationSection')
        except AttributeError as e_err:
            LOG.error('ERROR in read_xml() - {}'.format(e_err))
        return l_dict


class API(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self):
        self.m_pyhouse_obj.Computer.Communication = Utility().read_xml(self.m_pyhouse_obj)

    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        l_xml = ET.Element('CommunicationSection')
        p_xml.append(l_xml)
        LOG.info("Saved XML.")
        return p_xml

# ## END DBK
