"""
-*- test-case-name: PyHouse.src.Modules.communications.test.test_send_email -*-

@name: PyHouse/src/Modules/communication/send_email.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 3, 2014
@summary: Allow PyHouse to send email.

Fake out gmail.com and look like sendmail is connected.

This uses gmail.
If you don't have an account - get one or write another module to handle your mail.


"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import EmailData
from Modules.utils import pyh_log
from Modules.utils.xml_tools import PutGetXML

g_debug = 1
LOG = pyh_log.getLogger('PyHouse.IrControl   ')


class ReadWriteConfigXml(PutGetXML):
    """
    """
    m_count = 0

    def read_email_data(self, p_pyhouse_obj):
        """
        @return: a ThermostatData object.
        """
        l_div_xml = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
        l_xml = l_div_xml.find('EmailSection')
        l_obj = EmailData
        l_obj.EmailFromAddress = self.get_text_from_xml(l_xml, 'EmailFromAddress')
        l_obj.EmailToAddress = self.get_text_from_xml(l_xml, 'EmailToAddress')
        l_obj.GmailLogin = self.get_text_from_xml(l_xml, 'GmailLogin')
        l_obj.GmailPassword = self.get_text_from_xml(l_xml, 'GmailPassword')
        return l_obj

    def write_email_xml(self, p_obj, p_xml):
        l_xml = ET.Element('EmailSection')
        self.put_text_element(p_xml, 'EmailFromAddress', p_obj.EmailFromAddress)
        pass



class Utility(object):
    """
    """
    def setup_xml(self, p_pyhouse_obj):
        l_xml = p_pyhouse_obj.Xml.XmlRoot
        try:
            l_xml = l_xml.find('ComputerDivision')
            l_xml = l_xml.find('EmailSection')
        except AttributeError as e_err:
            LOG.error('SetupXML ERROR {0:}'.format(e_err))
        return l_xml


class API(object):
    """
    """

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def Stop(self):
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        l_xml = self.write_email_xml(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Saved XML.")
        return p_xml

    def SendEmail(self, p_to_address, p_message):
        pass

# ## END DBK
