"""
@name:      PyHouse/src/Modules/Security/security.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 29, 2015
@Summary:

"""

__updated__ = '2019-01-28'

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import UuidData, GarageDoorData, MotionSensorData, SecurityData
from Modules.Families.family_utils import FamUtil
from Modules.Housing.Security.pi_camera import API as cameraApi
from Modules.Core.Utilities.device_tools import XML as deviceXML
from Modules.Core.Utilities.uuid_tools import Uuid as UtilUuid
from Modules.Core.Utilities.xml_tools import PutGetXML
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.Computer.Mqtt.mqtt_actions import get_mqtt_field
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Security       ')

# LOCATION = House.Security


class MqttActions(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def decode(self, p_topic, p_message):
        """ Decode the Mqtt message
        ==> pyhouse/<house name>/security/<type>/<Name>
        <type> = garage door, motion sensor, camera
        """
        l_logmsg = '\tSecurity:\n'
        if p_topic[0] == 'garage_door':
            l_logmsg += '\tGarage Door: {}\n'.format(get_mqtt_field(p_message, 'Name'))
        elif p_topic[0] == 'motion_sensor':
            l_logmsg += '\tMotion Sensor:{}\n\t{}'.format(get_mqtt_field(p_message, 'Name'), get_mqtt_field(p_message, 'Status'))
        else:
            l_logmsg += '\tUnknown sub-topic {}'.format(PrettyFormatAny.form(p_message, 'Security msg', 160))
        return l_logmsg


class Utility(object):

    @staticmethod
    def _read_base_device(p_pyhouse_obj, p_xml):
        """
        @param p_xml: is the XML Element for the entire device
        @return: a Lighting device data object with the base info filled in
        """
        l_obj = GarageDoorData()
        l_obj = deviceXML.read_base_device_object_xml(l_obj, p_xml)
        l_obj.DeviceType = 3
        l_obj.DeviceSubType = 1
        return l_obj

    @staticmethod
    def _write_base_device(_p_pyhouse_obj, p_door_obj):
        l_xml = deviceXML.write_base_device_object_xml('GarageDoor', p_door_obj)
        return l_xml

    @staticmethod
    def _read_base_motion_device(p_pyhouse_obj, p_xml):
        """
        @param p_xml: is the XML Element for the entire device
        @return: a Lighting device data object with the base info filled in
        """
        l_obj = MotionSensorData()
        l_obj = deviceXML.read_base_device_object_xml(l_obj, p_xml)
        l_obj.DeviceType = 3
        l_obj.DeviceSubType = 2
        return l_obj

    @staticmethod
    def _write_base_motion_device(_p_pyhouse_obj, p_door_obj):
        l_xml = deviceXML.write_base_device_object_xml('Motion', p_door_obj)
        return l_xml

    @staticmethod
    def _read_door_data(_p_pyhouse_obj, p_obj, p_xml):
        p_obj.Status = PutGetXML.get_text_from_xml(p_xml, 'Status', False)
        return p_obj  # for testing

    @staticmethod
    def _write_door_data(p_obj, p_xml):
        PutGetXML.put_text_element(p_xml, 'Status', p_obj.Status)
        return p_xml

    @staticmethod
    def _read_motion_data(_p_pyhouse_obj, p_obj, p_xml):
        return p_obj  # for testing

    @staticmethod
    def _write_motion_data(p_obj, p_xml):
        return p_xml

    @staticmethod
    def _read_family_data(p_pyhouse_obj, p_obj, p_xml):
        l_api = FamUtil.read_family_data(p_pyhouse_obj, p_obj, p_xml)
        return l_api  # for testing

    @staticmethod
    def _write_family_data(p_pyhouse_obj, p_obj, p_xml):
        try:
            l_family = p_obj.DeviceFamily
            l_family_obj = p_pyhouse_obj.House.FamilyData[l_family]
            l_api = l_family_obj.FamilyXmlModuleAPI
            l_api.WriteXml(p_xml, p_obj)
        except Exception as e_err:
            LOG.error('ERROR - {}'.format(e_err))

    @staticmethod
    def _read_one_door_xml(p_pyhouse_obj, p_xml):
        """
        Load all the xml for one controller.
        Base Device, Light, Family
        """
        try:
            l_obj = Utility._read_base_device(p_pyhouse_obj, p_xml)
            Utility._read_door_data(p_pyhouse_obj, l_obj, p_xml)
            Utility._read_family_data(p_pyhouse_obj, l_obj, p_xml)
        except Exception as e_err:
            LOG.error('ERROR - ReadOneGarageDoor - {}'.format(e_err))
            l_obj = GarageDoorData()
        return l_obj

    @staticmethod
    def _write_one_door_xml(p_pyhouse_obj, p_controller_obj):
        l_xml = Utility._write_base_device(p_pyhouse_obj, p_controller_obj)
        Utility._write_door_data(p_controller_obj, l_xml)
        Utility._write_family_data(p_pyhouse_obj, p_controller_obj, l_xml)
        return l_xml

    @staticmethod
    def _read_one_motion_xml(p_pyhouse_obj, p_xml):
        """
        Load all the xml for one Motion Sensor.
        Base Device, Light, Family
        """
        try:
            l_obj = Utility._read_base_motion_device(p_pyhouse_obj, p_xml)
            Utility._read_motion_data(p_pyhouse_obj, l_obj, p_xml)
            Utility._read_family_data(p_pyhouse_obj, l_obj, p_xml)
        except Exception as e_err:
            LOG.error('ERROR - ReadOneMotionSensor - {}'.format(e_err))
            l_obj = MotionSensorData()
        return l_obj

    @staticmethod
    def _write_one_motion_xml(p_pyhouse_obj, p_controller_obj):
        l_xml = Utility._write_base_motion_device(p_pyhouse_obj, p_controller_obj)
        Utility._write_motion_data(p_controller_obj, l_xml)
        Utility._write_family_data(p_pyhouse_obj, p_controller_obj, l_xml)
        return l_xml


class XML(object):
    """
    """

    @staticmethod
    def read_all_MotionSensors_xml(p_pyhouse_obj):
        """
        @param p_pyhouse_obj: is the master information store
        @return: a dict of Motion Sensor info
        """
        l_count = 0
        l_dict = {}
        l_xml = p_pyhouse_obj.Xml.XmlRoot
        if l_xml is None:
            return l_dict
        l_xml = l_xml.find('HouseDivision')
        if l_xml is None:
            return l_dict
        l_xml = l_xml.find('SecuritySection')
        if l_xml is None:
            return l_dict
        l_xml = l_xml.find('MotionDetectorSection')
        if l_xml is None:
            return l_dict
        try:
            for l_one_xml in l_xml.iterfind('Motion'):
                l_obj = Utility._read_one_motion_xml(p_pyhouse_obj, l_one_xml)
                l_obj.Key = l_count  # Renumber
                l_dict[l_count] = l_obj
                l_uuid_obj = UuidData()
                l_uuid_obj.UUID = l_obj.UUID
                l_uuid_obj.UuidType = 'MotionDetector'
                UtilUuid.add_uuid(p_pyhouse_obj, l_uuid_obj)
                LOG.info('Loaded Motion Detectors {}'.format(l_obj.Name))
                l_count += 1
        except AttributeError as e_err:  # No such section
            LOG.warning('No Motion Detectors defined - {}'.format(e_err))
            #  print('XXX-1', e_err)
            l_dict = {}
        LOG.info("Loaded {} Motion Detectors".format(l_count))
        return l_dict

    @staticmethod
    def write_all_MotionSensors_xml(p_pyhouse_obj):
        l_xml = ET.Element('MotionDetectorSection')
        l_count = 0
        for l_obj in p_pyhouse_obj.House.Security.MotionSensors.values():
            l_one = Utility._write_one_motion_xml(p_pyhouse_obj, l_obj)
            l_xml.append(l_one)
            l_count += 1
        LOG.info('Saved {} Motion Detectors XML'.format(l_count))
        return l_xml

    @staticmethod
    def read_all_GarageDoors_xml(p_pyhouse_obj):
        """
        @param p_pyhouse_obj: is the master information store
        @param p_version: is the XML version of the file to use.
        @return: a dict of Garage Doors info
        """
        l_count = 0
        l_dict = {}
        l_xml = p_pyhouse_obj.Xml.XmlRoot
        if l_xml is None:
            return l_dict
        l_xml = l_xml.find('HouseDivision')
        if l_xml is None:
            return l_dict
        l_xml = l_xml.find('SecuritySection')
        if l_xml is None:
            return l_dict
        l_xml = l_xml.find('GarageDoorSection')
        if l_xml is None:
            return l_dict
        try:
            for l_one_xml in l_xml.iterfind('GarageDoor'):
                l_obj = Utility._read_one_door_xml(p_pyhouse_obj, l_one_xml)
                l_obj.Key = l_count  # Renumber
                l_dict[l_count] = l_obj
                l_uuid_obj = UuidData()
                l_uuid_obj.UUID = l_obj.UUID
                l_uuid_obj.UuidType = 'GarageDoor'
                UtilUuid.add_uuid(p_pyhouse_obj, l_uuid_obj)
                LOG.info('Loaded Garage Door {}'.format(l_obj.Name))
                l_count += 1
        except AttributeError as e_err:  # No Lights section
            LOG.warning('No Garage Doors defined - {}'.format(e_err))
            #  print('XXX-1', e_err)
            l_dict = {}
        LOG.info("Loaded {} Garage Doors".format(l_count))
        return l_dict

    @staticmethod
    def write_all_GarageDoors_xml(p_pyhouse_obj):
        l_xml = ET.Element('GarageDoorSection')
        l_count = 0
        for l_obj in p_pyhouse_obj.House.Security.GarageDoors.values():
            l_one = Utility._write_one_door_xml(p_pyhouse_obj, l_obj)
            l_xml.append(l_one)
            l_count += 1
        LOG.info('Saved {} GarageDoors XML'.format(l_count))
        return l_xml


class API(object):
    """ Called from house.

    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_api = cameraApi(p_pyhouse_obj)
        LOG.info('Initialized')

    def LoadXml(self, p_pyhouse_obj):
        """ Load the Security Information
        """
        LOG.info('Loading XML')
        p_pyhouse_obj.House.Security = SecurityData()  # Clear before loading
        p_pyhouse_obj.House.Security.GarageDoors = XML.read_all_GarageDoors_xml(p_pyhouse_obj)
        p_pyhouse_obj.House.Security.MotionSensors = XML.read_all_MotionSensors_xml(p_pyhouse_obj)
        LOG.info('Loaded XML')
        return p_pyhouse_obj.House.Security

    def Start(self):
        self.m_api.Start()
        LOG.info("Started.")

    def SaveXml(self, p_xml):
        l_xml = ET.Element('SecuritySection')
        l_xml.append(XML.write_all_GarageDoors_xml(self.m_pyhouse_obj))
        l_xml.append(XML.write_all_MotionSensors_xml(self.m_pyhouse_obj))
        p_xml.append(l_xml)
        LOG.info("Saved XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
