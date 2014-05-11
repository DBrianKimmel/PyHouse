#!/usr/bin/python

"""Insteon Device module.

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
from Modules.lights import lighting
from Modules.families.Insteon import Insteon_utils
from Modules.utils import xml_tools
from Modules.utils import pyh_log
#
# from Modules.utils.tools import PrintObject


g_debug = 1
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Minor routines
# + = NOT USED HERE
LOG = pyh_log.getLogger('PyHouse.Dev_Insteon ')


class InsteonData (lighting.LightData):
    """This class contains the Insteon specific information about the various devices
    controlled by PyHouse.
    """

    def __init__(self):
        super(InsteonData, self).__init__()
        self.InsteonAddress = 0  # 3 bytes
        self.Controller = False
        self.DevCat = 0  # DevCat and SubCat (2 bytes)
        self.Family = 'Insteon'
        self.GroupList = ''
        self.GroupNumber = 0
        self.Master = False  # False is Slave
        self.ProductKey = ''
        self.Responder = False

    def reprJSON(self, p_ret):
        """Device_Insteon.
        """
        p_ret.update(dict(
            InsteonAddress = Insteon_utils.int2dotted_hex(self.InsteonAddress),
            Controller = self.Controller,
            DevCat = self.DevCat,
            GroupList = self.GroupList,
            GroupNumber = self.GroupNumber,
            Master = self.Master,
            Responder = self.Responder,
            ProductKey = self.ProductKey
            ))
        return p_ret


class CoreAPI(xml_tools.ConfigTools):

    def extract_device_xml(self, p_entry_xml, p_device_obj):
        """
        @param p_entry_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
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

    def __init__(self, p_house_obj):
        self.m_house_obj = p_house_obj

    def Start(self, p_house_obj):
        """For the given house, this will start all the controllers for family = Insteon in that house.
        """
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
