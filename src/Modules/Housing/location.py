"""
-*- test-case-name: PyHouse.src.Modules.Housing.test.test_location -*-

@name:      PyHouse/src/Modules/Housing/location.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Handle the location information for a house.

There is location information for the house.  This is for calculating the
time of sunrise and sunset.  Additional calculations may be added such
moon rise, tides, etc.
"""

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files
from Modules.Core.data_objects import LocationData, RiseSetData
from Modules.Core.Utilities.xml_tools import PutGetXML
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Location       ')


class Xml(object):
    """Use the internal data to read / write an updated XML config file.
    """

    @staticmethod
    def read_location_xml(p_pyhouse_obj):
        """
        @param p_house_xml: is the config file xml for a house.
        """
        l_obj = LocationData()
        l_obj.RiseSet = RiseSetData()
        p_pyhouse_obj.House.Location = l_obj
        try:
            l_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision')
            if l_xml is None:
                return l_obj
            l_xml = l_xml.find('LocationSection')
            if l_xml is None:
                return l_obj
            l_obj.Street = PutGetXML.get_text_from_xml(l_xml, 'Street')
            l_obj.City = PutGetXML.get_text_from_xml(l_xml, 'City')
            l_obj.State = PutGetXML.get_text_from_xml(l_xml, 'State')
            l_obj.ZipCode = PutGetXML.get_text_from_xml(l_xml, 'ZipCode', '99999')
            l_obj.Region = PutGetXML.get_text_from_xml(l_xml, 'Region', 'America')
            l_obj.Phone = PutGetXML.get_text_from_xml(l_xml, 'Phone')
            l_obj.Latitude = PutGetXML.get_float_from_xml(l_xml, 'Latitude')
            l_obj.Longitude = PutGetXML.get_float_from_xml(l_xml, 'Longitude')
            l_obj.Elevation = PutGetXML.get_float_from_xml(l_xml, 'Elevation', 10)
            l_obj.TimeZoneName = PutGetXML.get_text_from_xml(l_xml, 'TimeZoneName', 'America/New_York')
        except AttributeError as e_err:
            LOG.error('ERROR getting location Data - {}'.format(e_err))
        p_pyhouse_obj.House.Location = l_obj
        LOG.info('Loaded location information.')
        return l_obj

    @staticmethod
    def write_location_xml(p_location_obj):
        """Replace the data in the 'House/Location' section with the current data.
        """
        l_entry = ET.Element('LocationSection')
        PutGetXML.put_text_element(l_entry, 'Street', p_location_obj.Street)
        PutGetXML.put_text_element(l_entry, 'City', p_location_obj.City)
        PutGetXML.put_text_element(l_entry, 'State', p_location_obj.State)
        PutGetXML.put_text_element(l_entry, 'ZipCode', p_location_obj.ZipCode)
        PutGetXML.put_text_element(l_entry, 'Region', p_location_obj.Region)
        PutGetXML.put_text_element(l_entry, 'Phone', p_location_obj.Phone)
        PutGetXML.put_float_element(l_entry, 'Latitude', p_location_obj.Latitude)
        PutGetXML.put_float_element(l_entry, 'Longitude', p_location_obj.Longitude)
        PutGetXML.put_float_element(l_entry, 'Elevation', p_location_obj.Elevation)
        PutGetXML.put_text_element(l_entry, 'TimeZoneName', p_location_obj.TimeZoneName)
        LOG.info('Saved Location XML')
        return l_entry

#  ## END DBK
