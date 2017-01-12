"""
@name:      PyHouse/src/Modules/Computer/Web/test/test_web_thermostat.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by briank
@license:   MIT License
@note:      Created on Jul 1, 2014
@Summary:

"""

__updated__ = '2017-01-11'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import WebData, LoginData
from Modules.Computer.Web.web_xml import Xml as webXml
from Modules.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)
        self.m_pyhouse_obj.Computer.Web = WebData()
        self.m_pyhouse_obj.Computer.Web.Logins = LoginData()
        self.m_api = webXml()


class A0(unittest.TestCase):
    def setUp(self):
        pass
    def test_00_Print(self):
        print('Id: test_web_thermostat')

# ## END DBK
