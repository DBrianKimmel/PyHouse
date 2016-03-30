"""
-*- test-case-name: PyHouse.src.Modules.Scheduling.test.test_schedule_xml -*-

@name:      PyHouse/src/Modules/Scheduling/schedule_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 2, 2013
@summary:   Schedule events

"""

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files
from Modules.Core.data_objects import ScheduleBaseData, ScheduleLightData
from Modules.Utilities.xml_tools import XmlConfigTools, PutGetXML, stuff_new_attrs
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.ScheduleXml ')


class Xml(object):

    @staticmethod
    def _read_one_lighting_schedule(p_schedule_element):
        """Extract schedule information from a schedule xml element.
        """
        l_obj = ScheduleLightData()
        l_obj.Level = PutGetXML.get_int_from_xml(p_schedule_element, 'Level')
        l_obj.LightName = PutGetXML.get_text_from_xml(p_schedule_element, 'LightName')
        l_obj.Rate = PutGetXML.get_int_from_xml(p_schedule_element, 'Rate')
        l_obj.RoomName = PutGetXML.get_text_from_xml(p_schedule_element, 'RoomName')
        return l_obj  #  for testing

    @staticmethod
    def _read_one_base_schedule(p_schedule_element):
        """Extract schedule information from a schedule xml element.
        """
        l_obj = ScheduleBaseData()
        XmlConfigTools.read_base_object_xml(l_obj, p_schedule_element)
        l_obj.Time = PutGetXML.get_text_from_xml(p_schedule_element, 'Time')
        l_obj.ScheduleType = PutGetXML.get_text_from_xml(p_schedule_element, 'ScheduleType')
        if l_obj.ScheduleType == 'LightingDevice':
            l_obj.ScheduleType = 'Lighting'
        try:
            l_obj.DOW = PutGetXML.get_int_from_xml(l_obj, 'DayOfWeek', 0x7F)
        except:
            l_obj.DOW = 0x7F
        try:
            l_obj.Mode = PutGetXML.get_int_from_xml(l_obj, 'Mode', 0)
        except:
            l_obj.Mode = 0
        return l_obj

    @staticmethod
    def _read_one_schedule(p_schedule_element):
        l_obj = Xml._read_one_base_schedule(p_schedule_element)
        if l_obj.ScheduleType == 'Lighting':
            l_type = Xml._read_one_lighting_schedule(p_schedule_element)
        else:
            LOG.error('ERROR - invalid device found - {} for {}'.format(l_obj.ScheduleType, l_obj.Name))
            l_type = {}
        stuff_new_attrs(l_obj, l_type)
        return l_obj

    @staticmethod
    def read_schedules_xml(p_pyhouse_obj):
        """
        @param p_house_xml: is the e-tree XML house object
        @return: a dict of the entry to be attached to a house object.
        """
        l_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
        l_count = 0
        l_dict = {}
        try:
            l_xml = l_xml.find('ScheduleSection')
            if l_xml == None:
                return l_dict
            for l_entry in l_xml.iterfind('Schedule'):
                l_schedule_obj = Xml._read_one_schedule(l_entry)
                l_schedule_obj.Key = l_count  #  Renumber
                l_dict[l_count] = l_schedule_obj
                l_count += 1
        except AttributeError as e_err:
            LOG.error('ERROR in schedule.read_schedules_xml() - {0:}'.format(e_err))
        return l_dict


    @staticmethod
    def _write_one_base_schedule(p_schedule_obj):
        """
        """
        l_entry = XmlConfigTools.write_base_object_xml('Schedule', p_schedule_obj)
        PutGetXML.put_text_element(l_entry, 'ScheduleType', p_schedule_obj.ScheduleType)
        PutGetXML.put_text_element(l_entry, 'Time', p_schedule_obj.Time)
        PutGetXML.put_int_element(l_entry, 'DayOfWeek', int(p_schedule_obj.DOW))
        PutGetXML.put_int_element(l_entry, 'Mode', p_schedule_obj.Mode)
        return l_entry

    @staticmethod
    def _write_one_light_schedule(p_schedule_obj, p_entry):
        """
        Shove our entries in.
        """
        PutGetXML.put_int_element(p_entry, 'Level', p_schedule_obj.Level)
        PutGetXML.put_text_element(p_entry, 'LightName', p_schedule_obj.LightName)
        PutGetXML.put_int_element(p_entry, 'Rate', p_schedule_obj.Rate)
        PutGetXML.put_text_element(p_entry, 'RoomName', p_schedule_obj.RoomName)

    @staticmethod
    def _write_one_schedule(p_schedule_obj):
        """
        """
        l_entry = Xml._write_one_base_schedule(p_schedule_obj)
        if p_schedule_obj.ScheduleType == 'Lighting':
            Xml._write_one_light_schedule(p_schedule_obj, l_entry)
        else:
            LOG.error('ERROR - invalid schedule type {}'.format(p_schedule_obj.ScheduleType))
        return l_entry

    @staticmethod
    def write_schedules_xml(p_schedules_obj):
        """Replace all the data in the 'Schedules' section with the current data.
        @param p_parent: is the 'schedules' element
        """
        l_count = 0
        l_xml = ET.Element('ScheduleSection')
        try:
            for l_schedule_obj in p_schedules_obj.itervalues():
                l_entry = Xml._write_one_schedule(l_schedule_obj)
                l_xml.append(l_entry)
                l_count += 1
        except AttributeError as e_err:
            LOG.error('Attr err {}'.format(e_err))
        return l_xml, l_count

#  ## END DBK
