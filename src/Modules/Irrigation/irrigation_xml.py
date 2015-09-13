"""
-*- test-case-name: PyHouse.src.Modules.Irrigation.test.test_irrigation_xml -*-

@name:      PyHouse/src/Modules/Irrigation/irrigation_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 30, 2015
@Summary:   Read/Write the Irrigation portions of the XML Configuration file.

This is a skeleton until we start the use of the data.  Things are just a placeholder for now.

"""


# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files and modules.
from Modules.Core.data_objects import IrrigationSystemData, IrrigationZoneData
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.xml_tools import PutGetXML, XmlConfigTools

LOG = Logger.getLogger('PyHouse.IrrigationXml  ')
DIVISION = 'HouseDivision'
SECTION = 'IrrigationSection'
SYSTEM = 'IrrigationSystem'
ZONE = 'Zone'


class Xml(object):
    """
    """

    @staticmethod
    def _read_one_zone(p_xml):
        """
        @param p_xml: XML information for one Zone.
        @return: an IrrigationZone object filled in with data from the XML passed in
        """
        l_obj = IrrigationZoneData()
        XmlConfigTools.read_base_object_xml(l_obj, p_xml)
        l_obj.Comment = PutGetXML.get_text_from_xml(p_xml, 'Comment')
        l_obj.Duration = PutGetXML.get_int_from_xml(p_xml, 'Duration', 0)
        # Expand with much more control data
        return l_obj

    @staticmethod
    def _read_one_irrigation_system(p_xml):
        """
        May contain zero or more zones.
        In general each zone is controlled by a solenoid controlled valve.
        """
        l_sys = IrrigationSystemData()
        l_count = 0
        XmlConfigTools.read_base_object_xml(l_sys, p_xml)
        try:
            l_sys.Comment = PutGetXML.get_text_from_xml(p_xml, 'Comment')
            for l_zone in p_xml.iterfind(ZONE):
                l_obj = Xml._read_one_zone(l_zone)
                l_sys.Zones[l_count] = l_obj
                l_count += 1
        except AttributeError as e_err:
            LOG.error('Zone: {}'.format(e_err))
        return l_sys

    @staticmethod
    def read_irrigation_xml(p_pyhouse_obj):
        """
        May contain zero or more irrigation systems.
        Each system may be controlled by a master valve (solenoid).
        Also may need to trigger a well pump solenoid.
        @param p_pyhouse_obj: is the master object containing the XML
        @return: the Irrigation object.
        """
        l_obj = {}
        l_count = 0
        try:
            l_section = p_pyhouse_obj.Xml.XmlRoot.find(DIVISION).find(SECTION)
        except AttributeError as e_err:
            LOG.error('ERROR Reading irrigation information - {}'.format(e_err))
            l_section = None
        try:
            for l_xml in l_section.iterfind(SYSTEM):
                l_system = Xml._read_one_irrigation_system(l_xml)
                l_obj[l_count] = l_system
                l_count += 1
        except AttributeError as e_err:
            LOG.error('irrigationSystem: {}'.format(e_err))
        LOG.info('Loaded {} Irrigation Systems.'.format(l_count))
        return l_obj



    @staticmethod
    def _write_one_zone(p_obj):
        """
        @param p_obj: is one zone object
        @return the XML for one Zone
        """
        l_xml = XmlConfigTools.write_base_object_xml('Zone', p_obj)
        PutGetXML.put_text_element(l_xml, 'Comment', p_obj.Comment)
        PutGetXML.put_int_element(l_xml, 'Duration', p_obj.Duration)
        return l_xml

    @staticmethod
    def _write_one_system(p_obj):
        """
        @param p_obj: is one irrigation system object.
        @return: the XML for one complete IrrigationSystem
        """
        l_xml = XmlConfigTools.write_base_object_xml('IrrigationSystem', p_obj)
        PutGetXML.put_text_element(l_xml, 'Comment', p_obj.Comment)
        for l_obj in p_obj.Zones.itervalues():
            l_zone = Xml._write_one_zone(l_obj)
            l_xml.append(l_zone)
        return l_xml

    @staticmethod
    def write_irrigation_xml(p_obj):
        """
        @param p_obj: is the Irrigation sub-object in p_pyhouse_obj
        @return:  XML for the IrrigationSection
        """
        l_xml = ET.Element(SECTION)
        l_count = 0
        try:
            for l_obj in p_obj.itervalues():
                l_obj.Key = l_count
                l_sys = Xml._write_one_system(l_obj)
                l_xml.append(l_sys)
                l_count += 1
        except AttributeError as e_err:
            LOG.error('Err: {}'.format(e_err))
        return (l_xml, l_count)

# ## END DBK
