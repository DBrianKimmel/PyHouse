"""
-*- test-case-name: PyHouse.Modules.Lighting.test.test_lighting -*-

@name:      PyHouse/src/Modules/Lighting/lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2016 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system automation.

Lighting Device type is "1".

PyHouse.House.Lighting.
                       Buttons
                       Controllers
                       Lights
"""

__updated__ = '2016-11-01'

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyHouse files
from Modules.Core.data_objects import LightingData
from Modules.Families.family_utils import FamUtil
from Modules.Housing.Lighting.lighting_actions import Utility as actionUtility
from Modules.Housing.Lighting.lighting_buttons import API as buttonsAPI
from Modules.Housing.Lighting.lighting_controllers import API as controllersAPI
from Modules.Housing.Lighting.lighting_lights import API as lightsAPI
from Modules.Housing.Lighting.lighting_motion import API as motionAPI
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Lighting       ')


class Utility(object):
    """Commands we can run from high places.
    """

    def _setup_lighting(self, p_pyhouse_obj):
        """
        Find the lighting information
        Config file version 1.4 moved the lighting information into a separate LightingSection
        """
        l_root = p_pyhouse_obj.Xml.XmlRoot
        l_lighting_xml = None
        try:
            l_house_xml = l_root.find('HouseDivision')
        except AttributeError as e_err:
            LOG.error('House Division is missing in Config file.  {}'.format(e_err))
            l_house_xml = l_root
        try:
            l_lighting_xml = l_house_xml.find('LightingSection')
        except AttributeError as e_err:
            LOG.warning('No LightingSection {}'.format(e_err))
        #  We have an old version
        if l_lighting_xml is None or l_lighting_xml == 'None':
            l_lighting_xml = l_house_xml
        return l_lighting_xml

    def _read_lighting_xml(self, p_pyhouse_obj):
        """
        Get all the lighting components for a house
        Config file version 1.4 moved the lighting information into a separate LightingSection
        """
        l_xml = p_pyhouse_obj.Xml.XmlRoot
        l_lighting_xml = self._setup_lighting(p_pyhouse_obj)  # in case of old style file
        l_xml = l_xml.find('HouseDivision')
        if l_xml is None:
            return p_pyhouse_obj.House.Lighting
        l_xml = l_xml.find('LightingSection')
        if l_xml is None:
            return p_pyhouse_obj.House.Lighting
        p_pyhouse_obj.House.Lighting.Buttons = buttonsAPI.read_all_buttons_xml(p_pyhouse_obj)
        p_pyhouse_obj.House.Lighting.Controllers = controllersAPI.read_all_controllers_xml(p_pyhouse_obj)
        p_pyhouse_obj.House.Lighting.Lights = lightsAPI.read_all_lights_xml(p_pyhouse_obj)
        return p_pyhouse_obj.House.Lighting

    @staticmethod
    def _write_lighting_xml(p_pyhouse_obj, p_house_element):
        """
        @param p_pyhouse_obj: is the whole PyHouse Object
        @param p_house_element: is the XML
        """
        l_lighting_xml = ET.Element('LightingSection')
        l_lighting_xml.append(buttonsAPI.write_all_buttons_xml(p_pyhouse_obj))
        l_lighting_xml.append(controllersAPI.write_all_controllers_xml(p_pyhouse_obj))
        l_lighting_xml.append(lightsAPI.write_all_lights_xml(p_pyhouse_obj))
        return l_lighting_xml


class API(Utility):

    def __init__(self, p_pyhouse_obj):
        p_pyhouse_obj.House.Lighting = LightingData()
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized')

    def LoadXml(self, p_pyhouse_obj):
        """ Load the Lighting xml info.
        """
        p_pyhouse_obj.House.Lighting = LightingData()
        self._read_lighting_xml(p_pyhouse_obj)

    def SaveXml(self, p_xml):
        """ Save the Lighting section.
        It will contain several sub-sections
        """
        l_xml = Utility._write_lighting_xml(self.m_pyhouse_obj, p_xml)
        p_xml.append(l_xml)
        LOG.info("Saved Lighting XML.")
        return p_xml

    def Start(self):
        """Allow loading of sub modules and drivers.
        """
        self.m_pyhouse_obj.APIs.House.FamilyAPI.start_lighting_families(self.m_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        """Allow cleanup of all drivers.
        """
        LOG.info("Stopping all lighting families.")
        #  self.m_pyhouse_obj.APIs.House.FamilyAPI.stop_lighting_families(self.m_pyhouse_obj)
        LOG.info("Stopped.")

    def ChangeLight(self, p_light_obj, p_source, p_new_level, _p_rate=None):
        """
        Set an Insteon controlled light to a value - On, Off, or Dimmed.

        Called by:
            web_controlLights
            schedule
        """
        l_light_obj = actionUtility._find_full_obj(self.m_pyhouse_obj, p_light_obj)
        try:
            LOG.info("Turn Light {} to level {}, DeviceFamily:{}".format(l_light_obj.Name, p_new_level, l_light_obj.DeviceFamily))

            l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, l_light_obj)
            l_api.ChangeLight(l_light_obj, p_source, p_new_level)
        except Exception as e_err:
            LOG.error('ERROR - {}'.format(e_err))

#  ## END DBK
