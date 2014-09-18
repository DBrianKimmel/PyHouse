"""
@name: PyHouse/src/Modules/communication/test/test_send_email.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 3, 2014
@summary: Schedule events


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
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_XML(SetupMixin, unittest.TestCase):
    """
    This section will verify the XML in the 'Modules.test.xml_data' file is correct and what the node_local module can read/write.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        self.m_api = send_email.API()
        self.m_email_obj = EmailData()

    def test_0201_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.house_div.tag, 'HouseDivision', 'XML - No House Division')
        PrettyPrintAny(self.m_pyhouse_obj, 'Pyhouse', 120)
        PrettyPrintAny(self.m_pyhouse_obj.Computer, 'Pyhouse', 120)
        PrettyPrintAny(self.m_pyhouse_obj.House, 'Pyhouse', 120)

    def test_0210_Read(self):
        l_xml = self.m_api.read_xml(self.m_pyhouse_obj)
        self.assertEqual(l_xml.EmailFromAddress, 'mail.sender@Gmail.Com', 'Bad From Address')
        self.assertEqual(l_xml.EmailToAddress, 'mail.receiver@Gmail.Com', 'Bad To Address')
        self.assertEqual(l_xml.GmailLogin, 'TestAccount@Gmail.Com', 'Bad Login')
        self.assertEqual(l_xml.GmailPassword, 'Test=!=Password', 'Bad Password')
        PrettyPrintAny(l_xml, 'Xml', 120)

    def test_0220_Write(self):
        l_xml = self.m_api.read_xml(self.m_pyhouse_obj)
        l_ret = self.m_api.write_xml(l_xml)
        PrettyPrintAny(l_xml, 'Parsed', 120)
        PrettyPrintAny(l_ret, 'XML', 120)

    def test_0290_Send(self):
        l_xml = self.m_api.read_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.Computer.Email = l_xml
        l_ret = self.m_api.create_email_message(self.m_pyhouse_obj, l_xml.EmailToAddress, 'Test Subject', 'Test email Body', 'Test Attachment')
        PrettyPrintAny(l_xml, 'Parsed')
        PrettyPrintAny(l_ret, 'XML')


# ## END DBK
