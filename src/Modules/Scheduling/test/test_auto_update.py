"""
@name: PyHouse/src/Modules/Scheduling/test/test_auto_update.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on Dec 31, 2013
@license: MIT License
@summary: Handle the automatic updating of PyHouse

This module tests auto updating
"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import LightData
from Modules.Scheduling import auto_update
from Modules.Utilities.tools import PrettyPrintAny
from test import xml_data
from test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_02_XML(SetupMixin, unittest.TestCase):
    """ This section tests the reading and writing of XML used by node_local.
    """

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)


class Test_03_Local(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)

    def test_0301_PyHouse(self):
        l_file = auto_update.FindLocalVersion()._find_pyhouse_version_file()
        print('Local File = {0:}'.format(l_file))

    def test_0321_LocalVersion(self):
        l_version = auto_update.FindLocalVersion().get_version()
        print(l_version)


class Test_04_Repository(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self, ET.fromstring(xml_data.XML_LONG))
        SetupPyHouseObj().BuildXml(self.m_xml.root)

    def test_0402_RepositoryVersion(self):
        l_version = auto_update.FindRepositoryVersion().get_version()
        print(l_version)

# ## END DBK
