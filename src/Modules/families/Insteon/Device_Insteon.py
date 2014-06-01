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
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import InsteonData
from Modules.families.Insteon import Insteon_utils
from Modules.utils import xml_tools
from Modules.utils import pyh_log

g_debug = 1
LOG = pyh_log.getLogger('PyHouse.Dev_Insteon ')


class CoreAPI(xml_tools.ConfigTools):

    def extract_device_xml(self, p_entry_xml, p_device_obj):
        """
        A method to extract Insteon specific elements and insert them into a basic device object.

        @param p_entry_xml: is the device's XML element
        @param p_device_obj : is the Basic Object that will have the extracted elements inserted into.
        @return: a dict of the extracted Insteon Specific data.
        """
        l_insteon_obj = InsteonData()
        l_insteon_obj.InsteonAddress = Insteon_utils.dotted_hex2int(p_entry_xml.findtext('Address', default = 0))
        l_insteon_obj.Controller = p_entry_xml.findtext('Controller')
        l_insteon_obj.DevCat = p_entry_xml.findtext('DevCat')
        l_insteon_obj.GroupList = p_entry_xml.findtext('GroupList')
        l_insteon_obj.GroupNumber = p_entry_xml.findtext('GroupNumber')
        l_insteon_obj.Master = p_entry_xml.findtext('Master')
        l_insteon_obj.ProductKey = p_entry_xml.findtext('ProductKey')
        l_insteon_obj.Responder = p_entry_xml.findtext('Responder')
        xml_tools.stuff_new_attrs(p_device_obj, l_insteon_obj)
        return l_insteon_obj

    def insert_device_xml(self, p_entry_xml, p_device_obj):
        ET.SubElement(p_entry_xml, 'Address').text = Insteon_utils.int2dotted_hex(int(p_device_obj.InsteonAddress))
        ET.SubElement(p_entry_xml, 'Controller').text = self.put_bool(p_device_obj.Controller)
        ET.SubElement(p_entry_xml, 'DevCat').text = str(p_device_obj.DevCat)
        ET.SubElement(p_entry_xml, 'GroupList').text = str(p_device_obj.GroupList)
        ET.SubElement(p_entry_xml, 'GroupNumber').text = str(p_device_obj.GroupNumber)
        ET.SubElement(p_entry_xml, 'Master').text = str(p_device_obj.Master)
        ET.SubElement(p_entry_xml, 'ProductKey').text = str(p_device_obj.ProductKey)
        ET.SubElement(p_entry_xml, 'Responder').text = self.put_bool(p_device_obj.Responder)


class LightingAPI(CoreAPI):
    """Interface to the lights of this module.
    """

    def XXchange_light_setting(self, p_light_obj, p_level, p_house_obj):
        if p_light_obj.Family == 'Insteon':
            try:
                for l_controller_obj in self.m_house_obj.Controllers.itervalues():
                    if l_controller_obj.Family != 'Insteon':
                        continue
                    if l_controller_obj.Active != True:
                        continue
                    l_controller_obj._HandlerAPI.change_light_setting(p_light_obj, p_level)
            except AttributeError:
                pass  # no controllers for house(House is being added)


class API(LightingAPI):
    """
    """

    def __init__(self):
        # self.m_house_obj = p_house_obj
        pass

    def Start(self, p_house_obj):
        """For the given house, this will start all the controllers for family = Insteon in that house.
        """
        self.m_house_obj = p_house_obj
        l_count = 0
        for l_controller_obj in p_house_obj.Controllers.itervalues():
            if l_controller_obj.Family != 'Insteon':
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
                l_controller_obj._HandlerAPI = Insteon_PLM.API(p_house_obj)
                if l_controller_obj._HandlerAPI.Start(l_controller_obj):
                    l_count += 1
                else:
                    LOG.error('Controller {0:} failed to start.'.format(l_controller_obj.Name))
                    l_controller_obj.Active = False
        l_msg = 'Started {0:} Insteon Controllers, House:{1:}.'.format(l_count, p_house_obj.Name)
        LOG.info(l_msg)

    def Stop(self, p_xml):
        try:
            for l_controller_obj in self.m_house_obj.Controllers.itervalues():
                if l_controller_obj.Family != 'Insteon':
                    continue
                if l_controller_obj.Active != True:
                    continue
                l_controller_obj._HandlerAPI.Stop(l_controller_obj)
        except AttributeError:
            pass  # no controllers for house(House is being added)
        return p_xml

    def ChangeLight(self, p_light_obj, p_level, _p_rate = 0):
        if g_debug >= 1:
            LOG.debug('Change light Name:{0:}, Family:{1:}'.format(p_light_obj.Name, p_light_obj.Family))
        if p_light_obj.Family == 'Insteon':
            try:
                for l_controller_obj in self.m_house_obj.Controllers.itervalues():
                    if l_controller_obj.Family != 'Insteon':
                        continue
                    if l_controller_obj.Active != True:
                        continue
                    l_controller_obj._HandlerAPI.ChangeLight(p_light_obj, p_level)
            except AttributeError as e:  # no controllers for house. (House is being added).
                LOG.warning('Could not change light setting {0:}'.format(e))

# ## END DBK
