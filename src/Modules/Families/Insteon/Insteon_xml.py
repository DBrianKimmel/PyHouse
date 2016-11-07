"""
-*- test-case-name: PyHouse.src.Modules.Families.Insteon.test.test_Insteon_xml -*-

@name:      PyHouse/src/Modules/Families/Insteon/Insteon_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2016 by D. Brian Kimmel
@note:      Created on Apr 3, 2011
@license:   MIT License
@summary:   This module is for Insteon

This module merges the Insteon specific information (InsteonData) with the generic controllerI Information (ControllerData)
 giving an expanded ControllerData.
"""

__updated__ = '2016-11-05'

#  Import system type stuff

#  Import PyMh files
from Modules.Computer import logging_pyh as Logger
from Modules.Core import conversions
from Modules.Families.Insteon.Insteon_data import InsteonData
from Modules.Utilities.xml_tools import PutGetXML, stuff_new_attrs

LOG = Logger.getLogger('PyHouse.Insteon_xml ')


class Xml(object):
    """
    These routines are called from read_family_data in various modules.
    This is done so Lights, Thermostats, Irrigation and Pool devices can use the XML data for Insteon devices.

    This class and methods are pointed to by family.py and must be the same in every Device package.
    """

    @staticmethod
    def _read_product_key(p_entry_xml, p_default='98.76.54'):
        l_ret = p_default
        try:
            l_prod = PutGetXML.get_text_from_xml(p_entry_xml, 'ProductKey', p_default)
            l_ret = conversions.dotted_hex2int(l_prod)
        except Exception:
            l_ret.ProductKey = p_default
        return l_ret

    @staticmethod
    def _read_insteon(p_in_xml):
        l_insteon_obj = InsteonData()
        l_insteon_obj.ProductKey = Xml._read_product_key(p_in_xml)
        try:
            l_insteon_obj.InsteonAddress = conversions.dotted_hex2int(PutGetXML.get_text_from_xml(p_in_xml, 'InsteonAddress', '99.88.77'))
        except AttributeError:
            l_insteon_obj.InsteonAddress = conversions.dotted_hex2int(PutGetXML.get_text_from_xml(p_in_xml, 'Address', '99.88.66'))
        try:
            l_insteon_obj.DevCat = conversions.dotted_hex2int(PutGetXML.get_text_from_xml(p_in_xml, 'DevCat', 'A1.B2'))
            l_insteon_obj.GroupList = PutGetXML.get_text_from_xml(p_in_xml, 'GroupList')
            l_insteon_obj.GroupNumber = PutGetXML.get_int_from_xml(p_in_xml, 'GroupNumber', 0)
        except Exception as e_err:
            l_insteon_obj.GroupList = 'Error reading Insteon Group List.'
            LOG.error('ERROR: {}'.format(e_err))
        try:
            l_insteon_obj.EngineVersion = PutGetXML.get_int_from_xml(p_in_xml, 'EngineVersion', 1)
        except Exception as e_err:
            LOG.error('ERROR: {}'.format(e_err))
            l_insteon_obj.EngineVersion = 2
        try:
            l_insteon_obj.FirmwareVersion = PutGetXML.get_int_from_xml(p_in_xml, 'FirmwareVersion', 1)
        except Exception as e_err:
            LOG.error('ERROR: {}'.format(e_err))
            l_insteon_obj.FirmwareVersion = 2
        return l_insteon_obj

    @staticmethod
    def ReadXml(p_device_obj, p_in_xml):
        """
        A method to extract Insteon specific elements and insert them into an Insteon data object.

        We do this to keep the Insteon Data encapsulated.

        @param p_in_xml: is the device's XML element
        @param p_device_obj : is the Basic Object that will have the extracted elements inserted into.
        @return: a dict of the extracted Insteon Specific data.
        """
        l_insteon_obj = Xml._read_insteon(p_in_xml)
        stuff_new_attrs(p_device_obj, l_insteon_obj)
        return p_device_obj  # For testing only

    @staticmethod
    def WriteXml(p_out_xml, p_device):
        """
        @param p_xml_out: is a parent element to which the Insteon Specific information is appended.
        """
        PutGetXML.put_int_element(p_out_xml, 'DevCat', conversions.int2dotted_hex(p_device.DevCat, 2))
        PutGetXML.put_int_element(p_out_xml, 'EngineVersion', p_device.EngineVersion)
        PutGetXML.put_int_element(p_out_xml, 'FirmwareVersion', p_device.FirmwareVersion)
        PutGetXML.put_text_element(p_out_xml, 'GroupList', p_device.GroupList)
        PutGetXML.put_int_element(p_out_xml, 'GroupNumber', p_device.GroupNumber)
        PutGetXML.put_text_element(p_out_xml, 'InsteonAddress', conversions.int2dotted_hex(p_device.InsteonAddress, 3))
        PutGetXML.put_text_element(p_out_xml, 'ProductKey', conversions.int2dotted_hex(p_device.ProductKey, 3))
        return p_out_xml

#  ## END DBK
