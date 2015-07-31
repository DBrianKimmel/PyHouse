"""
@name:      PyHouse/src/Modules/Core/test/test_setup_logging.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 30, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class A1_SetupL(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(XML_LONG))
        # self.m_api = Logger.API()

    def test_01_XML(self):
        # PrettyPrintAny(setup_logging.LOGGING_DICT, 'Logging')
        pass

    def test_02_Handlers(self):
        # PrettyPrintAny(setup_logging.LOGGING_DICT['handlers'], 'Logging')
        pass

    def test_03_Debug(self):
        # PrettyPrintAny(setup_logging.LOGGING_DICT['handlers']['debug'], 'Logging')
        pass

    def test_04_Error(self):
        # PrettyPrintAny(setup_logging.LOGGING_DICT['handlers']['error'], 'Logging')
        pass

# ## END DBK
