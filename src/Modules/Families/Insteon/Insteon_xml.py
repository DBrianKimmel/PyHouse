"""
-*- test-case-name: PyHouse.src.Modules.Families.Insteon.test.test_Insteon_xml -*-

@name: PyHouse/src/Modules/Families/Insteon/Insteon_xml.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2011-2014 by D. Brian Kimmel
@note: Created on Apr 3, 2011
@license: MIT License
@summary: This module is for Insteon

This is the main module for the Insteon family of devices.
it provides the single interface into the family.
Several other Insteon modules are included by this and are invisible to the other families.

This module loads the information about all the Insteon devices.

InsteonControllers
serial_port

"""

# Import system type stuff

# Import PyMh files
from Modules.Families.Insteon.Insteon_data import InsteonData
from Modules.Core import conversions
from Modules.Utilities import xml_tools
from Modules.Computer import logging_pyh as Logger

g_debug = 0
LOG = Logger.getLogger('PyHouse.Insteon_xml ')


class ReadWriteConfigXml(xml_tools.XmlConfigTools):
    """
    These routines are called from read_family_data in various modules.
    This is done so Lights, Thermostats, Irrigation and Pool devices can use the XML data for Insteon devices.

    This class and methods are pointed to by family.py and must be the same in every Device package.
    """

    def _read_product_key(self, p_entry_xml, p_default = '98.76.54'):
        l_ret = p_default
        try:
            l_prod = self.get_text_from_xml(p_entry_xml, 'ProductKey', p_default)
            # print('Insteon_xml - _read_product_key = {0:}'.format(l_prod))
            l_ret = conversions.dotted_hex2int(l_prod)
        except Exception:
            l_ret.ProductKey = p_default
        return l_ret

    def ReadXml(self, p_device_obj, p_entry_xml):
        """
        A method to extract Insteon specific elements and insert them into a basic device object.

        We do this to keep the Insteon Data encapsulated.

        @param p_entry_xml: is the device's XML element
        @param p_device_obj : is the Basic Object that will have the extracted elements inserted into.
        @return: a dict of the extracted Insteon Specific data.
        """
        l_insteon_obj = InsteonData()
        l_insteon_obj.InsteonAddress = conversions.dotted_hex2int(self.get_text_from_xml(p_entry_xml, 'Address', '99.88.77'))
        l_insteon_obj.DevCat = conversions.dotted_hex2int(self.get_text_from_xml(p_entry_xml, 'DevCat', 'A1.B2'))
        l_insteon_obj.GroupList = self.get_text_from_xml(p_entry_xml, 'GroupList')
        l_insteon_obj.GroupNumber = self.get_int_from_xml(p_entry_xml, 'GroupNumber', 0)
        l_insteon_obj.IsController = self.get_bool_from_xml(p_entry_xml, 'IsController')
        l_insteon_obj.IsMaster = self.get_bool_from_xml(p_entry_xml, 'IsMaster')
        l_insteon_obj.IsResponder = self.get_bool_from_xml(p_entry_xml, 'IsResponder')
        l_insteon_obj.ProductKey = self._read_product_key(p_entry_xml)
        xml_tools.stuff_new_attrs(p_device_obj, l_insteon_obj)
        return l_insteon_obj

    def WriteXml(self, p_entry_xml, p_device_obj):
        if g_debug >= 1:
            LOG.info('Insteon Write {}'.format(p_device_obj.Name))
        self.put_text_element(p_entry_xml, 'Address', conversions.int2dotted_hex(p_device_obj.InsteonAddress, 3))
        self.put_int_element(p_entry_xml, 'DevCat', conversions.int2dotted_hex(p_device_obj.DevCat, 2))
        self.put_text_element(p_entry_xml, 'GroupList', p_device_obj.GroupList)
        self.put_int_element(p_entry_xml, 'GroupNumber', p_device_obj.GroupNumber)
        self.put_bool_element(p_entry_xml, 'IsController', p_device_obj.IsController)
        self.put_bool_element(p_entry_xml, 'IsMaster', p_device_obj.IsMaster)
        self.put_bool_element(p_entry_xml, 'IsResponder', p_device_obj.IsResponder)
        self.put_text_element(p_entry_xml, 'ProductKey', conversions.int2dotted_hex(p_device_obj.ProductKey, 3))

# ## END DBK
