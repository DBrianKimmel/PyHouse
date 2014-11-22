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
This is because the things we wish to automate all have some controller that
speaks to that class of device.

"""

# Import system type stuff

# Import PyHouse files
from Modules.Computer import logging_pyh as Logger

# Import PyMh files and modules.
from Modules.Utilities.tools import PrettyPrintAny



g_debug = 0
LOG = Logger.getLogger('PyHouse.FamilyUtils ')



class FamUtil(object):

    @staticmethod
    def get_family(p_device_obj):
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
            l_api = p_pyhouse_obj.House.OBJs.FamilyData[l_family].FamilyModuleAPI
        except:
            l_msg = 'ERROR - Device:"{}"; Family:"{}" Cannot find API info '.format(p_device_obj.Name, l_family)
            LOG.error(l_msg)
            print(l_msg)
            l_api = None
        return l_api

    def read_family_data(self, p_pyhouse_obj, p_device_obj, p_xml):
        l_api = FamUtil.get_family_api(p_pyhouse_obj, p_device_obj)
        # print('Family_utils Api: {}'.format(l_api))
        try:
            l_ret = l_api.ReadXml(p_device_obj, p_xml)
            # PrettyPrintAny(l_ret, 'Family_utils - line 64')
        except Exception as e_err:
            l_ret = 'ERROR in family_utils.read_family_data.  Device:"{}"  - {}'.format(p_device_obj.Name, e_err)
            LOG.error(l_ret)
            print(l_ret)
        return l_ret  # for testing

    def write_family_data(self, p_pyhouse_obj, p_out_xml, p_device):
        l_api = FamUtil.get_family_api(p_pyhouse_obj, p_device)
        try:
            l_ret = l_api.WriteXml(p_out_xml, p_device)
        except Exception as e_err:
            l_ret = 'ERROR in family_utils.write_family_data.  Device:"{}"  - {}'.format(p_device.Name, e_err)
            LOG.error(l_ret)
            print(l_ret)
        return l_ret  # for testing

# ## END DBK
