"""
-*- test-case-name: PyHouse.src.Modules.Families.test.test_family_utils -*-

@name:      PyHouse/src/Modules/Families/family_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@note:      Created on Aug 9, 2011
@license:   MIT License
@summary:   This module is for using device families


All device objects use 'DeviceFamily' to designate the family.
This is because the things we wish to automate all have some controller that speaks to that
 class of device.

"""

# Import system type stuff.

# Import PyHouse files and modules.
from Modules.Computer import logging_pyh as Logger


LOG = Logger.getLogger('PyHouse.FamilyUtils ')



class FamUtil(object):

    @staticmethod
    def _get_device_name(p_device_obj):
        """
        Given some device object, extract the Family Name
        """
        return p_device_obj.Name

    @staticmethod
    def _get_family_name(p_device_obj):
        """
        Given some device object, extract the Family Name
        """
        return p_device_obj.DeviceFamily

    @staticmethod
    def _get_family_obj(p_pyhouse_obj, p_device_obj):
        """
        Given some device object, extract the Family Name
        """
        try:
            l_name = FamUtil._get_family_name(p_device_obj)
            l_family_obj = p_pyhouse_obj.House.RefOBJs.FamilyData[l_name]
        except Exception as e_err:
            LOG.error('Could not get family object for Name:{}\n\t{}'.format(l_name, e_err))
            l_family_obj = p_pyhouse_obj.House.RefOBJs.FamilyData['Null']
        return l_family_obj

    @staticmethod
    def _get_device_family(p_device_obj):
        return p_device_obj.DeviceFamily

    @staticmethod
    def get_device_driver_API(p_controller_obj):
        """
        Based on the InterfaceType of the controller, load the appropriate driver and get its API().
        """
        l_dev_name = FamUtil._get_device_name(p_controller_obj)
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
            LOG.error('No driver for device: {} with interface type: {}'.format(l_dev_name, p_controller_obj.InterfaceType))
            from Modules.Drivers.Null import Null_driver
            l_driver = Null_driver.API()
        p_controller_obj._DriverAPI = l_driver
        return l_driver

    @staticmethod
    def get_family(p_device_obj):
        """
        @param p_device_obj: contains the info about the device we are working on.
        """
        l_dev_name = FamUtil._get_device_name(p_device_obj)
        # l_dev_family = FamUtil._get_device_family(p_device_obj)
        try:
            l_family = p_device_obj.DeviceFamily
        except AttributeError as e_err:
            l_msg = 'ERROR - Device "{}" has no DeviceFamily Attribute - {}'.format(l_dev_name, e_err)
            LOG.error(l_msg)
            print(l_msg)
            l_family = 'Null'
        return l_family

    @staticmethod
    def _get_family_device_api(p_pyhouse_obj, p_device_obj):
        """
        """
        l_dev_name = FamUtil._get_device_name(p_device_obj)
        try:
            l_family = FamUtil.get_family(p_device_obj)
            l_family_obj = p_pyhouse_obj.House.RefOBJs.FamilyData[l_family]
            l_api = l_family_obj.FamilyModuleAPI
        except:
            l_msg = 'ERROR - Device:"{}"\n\tFamily:"{}"\n\tCannot find API info '.format(l_dev_name, l_family)
            LOG.error(l_msg)
            print(l_msg)
            l_api = None
        return l_api

    @staticmethod
    def _get_family_xml_api(p_pyhouse_obj, p_device_obj):
        """
        This will get the address where we can read or write family specific XML data
        @return: The XmlApi of the family specific data.
        """
        l_dev_name = FamUtil._get_device_name(p_device_obj)
        l_family_obj = FamUtil._get_family_obj(p_pyhouse_obj, p_device_obj)
        try:
            l_xmlAPI = l_family_obj.FamilyXmlModuleAPI
        except:
            l_msg = 'ERROR FamUtil-95 - Device:"{}"; Family:"{}" Cannot find XmlAPI info '.format(l_dev_name, l_family_obj.Name)
            LOG.error(l_msg)
            print(l_msg)
            l_xmlAPI = None
        return l_xmlAPI

    @staticmethod
    def read_family_data(p_pyhouse_obj, p_device_obj, p_xml):
        """
        Get the family specific XML data for any device.
        @param p_pyhouse_obj: is the entire PyHouse Data
        @param p_device_obj: is the device we will be outputting info for.
        @param p_xml: is the XML data for the entire device.
        """
        l_dev_name = FamUtil._get_device_name(p_device_obj)
        l_api = FamUtil._get_family_xml_api(p_pyhouse_obj, p_device_obj)
        try:
            l_ret = l_api.ReadXml(p_device_obj, p_xml)
        except Exception as e_err:
            l_ret = 'ERROR family_utils-110  API:{}  Device:"{}"\n   {}'.format(l_api, l_dev_name, e_err)
            LOG.error(l_ret)
            print(l_ret)
        return l_ret  # for testing

    @staticmethod
    def write_family_data(p_pyhouse_obj, p_out_xml, p_device_obj):
        """
        Write out the Family Specific XML for a given device
        @param p_pyhouse_obj: The entire PyHouse Data
        @param p_out_xml: is the XML data we are writing out.
        @param p_device_obj: is the device we will be outputting info for.
        """
        l_dev_name = FamUtil._get_device_name(p_device_obj)
        l_api = FamUtil._get_family_xml_api(p_pyhouse_obj, p_device_obj)
        try:
            l_ret = l_api.WriteXml(p_out_xml, p_device_obj)
        except Exception as e_err:
            l_ret = 'ERROR in family_utils.write_family_data.  Device:"{}"\n  Api:{}\n   Err:{}'.format(l_dev_name, l_api, e_err)
            LOG.error(l_ret)
            print(l_ret)
        return l_ret  # for testing

# ## END DBK
