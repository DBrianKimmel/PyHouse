"""
@name:      Modules/House/Family/Hue/Hue_config.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2019 by D. Brian Kimmel
@note:      Created on Dec 18, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2019-08-01'

# Import system type stuff

# Import PyMh files
from Modules.Core.Utilities.xml_tools import PutGetXML, stuff_new_attrs
from Modules.House.Family.Hue.Hue_data import HueAddInData

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Hue_xml    ')


class HueInformation:
    """
    """

    def __init__(self):
        self.Family = None
        self.Address = None
        self.Host = None
        self.Port = None


class Config:
    """
    """

    def extract_family_config(self, p_config):
        """
        Device:
           Family:
              Name: Insteon
              Address: 12.34.56

        @param p_config: is the yaml fragment containing the family tree.
        """
        l_obj = InsteonInformation()
        l_required = ['Name', 'Address']
        for l_key, l_value in p_config.items():  # A map
            print('Insteon Family Config Key:{}; Value{}'.format(l_key, l_value))
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.error('Insteon Family config is missing a required entry for "{}"'.format(l_key))
        return l_obj


class Xml(object):
    """ bridges_xml calls these when the
    """

    @staticmethod
    def _read_hue(p_in_xml):
        l_hue_obj = HueAddInData()
        l_hue_obj.ApiKey = PutGetXML.get_text_from_xml(p_in_xml, 'ApiKey')
        return l_hue_obj

    @staticmethod
    def _write_hue(p_xml, p_obj):
        """
        """
        PutGetXML.put_text_element(p_xml, 'ApiKey', p_obj.ApiKey)
        return p_xml  # for testing

    @staticmethod
    def ReadXml(p_device_obj, p_entry_xml):
        """
        A method to extract Hue specific elements and insert them into an Bridge data object.

        We do this to keep the Hue Data encapsulated.

        @param p_device_obj : is the Object that will have the extracted elements inserted into.
        @param p_entry_xml: is the device's XML element
        @return: a dict of the extracted Hue Specific data.
        """
        l_hue_obj = Xml._read_hue(p_entry_xml)
        stuff_new_attrs(p_device_obj, l_hue_obj)
        return p_device_obj  # For testing only

    @staticmethod
    def WriteXml(p_xml, p_obj):
        """
        @param p_xml: is a parent element to which the Hue Specific information is appended.
        @param p_obj: is the object for which we are putting the xml
        """
        Xml._write_hue(p_xml, p_obj)
        return p_xml

# ## END DBK
