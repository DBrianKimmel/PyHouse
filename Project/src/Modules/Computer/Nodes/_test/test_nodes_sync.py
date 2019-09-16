"""
@name:       Modules/Computer/Nodes/_test/test_nodes_sync.py
@author:     D. Brian Kimmel
@contact:    d.briankimmel@gmail.com
@copyright:  2016-2019 by D. Brian Kimmel
@date:       Created on Jun 2, 2016
@licencse:   MIT License
@summary:

Passed all 8 tests - DBK - 2019-01-19

"""

__updated__ = '2019-09-16'

# Import system type stuff
import xml.etree.ElementTree as ET
from twisted.trial import unittest

# Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import NodeInformation, NodeInterfaceData
from Modules.Computer.Nodes.node_sync import Util
from Modules.Core.Utilities import json_tools

from Modules.Core.Utilities.debug_tools import PrettyFormatAny


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title')  # so it is defined when printing is cleaned up.
        print('Id: test_nodes_sync')


class C1_Util(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the _test
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeInformation()

    def test_01_Who(self):
        # Util.send_who_is_there(self.m_pyhouse_obj)
        pass

    def test_02_Who(self):
        l_node = nodesXml._read_one_node_xml(self.m_xml.node)
        # print(PrettyFormatAny.form(l_node, 'C1-01-A - Node'))
        l_json = json_tools.encode_json(l_node)
        # print(PrettyFormatAny.form(l_json, 'C1-01-B - PyHouse'))
        l_msg = json_tools.decode_json_unicode(l_json)
        Util.add_node(self.m_pyhouse_obj, l_msg)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer.Nodes, 'C1-01-C - PyHouse'))

# ## END DBK
