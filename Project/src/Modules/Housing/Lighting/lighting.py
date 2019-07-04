"""
@name:      PyHouse/Project/src/Modules/Housing/Lighting/lighting.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2019 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system automation.

Lighting Device type is "1".

PyHouse.House.Lighting.
                       Buttons
                       Controllers
                       Lights
"""

__updated__ = '2019-07-02'
__version_info__ = (19, 5, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from typing import Any
import xml.etree.ElementTree as ET

#  Import PyHouse files
from Modules.Core.data_objects import LightingData, PyHouseInformation
from Modules.Core.Utilities.xml_tools import XmlConfigTools
from Modules.Housing.Lighting.lighting_buttons import XML as buttonsXML
from Modules.Housing.Lighting.lighting_controllers import XML as controllersXML, MqttActions as controllerMqtt
from Modules.Housing.Lighting.lighting_lights import MqttActions as lightMqtt, XML as lightXML
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Lighting       ')


class MqttActions:
    """
    """

    def __init__(self, p_pyhouse_obj: PyHouseInformation) -> None:
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_topic: list, p_message, p_logmsg) -> str:
        """
        --> pyhouse/<housename>/lighting/<category>/xxx
        """
        p_logmsg += '\tLighting: {}\n'.format(self.m_pyhouse_obj.House.Name)
        LOG.debug('MqttLightingDispatch Topic:{}'.format(p_topic))
        if p_topic[0] == 'button':
            pass
        elif p_topic[0] == 'controller':
            p_logmsg += controllerMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message)
        elif p_topic[0] == 'light':
            p_logmsg += lightMqtt(self.m_pyhouse_obj).decode(p_topic[1:], p_message)
        else:
            p_logmsg += '\tUnknown Lighting sub-topic {}'.format(p_message)
            LOG.warn('Unknown Lighting Topic: {}'.format(p_topic[0]))
        return p_logmsg

    def XXdecode_light(self, p_topic, p_message):
        """
        --> pyhouse/housename/lighting/light/xxx
        """
        l_logmsg = '\tLight: {}\n'.format(self.m_pyhouse_obj.House.Name)
        if p_topic[0] == 'status':
            pass
        else:
            l_logmsg += '\tUnknown Light sub-topic {}'.format(p_message)
        return l_logmsg


class Yaml:
    """
    """


class XML:
    """Commands we can run from high places.
    """

    def read_lighting_xml(self, p_pyhouse_obj):
        """
        Get all the lighting components for a house
        Config file version 1.4 moved the lighting information into a separate LightingSection
        """
        l_xml = XmlConfigTools.find_xml_section(p_pyhouse_obj, 'HouseDivision/LightingSection')
        if l_xml is None:
            return p_pyhouse_obj.House.Lighting
        p_pyhouse_obj.House.Lighting.Buttons = buttonsXML().read_all_buttons_xml(p_pyhouse_obj)
        p_pyhouse_obj.House.Lighting.Controllers = controllersXML().read_all_controllers_xml(p_pyhouse_obj)
        p_pyhouse_obj.House.Lighting.Lights = lightXML().read_all_lights_xml(p_pyhouse_obj)
        return p_pyhouse_obj.House.Lighting

    def write_lighting_xml(self, p_pyhouse_obj, _p_house_element):
        """
        @param p_pyhouse_obj: is the whole PyHouse Object
        @param p_house_element: is the XML
        """
        l_lighting_xml = ET.Element('LightingSection')
        l_lighting_xml.append(buttonsXML().write_all_buttons_xml(p_pyhouse_obj))
        l_lighting_xml.append(controllersXML().write_all_controllers_xml(p_pyhouse_obj))
        l_lighting_xml.append(lightXML().write_all_lights_xml(p_pyhouse_obj))
        return l_lighting_xml


class API(XML):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

    def LoadConfig(self, p_pyhouse_obj):
        """ Load the Lighting xml info.
        """
        p_pyhouse_obj.House.Lighting = LightingData()  # Clear before loading
        self.read_lighting_xml(p_pyhouse_obj)

    def SaveConfig(self, p_xml):
        """ Save the Lighting section.
        It will contain several sub-sections
        """
        l_xml = self.write_lighting_xml(self.m_pyhouse_obj, p_xml)
        p_xml.append(l_xml)
        LOG.info("Saved Lighting XML.")
        return p_xml

    def Start(self):
        """ Allow loading of sub modules and drivers.
        """
        self.m_pyhouse_obj._APIs.House.FamilyAPI.start_lighting_families(self.m_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        """ Allow cleanup of all drivers.
        """
        LOG.info("Stopping all lighting families.")
        #  self.m_pyhouse_obj._APIs.House.FamilyAPI.stop_lighting_families(self.m_pyhouse_obj)
        LOG.info("Stopped.")

    def AbstractControlLight(self, p_device_obj, p_controller_obj, p_control):
        """
        Insteon specific version of control light
        All that Insteon can control is Brightness and Fade Rate.

        @param p_controller_obj: optional
        @param p_device_obj: the device being controlled
        @param p_control: the idealized light control params
        """
        if self.m_plm == None:
            LOG.info('No PLM was defined - Quitting.')
            return
        # l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, p_device_obj)
        self.m_plm.AbstractControlLight(p_device_obj, p_controller_obj, p_control)

#  ## END DBK
