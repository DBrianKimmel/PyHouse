"""
@name:      PyHouse/src/Modules/communication/test/test_send_email.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 3, 2014
@summary:   Send some email testing

    From nobody Wed Jul 30 22:41:30 2014
    Content-Type: multipart/mixed; boundary="===============1622763079=="
    MIME-Version: 1.0
    Subject: Test Subject
    From: mail.sender@Gmail.Com
    To: mail.receiver@Gmail.Com

    --===============1622763079==
    Content-Type: text/plain; charset="us-ascii"
    MIME-Version: 1.0
    Content-Transfer-Encoding: 7bit

    Test email Body
    --===============1622763079==
    Content-Type: application/binary
    MIME-Version: 1.0
    Content-Transfer-Encoding: base64
    Content-Disposition: attachment; filename="data.bin"

    VGVzdCBBdHRhY2htZW50
    --===============1622763079==--

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import EmailData
from Modules.Communication import send_email
from Modules.Communication.test.xml_communications import \
        TESTING_EMAIL_FROM_ADDRESS, \
        TESTING_EMAIL_TO_ADDRESS, \
        TESTING_GMAIL_LOGIN, \
        TESTING_GMAIL_PASSWORD
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_Setup(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = send_email.API(self.m_pyhouse_obj)
        self.m_email_obj = EmailData()

    def test_01_Xml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision')
        self.assertEqual(self.m_xml.communication_sect.tag, 'CommunicationSection')
        self.assertEqual(self.m_xml.email_sect.tag, 'EmailSection')
        self.assertEqual(self.m_xml.twitter_sect.tag, 'TwitterSection')
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'Pyhouse', 120))
        print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer.Comm, 'Pyhouse', 120))


class C02_Read(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = send_email.API(self.m_pyhouse_obj)
        self.m_email_obj = EmailData()

    def test_01_All(self):
        l_xml = self.m_api.read_xml(self.m_pyhouse_obj)
        self.assertEqual(l_xml.EmailFromAddress, TESTING_EMAIL_FROM_ADDRESS)
        self.assertEqual(l_xml.EmailToAddress, TESTING_EMAIL_TO_ADDRESS)
        self.assertEqual(l_xml.GmailLogin, TESTING_GMAIL_LOGIN)
        self.assertEqual(l_xml.GmailPassword, TESTING_GMAIL_PASSWORD)


class C03_Write(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = send_email.API(self.m_pyhouse_obj)
        self.m_email_obj = EmailData()

    def test_03_All(self):
        l_xml = self.m_api.read_xml(self.m_pyhouse_obj)
        l_ret = self.m_api.write_xml(l_xml)


class C04_Send(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        self.m_api = send_email.API(self.m_pyhouse_obj)
        self.m_email_obj = EmailData()

    def test_01_One(self):
        l_xml = self.m_api.read_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Email = l_xml
        l_ret = self.m_api.create_email_message(self.m_pyhouse_obj, l_xml.EmailToAddress, 'Test Subject', 'Test email Body', 'Test Attachment')

# ## END DBK
