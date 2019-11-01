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

__updated__ = '2019-10-31'

#  Import system type stuff.

#  Import PyHouse files and modules.
from Modules.Core import logging_pyh as Logger
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.House.Family.family import FamilyModuleInformation

LOG = Logger.getLogger('PyHouse.FamilyUtils ')


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
    def get_family(p_device_obj):
        """
        @param p_device_obj: contains the info about the device we are working on.
        @return: the Family.Name which is the Name of the family (e.g. Insteon)
        """
        l_dev_name = p_device_obj.Name
        try:
            l_family = p_device_obj.Family.Name
        except AttributeError as e_err:
            l_msg = 'ERROR - Device "{}" has no Family.Name Attribute - {}'.format(l_dev_name, e_err)
            LOG.error(l_msg)
            l_family = 'Null'
        return l_family.lower()

    @staticmethod
    def _get_family_device_api(p_pyhouse_obj, p_device_obj):
        """ Get the pointer to the correct family module Api class.

        @param p_device_obj: is the device to find the Api for.
        @return: the pointer to the Api class of the proper device family
        """
        l_dev_name = p_device_obj.Name
        try:
            l_family = FamUtil.get_family(p_device_obj)
            l_family_obj = p_pyhouse_obj.House.Family[l_family]
            l_device_api = l_family_obj._Api
            LOG.info('Got Api for "{}"'.format(l_family))
        except Exception as e_err:
            l_msg = 'ERROR - Device:"{}"\n\tFamily:"{}"\n\tCannot find Api info\n\tError: {}'.format(l_dev_name, l_family, e_err)
            LOG.error(l_msg)
            l_device_api = None
        return l_device_api

#  ## END DBK
