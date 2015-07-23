"""
-*- test-case-name: PyHouse.src.Modules.Housing.test.test_location -*-

@name:      PyHouse/src/Modules/Housing/location.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Apr 10, 2013
@summary:   Handle the location information for a house.

There is location information for the house.  This is for calculating the
time of sunrise and sunset.  Additional calculations may be added such
moon rise, tides, etc.
"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import LocationData, RiseSetData
from Modules.Utilities.xml_tools import PutGetXML, XmlConfigTools
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Location       ')


class Xml(object):
    """Use the internal data to read / write an updated XML config file.
    """

    @staticmethod
    def read_location_xml(p_house_xml):
        """
        @param p_house_xml: is the config file xml for a house.
        """
        l_obj = LocationData()
        l_obj.RiseSet = RiseSetData()
        try:
            l_location_xml = p_house_xml.find('LocationSection')
            l_obj.Street = PutGetXML.get_text_from_xml(l_location_xml, 'Street')
            l_obj.City = PutGetXML.get_text_from_xml(l_location_xml, 'City')
            l_obj.State = PutGetXML.get_text_from_xml(l_location_xml, 'State')
            l_obj.ZipCode = PutGetXML.get_text_from_xml(l_location_xml, 'ZipCode')
            l_obj.Phone = PutGetXML.get_text_from_xml(l_location_xml, 'Phone')
            l_obj.Latitude = PutGetXML.get_float_from_xml(l_location_xml, 'Latitude')
            l_obj.Longitude = PutGetXML.get_float_from_xml(l_location_xml, 'Longitude')
            l_obj.TimeZoneName = PutGetXML.get_text_from_xml(l_location_xml, 'TimeZoneName')
        except AttributeError as e_err:
            LOG.error('ERROR if getting location Data - {}'.format(e_err))
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
        PutGetXML.put_text_element(l_entry, 'Phone', p_location_obj.Phone)
        PutGetXML.put_float_element(l_entry, 'Latitude', p_location_obj.Latitude)
        PutGetXML.put_float_element(l_entry, 'Longitude', p_location_obj.Longitude)
        PutGetXML.put_text_element(l_entry, 'TimeZoneName', p_location_obj.TimeZoneName)
        LOG.info('Saved Location XML')
        return l_entry

# ## END DBK
