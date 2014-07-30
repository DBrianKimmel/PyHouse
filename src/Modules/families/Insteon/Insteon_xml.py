"""
Created on Jul 29, 2014

-*- test-case-name: PyHouse.src.Modules.families.Insteon.test.test_Device_Insteon -*-

@name: PyHouse/src/Modules/families/Insteon/Device_Insteon.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
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
from Modules.Core.data_objects import InsteonData
from Modules.Core import conversions
from Modules.utils import xml_tools
from Modules.utils import pyh_log
# from Modules.utils.tools import PrettyPrintAny

g_debug = 1
LOG = pyh_log.getLogger('PyHouse.Dev_Insteon ')


class ReadWriteConfigXml(xml_tools.XmlConfigTools):
    """
    These routines are called from read_family_data in various modules.
    This is done so Lights, Thermostats, Irrigation and Pool devices can use the XML data for Insteon devices.

    This class and methods are pointed to by family.py and must be the same in every Device package.
    """

    def extract_device_xml(self, p_device_obj, p_entry_xml):
        """
        A method to extract Insteon specific elements and insert them into a basic device object.

        @param p_entry_xml: is the device's XML element
        @param p_device_obj : is the Basic Object that will have the extracted elements inserted into.
        @return: a dict of the extracted Insteon Specific data.
        """
        # PrettyPrintAny(p_entry_xml, 'DeviceInsteon extract  XML', 120)
        l_insteon_obj = InsteonData()
        l_insteon_obj.InsteonAddress = conversions.dotted_hex2int(self.get_text_from_xml(p_entry_xml, 'Address', '77.88.99'))
        l_insteon_obj.DevCat = conversions.dotted_hex2int(self.get_text_from_xml(p_entry_xml, 'DevCat', 'A1.B2'))
        l_insteon_obj.GroupList = self.get_text_from_xml(p_entry_xml, 'GroupList')
        l_insteon_obj.GroupNumber = self.get_int_from_xml(p_entry_xml, 'GroupNumber', 0)
        l_insteon_obj.IsController = self.get_bool_from_xml(p_entry_xml, 'IsController')
        l_insteon_obj.IsMaster = self.get_bool_from_xml(p_entry_xml, 'IsMaster')
        l_insteon_obj.IsResponder = self.get_bool_from_xml(p_entry_xml, 'IsResponder')
        try:
            l_insteon_obj.ProductKey = conversions.dotted_hex2int(self.get_text_from_xml(p_entry_xml, 'ProductKey', '98.76.54'))
        except Exception:
            l_insteon_obj.ProductKey = 0
        xml_tools.stuff_new_attrs(p_device_obj, l_insteon_obj)
        return l_insteon_obj

    def insert_device_xml(self, p_entry_xml, p_device_obj):
        if g_debug >= 1:
            LOG.debug('Insteon Write {0:}'.format(p_device_obj.Name))
        self.put_text_element(p_entry_xml, 'Address', conversions.int2dotted_hex(p_device_obj.InsteonAddress, 3))
        self.put_int_element(p_entry_xml, 'DevCat', conversions.int2dotted_hex(p_device_obj.DevCat, 2))
        self.put_text_element(p_entry_xml, 'GroupList', p_device_obj.GroupList)
        self.put_int_element(p_entry_xml, 'GroupNumber', p_device_obj.GroupNumber)
        self.put_bool_element(p_entry_xml, 'IsController', p_device_obj.IsController)
        self.put_bool_element(p_entry_xml, 'IsMaster', p_device_obj.IsMaster)
        self.put_bool_element(p_entry_xml, 'IsResponder', p_device_obj.IsResponder)
        self.put_text_element(p_entry_xml, 'ProductKey', conversions.int2dotted_hex(p_device_obj.ProductKey, 3))

# ## END DBK
