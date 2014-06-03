"""
@name: PyHouse/src/Modules/utils/tools.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on Apr 11, 2013
@license: MIT License
@summary: Various functions and utility methods.

"""


# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.Core.data_objects import PyHousesData
from Modules.utils import tools
from src.test import xml_data
from src.Modules.utils.tools import PrettyPrintXML, PrettyPrintObject, PrettyPrintAny


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_PrettyPrintObjects(self):
        l_obj = PyHousesData()
        PrettyPrintObject(l_obj)

    def test_02_PrettyPrintXML(self):
        l_xml = self.m_root_xml = ET.fromstring(xml_data.XML_LONG)
        PrettyPrintXML(l_xml)

    def test_03_any(self):
        l_any = {'abc': 'Long A B C', 'def' : 'Another long thing.'}
        PrettyPrintAny(l_any)

# ## END DBK
