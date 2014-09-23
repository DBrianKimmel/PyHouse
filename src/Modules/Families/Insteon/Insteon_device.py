"""
-*- test-case-name: PyHouse.src.Modules.families.Insteon.test.test_Insteon_device -*-

@name: PyHouse/src/Modules/families/Insteon/Insteon_device.py
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
from Modules.Families.Insteon import Insteon_xml
from Modules.Computer import logging_pyh as Logger
# from Modules.Utilities.tools import PrettyPrintAny

g_debug = 1
LOG = Logger.getLogger('PyHouse.Dev_Insteon ')


class Utility(object):
    """
    """

    def _is_insteon(self, p_obj):
        try:
            return p_obj.ControllerFamily == 'Insteon'
        except AttributeError:
            return False

    def _is_active(self, p_obj):
        try:
            return p_obj.Active == True
        except AttributeError:
            return False

    def _is_valid_controller(self, p_controller_obj):
        return self._is_insteon(p_controller_obj) and self._is_active(p_controller_obj)

    def _start_plm(self, p_pyhouse_obj, p_controller_obj):
        """
        import PLM module when we run this otherwise we will get a circular import
        """
        from Modules.Families.Insteon import Insteon_PLM
        l_plmAPI = Insteon_PLM.API()
        p_controller_obj._HandlerAPI = l_plmAPI
        if l_plmAPI.Start(p_pyhouse_obj, p_controller_obj):
            LOG.info('Successfully started Insteon controller {0:}'.format(p_controller_obj.Name))
            return l_plmAPI
        else:
            LOG.error('Controller {0:} failed to start.'.format(p_controller_obj.Name))
            p_controller_obj.Active = False
            return None

    def _start_all_controllers(self, p_pyhouse_obj):
        l_ret = None
        for l_controller_obj in p_pyhouse_obj.House.OBJs.Controllers.itervalues():
            if self._is_valid_controller(l_controller_obj):
                l_ret = self._start_plm(p_pyhouse_obj, l_controller_obj)
        return l_ret

    def _stop_all_controllers(self, p_pyhouse_obj):
        for l_controller_obj in p_pyhouse_obj.House.OBJs.Controllers.itervalues():
            if self._is_valid_controller(l_controller_obj):
                l_controller_obj._HandlerAPI.Stop(l_controller_obj)


class API(Utility):
    """
    These are the public methods available to use Insteon devices.
    """

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj):
        """
        This will start all the controllers for family = Insteon in the house.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_plm = self._start_all_controllers(p_pyhouse_obj)
        LOG.info('Started the Insteon Controllers.')

    def Stop(self):
        try:
            self._stop_all_controllers(self.m_pyhouse_obj)
        except AttributeError as e_err:
            LOG.warning('Stop Warning - {0:}'.format(e_err))  # no controllers for house(House is being added)

    def SaveXml(self, p_xml):
        return p_xml

    def ChangeLight(self, p_light_obj, p_level, _p_rate = 0):
        """
        Do the Insteon thing to change the level of an Insteon light
        """
        # if g_debug >= 1:
        LOG.debug('Change light Name:{0:}, ControllerFamily:{1:}'.format(p_light_obj.Name, p_light_obj.ControllerFamily))
        self.m_plm.ChangeLight(p_light_obj, p_level)

    def ReadXml(self, p_device_obj, p_entry_xml):
        # print('Insteon_device - ReadXml()')
        Insteon_xml.ReadWriteConfigXml().ReadXml(p_device_obj, p_entry_xml)

    def WriteXml(self, p_device_obj, p_entry_xml):
        Insteon_xml.ReadWriteConfigXml().WriteXml(p_device_obj, p_entry_xml)

# ## END DBK
