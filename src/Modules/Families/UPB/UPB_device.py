"""
-*- test-case-name: PyHouse.src.Modules.families.UPB.test.test_UPB_device -*-

@name: PyHouse/src/Modules/families/UPB/UPB_device.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2011-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Mar 27, 2011
@summary: This module is for communicating with UPB controllers.

Load the database with UPB devices.
Start Active UPB Controllers.
    If more than one ???

"""

# Import system type stuff

# Import PyMh files
from Modules.Families.UPB import UPB_Pim, UPB_xml
from Modules.Computer import logging_pyh as Logger

g_debug = 9
LOG = Logger.getLogger('PyHouse.UPB_device  ')


class API(object):

    def _is_upb_active(self, p_controller_obj):
        if p_controller_obj.ControllerFamily != 'UPB':
            return False
        if p_controller_obj.Active:
            return True

    def __init__(self):
        """Constructor for the UPB.
        """
        pass

    def Start(self, p_pyhouse_obj):
        """For the given house, this will start all the controllers for family = UPB in that house.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        l_count = 0
        for l_controller_obj in self.m_pyhouse_obj.House.OBJs.Controllers.itervalues():
            if self._is_upb_active(l_controller_obj):
                l_controller_obj._HandlerAPI = UPB_Pim.API()
                if l_controller_obj._HandlerAPI.Start(p_pyhouse_obj, l_controller_obj):
                    LOG.info('Controller {0:} Started.'.format(l_controller_obj.Name))
                    l_count += 1
                else:
                    LOG.error('Controller {0:} failed to start.'.format(l_controller_obj.Name))
                    l_controller_obj.Active = False
        LOG.info('Started {0:} UPB Controllers.'.format(l_count))

    def Stop(self):
        try:
            for l_controller_obj in self.m_pyhouse_obj.House.OBJs.Controllers.itervalues():
                if self._is_upb_active(l_controller_obj):
                    l_controller_obj._HandlerAPI.Stop(l_controller_obj)
        except AttributeError as e_err:
            LOG.error('Stop ERROR {0:}'.format(e_err))


    def SaveXml(self, p_xml):
        return p_xml

    def ChangeLight(self, p_light_obj, p_level, _p_rate = 0):
        LOG.debug('Change light Name:{0:}, ControllerFamily:{1:}'.format(p_light_obj.Name, p_light_obj.ControllerFamily))
        _l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[p_light_obj.ControllerFamily].FamilyModuleAPI
        self.m_plm.ChangeLight(p_light_obj, p_level)

    def ReadXml(self, p_device, p_xml):
        UPB_xml.ReadXml(p_device, p_xml)

    def WriteXml(self, p_device_obj, p_entry_xml):
        UPB_xml.WriteXml(p_device_obj, p_entry_xml)

# ## END
