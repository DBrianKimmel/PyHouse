"""
@name:      PyHouse/Project/src/Modules/Lighting/lighting_controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2010-2019 by D. Brian Kimmel
@note:      Created on Apr 2, 2010
@license:   MIT License
@summary:   Handle the home lighting system automation.

Reading and writing XML to save controller information is fairly comples.
First we have the basic information about the controller.
Then we have the Lighting system information.
Then we have the information specific to the family of the controller (Insteon, USB, Zigbee, etc.).
Then we have the interface information (Ethernet, USB, Serial, ...).
And we also have information about the controller class of devices.


"""

__updated__ = '2019-05-21'

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Core.data_objects import ControllerData, UuidData
# from Modules.Families.family_utils import FamUtil
from Modules.Drivers.interface import Xml as interfaceXML
# from Modules.Core.Utilities.device_tools import XML as deviceXML
from Modules.Core.Utilities.uuid_tools import Uuid as UtilUuid
from Modules.Core.Utilities.xml_tools import PutGetXML, XmlConfigTools
from Modules.Housing.Lighting.lighting_xml import LightingXML
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.LightController')


class MqttActions:
    """ Mqtt section
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_topic, p_message):
        """ Decode Mqtt message
        ==> pyhouse/<house name>/lighting/controller/<action>

        @param p_topic: is the topic after 'controller'
        @return: a message to be logged as a Mqtt message
        """
        l_logmsg = '\tLighting/Controllers: {}\n\t'.format(p_topic)
        LOG.debug('MqttLightingControllersDispatch Topic:{}'.format(p_topic))
        if p_topic[0] == 'control':
            l_logmsg += 'Controller Control: {}'.format(PrettyFormatAny.form(p_message, 'Controller Control'))
            LOG.debug(l_logmsg)
        elif p_topic[0] == 'status':
            # The status is contained in LightData() above.
            l_logmsg += 'Controller Status: {}'.format(PrettyFormatAny.form(p_message, 'Controller Status'))
            LOG.debug(l_logmsg)
        else:
            l_logmsg += '\tUnknown Lighting/Controller sub-topic:{}\n\t{}'.format(p_topic, PrettyFormatAny.form(p_message, 'Controller Status'))
            LOG.debug(l_logmsg)
        return l_logmsg


class XML:

    def _read_controller_data(self, _p_pyhouse_obj, p_obj, p_xml):
        """
        There are extra fields for controllers - get them.
        See ControllerData()
        """
        p_obj.InterfaceType = PutGetXML.get_text_from_xml(p_xml, 'InterfaceType')
        p_obj.Port = PutGetXML.get_text_from_xml(p_xml, 'Port')
        return p_obj  # for testing

    def _write_controller_data(self, p_obj, p_xml):
        PutGetXML.put_text_element(p_xml, 'InterfaceType', p_obj.InterfaceType)
        PutGetXML.put_text_element(p_xml, 'Port', p_obj.Port)
        return p_xml

    def _read_interface_data(self, _p_pyhouse_obj, p_obj, p_xml):
        try:
            interfaceXML.read_interface_xml(p_obj, p_xml)
        except Exception as e_err:  # DeviceFamily invalid or missing
            LOG.error('ERROR - Read Interface Data - {} - {} - {}'.format(e_err, p_obj.Name, p_obj.InterfaceType))
        return p_obj

    def _write_interface_data(self, p_obj, p_xml):
        try:
            l_xml = interfaceXML.write_interface_xml(p_obj)
            p_xml.append(l_xml)
        except Exception:
            pass
        return p_xml

    def _read_one_controller_xml(self, p_pyhouse_obj, p_xml):
        """
        Load all the xml for one controller.
        Base Device, Controller, Family and Interface
        """
        l_obj = ControllerData()
        l_obj.DeviceType = 1  # Lighting
        l_obj.DeviceSubType = 2  # Controller
        LightingXML()._read_base_device(l_obj, p_xml)
        try:
            self._read_controller_data(p_pyhouse_obj, l_obj, p_xml)
            self._read_interface_data(p_pyhouse_obj, l_obj, p_xml)
            LightingXML()._read_family_data(p_pyhouse_obj, l_obj, p_xml)
        except Exception as e_err:
            LOG.error('ERROR - ReadOneController - {}'.format(e_err))
            l_obj = ControllerData()
        return l_obj

    def _write_one_controller_xml(self, p_pyhouse_obj, p_controller_obj):
        l_controller_xml = LightingXML()._write_base_device('Controller', p_controller_obj)
        self._write_controller_data(p_controller_obj, l_controller_xml)
        self._write_interface_data(p_controller_obj, l_controller_xml)
        LightingXML()._write_family_data(p_pyhouse_obj, p_controller_obj, l_controller_xml)
        return l_controller_xml

    def read_all_controllers_xml(self, p_pyhouse_obj):
        """Called from lighting.
        Get the entire configuration of all the controllers and place them in a holding dict.

        @param p_pyhouse_obj: is the entire PyHouse Data
        @param p_controller_section_xml: is the XML element containing all controllers. <ControllerSection>
        @param p_version: is the old version of the XML Config file
        @return: a dict of all the controllers configured.
        """
        l_count = 0
        l_dict = {}
        l_xml = XmlConfigTools.find_section(p_pyhouse_obj, 'HouseDivision/LightingSection/ControllerSection')
        if l_xml is None:
            return l_dict
        try:
            for l_one_xml in l_xml.iterfind('Controller'):
                l_obj = self._read_one_controller_xml(p_pyhouse_obj, l_one_xml)
                l_obj.Key = l_count
                l_dict[l_count] = l_obj
                l_uuid_obj = UuidData()
                l_uuid_obj.UUID = l_obj.UUID
                l_uuid_obj.UuidType = 'Controller'
                UtilUuid.add_uuid(p_pyhouse_obj, l_uuid_obj)
                LOG.info('Loaded controller {}'.format(l_obj.Name))
                l_count += 1
        except AttributeError as e_error:  # No Controller section
            LOG.warning('No Controllers found - {}'.format(e_error))
        LOG.info("Loaded {} Controllers".format(l_count))
        return l_dict

    def write_all_controllers_xml(self, p_pyhouse_obj):
        l_count = 0
        l_controllers_xml = ET.Element('ControllerSection')
        for l_controller_obj in p_pyhouse_obj.House.Lighting.Controllers.values():
            l_controllers_xml.append(self._write_one_controller_xml(p_pyhouse_obj, l_controller_obj))
            l_count += 1
        LOG.info('Saved {} Controllers XML'.format(l_count))
        return l_controllers_xml

#  ## END DBK
