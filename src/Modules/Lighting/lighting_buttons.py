#!/usr/bin/env python

"""Handle the controller component of the lighting system.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyHouse files
from Modules.Core.data_objects import ButtonData
from Modules.Lighting.lighting_core import ReadWriteConfigXml
from Modules.Lighting.lighting_utils import Utility
from Modules.Computer import logging_pyh as Logging
# from Modules.Utilities.tools import PrettyPrintAny


g_debug = 0
LOG = Logging.getLogger('PyHouse.LightgButton')

BUTTONS_XML = """
        <ButtonSection>
            <Button Active="False" Key="0" Name="kpl_1_A">
                <Comment>KeypadLink Button A</Comment>
                <Coords />
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Master Bath</RoomName>
                <LightingType>Button</LightingType>
                <Address>16.E5.B6</Address>
                <IsController>True</IsController>
                <DevCat>0x0</DevCat>
                <GroupList>All_Lights|MasterBedroom(0;0)</GroupList>
                <GroupNumber>1</GroupNumber>
                <IsMaster>True</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
            </Button>
            <Button Active="False" Key="1" Name="kpl_1_B">
                <Comment>KeypadLink Button B</Comment>
                <Coords />
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <Room />
                <LightingType>Button</LightingType>
                <Address>16.E5.B6</Address>
                <IsController>True</IsController>
                <DevCat>0</DevCat>
                <GroupList>All_Buttons</GroupList>
                <GroupNumber>2</GroupNumber>
                <IsMaster>False</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
            </Button>
            <Button Active="False" Key="2" Name="kpl_1_C">
                <Comment>KeypadLink Button C</Comment>
                <Coords />
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <Room />
                <LightingType>Button</LightingType>
                <Address>16.E5.B6</Address>
                <IsController>True</IsController>
                <DevCat>0</DevCat>
                <GroupList>All_Buttons</GroupList>
                <GroupNumber>3</GroupNumber>
                <IsMaster>False</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
            </Button>
            <Button Active="False" Key="3" Name="kpl_1_D">
                <Comment>KeypadLink Button D</Comment>
                <Coords />
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <Room />
                <LightingType>Button</LightingType>
                <Address>16.E5.B6</Address>
                <IsController>True</IsController>
                <DevCat>0</DevCat><GroupList>All_Buttons</GroupList><GroupNumber>4</GroupNumber>
                <IsMaster>False</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
            </Button>
        </ButtonSection>
"""



class ButtonsAPI(ReadWriteConfigXml):

    m_count = 0

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_utils = Utility(p_pyhouse_obj)

    def _read_button_data(self, p_xml):
        l_obj = ButtonData()
        l_obj = self.read_base_lighting_xml(l_obj, p_xml)
        return l_obj

    def _read_family_data(self, p_obj, p_xml):
        l_api = self.m_utils.read_family_data(p_obj, p_xml)
        return l_api  # for testing

    def read_one_button_xml(self, p_button_xml):
        l_button_obj = self._read_button_data(p_button_xml)
        self._read_family_data(l_button_obj, p_button_xml)
        l_button_obj.Key = self.m_count  # Renumber
        return l_button_obj

    def read_all_buttons_xml(self, p_button_sect_xml):
        self.m_count = 0
        l_button_dict = {}
        try:
            for l_button_xml in p_button_sect_xml.iterfind('Button'):
                l_button_dict[self.m_count] = self.read_one_button_xml(l_button_xml)
                self.m_count += 1
        except AttributeError as e_error:  # No Buttons
            LOG.warning('No Buttons defined - {0:}'.format(e_error))
            l_button_dict = {}
        return l_button_dict

    def write_one_button_xml(self, p_button_obj):
        # l_button_xml = self.write_base_object_xml('Button', p_button_obj)
        l_button_xml = self.write_base_lighting_xml(p_button_obj)
        self._add_family_data(p_button_obj, l_button_xml)
        return l_button_xml

    def write_buttons_xml(self, p_buttons_obj):
        self.m_count = 0
        l_buttons_xml = ET.Element('ButtonSection')
        for l_button_obj in p_buttons_obj.itervalues():
            l_entry = self.write_one_button_xml(l_button_obj)
            l_buttons_xml.append(l_entry)
            self.m_count += 1
        return l_buttons_xml


# ## END DBK
