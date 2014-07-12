"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/irrigation/test/test_irrigation.py
@author: briank
@contact: <d.briankimmel@gmail.com>
@Copyright: (c)  2014 by briank
@license: MIT License
@note: Created on Jul 4, 2014
@Summary:

"""
# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import IrrigationData
from Modules.irrigation import irrigation
from Modules.web import web_utils
from Modules.Core import setup
from Modules.utils.tools import PrettyPrintAny
from test import xml_data


class SetupMixin(object):
    """
    """

    def setUp(self):
        self.m_pyhouse_obj = setup.build_pyhouse_obj(self)
        self.m_pyhouse_obj.Xml.XmlRoot = self.m_root_xml
        self.m_irrigation_obj = IrrigationData()
        return self.m_pyhouse_obj


class Test_02_XML(SetupMixin, unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testName(self):
        pass

# ## END DBK
