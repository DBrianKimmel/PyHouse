"""
@name:      Modules/Computer/Nodes/_test/test_nodes.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 15, 2015
@Summary:

Passed 6 of 7 tests - DBK - 2019-09-16

"""

__updated__ = '2019-09-16'

# Import system type stuff
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import NodeInformation, NodeInterfaceData
from Modules.Computer.Nodes.nodes import API as nodesApi
from Modules.Computer.Nodes.node_local import API as localApi
from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_nodes')


class A1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the _test
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeInformation()

    def test_01_FindXml(self):
        """ Be sure that the XML contains the right stuff.
        """
        # print(PrettyFormatAny.form(self.m_xml, 'Xml'))


class B1_Setup(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the _test
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeInformation()

    def test_01_PyHouse(self):
        nodesApi(self.m_pyhouse_obj).LoadConfig()
        l_nodes = self.m_pyhouse_obj.Computer.Nodes
        # print(PrettyFormatAny.form(l_nodes, 'B1-01-A - Nodes'))
        # print(PrettyFormatAny.form(l_nodes[TESTING_NODES_NODE_UUID_0], 'B1-01-B - PyHouse'))
        pass


class C1_Api(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_init(self):
        _l_api = localApi(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'PyHouse Computer'))
        pass

    def test_02_LoadXml(self):
        l_api = localApi(self.m_pyhouse_obj)
        _l_ret = l_api.LoadConfig()
        # print(PrettyFormatAny.form(l_ret, 'PyHouse Computer'))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'PyHouse Computer'))
        pass

    def test_02_Start(self):
        #  self.m_api.Start(self.m_pyhouse_obj)
        pass

    def test_03_Stop(self):
        #  self.m_api.Stop()
        pass

# ## END DBK
