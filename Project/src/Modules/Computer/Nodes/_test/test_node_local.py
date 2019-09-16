"""
@name:      Modules/Computer/Nodes/_test/test_node_local.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 29, 2014
@summary:   This module is for testing local node data.

Passed all 19 tests - DBK - 2019-01-19

"""

__updated__ = '2019-09-16'

#  Import system type stuff
from twisted.trial import unittest
import netifaces
from netifaces import *

#  Import PyMh files and modules.
from _test.testing_mixin import SetupPyHouseObj
from Modules.Core.data_objects import NodeInformation, NodeInterfaceData
from Modules.Computer.Nodes.node_local import \
    Interfaces, \
    API as localApi, \
    Devices as localDevices, \
    Util as localUtil
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

""" The following definitions are fake in order to keep eclipse errors from coming up on the netifaces module.
This is cosmetic - the code runs but eclipse does not find the definitions.
"""
L_INET = 2
L_INET6 = 10

INTERFACE_LO = 'lo'
INTERFACE_EN = 'enp3s0'
INTERFACE_wL = 'wlp2s0'


class SetupMixin(object):

    def setUp(self):
        self.m_pyhouse_obj = SetupPyHouseObj().BuildPyHouseObj()


class FakeNetiface(object):
    """
    """


class A0(unittest.TestCase):

    def test_00_Print(self):
        _x = PrettyFormatAny.form('_test', 'title', 190)  # so it is defined when printing is cleaned up.
        print('Id: test_node_local')


