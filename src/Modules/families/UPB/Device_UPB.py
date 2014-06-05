#!/usr/bin/python

"""Load the database with UPB devices.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import LightData
from Modules.lights import lighting
from Modules.utils import pyh_log


g_debug = 0

LOG = pyh_log.getLogger('PyHouse.Device_UPB  ')


class LightingAPI(lighting.LightingAPI):
    """Interface to the lights of this module.
    """

    def extract_device_xml(self, p_device_obj, p_entry_xml):
        """
        @param p_entry_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        """
        p_device_obj.NetworkID = p_entry_xml.findtext('NetworkID')
        p_device_obj.Password = p_entry_xml.findtext('Password')
        p_device_obj.UnitID = p_entry_xml.findtext('UnitID')
        return p_device_obj

    def insert_device_xml(self, p_entry_xml, p_device_obj):
        try:
            ET.SubElement(p_entry_xml, 'NetworkID').text = self.put_str(p_device_obj.NetworkID)
            ET.SubElement(p_entry_xml, 'Password').text = str(p_device_obj.Password)
            ET.SubElement(p_entry_xml, 'UnitID').text = str(p_device_obj.UnitID)
        except AttributeError:
            pass


class LoadSaveInsteonData(LightingAPI): pass

import UPB_Pim


class API(LightingAPI):

    def __init__(self):
        """Constructor for the UPB.
        """
        pass

    def Start(self, p_house_obj):
        """For the given house, this will start all the controllers for family = UPB in that house.
        """
        self.m_house_obj = p_house_obj
        l_count = 0
        for l_controller_obj in self.m_house_obj.Controllers.itervalues():
            if l_controller_obj.Family != 'UPB':
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
                # from Modules.families.Insteon import Insteon_PLM
                l_controller_obj._HandlerAPI = UPB_Pim.API(p_house_obj)
                if l_controller_obj._HandlerAPI.Start(l_controller_obj):
                    l_count += 1
                else:
                    LOG.error('Controller {0:} failed to start.'.format(l_controller_obj.Name))
                    l_controller_obj.Active = False
        l_msg = 'Started {0:} UPB Controllers, House:{1:}.'.format(l_count, p_house_obj.Name)
        LOG.info(l_msg)

    def Stop(self, p_xml):
        try:
            for l_controller_obj in self.m_house_obj.Controllers.itervalues():
                if l_controller_obj.Family != 'UPB':
                    continue
                if l_controller_obj.Active != True:
                    continue
                l_controller_obj._HandlerAPI.Stop(l_controller_obj)
        except AttributeError:
            pass  # no controllers for house (House is being added)
        return p_xml

    def ChangeLight(self, p_light_obj, p_level, _p_rate = 0):
        try:
            for l_controller_obj in self.m_house_obj.Controllers.itervalues():
                if (l_controller_obj.Family == 'UPB') and (l_controller_obj.Active == True):
                    l_controller_obj._HandlerAPI.ChangeLight(p_light_obj, p_level)
        except AttributeError:
            pass

# ## END
