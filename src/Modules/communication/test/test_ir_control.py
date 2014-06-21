"""
@name: PyHouse/src/communication/test/test_ir_control.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Mar 22, 2014
@summary: Test

"""

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files
from Modules.communication import ir_control
from src.test import xml_data, test_mixin

XML = xml_data.XML_LONG


class SetupMixin(object):
    """
    """

    def setUp(self):
        test_mixin.Setup()


class Test_02_XML(unittest.TestCase):

    def setUp(self):
        self.m_api = ir_control.API()

    def tearDown(self):
        pass

# ## END DBK
