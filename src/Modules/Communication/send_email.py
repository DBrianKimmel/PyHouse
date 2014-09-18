"""
-*- test-case-name: PyHouse.src.Modules.Communications.test.test_send_email -*-

@name: PyHouse/src/Modules/Communication/send_email.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 3, 2014
@summary: Allow PyHouse to send email.

Fake out gmail.com and look like sendmail is connected.

This uses gmail as a mail relay agent
If you don't have an account - get one or write another module to handle your mail.

"""

# Import system type stuff
import email.mime.application
import xml.etree.ElementTree as ET
from twisted.internet.defer import Deferred
try:
    from cStringIO import cStringIO as StringIO
except ImportError:
    from StringIO import StringIO

# Import PyMh files
from Modules.Core.data_objects import EmailData
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.xml_tools import PutGetXML

g_debug = 1
LOG = Logger.getLogger('PyHouse.Email      ')


class ReadWriteConfigXml(PutGetXML):
    """
    """
    m_count = 0

    def read_xml(self, p_pyhouse_obj):
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

    def write_xml(self, p_obj):
        l_xml = ET.Element('EmailSection')
        self.put_text_element(l_xml, 'EmailFromAddress', p_obj.EmailFromAddress)
        self.put_text_element(l_xml, 'EmailToAddress', p_obj.EmailToAddress)
        self.put_text_element(l_xml, 'GmailLogin', p_obj.GmailLogin)
        self.put_text_element(l_xml, 'GmailPassword', p_obj.GmailPassword)
        return l_xml


class Utility(ReadWriteConfigXml):
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

    def create_email_message(self, p_pyhouse_obj, p_address, p_subject, p_body, p_attachment = None):
        l_msg = email.mime.Multipart.MIMEMultipart()
        l_msg['Subject'] = p_subject
        l_msg['From'] = p_pyhouse_obj.Computer.Email.EmailFromAddress
        l_msg['To'] = p_address
        l_body = email.mime.Text.MIMEText(p_body)
        l_msg.attach(l_body)
        l_att = email.mime.application.MIMEApplication(p_attachment, _subtype = "binary")
        l_att.add_header('Content-Disposition', 'attachment', filename = "data.bin")
        l_msg.attach(l_att)
        # Create a context factory which only allows SSLv3 and does not verify the peer's certificate.
        return str(l_msg)

    def send_email_message(self, p_pyhouse_obj, smtp_server, smtp_port, username, password, from_, to, msg):
        # contextFactory = ClientContextFactory()
        # contextFactory.method = SSLv3_METHOD
        resultDeferred = Deferred()
        mime_obj = StringIO(str(msg))
        # senderFactory = ESMTPSenderFactory(username, password, from_, to, mime_obj, resultDeferred, contextFactory = contextFactory)
        # reactor.connectTCP(smtp_server, smtp_port, senderFactory)
        print "Sending Email"
        return resultDeferred


class API(Utility):
    """
    """
    m_pyhouse_obj = None

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.Computer.Email = self.read_email_xml(p_pyhouse_obj)

    def Stop(self):
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        l_xml = self.write_email_xml(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Saved XML.")
        return p_xml

    def SendEmail(self, p_to_address, p_subject, p_message, p_attachment):
        """
        This is the main interface to email.
        """
        l_email = self.create_email(self.m_pyhouse_obj, p_to_address, p_subject, p_message, p_attachment)
        # self.send_email(smtp_server, smtp_port, username, password, from_, to, msg)

# ## END DBK
