"""
@name:      Modules/House/Family/family_utils.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@note:      Created on Aug 9, 2011
@license:   MIT License
@summary:   This module is for *USING* device families

All device objects use 'Family.Name' to designate the family.
This is because the things we wish to automate all have some controller that speaks to that
 class of device.

"""

__updated__ = '2019-09-06'

#  Import system type stuff.

#  Import PyHouse files and modules.
from Modules.Core import logging_pyh as Logger
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.House.Family.family import FamilyModuleInformation

LOG = Logger.getLogger('PyHouse.FamilyUtils ')


def _get_device_name(p_device_obj):
    """
    Given some device object, extract the Family Name
    """
    return p_device_obj.Name


class FamUtil(object):

    @staticmethod
    def _get_family_obj(p_pyhouse_obj, p_device_obj):
        """
        Given some device object, extract the Family object using .Family.Name
        """
        l_family_name = p_device_obj.Family.Name
        try:
            l_family_obj = p_pyhouse_obj.House.Family[l_family_name]
        except (KeyError, TypeError) as e_err:
            l_msg = PrettyFormatAny.form(p_pyhouse_obj.House, ' House Information', 40)
            LOG.error('Could not get family object for:\n\tDevice Name:\t{}\n\tFamily:\t\t{}\n\tKey Error:\t{}{}'
                      .format(p_device_obj.Name, l_family_name, e_err, l_msg))
            if l_family_name == 'Null':
                p_pyhouse_obj.House.Family['null'] = FamilyModuleInformation()
                p_pyhouse_obj.House.Family['null'].Name = 'Null'
            l_family_obj = p_pyhouse_obj.House.Family['null']
        return l_family_obj

    @staticmethod
    def get_device_driver_API(p_pyhouse_obj, p_controller_obj):
        """
        Based on the InterfaceType of the controller, load the appropriate driver and get its API().
        @return: a pointer to the device driver or None
        """
        LOG.debug(PrettyFormatAny.form(p_controller_obj, 'Controller'))
        l_dev_name = _get_device_name(p_controller_obj)
        l_type = _get_interface_type(p_controller_obj)
        if l_type == 'serial':
            from Modules.Core.Drivers.Serial import Serial_driver
            l_driver = Serial_driver.API(p_pyhouse_obj).Start(p_controller_obj)

        elif l_type == 'ethernet':
            from Modules.Core.Drivers.Ethernet import Ethernet_driver
            l_driver = Ethernet_driver.API(p_pyhouse_obj).Start(p_controller_obj)

        elif l_type == 'usb':
            from Modules.Core.Drivers.USB import USB_driver
            l_driver = USB_driver.API(p_pyhouse_obj).Start(p_controller_obj)

        else:
            LOG.error('No driver for device: {} with interface type: {}'.format(
                    l_dev_name, p_controller_obj.Interface.Type))
            from Modules.Core.Drivers.Null import Null_driver
            l_driver = Null_driver.API(p_pyhouse_obj).Start(p_controller_obj)

        p_controller_obj.Interface._DriverApi = l_driver
        return l_driver

    @staticmethod
    def get_family(p_device_obj):
        """
        @param p_device_obj: contains the info about the device we are working on.
        @return: the Family.Name which is the Name of the family (e.g. Insteon)
        """
        l_dev_name = _get_device_name(p_device_obj)
        try:
            l_family = p_device_obj.Family.Name
        except AttributeError as e_err:
            l_msg = 'ERROR - Device "{}" has no Family.Name Attribute - {}'.format(l_dev_name, e_err)
            LOG.error(l_msg)
            l_family = 'Null'
        return l_family.lower()

    @staticmethod
    def _get_family_device_api(p_pyhouse_obj, p_device_obj):
        """ Get the pointer to the correct family module API class.

        @param p_device_obj: is the device to find the API for.
        @return: the pointer to the API class of the proper device family
        """
        l_dev_name = _get_device_name(p_device_obj)
        try:
            l_family = FamUtil.get_family(p_device_obj)
            l_family_obj = p_pyhouse_obj.House.Family[l_family]
            l_device_api = l_family_obj.DeviceAPI
            LOG.info('Got API for "{}"'.format(l_family))
        except Exception as e_err:
            l_msg = 'ERROR - Device:"{}"\n\tFamily:"{}"\n\tCannot find API info\n\tError: {}'.format(l_dev_name, l_family, e_err)
            LOG.error(l_msg)
            l_device_api = None
        return l_device_api

    @staticmethod
    def XXX_get_family_xml_api(p_pyhouse_obj, p_device_obj):
        """
        This will get the reference to a family which will read or write family specific XML data

        @param p_pyhouse_obj: is the entire PyHouse Data
        @param p_device_obj: is the device we will be outputting info for.
        @return: The XmlApi of the family specific data.
        """
        l_family_obj = FamUtil._get_family_obj(p_pyhouse_obj, p_device_obj)
        try:
            l_xmlAPI = l_family_obj.FamilyXml_ModuleAPI
        except:
            l_msg = 'ERROR FamUtil-95 - Device:"{}"; Family:"{}" Cannot find XmlAPI info '.format(p_device_obj.Name, l_family_obj.Name)
            LOG.error(l_msg)
            l_xmlAPI = None
        return l_xmlAPI

    @staticmethod
    def XXXread_family_data(p_pyhouse_obj, p_device_obj, p_xml):
        """
        This is a dispatch type routine.  It will use the Family.Name field contents to run the
        appropiate family XML-read routine.

        Get the family specific XML data for any device.

        @param p_pyhouse_obj: is the entire PyHouse Data
        @param p_device_obj: is the device we will be outputting info for.
        @param p_xml: is the XML data for the entire device.
        """
        l_xml_api = FamUtil._get_family_xml_api(p_pyhouse_obj, p_device_obj)
        try:
            l_ret = l_xml_api.ReadXml(p_device_obj, p_xml)
        except Exception as e_err:
            l_ret = 'ERROR family_utils-149  API:{}  Device:"{}"\n   {}'.format(l_xml_api, p_device_obj.Name, e_err)
            LOG.error('ERROR - Unable to load family information for a device.'
                      '\n\tDevice: {}\n\tFamily: {}\n\t{}'.format(p_device_obj.Name, p_device_obj.Family.Name, e_err))
        return l_ret  # for testing

#  ## END DBK
