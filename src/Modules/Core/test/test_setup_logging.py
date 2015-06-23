"""
@name:      PyHouse/src/Modules/Core/test/test_setup_logging.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@Copyright: (c)  2014 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 30, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core import setup_logging
from test import xml_data
from test.testing_mixin import SetupPyHouseObj
from Modules.Utilities.tools import PrettyPrintAny


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class C01_NoXML(SetupMixin, unittest.TestCase):
    """
    This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_EMPTY))
        # self.m_api = Logger.API()

    def test_01(self):
        PrettyPrintAny(setup_logging.LOGGING_DICT, 'Logging')

# ## END DBK
