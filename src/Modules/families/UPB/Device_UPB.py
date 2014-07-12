#!/usr/bin/python

"""Load the database with UPB devices.
"""

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import UPBData
from Modules.utils import xml_tools
from Modules.utils import pyh_log

g_debug = 9
LOG = pyh_log.getLogger('PyHouse.Device_UPB  ')


class ReadWriteXml(xml_tools.XmlConfigTools):
    """Interface to the lights of this module.
    """

    def extract_device_xml(self, p_device_obj, p_entry_xml):
        """
        @param p_entry_xml: is the e-tree XML house object
        @param p_house: is the text name of the House.
        @return: a dict of the entry to be attached to a house object.
        """
        l_obj = UPBData()
        l_obj.UPBAddress = self.get_int_from_xml(p_entry_xml, 'Address', 255)
        l_obj.UPBNetworkID = self.get_int_from_xml(p_entry_xml, 'UPBNetworkID')
        l_obj.UPBPassword = self.get_int_from_xml(p_entry_xml, 'UPBPassword')
        xml_tools.stuff_new_attrs(p_device_obj, l_obj)
        return p_device_obj

    def insert_device_xml(self, p_entry_xml, p_device_obj):
        try:
            self.put_int_element(p_entry_xml, 'UPBAddress', p_device_obj.UPBAddress)
            self.put_int_element(p_entry_xml, 'UPBNetworkID', p_device_obj.UPBNetworkID)
            self.put_int_element(p_entry_xml, 'UPBPassword', p_device_obj.UPBPassword)
        except AttributeError as e_err:
            LOG.error('InsertDeviceXML ERROR {0:}'.format(e_err))


import UPB_Pim


class API(ReadWriteXml):

    def __init__(self):
        """Constructor for the UPB.
        """
        pass

    def Start(self, p_pyhouse_obj):
        """For the given house, this will start all the controllers for family = UPB in that house.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_house_obj = p_pyhouse_obj.House.OBJs
        l_count = 0
        for l_controller_obj in self.m_house_obj.Controllers.itervalues():
            if l_controller_obj.ControllerFamily != 'UPB':
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
                l_controller_obj._HandlerAPI = UPB_Pim.API()
                if l_controller_obj._HandlerAPI.Start(p_pyhouse_obj, l_controller_obj):
                    l_count += 1
                else:
                    LOG.error('Controller {0:} failed to start.'.format(l_controller_obj.Name))
                    l_controller_obj.Active = False
        l_msg = 'Started {0:} UPB Controllers, House:{1:}.'.format(l_count, p_pyhouse_obj.House.Name)
        LOG.info(l_msg)

    def Stop(self, p_xml):
        try:
            for l_controller_obj in self.m_house_obj.Controllers.itervalues():
                if l_controller_obj.ControllerFamily != 'UPB':
                    continue
                if l_controller_obj.Active != True:
                    continue
                l_controller_obj._HandlerAPI.Stop(l_controller_obj)
        except AttributeError as e_err:
            LOG.error('Stop ERROR {0:}'.format(e_err))
            pass  # no controllers for house (House is being added)
        return p_xml

    def ChangeLight(self, p_light_obj, p_level, _p_rate = 0):
        if g_debug >= 1:
            LOG.debug('Change light Name:{0:}, ControllerFamily:{1:}'.format(p_light_obj.Name, p_light_obj.ControllerFamily))
        _l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[p_light_obj.ControllerFamily].ModuleAPI
        self.m_plm.ChangeLight(p_light_obj, p_level)

# ## END
