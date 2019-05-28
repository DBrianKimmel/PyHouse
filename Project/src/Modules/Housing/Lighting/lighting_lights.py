"""
@name:      PyHouse/Project/src/Modules/Housing/Lighting/lighting_lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2011-2019 by D. Brian Kimmel
@note:      Created on May 1, 2011
@license:   MIT License
@summary:   This module handles the lights component of the lighting system.

Inherit from lighting_core.

Each entry should contain enough information to allow functionality of various family of lighting controllers.

Insteon is the first type coded and UPB is to follow.

The real work of controlling the devices is delegated to the modules for that family of devices.

"""

__updated__ = '2019-05-28'
__version_info__ = (19, 5, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyHouse files
from Modules.Core.data_objects import UuidData, CoreLightingData
from Modules.Families.family_utils import FamUtil
from Modules.Core.Utilities import extract_tools
from Modules.Core.Utilities.uuid_tools import Uuid as UtilUuid
from Modules.Core.Utilities.xml_tools import PutGetXML, XmlConfigTools
from Modules.Housing.Lighting.lighting_utility import Utility as lightingUtility
from Modules.Housing.Lighting.lighting_xml import LightingXML
from Modules.Core.state import State
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logging
LOG = Logging.getLogger('PyHouse.LightingLights ')
SECTION = 'LightSection'


class LightData(CoreLightingData):
    """ This is the idealized light info.
    This class contains all the reportable and controllable information a light might have.

    ==> PyHouse.House.Lighting.Lights.xxx as in the def below
    """

    def __init__(self):
        super(LightData, self).__init__()
        self.BrightnessPct = 0  # 0% to 100%
        self.Hue = 0  # 0 to 65535
        self.Saturation = 0  # 0 to 255
        self.ColorTemperature = 0  # degrees Kelvin - 0 is not supported
        self.RGB = 0xffffff
        self.TransitionTime = 0  # 0 to 65535 ms = time to turn on or off (fade Time or Rate)
        self.State = State.UNKNOWN
        self.IsDimmable = False
        self.IsColorChanging = False


class MqttActions:
    """ Mqtt section
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _decode_control(self, p_message):
        """
        pyhouse/<housename>/house/lighting/light/xxx
        """
        l_control = LightData()
        l_light_name = extract_tools.get_mqtt_field(p_message, 'LightName')
        l_control.BrightnessPct = _l_brightness = extract_tools.get_mqtt_field(p_message, 'Brightness')
        # LOG.debug(PrettyFormatAny.form(l_control, 'Control', 190))
        #
        l_light_obj = lightingUtility().get_object_by_id(self.m_pyhouse_obj.House.Lighting.Lights, name=l_light_name)
        if l_light_obj == None:
            LOG.warn(' Light "{}" was not found.'.format(l_light_name))
            return
        # LOG.debug(PrettyFormatAny.form(l_light_obj, 'Light', 190))
        #
        l_controller_obj = lightingUtility().get_controller_objs_by_family(self.m_pyhouse_obj.House.Lighting.Controllers, 'Insteon')
        # LOG.debug(PrettyFormatAny.form(l_controller_obj, 'Controller', 190))
        #
        if len(l_controller_obj) > 0:
            l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, l_light_obj)
            l_api.AbstractControlLight(self.m_pyhouse_obj, l_light_obj, l_controller_obj[0], l_control)

    def decode(self, p_topic, p_message):
        """ Decode Mqtt message
        ==> pyhouse/<house name>/house/lighting/light/<action>

        @param p_topic: is the topic after 'lighting'
        @return: a message to be logged as a Mqtt message
        """
        l_logmsg = '\tLighting/Lights: {}\n\t'.format(p_topic)
        LOG.debug('MqttLightingLightsDispatch Topic:{}'.format(p_topic))
        if p_topic[0] == 'control':
            self._decode_control(p_message)
            l_logmsg += 'Light Control: {}'.format(PrettyFormatAny.form(p_message, 'Light Control'))
            LOG.debug(l_logmsg)
        elif p_topic[0] == 'status':
            # The status is contained in LightData() above.
            l_logmsg += 'Light Status: {}'.format(PrettyFormatAny.form(p_message, 'Light Status'))
            LOG.debug(l_logmsg)
        else:
            l_logmsg += '\tUnknown Lighting/Light sub-topic:{}\n\t{}'.format(p_topic, PrettyFormatAny.form(p_message, 'Light Status'))
            LOG.warn('Unknown Topic: {}'.format(p_topic[0]))
        return l_logmsg


class XML:

    def _read_light_data(self, p_obj, p_xml):
        # p_obj.Comment = PutGetXML.get_text_from_xml(p_xml, 'Comment')
        if (p_xml.find('Brightness') != None):
            p_obj.BrightnessPct = PutGetXML.get_int_from_xml(p_xml, 'Brightness', 44)
        else:
            p_obj.BrightnessPct = PutGetXML.get_int_from_xml(p_xml, 'CurLevel', 45)
        p_obj.IsDimmable = PutGetXML.get_bool_from_xml(p_xml, 'IsDimmable', False)
        p_obj.DeviceType = PutGetXML.get_int_from_xml(p_xml, 'DeviceType', 41)
        p_obj.DeviceSubType = PutGetXML.get_int_from_xml(p_xml, 'DeviceSubType', 43)
        p_obj.RoomName = PutGetXML.get_text_from_xml(p_xml, 'RoomName')
        p_obj.RoomUUID = PutGetXML.get_uuid_from_xml(p_xml, 'RoomUUID')
        p_obj.RoomCoords = PutGetXML.get_coords_from_xml(p_xml, 'RoomCoords')
        return p_obj  # for testing

    def _write_light_data(self, p_obj, p_xml):
        PutGetXML.put_text_element(p_xml, 'Brightness', p_obj.BrightnessPct)
        PutGetXML.put_text_element(p_xml, 'IsDimmable', p_obj.IsDimmable)
        return p_xml

    def _read_one_light_xml(self, p_pyhouse_obj, p_xml):
        """
        Load all the xml for one controller.
        Base Device, Light, Family
        """
        l_obj = LightData()
        l_obj.DeviceType = 1  # Lighting
        l_obj.DeviceSubType = 3  # Lights
        try:
            l_obj = LightingXML()._read_base_device(l_obj, p_xml)
            self._read_light_data(l_obj, p_xml)
            LightingXML()._read_family_data(p_pyhouse_obj, l_obj, p_xml)
        except Exception as e_err:
            LOG.error('ERROR - ReadOneController - {}'.format(e_err))
            l_obj = LightData()
        return l_obj

    def _write_one_light_xml(self, p_pyhouse_obj, p_controller_obj):
        l_xml = LightingXML()._write_base_device('Light', p_controller_obj)
        self._write_light_data(p_controller_obj, l_xml)
        LightingXML()._write_family_data(p_pyhouse_obj, p_controller_obj, l_xml)
        return l_xml

    def read_all_lights_xml(self, p_pyhouse_obj):
        """
        @param p_pyhouse_obj: is the master information store
        @param p_version: is the XML version of the file to use.
        @return: a dict of lights info
        """
        l_count = 0
        l_dict = {}
        l_xml = XmlConfigTools.find_section(p_pyhouse_obj, 'HouseDivision/LightingSection/LightSection')
        if l_xml is None:
            return l_dict
        try:
            for l_one_xml in l_xml.iterfind('Light'):
                l_obj = self._read_one_light_xml(p_pyhouse_obj, l_one_xml)
                l_obj.Key = l_count  # Renumber
                l_dict[l_count] = l_obj
                l_uuid_obj = UuidData()
                l_uuid_obj.UUID = l_obj.UUID
                l_uuid_obj.UuidType = 'Light'
                UtilUuid.add_uuid(p_pyhouse_obj, l_uuid_obj)
                LOG.info('Loaded light {}'.format(l_obj.Name))
                l_count += 1
        except AttributeError as e_err:  # No Lights section
            LOG.warning('Lighting_Lights - No Lights defined - {}'.format(e_err))
            #  print('XXX-1', e_err)
            l_dict = {}
        LOG.info("Loaded {} Lights".format(l_count))
        return l_dict

    def write_all_lights_xml(self, p_pyhouse_obj):
        l_xml = ET.Element(SECTION)
        l_count = 0
        for l_light_obj in p_pyhouse_obj.House.Lighting.Lights.values():
            l_one = self._write_one_light_xml(p_pyhouse_obj, l_light_obj)
            l_xml.append(l_one)
            l_count += 1
        LOG.info('Saved {} Lights XML'.format(l_count))
        return l_xml


class API(MqttActions):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized - Version:{}".format(__version__))

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
        l_api = FamUtil._get_family_device_api(self.m_pyhouse_obj, p_device_obj)
        l_api.AbstractControlLight(p_device_obj, p_controller_obj, p_control)

#  ## END DBK
