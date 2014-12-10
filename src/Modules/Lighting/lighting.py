"""
-*- test-case-name: PyHouse.Modules.Lighting.test.test_lighting -*-

@name: PyHouse/src/Modules/Lighting/lighting.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2010-2014 by D. Brian Kimmel
@note: Created on Apr 2, 2010
@license: MIT License
@summary: Handle the home lighting system automation.

This is called from 'schedule' which is called from 'house' so there is one instance of this
for every house.
"""

# Import system type stuff

# Import PyHouse files
from Modules.Families import family
from Modules.Lighting.lighting_buttons import ButtonsAPI
from Modules.Lighting.lighting_controllers import ControllersAPI
from Modules.Lighting.lighting_lights import LightingLightsAPI
from Modules.Computer import logging_pyh as Logger
# from Modules.Utilities.tools import PrettyPrintAny

g_debug = 9
LOG = Logger.getLogger('PyHouse.Lighting       ')


class Utility(ControllersAPI, ButtonsAPI, LightingLightsAPI):
    """Commands we can run from high places.
    """

    def _read_lighting_xml(self, p_pyhouse_obj):
        """
        Get all the lighting components for a house
        Uses p_pyhouse_obj since many sections of xml are needed.
        """
        l_house_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
        try:
            p_pyhouse_obj.House.DeviceOBJs.Controllers = ControllersAPI(p_pyhouse_obj).read_all_controllers_xml(l_house_xml.find('ControllerSection'))
            p_pyhouse_obj.House.DeviceOBJs.Buttons = ButtonsAPI(p_pyhouse_obj).read_all_buttons_xml(l_house_xml.find('ButtonSection'))
            p_pyhouse_obj.House.DeviceOBJs.Lights = LightingLightsAPI(p_pyhouse_obj).read_all_lights_xml(l_house_xml.find('LightSection'))
        except AttributeError:
            p_pyhouse_obj.House.DeviceOBJs.Controllers = {}
            p_pyhouse_obj.House.DeviceOBJs.Buttons = {}
            p_pyhouse_obj.House.DeviceOBJs.Lights = {}

    def _write_lighting_xml(self, p_house_objs, p_house_element):
        try:
            p_house_element.append(self.write_all_lights_xml(p_house_objs.Lights))
            p_house_element.append(self.write_buttons_xml(p_house_objs.Buttons))
            p_house_element.append(self.write_controllers_xml(p_house_objs.Controllers))
        except AttributeError as e_err:
            LOG.error('ERRROR in writing lighting {0:}'.format(e_err))

    def _find_full_obj(self, p_lights, p_web_obj):
        """
        given the limited information from the web browser, look up and return the full object.

        If more than one light has the same name, return the first one found.
        """
        for l_light in p_lights.itervalues():
            if p_web_obj.Name == l_light.Name:
                return l_light
        LOG.error('ERROR - no light with name {0:} was found.'.format(p_web_obj.Name))
        return None


class API(Utility):

    def __init__(self):
        self.m_family = family.API()

    def Start(self, p_pyhouse_obj):
        """Allow loading of sub modules and drivers.
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_house_obj = p_pyhouse_obj.House.DeviceOBJs
        self._read_lighting_xml(p_pyhouse_obj)
        self.m_family.start_lighting_families(p_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        """Allow cleanup of all drivers.
        """
        LOG.info("Stopping all lighting families.")
        self.m_family.stop_lighting_families(self.m_house_obj)
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        LOG.info("Saving config info..")
        self.m_family.save_lighting_families(p_xml, self.m_pyhouse_obj.House.RefOBJs)
        self._write_lighting_xml(self.m_pyhouse_obj.House.DeviceOBJs, p_xml)
        LOG.info("Saved XML.")

    def _get_api_for_family(self, p_pyhouse_obj, p_light_obj):
        """
        The light we are changing can be in any lighting family.
        Get the instance pointer for the proper family so we can deal with the proper light.
        """
        l_ret = p_pyhouse_obj.House.RefOBJs.FamilyData[p_light_obj.ControllerFamily].FamilyModuleAPI
        LOG.info('{}'.format(l_ret))
        return l_ret

    def ChangeLight(self, p_light_obj, p_new_level, _p_rate = None):
        """
        Called by:
            web_controlLights
            schedule
        """
        l_light_obj = self._find_full_obj(self.m_pyhouse_obj.House.DeviceOBJs.Lights, p_light_obj)

        try:
            LOG.info("Turn Light {} to level {}, ControllerFamily:{}".format(l_light_obj.Name, p_new_level, l_light_obj.ControllerFamily))
            l_api = self._get_api_for_family(self.m_pyhouse_obj, l_light_obj)
            l_api.ChangeLight(l_light_obj, p_new_level)
        except Exception as e_err:
            LOG.error('ERROR - {}'.format(e_err))

# ## END DBK
