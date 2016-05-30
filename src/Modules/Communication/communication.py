"""
@name:      PyHouse/src/Modules/Communication/communication.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 28, 2015
@Summary:

"""

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Communication.bluetooth import API as bluetoothAPI
from Modules.Communication.send_email import API as emailAPI
from Modules.Communication.phone import API as phoneAPI
from Modules.Communication.twitter import API as twitterAPI
from Modules.Computer import logging_pyh as Logger
from Modules.Core.data_objects import CommunicationAPIs, CommunicationData

LOG = Logger.getLogger('PyHouse.Communication  ')


class Utility(object):

    def read_xml(self, p_pyhouse_obj):
        """Read all the information.
        """
        self.m_count = 0
        l_dict = {}
        try:
            l_xml = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
            if l_xml is None:
                return l_dict
            l_xml = l_xml.find('CommunicationSection')
            if l_xml is None:
                return l_dict
        except AttributeError as e_err:
            LOG.error('ERROR in read_xml() - {}'.format(e_err))
        return l_dict


class API(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.APIs.Computer.Communication = CommunicationAPIs()
        p_pyhouse_obj.APIs.Computer.Communication.BluetoothAPI = bluetoothAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.Communication.EmailAPI = emailAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.Communication.PhoneAPI = phoneAPI(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.Communication.TwitterAPI = twitterAPI(p_pyhouse_obj)

    def LoadXml(self, p_pyhouse_obj):
        p_pyhouse_obj.Computer.Communication = Utility().read_xml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.Communication.EmailAPI.LoadXml(p_pyhouse_obj)
        p_pyhouse_obj.APIs.Computer.Communication.TwitterAPI.LoadXml(p_pyhouse_obj)

    def Start(self):
        self.m_pyhouse_obj.APIs.Computer.Communication.EmailAPI.Start()
        self.m_pyhouse_obj.APIs.Computer.Communication.TwitterAPI.Start()
        pass

    def SaveXml(self, p_xml):
        l_xml = ET.Element('CommunicationSection')
        p_xml.append(l_xml)
        self.m_pyhouse_obj.APIs.Computer.Communication.EmailAPI.SaveXml(p_xml)
        self.m_pyhouse_obj.APIs.Computer.Communication.TwitterAPI.SaveXml(p_xml)
        LOG.info("Saved XML.")
        return p_xml

    def Stop(self):
        self.m_pyhouse_obj.APIs.Computer.Communication.EmailAPI.Stop()
        pass

#  ## END DBK
