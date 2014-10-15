"""
-*- test-case-name: PyHouse.src.Modules.lights.test.test_lighting_lights -*-

@name: PyHouse/src/Modules/lights/lighting_lights.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2011-2014 by D. Brian Kimmel
@note: Created on May 1, 2011
@license: MIT License
@summary: This module handles the lights component of the lighting system.

Inherit from lighting_core.

Each entry should contain enough information to allow functionality of various family of lighting controllers.

Insteon is the first type coded and UPB is to follow.

The real work of controlling the devices is delegated to the modules for that family of devices.

"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyHouse files
from Modules.Core.data_objects import LightData
from Modules.Lighting.lighting_core import ReadWriteConfigXml
from Modules.Lighting.lighting_utils import Utility
from Modules.Computer import logging_pyh as Logging
# from Modules.Utilities.tools import PrettyPrintAny

g_debug = 0
LOG = Logging.getLogger('PyHouse.LightgLights')


LIGHTS_XML = """
        <LightSection>
            <Light Active="True" Key="0" Name="outside_front">
                <Comment>SwitchLink On/Off</Comment>
                <Coords>['0', '0']</Coords>
                <IsDimmable>False</IsDimmable>
                <RoomName>Foyer</RoomName>
                <LightingType>Light</LightingType>
                <ControllerFamily>Insteon</ControllerFamily>

                <Address>16.62.2D</Address>
                <IsController>True</IsController>
                <DevCat>02.0A</DevCat>
                <GroupList>All_Lights|Outside|Foyer(0;0)</GroupList>
                <GroupNumber>0</GroupNumber>
                <IsMaster>True</IsMaster>
                <ProductKey>30.1A.35</ProductKey>
                <IsResponder>True</IsResponder>
                <CurLevel>73</CurLevel>
            </Light>
            <Light Active="True" Key="1" Name="outside_gar">
                <Comment>SwitchLink On/Off</Comment>
                <Coords>['0', '0']</Coords>
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Garage</RoomName>
                <LightingType>Light</LightingType>
                <Address>17.47.A1</Address>
                <IsController>True</IsController>
                <DevCat>0x0</DevCat>
                <GroupList>All_Lights|Outside|Garage(0;0)</GroupList>
                <GroupNumber>0</GroupNumber>
                <IsMaster>True</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
            </Light>
            <Light Active="True" Key="2" Name="dr_chand">
                <Comment>SwitchLink dimmer</Comment><Coords>['0', '0']</Coords>
                <IsDimmable>True</IsDimmable><ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Dining Room</RoomName><LightingType>Light</LightingType><Address>16.C9.37</Address>
                <IsController>True</IsController><DevCat>0</DevCat><GroupList>All_Lights|DiningRoom(12;12)</GroupList>
                <GroupNumber>0</GroupNumber>
                <IsMaster>True</IsMaster>
                <ProductKey>F4.20.20</ProductKey>
                <IsResponder>True</IsResponder></Light>
            <Light Active="True" Key="3" Name="dr_chand_slave">
                <Comment>SwitchLink dimmer</Comment>
                <Coords>['0', '0']</Coords>
                <IsDimmable>True</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Dining Room</RoomName>
                <LightingType>Light</LightingType>
                <Address>16.C9.D0</Address>
                <IsController>True</IsController>
                <DevCat>8007</DevCat>
                <GroupList>All_Lights|Pantry(0;0)</GroupList>
                <GroupNumber>0</GroupNumber>
                <IsMaster>False</IsMaster>
                <ProductKey>EB.2A.A8</ProductKey>
                <IsResponder>True</IsResponder>
            </Light>
            <Light Active="True" Key="4" Name="nook_chand">
                <Comment>SwitchLink dimmer</Comment>
                <Coords>['0', '0']</Coords>
                <IsDimmable>True</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Breakfast Nook</RoomName>
                <LightingType>Light</LightingType>
                <Address>17.C2.72</Address>
                <IsController>True</IsController>
                <DevCat>0xc44</DevCat>
                <GroupList>All_Lights|Pantry(0;0)</GroupList>
                <GroupNumber>0</GroupNumber>
                <IsMaster>True</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
            </Light>
        </LightSection>
"""



class LightingLightsAPI(ReadWriteConfigXml):
    """
    Get/Put all the information about one light:
        Base Light Data
        Light Data
        Family Data
    """

    m_count = 0

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_utils = Utility(p_pyhouse_obj)

    def _read_light_data(self, p_xml):
        l_light_obj = LightData()
        l_light_obj = self.read_base_lighting_xml(l_light_obj, p_xml)
        # l_light_obj.IsController = self.get_text_from_xml(p_xml, 'IsController')
        l_light_obj.CurLevel = self.get_int_from_xml(p_xml, 'CurLevel', 0)
        return l_light_obj

    def _read_family_data(self, p_obj, p_xml):
        # print('lighting_lights - read_family_data() - utils {0:}'.format(self.m_utils))
        l_api = self.m_utils.read_family_data(p_obj, p_xml)
        return l_api  # for testing

    def _read_one_light_xml(self, p_light_xml):
        l_light_obj = self._read_light_data(p_light_xml)
        # print('lighting_lights - read_one_light() - Light {0:}'.format(l_light_obj.Name))
        l_light_obj.Key = self.m_count  # Renumber
        self._read_family_data(l_light_obj, p_light_xml)
        return l_light_obj

    def read_all_lights_xml(self, p_light_sect_xml):
        self.m_count = 0
        l_lights_dict = {}
        try:
            for l_light_xml in p_light_sect_xml.iterfind('Light'):
                l_lights_dict[self.m_count] = self._read_one_light_xml(l_light_xml)
                self.m_count += 1
        except AttributeError as e_error:  # No Lights section
            LOG.warning('Lighting_Lights - No Lights defined - {0:}'.format(e_error))
            l_lights_dict = {}
        return l_lights_dict


    def _write_light_data(self, p_light_obj, l_light_xml):
        # self.put_text_element(l_light_xml, 'IsController', p_light_obj.IsController)
        self.put_text_element(l_light_xml, 'LightingType', p_light_obj.LightingType)
        self.put_text_element(l_light_xml, 'CurLevel', p_light_obj.CurLevel)
        pass

    def _add_family_data(self, p_light_obj, p_light_xml):
        """
        Add the family specific information of the light to the XML.
        """
        l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[p_light_obj.ControllerFamily].FamilyModuleAPI
        l_api.WriteXml(p_light_xml, p_light_obj)

    def write_one_light_xml(self, p_light_obj):
        l_light_xml = self.write_base_lighting_xml(p_light_obj)
        self._write_light_data(p_light_obj, l_light_xml)
        self._add_family_data(p_light_obj, l_light_xml)
        return l_light_xml

    def write_all_lights_xml(self, p_lights_obj):
        l_xml = ET.Element('LightSection')
        self.m_count = 0
        for l_light_obj in p_lights_obj.itervalues():
            l_xml.append(self.write_one_light_xml(l_light_obj))
            self.m_count += 1
        return l_xml

# ## END DBK
