"""
@name:      Modules/House/Entertainment/pioneer/_test/test_pioneer.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 10, 2018
@summary:   Test

Passed all 3 tests - DBK - 2019-08-02

"""

__updated__ = '2019-08-02'

# Import system type stuff
from twisted.trial import unittest
from twisted.test import proto_helpers

# Import PyMh files
from _test.testing_mixin import SetupPyHouseObj
from Modules.House.Entertainment.pioneer.pioneer import \
        SECTION, \
        API as pioneerAPI, \
        PioneerFactory as pioFactory
from Modules.House.Entertainment.pioneer.test.xml_pioneer import \
        TESTING_PIONEER_DEVICE_NAME_0
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()

    def setup2(self):
        self.m_factory = pioFactory(self.m_pyhouse_obj)
        self.m_transport = proto_helpers.StringTransport()
        self.m_proto = self.m_factory.buildProtocol(('127.0.0.1', 0))
        self.m_proto.makeConnection(self.m_transport)


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_pioneer')


class A1_Setup(SetupMixin, unittest.TestCase):
    """Test that we have set up properly for the rest of the testing classes.
    """

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_BuildObjects(self):
        """ Test to be sure the compound object was built correctly.
        """
        pass


class E1_API(SetupMixin, unittest.TestCase):
    """ Test that we write out the xml properly
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_api = pioneerAPI(self.m_pyhouse_obj)

    def test_01_Find(self):
        """ Find the correct device obj
        """
        l_family = 'pioneer'
        l_device = '822-k'

# ## END DBK
