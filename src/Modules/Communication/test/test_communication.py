"""
@name:       PyHouse/src/Modules/Communication/test/test_communication.py
@author:     D. Brian Kimmel
@contact:    d.briankimmel@gmail.com
@copyright:  2016-2016 by D. Brian Kimmel
@date:       Created on May 30, 2016
@licencse:   MIT License
@summary:

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
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.APIs, 'Pyhouse', 120))

# ## END DBK
