"""
-*- test-case-name: PyHouse.src.Modules.Families.test.test_family_utils -*-

@name: PyHouse/src/Modules/Families/family_utils.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Aug 9, 2011
@license: MIT License
@summary: This module


All device objects use 'ControllerFamily' to designate the family.
This is because the things we wish to automate all have some controller that speaks to that
 class of device.

"""

# Import system type stuff

# Import PyHouse files
from Modules.Computer import logging_pyh as Logger

# Import PyMh files and modules.


LOG = Logger.getLogger('PyHouse.FamilyUtils ')



class FamUtil(object):

    @staticmethod
    def get_device_driver_API(p_controller_obj):
        """
        Based on the InterfaceType of the controller, load the appropriate driver and get its API().
        """
        if p_controller_obj.InterfaceType.lower() == 'serial':
            from Modules.Drivers.Serial import Serial_driver
            l_driver = Serial_driver.API()
        elif p_controller_obj.InterfaceType.lower() == 'ethernet':
            from Modules.Drivers.Ethernet import Ethernet_driver
            l_driver = Ethernet_driver.API()
        elif p_controller_obj.InterfaceType.lower() == 'usb':
            from Modules.Drivers.USB import USB_driver
            l_driver = USB_driver.API()
        else:
            LOG.error('No driver for device: {} with interface type: {}'.format(p_controller_obj.Name, p_controller_obj.InterfaceType))
            from Modules.Drivers.Null import Null_driver
            l_driver = Null_driver.API()
        p_controller_obj._DriverAPI = l_driver
        return l_driver

    @staticmethod
    def get_family(p_device_obj):
        """
        """
        try:
            l_family = p_device_obj.ControllerFamily
        except AttributeError as e_err:
            l_msg = 'ERROR - Device "{}" has no ControllerFamily Attribute - {}'.format(p_device_obj.Name, e_err)
            LOG.error(l_msg)
            print(l_msg)
            l_family = 'Null'
        return l_family

    @staticmethod
    def get_family_api(p_pyhouse_obj, p_device_obj):
        try:
            l_family = FamUtil.get_family(p_device_obj)
            l_api = p_pyhouse_obj.House.RefOBJs.FamilyData[l_family].FamilyModuleAPI
        except:
            l_msg = 'ERROR - Device:"{}"; Family:"{}" Cannot find API info '.format(p_device_obj.Name, l_family)
            LOG.error(l_msg)
            print(l_msg)
            l_api = None
        return l_api

    @staticmethod
    def read_family_data(p_pyhouse_obj, p_device_obj, p_xml):
        l_api = FamUtil.get_family_api(p_pyhouse_obj, p_device_obj)
        try:
            l_ret = l_api.ReadXml(p_device_obj, p_xml)
        except Exception as e_err:
            l_ret = 'ERROR in family_utils.read_family_data.  Device:"{}"  - {}'.format(p_device_obj.Name, e_err)
            LOG.error(l_ret)
            print(l_ret)
        return l_ret  # for testing

    @staticmethod
    def write_family_data(p_pyhouse_obj, p_out_xml, p_device):
        l_api = FamUtil.get_family_api(p_pyhouse_obj, p_device)
        try:
            l_ret = l_api.WriteXml(p_out_xml, p_device)
        except Exception as e_err:
            l_ret = 'ERROR in family_utils.write_family_data.  Device:"{}"  - {}'.format(p_device.Name, e_err)
            LOG.error(l_ret)
            print(l_ret)
        return l_ret  # for testing

# ## END DBK