class B1_Netiface(SetupMixin, unittest.TestCase):
    """
    This section tests the setup of the _test
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_interface_obj = NodeInterfaceData()
        self.m_node_obj = NodeInformation()

    def test_01_Families(self):
        """ Check the AF list for what we assume is the correct number later.
        From Kubuntu 16.04:
        0                             AF_UNSPEC
        1                             AF_FILE
        2                             AF_INET
        3                             AF_AX25
        4                             AF_IPX
        5                             AF_APPLETALK
        6                             AF_NETROM
        7                             AF_BRIDGE
        8                             AF_ATMPVC
        9                             AF_X25
        10                            AF_INET6
        11                            AF_ROSE
        12                            AF_DECnet
        13                            AF_NETBEUI
        14                            AF_SECURITY
        15                            AF_KEY
        16                            AF_NETLINK
        17                            AF_PACKET
        18                            AF_ASH
        19                            AF_ECONET
        20                            AF_ATMSVC
        22                            AF_SNA
        23                            AF_IRDA
        24                            AF_PPPOX
        25                            AF_WANPIPE
        31                            AF_BLUETOOTH
        34                            AF_ISDN
        """
        l_fam = Interfaces._list_families()
        # print(PrettyFormatAny.form(l_fam, 'B1-01-A - A_Families', 170))
        self.assertEqual(l_fam[2], 'AF_INET')
        self.assertEqual(l_fam[10], 'AF_INET6')
        self.assertEqual(l_fam[17], 'AF_PACKET')

    def test_02_Gateways(self):
        """ Check the gateways

        2                           [('192.168.1.1', 'wlo1', True)]
        10                          [('fe80::12bf:48ff:feb6:eb6f', 'wlo1', True)]
        default                     2        ('192.168.1.1', 'wlo1')
                                    10

        """
        l_gate = Interfaces._list_gateways()
        # print(PrettyFormatAny.form(l_gate, 'B1-02-A - Gateways', 100))
        l_v4 = l_gate[L_INET]  # 2 = AF_INET
        # print(PrettyFormatAny.form(l_v4, 'B1-02-B - Gateways', 100))
        self.assertEqual(l_v4[0][0], '192.168.1.1')

    def test_03_ListInterfaces(self):
        """ Check the interfaces in this computer
        """
        l_int = Interfaces._list_interfaces()
        # print(PrettyFormatAny.form(l_int, 'B1-03-A - Interfaces', 170))
        self.assertEqual(l_int[0], INTERFACE_LO)
        self.assertEqual(l_int[1], INTERFACE_EN)
        self.assertEqual(l_int[2], INTERFACE_wL)

    def test_04_Interfaces(self):
        """ Check the interfaces in this computer
        """
        l_int = Interfaces._list_interfaces()
        # print(PrettyFormatAny.form(l_int, 'B1-04-A - Interface Names', 170))
        for l_name in l_int:
            l_ifa = Interfaces._list_ifaddresses(l_name)
            # print(PrettyFormatAny.form(l_ifa, 'B1-04-B - Interface "{}" Addresses'.format(l_name), 170))
            self.assertGreaterEqual(len(l_ifa), 1)

    def test_05_All(self):
        l_all, _l_v4, _l_v6 = Interfaces()._get_all_interfaces()
        for _l_ix in l_all:
            # print('{} {}'.format(_l_ix, PrettyFormatAny.form(l_all[_l_ix], 'B1-05-A - Interface', 170)))
            pass
        # print(PrettyFormatAny.form(l_all, 'B1-05-B - Interfaces', 170))
        # print(PrettyFormatAny.form(self.m_pyhouse_obj, 'B1-05-C - PyHouse'))
        self.assertNotEqual(l_all, None)


class B2_Iface(SetupMixin, unittest.TestCase):
    """ _test getting interface information.
    """

    def setUp(self):
        SetupMixin.setUp(self)
        self.m_node = NodeInformation()
        self.m_iface_api = Interfaces()

    def test_01_AllIfaceNames(self):
        """ This will be different on different computers

        I don't know how to _test the returned list for validity.
        Uncomment the print to see what your computer returned.
        """
        l_names = Interfaces()._find_all_interface_names()
        # print(PrettyFormatAny.form(l_names, 'B1-01-A - Names'))
        self.assertEqual(l_names[0], INTERFACE_LO)
        self.assertEqual(l_names[1], INTERFACE_EN)
        self.assertEqual(l_names[2], INTERFACE_wL)
        self.assertGreater(len(l_names), 1)

    def test_02_AddrFamilyName(self):
        """
        We are interested in:
            IPv4 (AF_INET)     = IPv4
            IPv6 (AF_INET6)    = IPv6
            MAC  (AF_LINK)
        """
        l_ret = Interfaces()._find_addr_family_name(L_INET)
        # print(PrettyFormatAny.form(l_ret, 'B1-02 B Address Lists'))
        self.assertEqual(l_ret, 'AF_INET')
        l_ret = Interfaces()._find_addr_family_name(L_INET6)
        # print(PrettyFormatAny.form(l_ret, 'B1-02 C Address Lists'))
        self.assertEqual(l_ret, 'AF_INET6')

    def test_03_AddrLists(self):
        """
        I don't know how to _test the returned list for validity.
        Uncomment the print to see what your computer returned.
        """
        l_names = Interfaces()._find_all_interface_names()
        # print(PrettyFormatAny.form(l_names, 'B2-03-A - Address Lists'))
        self.assertEqual(l_names[0], INTERFACE_LO)
        self.assertEqual(l_names[1], INTERFACE_EN)
        self.assertEqual(l_names[2], INTERFACE_wL)
        #
        l_lo = Interfaces()._find_addr_lists(l_names[0])
        # print(PrettyFormatAny.form(l_lo, 'B2-03-B - lo Address Lists'))
        self.assertEqual(l_lo[L_INET][0]['addr'], '127.0.0.1')
        self.assertEqual(l_lo[L_INET6][0]['addr'], '::1')
        #
        _l_en = Interfaces()._find_addr_lists(l_names[1])
        # print(PrettyFormatAny.form(l_en, 'B2-03-C - eno1 Address Lists'))
        # self.assertEqual(l_en[L_INET][0]['addr'], '127.0.0.1')
        #
        l_wl = Interfaces()._find_addr_lists(l_names[2])
        # print(PrettyFormatAny.form(l_wl, 'B2-03-D - wlo1 Address Lists'))
        self.assertEqual(l_wl[L_INET][0]['addr'], '192.168.1.50')
        # self.assertEqual(l_wl[L_INET6][0]['addr'], '2222:3333')

    def test_04_AddrListInet(self):
        pass

    def test_05_OneInterfaces(self):
        l_names = Interfaces()._find_all_interface_names()
        # print(PrettyFormatAny.form(l_names, 'B2-05-A - Interface Names'))
        self.assertEqual(l_names[0], INTERFACE_LO)
        self.assertEqual(l_names[1], INTERFACE_EN)
        self.assertEqual(l_names[2], INTERFACE_wL)
        #
        l_node = Interfaces()._get_one_interface(l_names[2])
        # print(PrettyFormatAny.form(l_node[0], 'B2-05-B - Node Interfaces'))
        self.assertEqual(l_node[0].Name, INTERFACE_wL)

    def test_06_AllInterfaces(self):
        l_node = NodeInformation()
        l_if, _l_v4, _l_v6 = Interfaces()._get_all_interfaces()
        l_node.NodeInterfaces = l_if
        # print(PrettyFormatAny.form(l_node.NodeInterfaces, 'B2-06-A - Node Interfaces'))
        self.assertEqual(len(l_node.NodeInterfaces), 4)
        # print(PrettyFormatAny.form(l_node.NodeInterfaces[0], 'B2-06-B - Node Interfaces'))
        self.assertEqual(l_node.NodeInterfaces[0].Name, 'lo')
        # print(PrettyFormatAny.form(l_node.NodeInterfaces[1], 'B2-06-C - Node Interfaces'))
        self.assertEqual(l_node.NodeInterfaces[1].Name, 'enp3s0')
        # print(PrettyFormatAny.form(l_node.NodeInterfaces[2], 'B2-06-D - Node Interfaces'))
        self.assertEqual(l_node.NodeInterfaces[2].Name, 'wlp2s0')
        # print(PrettyFormatAny.form(l_node.NodeInterfaces[3], 'B2-06-E - Node Interfaces'))
        self.assertEqual(l_node.NodeInterfaces[3].Name, 'docker0')


class B3_Node(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Node(self):
        """
        """
        l_node = localUtil(self.m_pyhouse_obj).create_local_node()
        print(PrettyFormatAny.form(l_node, 'B3-01-A - Node'))
        self.assertEqual(l_node.Name, 'Laptop-4')
        self.assertEqual(l_node.Key, 0)
        self.assertEqual(l_node.Active, True)


class C1_Api(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_Api(self):
        _l_api = localApi(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(self.m_pyhouse_obj.Computer, 'C1-01-A - PyHouse Computer'))

    def test_02_LoadXml(self):
        l_api = localApi(self.m_pyhouse_obj)
        _l_ret = l_api.LoadXml(self.m_pyhouse_obj)
        # print(PrettyFormatAny.form(l_ret, 'C1-02-A - PyHouse Computer'))

    def test_03_Start(self):
        #  self.m_api.Start(self.m_pyhouse_obj)
        pass

    def test_05_Stop(self):
        localApi(self.m_pyhouse_obj).Stop()
        pass


class D1_Devices(SetupMixin, unittest.TestCase):

    def setUp(self):
        SetupMixin.setUp(self)

    def test_01_lsusb(self):
        l_usb = localDevices()._lsusb()
        # l_lines = l_usb.split('\n')
        print('D1-01-A ', l_usb)

    def test_03_find(self):
        """Find all controllers
        """
        l_ret = localDevices()._find_controllers()
        print('D1-03-A ', l_ret, len(l_ret))

#  ## END DBK
