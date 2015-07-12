"""
-*- test-case-name: PyHouse.Modules.Lighting.test.test_lighting -*-

@name:      PyHouse/src/Modules/Lighting/lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2015 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system automation.

This is called from 'schedule' which is called from 'house' so there is one instance of this
for every house.
"""

# Import system type stuff

# Import PyHouse files
from Modules.Lighting.lighting_buttons import LBApi
from Modules.Lighting.lighting_controllers import LCApi
from Modules.Lighting.lighting_lights import LLApi
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Lighting       ')


class Utility(LCApi, LBApi, LLApi):
    """Commands we can run from high places.
    """

    def _setup_lighting(self, p_pyhouse_obj):
        """
        Find the lighting information
        Config file version 1.4 moved the lighting information into a separate LightingSection
        """
        l_root = p_pyhouse_obj.Xml.XmlRoot
        try:
            l_house_xml = l_root.find('HouseDivision')
        except AttributeError as e_err:
            LOG.error('House Division is missing in Config file.  {}'.format(e_err))
            l_house_xml = l_root
        try:
            l_lighting_xml = l_house_xml.find('LightingSection')
        except AttributeError as e_err:
            LOG.warning('Old version of Config file found.  No LightingSection {}'.format(e_err))
        if l_lighting_xml == None:
            l_lighting_xml = l_house_xml
        return l_lighting_xml

    def _read_lighting_xml(self, p_pyhouse_obj):
        """
        Get all the lighting components for a house
        Config file version 1.4 moved the lighting information into a separate LightingSection
        """
        l_lighting_xml = self._setup_lighting(p_pyhouse_obj)
        l_house_obj = p_pyhouse_obj.House.DeviceOBJs
        try:
            l_xml = l_lighting_xml.find('ControllerSection')
            l_house_obj.Controllers = LCApi(p_pyhouse_obj).read_all_controllers_xml(l_xml)
        except AttributeError as e_err:
            l_house_obj.Controllers = {}
            print('No Controllers found {}'.format(e_err))
        try:
            l_xml = l_lighting_xml.find('ButtonSection')
            l_house_obj.Buttons = LBApi(p_pyhouse_obj).read_all_buttons_xml(l_xml)
        except AttributeError as e_err:
            l_house_obj.Buttons = {}
            print('No Controllers found {}'.format(e_err))
        try:
            l_xml = l_lighting_xml.find('LightSection')
            l_house_obj.Lights = LLApi(p_pyhouse_obj).read_all_lights_xml(l_xml)
        except AttributeError as e_err:
            l_house_obj.Lights = {}
            print('No Lights found {}'.format(e_err))
        return l_house_obj

    def _write_lighting_xml(self, p_house_objs, p_house_element):
        try:
            l_xml = self.write_all_lights_xml(p_house_objs.Lights)
            p_house_element.append(l_xml)
            p_house_element.append(self.write_buttons_xml(p_house_objs.Buttons))
            p_house_element.append(self.write_all_controllers_xml(p_house_objs.Controllers))
        except AttributeError as e_err:
            l_msg = 'ERROR in writing lighting {0:}'.format(e_err)
            LOG.error(l_msg)
            print(l_msg)

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

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized')

    def Start(self):
        """Allow loading of sub modules and drivers.
        """
        self.m_house_obj = self.m_pyhouse_obj.House.DeviceOBJs
        self._read_lighting_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.APIs.House.FamilyAPI.start_lighting_families(self.m_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        """Allow cleanup of all drivers.
        """
        LOG.info("Stopping all lighting families.")
        self.m_pyhouse_obj.APIs.House.FamilyAPI.stop_lighting_families(self.m_house_obj)
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        LOG.info("Saving config info..")
        # self.m_pyhouse_obj.APIs.House.FamilyAPI.save_lighting_families(p_xml, self.m_pyhouse_obj.House.RefOBJs)
        self._write_lighting_xml(self.m_pyhouse_obj.House.DeviceOBJs, p_xml)
        LOG.info("Saved XML.")

    def _get_api_for_family(self, p_pyhouse_obj, p_light_obj):
        """
        The light we are changing can be in any lighting family.
        Get the instance pointer for the proper family so we can deal with the proper light.
        """
        l_ret = p_pyhouse_obj.House.RefOBJs.FamilyData[p_light_obj.DeviceFamily].FamilyModuleAPI
        LOG.info('{}'.format(l_ret))
        return l_ret

    def ChangeLight(self, p_light_obj, p_new_level, _p_rate = None):
        """
        Set an Insteon controlled light to a value - On, Off, or Dimmed.

        Called by:
            web_controlLights
            schedule
        """
        l_light_obj = self._find_full_obj(self.m_pyhouse_obj.House.DeviceOBJs.Lights, p_light_obj)
        try:
            LOG.info("Turn Light {} to level {}, DeviceFamily:{}".format(l_light_obj.Name, p_new_level, l_light_obj.DeviceFamily))
            l_api = self._get_api_for_family(self.m_pyhouse_obj, l_light_obj)
            l_api.ChangeLight(l_light_obj, p_new_level)
        except Exception as e_err:
            LOG.error('ERROR - {}'.format(e_err))

# ## END DBK
