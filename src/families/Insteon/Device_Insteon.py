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
import logging
import xml.etree.ElementTree as ET

# Import PyMh files
#from src.lights import lighting
from src.families.Insteon import Insteon_PLM
from src.families.Insteon import Insteon_utils


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Minor routines
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.Dev_Inst')


class InsteonData (object):
    """This class contains the Insteon specific information about the various devices
    controlled by PyHouse.
    """

    def __init__(self):
        self.InsteonAddress = 0  # 3 bytes
        self.Controller = False
        self.DevCat = 0  # DevCat and SubCat (2 bytes)
        self.Family = 'Insteon'
        self.GroupList = ''
        self.GroupNumber = 0
        self.Master = False  # False is Slave
        self.ProductKey = ''
        self.Responder = False
        self.Command1 = 0
        self.Command2 = 0

    def reprJSON(self):
        print "Device_Insteon.reprJSON() {0:}".format(self.InsteonAddress)
        l_ret = super(InsteonData, self).reprJSON()  # The core data
        l_ret.update(dict(
                    InsteonAddress = self.InsteonAddress,
                    Controller = self.Controller,
                    DevCat = self.DevCat,
                    GroupList = self.GroupList,
                    GroupNumber = self.GroupNumber,
                    Master = self.Master,
                    Responder = self.Responder,
                    ProductKey = self.ProductKey
                    ))
        return l_ret


class CoreAPI(object):

    def extract_device_xml(self, p_entry_xml, p_device_obj):
        """
        @param p_entry_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        """
        if g_debug >= 3:
            print "Device_Insteon.extract_device_xml()", p_device_obj
        try:
            p_device_obj.InsteonAddress = Insteon_utils.dotted_hex2int(p_entry_xml.findtext('Address'))
        except AttributeError:
            p_device_obj.InsteonAddress = '11.22.33'
        p_device_obj.Controller = p_entry_xml.findtext('Controller')
        p_device_obj.DevCat = p_entry_xml.findtext('DevCat')
        p_device_obj.GroupList = p_entry_xml.findtext('GroupList')
        p_device_obj.GroupNumber = p_entry_xml.findtext('GroupNumber')
        p_device_obj.Master = p_entry_xml.findtext('Master')
        p_device_obj.ProductKey = p_entry_xml.findtext('ProductKey')
        p_device_obj.Responder = p_entry_xml.findtext('Responder')
        return p_device_obj

    def insert_device_xml(self, p_entry_xml, p_device_obj):
        if g_debug >= 3:
            print "Device_Insteon.insert_device_xml()", p_device_obj
        ET.SubElement(p_entry_xml, 'Address').text = Insteon_utils.int2dotted_hex(p_device_obj.InsteonAddress)
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

    def change_light_setting(self, p_light_obj, p_level, p_house_obj):
        if g_debug >= 3:
            print "Device_Insteon.change_light_setting()", p_level,
            print "    Light:", p_light_obj
            print "    House:", p_house_obj
        if p_light_obj.Family == 'Insteon':
            try:
                for l_controller_obj in self.m_house_obj.Controllers.itervalues():
                    if l_controller_obj.Family != 'Insteon':
                        continue
                    if l_controller_obj.Active != True:
                        continue
                    l_controller_obj.HandlerAPI.change_light_setting(p_light_obj, p_level)
            except AttributeError:
                pass  # no controllers for house(House is being added)


class API(LightingAPI):
    """
    """

    def __init__(self, p_house_obj):
        if g_debug >= 2:
            print "Device_Insteon.API()", p_house_obj
        self.m_house_obj = p_house_obj
        g_logger.info('Initialized.')


    def Start(self, p_house_obj):
        """For the given house, this will start all the controllers for family = Insteon in that house.
        """
        if g_debug >= 2:
            print "Device_Insteon.API.Start() - House:{0:}".format(p_house_obj.Name), p_house_obj
        g_logger.info('Starting.')
        l_count = 0
        for l_controller_obj in p_house_obj.Controllers.itervalues():
            if g_debug >= 3:
                print "Device_Insteon.Start() - House:{0:}, Controller:{1:}".format(p_house_obj.Name, l_controller_obj.Name)
            if l_controller_obj.Family != 'Insteon':
                if g_debug >= 3:
                    print "Device_Insteon.Start() - Skipping, Family:{0:}".format(l_controller_obj.Family)
                continue
            if l_controller_obj.Active != True:
                if g_debug >= 2:
                    print "Device_Insteon.Start() - Skipping, Active:{0:}".format(l_controller_obj.Active)
                continue
            if g_debug >= 4:
                print "Device_Insteon.Start() - trying."
            # Only one controller may be active at a time (for now).
            # But all controllers need to be processed so they may be written back to XML.
            if l_count > 0:
                if g_debug >= 4:
                    print "Device_Insteon.Start() - Skipping - another controller is already active."
                l_controller_obj.Active = False
                continue
            else:
                l_controller_obj.HandlerAPI = Insteon_PLM.API(p_house_obj)
                if l_controller_obj.HandlerAPI.Start(l_controller_obj):
                    l_count += 1
                    if g_debug >= 2:
                        print "Device_Insteon.Start() - Started - House:{0:}, Controller:{1:}".format(p_house_obj.Name, l_controller_obj.Name)
                else:
                    if g_debug >= 2:
                        print "Device_Insteon.Start() - Did NOT start- House:{0:}, Controller:{1:}".format(p_house_obj.Name, l_controller_obj.Name)
                    l_controller_obj.Active = False
        l_msg = 'Started {0:} Controllers, House:{1:}.'.format(l_count, p_house_obj.Name)
        if g_debug >= 2:
            print "Device_Insteon.Start() - {0:}".format(l_msg)
        g_logger.info(l_msg)

    def Stop(self, p_xml):
        if g_debug >= 2:
            print "Device_Insteon.API.Stop()"
        try:
            for l_controller_obj in self.m_house_obj.Controllers.itervalues():
                if l_controller_obj.Family != 'Insteon':
                    continue
                if l_controller_obj.Active != True:
                    continue
                l_controller_obj.HandlerAPI.Stop(l_controller_obj)
        except AttributeError:
            pass  # no controllers for house(House is being added)
        return p_xml

# ## END DBK
