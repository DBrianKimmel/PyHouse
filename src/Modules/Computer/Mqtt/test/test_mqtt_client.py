"""
@name:      PyHouse/src/Modules/Computer/Mqtt/test/test_mqtt_client.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@Copyright: (c)  2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 5, 2015
@Summary:

"""


# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
# from Modules.Core.data_objects import MqttBrokerData
from test import xml_data
# from test.xml_data import *
from Modules.Computer.Mqtt import mqtt_client
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_api = mqtt_client.API()


class C01_API(SetupMixin, unittest.TestCase):
    """
    Test Staticmethods
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))

    def test_01_start(self):
        """ Be sure that the XML contains the right stuff.
        """
        self.m_api.mqtt_start(self.m_pyhouse_obj)
        # PrettyPrintAny(self.m_xml.root, 'XML')
        self.assertEqual(self.m_xml.root.tag, 'PyHouse', 'Invalid XML - not a PyHouse XML config file')
        self.assertEqual(self.m_xml.computer_div.tag, 'ComputerDivision', 'XML - No Computer Division')
        self.assertEqual(self.m_xml.mqtt_sect.tag, 'MqttSection', 'XML - No Mqtt section')
        PrettyPrintAny(self.m_pyhouse_obj.Xml, 'XML')
        PrettyPrintAny(self.m_xml.mqtt_sect, 'Mqtt')



# ## END DBK
