"""
-*- test-case-name: PyHouse.src.Modules.Communications.test.test_send_email -*-

@name:      PyHouse/src/Modules/Communication/send_email.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2014
@summary:   Allow PyHouse to send email.

Fake out gmail.com and look like sendmail is connected.

This uses gmail as a mail relay agent
If you don't have an account - get one or write another module to handle your mail.

"""

__updated__ = '2016-09-23'

#  Import system type stuff
import email.mime.application
import xml.etree.ElementTree as ET
from twisted.internet.defer import Deferred
try:
    from cStringIO import cStringIO as StringIO
except ImportError:
    from StringIO import StringIO

#  Import PyMh files
from Modules.Core.data_objects import EmailData
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.xml_tools import PutGetXML

LOG = Logger.getLogger('PyHouse.Email          ')


class ApiXml(PutGetXML):
    """
    """
    m_count = 0

    def read_xml(self, p_pyhouse_obj):
        """
        @return: a EmailData object.
        """
        l_dict = EmailData()
        try:
            l_xml = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
            if l_xml is None:
                return l_dict
            l_xml = l_xml.find('CommunicationSection')
            if l_xml is None:
                return l_dict
            l_xml = l_xml.find('EmailSection')
            if l_xml is None:
                return l_dict
            l_dict.EmailFromAddress = PutGetXML.get_text_from_xml(l_xml, 'EmailFromAddress')
            l_dict.EmailToAddress = PutGetXML.get_text_from_xml(l_xml, 'EmailToAddress')
            l_dict.GmailLogin = PutGetXML.get_text_from_xml(l_xml, 'GmailLogin')
            l_dict.GmailPassword = PutGetXML.get_text_from_xml(l_xml, 'GmailPassword')
        except AttributeError as e_err:
            LOG.error('ERROR in mqtt_xml.read_xml() - {}'.format(e_err))
        return l_dict

    def write_xml(self, p_obj):
        l_xml = ET.Element('EmailSection')
        try:
            l_obj = p_obj.Computer.Email
            PutGetXML.put_text_element(l_xml, 'EmailFromAddress', l_obj.EmailFromAddress)
            PutGetXML.put_text_element(l_xml, 'EmailToAddress', l_obj.EmailToAddress)
            PutGetXML.put_text_element(l_xml, 'GmailLogin', l_obj.GmailLogin)
            PutGetXML.put_text_element(l_xml, 'GmailPassword', l_obj.GmailPassword)
        except AttributeError as e_err:
            LOG.error('ERROR in mqtt_xml.write_xml() - {}'.format(e_err))
        return l_xml


class Utility(ApiXml):
    """
    """

    def setup_xml(self, p_pyhouse_obj):
        l_xml = p_pyhouse_obj.Xml.XmlRoot
        try:
            l_xml = l_xml.find('ComputerDivision')
            l_xml = l_xml.find('EmailSection')
        except AttributeError as e_err:
            LOG.error('SetupXML ERROR {}'.format(e_err))
        return l_xml

    def create_email_message(self, p_pyhouse_obj, p_address, p_subject, p_body, p_attachment=None):
        l_msg = email.mime.Multipart.MIMEMultipart()
        l_msg['Subject'] = p_subject
        l_msg['From'] = p_pyhouse_obj.Computer.Email.EmailFromAddress
        l_msg['To'] = p_address
        l_body = email.mime.Text.MIMEText(p_body)
        l_msg.attach(l_body)
        l_att = email.mime.application.MIMEApplication(p_attachment, _subtype="binary")
        l_att.add_header('Content-Disposition', 'attachment', filename="data.bin")
        l_msg.attach(l_att)
        #  Create a context factory which only allows SSLv3 and does not verify the peer's certificate.
        return str(l_msg)

    def send_email_message(self, _p_pyhouse_obj, _p_smtp_server, _p_smtp_port, _p_username, _p_password,
                           _p_fromaddress, _p_toaddress, p_message):
        #  l_contextFactory = ClientContextFactory()
        #  l_contextFactory.method = None  # SSLv3_METHOD
        l_deferred = Deferred()
        _mime_obj = StringIO(str(p_message))
        #  l_senderFactory = ESMTPSenderFactory(
        #    p_username, p_password,
        #    p_fromaddress, p_toaddress,
        #    p_message,
        #    l_deferred,
        #    contextFactory = l_contextFactory)
        #  p_pyhouse_obj.Twisted.Reactor.connectTCP(p_smtp_server, p_smtp_port, l_senderFactory)
        LOG.i("Sending Email")
        return l_deferred


class API(Utility):
    """
    """
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def LoadXml(self, p_pyhouse_obj):
        p_pyhouse_obj.Computer.Email = self.read_xml(p_pyhouse_obj)
        pass

    def Start(self):
        #  self.m_pyhouse_obj.Computer.Email = self.read_xml(self.m_pyhouse_obj)
        pass

    def SaveXml(self, p_xml):
        l_xml = self.write_xml(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Saved XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopped.")

    def SendEmail(self, p_to_address, p_subject, p_message, p_attachment):
        """
        This is the main interface to email.
        """
        _l_email = self.create_email(self.m_pyhouse_obj, p_to_address, p_subject, p_message, p_attachment)
        #  self.send_email(smtp_server, smtp_port, username, password, from_, to, msg)

#  ## END DBK
