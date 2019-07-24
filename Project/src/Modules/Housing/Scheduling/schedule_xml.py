"""
@name:      Modules/Housing/Scheduling/schedule_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 2, 2013
@summary:   Schedule events

"""

__updated__ = '2019-07-09'

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files
from Modules.Core.data_objects import ScheduleBaseData, ScheduleIrrigationData, ScheduleLightData
from Modules.Core.Utilities.xml_tools import XmlConfigTools, PutGetXML, stuff_new_attrs
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.ScheduleXml ')
SCHEDULE_SECTION = 'ScheduleSection'
SCHEDULE_ATTR = 'Schedule'


class Xml(object):

    @staticmethod
    def _read_one_base_schedule(p_schedule_element):
        """Extract schedule information from a Base schedule xml element.

        ScheduleBaseData()
        """
        l_obj = ScheduleBaseData()
        XmlConfigTools.read_base_UUID_object_xml(l_obj, p_schedule_element)
        l_obj.DayOfWeek = PutGetXML.get_int_from_xml(p_schedule_element, 'DayOfWeek', '127')
        l_obj.ScheduleMode = PutGetXML.get_text_from_xml(p_schedule_element, 'ScheduleMode', 'Default Mode')
        l_obj.ScheduleType = PutGetXML.get_text_from_xml(p_schedule_element, 'ScheduleType')
        l_obj.Time = PutGetXML.get_text_from_xml(p_schedule_element, 'Time')
        # if l_obj.ScheduleType == 'LightingDevice':
        #    l_obj.ScheduleType = 'Lighting'
        return l_obj

    @staticmethod
    def _read_one_irrigation_schedule(p_schedule_element):
        """Extract schedule information from a schedule xml element.
        """
        l_obj = ScheduleIrrigationData()
        l_obj.System = PutGetXML.get_text_from_xml(p_schedule_element, 'System')
        l_obj.SystemUUID = None
        l_obj.Duration = PutGetXML.get_int_from_xml(p_schedule_element, 'Duration')
        return l_obj

    @staticmethod
    def _read_one_lighting_schedule(p_schedule_element):
        """Extract schedule information from a schedule xml element.
        """
        l_obj = ScheduleLightData()
        l_obj.Level = PutGetXML.get_int_from_xml(p_schedule_element, 'Level')
        l_obj.LightName = PutGetXML.get_text_from_xml(p_schedule_element, 'LightName')
        l_obj.LightUUID = PutGetXML.get_uuid_from_xml(p_schedule_element, 'LightUUID')
        l_obj.Rate = PutGetXML.get_int_from_xml(p_schedule_element, 'Rate')
        l_obj.RoomName = PutGetXML.get_text_from_xml(p_schedule_element, 'RoomName')
        l_obj.RoomUUID = PutGetXML.get_uuid_from_xml(p_schedule_element, 'RoomUUID')
        return l_obj

    @staticmethod
    def _read_one_schedule(p_schedule_element):
        l_obj = Xml._read_one_base_schedule(p_schedule_element)
        if l_obj.ScheduleType == 'Lighting':
            l_type = Xml._read_one_lighting_schedule(p_schedule_element)
        elif l_obj.ScheduleType == 'Irrigation':
            l_type = Xml._read_one_irrigation_schedule(p_schedule_element)
        else:
            LOG.error('ERROR - invalid ScheduleType found - "{}" for Schedule "{}"({})'.format(l_obj.ScheduleType, l_obj.Name), l_obj.Key)
            l_type = {}
        stuff_new_attrs(l_obj, l_type)
        return l_obj

    @staticmethod
    def read_schedules_xml(p_pyhouse_obj):
        """
        @param p_pyhouse_obj: is the big object of everything
        @return: a dict of all the schedules.
        """
        l_count = 0
        l_dict = {}
        l_xml = XmlConfigTools.find_xml_section(p_pyhouse_obj, 'HouseDivision')
        if l_xml is None:
            return l_dict
        l_xml = l_xml.find(SCHEDULE_SECTION)
        if l_xml is None:
            return l_dict
        try:
            for l_entry in l_xml.iterfind(SCHEDULE_ATTR):
                l_schedule_obj = Xml._read_one_schedule(l_entry)
                l_schedule_obj.Key = l_count  # Renumber
                l_dict[l_count] = l_schedule_obj
                l_count += 1
        except AttributeError as e_err:
            LOG.error('ERROR in schedule.read_schedules_xml() - {}'.format(e_err))
        return l_dict

    @staticmethod
    def _write_one_base_schedule(p_schedule_obj):
        """
        """
        l_entry = XmlConfigTools.write_base_UUID_object_xml(SCHEDULE_ATTR, p_schedule_obj)
        PutGetXML.put_int_element(l_entry, 'DayOfWeek', int(p_schedule_obj.DayOfWeek))
        PutGetXML.put_text_element(l_entry, 'ScheduleMode', p_schedule_obj.ScheduleMode)
        PutGetXML.put_text_element(l_entry, 'ScheduleType', p_schedule_obj.ScheduleType)
        PutGetXML.put_text_element(l_entry, 'Time', p_schedule_obj.Time)
        return l_entry

    @staticmethod
    def _write_one_irrigation_schedule(p_schedule_obj, p_entry):
        """
        Shove our entries in.
        """
        PutGetXML.put_int_element(p_entry, 'Duration', p_schedule_obj.Duration)

    @staticmethod
    def _write_one_light_schedule(p_schedule_obj, p_entry):
        """
        Shove our entries in.
        """
        PutGetXML.put_int_element(p_entry, 'Level', p_schedule_obj.Level)
        PutGetXML.put_text_element(p_entry, 'LightName', p_schedule_obj.LightName)
        PutGetXML.put_text_element(p_entry, 'LightUUID', p_schedule_obj.LightUUID)
        PutGetXML.put_int_element(p_entry, 'Rate', p_schedule_obj.Rate)
        PutGetXML.put_text_element(p_entry, 'RoomName', p_schedule_obj.RoomName)
        PutGetXML.put_text_element(p_entry, 'RoomUUID', p_schedule_obj.RoomUUID)

    @staticmethod
    def _write_one_schedule(p_schedule_obj):
        """
        """
        l_entry = Xml._write_one_base_schedule(p_schedule_obj)
        if p_schedule_obj.ScheduleType == 'Lighting':
            Xml._write_one_light_schedule(p_schedule_obj, l_entry)
        elif p_schedule_obj.ScheduleType == 'Irrigation':
            Xml._write_one_irrigation_schedule(p_schedule_obj, l_entry)
        else:
            LOG.error('ERROR - invalid schedule type {}'.format(p_schedule_obj.ScheduleType))
        return l_entry

    @staticmethod
    def write_schedules_xml(p_schedules_obj):
        """Replace all the data in the 'Schedules' section with the current data.
        @param p_parent: is the 'schedules' element
        """
        l_count = 0
        l_xml = ET.Element(SCHEDULE_SECTION)
        try:
            for l_schedule_obj in p_schedules_obj.values():
                l_entry = Xml._write_one_schedule(l_schedule_obj)
                l_xml.append(l_entry)
                l_count += 1
        except AttributeError as e_err:
            LOG.error('Attr err {}'.format(e_err))
        return l_xml, l_count

#  ## END DBK
