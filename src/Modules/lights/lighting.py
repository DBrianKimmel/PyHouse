"""
-*- test-case-name: PyHouse.Modules.lights.test.test_lighting -*-

@name: PyHouse/src/Modules/lights/lighting.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2010-2014 by D. Brian Kimmel
@note: Created on Apr 2, 2010
@license: MIT License
@summary: Handle the home lighting system automation.

This is called from 'schedule' which is called from 'house' so there is one instance of this
for every house.
"""

# Import system type stuff

# Import PyHouse files
from Modules.families import family
from Modules.lights.lighting_buttons import ButtonsAPI
from Modules.lights.lighting_controllers import ControllersAPI
from Modules.lights.lighting_lights import LightingLightsAPI
from Modules.utils import pyh_log
# from Modules.utils.tools import PrettyPrintAny

g_debug = 9
LOG = pyh_log.getLogger('PyHouse.Lighting    ')


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
            p_pyhouse_obj.House.OBJs.Controllers = ControllersAPI(p_pyhouse_obj).read_controllers_xml(l_house_xml.find('ControllerSection'))
            p_pyhouse_obj.House.OBJs.Buttons = ButtonsAPI(p_pyhouse_obj).read_buttons_xml(l_house_xml.find('ButtonSection'))
            p_pyhouse_obj.House.OBJs.Lights = LightingLightsAPI(p_pyhouse_obj).read_all_lights_xml(l_house_xml.find('LightSection'))
        except AttributeError as e_err:
            LOG.error('ReadLighting ERROR - {0:}'.format(e_err))

    def _write_lighting_xml(self, p_house_objs, p_house_element):
        LOG.info('Writing lights, buttons and controllers ')
        p_house_element.append(self.write_all_lights_xml(p_house_objs.Lights))
        p_house_element.append(self.write_buttons_xml(p_house_objs.Buttons))
        p_house_element.append(self.write_controllers_xml(p_house_objs.Controllers))


class API(Utility):

    def __init__(self):
        self.m_family = family.API()
        LOG.info("Initialized.")

    def Start(self, p_pyhouse_obj):
        """Allow loading of sub modules and drivers.
        """
        LOG.info("Starting.")
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_house_obj = p_pyhouse_obj.House.OBJs
        self.m_house_obj.FamilyData = self.m_family.build_lighting_family_info()
        self._read_lighting_xml(p_pyhouse_obj)
        self.m_family.start_lighting_families(p_pyhouse_obj, self.m_house_obj)
        LOG.info("Started.")

    def Stop(self):
        """Allow cleanup of all drivers.
        """
        LOG.info("Stopping all lighting families.")
        self.m_family.stop_lighting_families(self.m_house_obj)
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        """Allow cleanup of all drivers.
        """
        LOG.info("Stopping all lighting families.")
        self.m_family.save_lighting_families(p_xml, self.m_house_obj)
        self._write_lighting_xml(self.m_pyhouse_obj.House.OBJs, p_xml)
        LOG.info("Saved XML.")

    def ChangeLight(self, p_light_obj, p_level, _p_rate = None):
        """
        Called by:
            web_controlLights
            schedule
        """
        try:
            l_key = p_light_obj.Key
            l_light_obj = self.m_pyhouse_obj.House.OBJs.Lights[l_key]
            LOG.info("Turn Light {0:} to level {1:}, ControllerFamily:{2:}".format(l_light_obj.Name, p_level, l_light_obj.ControllerFamily))
            l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[l_light_obj.ControllerFamily].ModuleAPI
            l_api.ChangeLight(l_light_obj, p_level)
        except Exception as e_err:
            LOG.error('ChangeLight ERROR - {0:}'.format(e_err))

# ## END DBK
