"""
@name:      PyHouse/src/communication/_test/test_ir_control.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Mar 22, 2014
@summary:   Test

"""

__updated__ = '2019-10-08'

#  Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

#  Import PyMh files
# from Modules.Communication import ir_control
from _test.testing_mixin import SetupPyHouseObj


class SetupMixin(object):
    """
    """

    def setUp(self, p_root):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj(p_root)
        self.m_xml = SetupPyHouseObj().BuildXml(p_root)


class Test_01_Protocol(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = ir_control.Api()

    def tearDown(self):
        pass


class Test_02_Factory(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = ir_control.Api()

    def tearDown(self):
        pass


class Test_03_Connection(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = ir_control.Api()

    def tearDown(self):
        pass


class Test_04_Dispatch(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = ir_control.Api()

    def tearDown(self):
        pass


class Test_05_Utility(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = ir_control.Api()

    def tearDown(self):
        pass


class Test_06_Api(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = ir_control.Api()

    def tearDown(self):
        pass

#  ## END DBK
