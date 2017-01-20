"""
@name:      PyHouse/src/Modules/Core/test/test_setup_logging.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 30, 2014
@Summary:

"""

__updated__ = '2017-01-20'


# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from test.xml_data import XML_LONG
from test.testing_mixin import SetupPyHouseObj


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
        pass

    def test_02_Handlers(self):
        pass

    def test_03_Debug(self):
        pass

    def test_04_Error(self):
        pass

# ## END DBK
