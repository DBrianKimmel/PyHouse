"""
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
from Modules.families.Insteon import Insteon_utils
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
        l_insteon_obj = InsteonData()
        l_insteon_obj.InsteonAddress = Insteon_utils.dotted_hex2int(self.get_text_from_xml(p_entry_xml, 'Address', '88.88.88'))
        l_insteon_obj.DevCat = self.get_int_from_xml(p_entry_xml, 'DevCat')
        l_insteon_obj.GroupList = self.get_text_from_xml(p_entry_xml, 'GroupList')
        l_insteon_obj.GroupNumber = self.get_int_from_xml(p_entry_xml, 'GroupNumber')
        l_insteon_obj.IsController = self.get_bool_from_xml(p_entry_xml, 'IsController')
        l_insteon_obj.IsMaster = self.get_bool_from_xml(p_entry_xml, 'IsMaster')
        l_insteon_obj.IsResponder = self.get_bool_from_xml(p_entry_xml, 'IsResponder')
        l_insteon_obj.ProductKey = self.get_text_from_xml(p_entry_xml, 'ProductKey')
        xml_tools.stuff_new_attrs(p_device_obj, l_insteon_obj)
        return l_insteon_obj

    def insert_device_xml(self, p_entry_xml, p_device_obj):
        self.put_text_element(p_entry_xml, 'Address', Insteon_utils.int2dotted_hex(int(p_device_obj.InsteonAddress)))
        self.put_int_element(p_entry_xml, 'DevCat', p_device_obj.DevCat)
        self.put_text_element(p_entry_xml, 'GroupList', p_device_obj.GroupList)
        self.put_int_element(p_entry_xml, 'GroupNumber', p_device_obj.GroupNumber)
        self.put_bool_element(p_entry_xml, 'IsController', p_device_obj.IsController)
        self.put_bool_element(p_entry_xml, 'IsMaster', p_device_obj.IsMaster)
        self.put_bool_element(p_entry_xml, 'IsResoonder', p_device_obj.IsResponder)
        self.put_text_element(p_entry_xml, 'ProductKey', p_device_obj.ProductKey)


class API(ReadWriteConfigXml):
    """
    """

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj):
        """
        This will start all the controllers for family = Insteon in the house.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_house_obj = p_pyhouse_obj.House.OBJs
        l_count = 0
        for l_controller_obj in p_pyhouse_obj.House.OBJs.Controllers.itervalues():
            if l_controller_obj.ControllerFamily != 'Insteon':
                continue
            if l_controller_obj.Active != True:
                continue
            # Only one controller may be active at a time (for now).
            # But all controllers need to be processed so they may be written back to XML.
            if l_count > 0:
                l_controller_obj.Active = False
                LOG.warning('Controller {0:} skipped - another one is active.'.format(l_controller_obj.Name))
                continue
            else:
                from Modules.families.Insteon import Insteon_PLM
                self.m_plm = l_controller_obj._HandlerAPI = Insteon_PLM.API()
                if l_controller_obj._HandlerAPI.Start(p_pyhouse_obj, l_controller_obj):
                    l_count += 1
                else:
                    LOG.error('Controller {0:} failed to start.'.format(l_controller_obj.Name))
                    l_controller_obj.Active = False
        l_msg = 'Started {0:} Insteon Controllers, House:{1:}.'.format(l_count, p_pyhouse_obj.House.Name)
        LOG.info(l_msg)

    def Stop(self, p_xml):
        try:
            for l_controller_obj in self.m_house_obj.Controllers.itervalues():
                if l_controller_obj.ControllerFamily != 'Insteon':
                    continue
                if l_controller_obj.Active != True:
                    continue
                l_controller_obj._HandlerAPI.Stop(l_controller_obj)
        except AttributeError as e_err:
            LOG.warning('Stop Warning - {0:}'.format(e_err))  # no controllers for house(House is being added)
        return p_xml

    def ChangeLight(self, p_light_obj, p_level, _p_rate = 0):
        """
        Do the Insteon thing to change the level of an Insteon light
        """
        if g_debug >= 1:
            LOG.debug('Change light Name:{0:}, ControllerFamily:{1:}'.format(p_light_obj.Name, p_light_obj.ControllerFamily))
        _l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[p_light_obj.ControllerFamily].ModuleAPI
        self.m_plm.ChangeLight(p_light_obj, p_level)

# ## END DBK
