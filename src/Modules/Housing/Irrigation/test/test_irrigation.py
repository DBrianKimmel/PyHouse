"""
@name:      PyHouse/src/Modules/irrigation/test/test_irrigation.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2016 by briank
@license:   MIT License
@note:      Created on Jul 4, 2014
@Summary:

Passed all 1 tests - DBK - 2016-08-24

"""

__updated__ = '2016-08-24'

# Import system type stuff
# import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from Modules.Core.data_objects import IrrigationData


class SetupMixin(object):
    """
    """

    def setUp(self):
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