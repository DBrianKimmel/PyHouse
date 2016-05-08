"""
-*- test-case-name: PyHouse.src.Modules.Utilities.test.test_xml_tools -*-

@name:      PyHouse/src/Modules/Utilities/xml_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2012-2016 by D. Brian Kimmel
@note:      Created on Jun 2, 2012
@license:   MIT License
@summary:   Various XML functions and utility methods.

"""

#  Import system type stuff
from Modules.Computer import logging_pyh as Logger
from Modules.Core.data_objects import CoordinateData
from Modules.Utilities import convert
from Modules.Utilities.uuid_tools import Uuid
from xml.etree import ElementTree as ET
import dateutil.parser as dparser
import uuid

#  Import PyMh files
#  from formless.annotate import String

LOG = Logger.getLogger('PyHouse.XmlTools       ')


class XML(object):

    @staticmethod
    def get_element_field(p_xml, p_name):
        try:
            l_xml = p_xml.find(p_name).text
        except AttributeError:
            l_xml = None
        return l_xml

    @staticmethod
    def get_attribute_field(p_xml, p_name):
        try:
            l_xml = p_xml.get(p_name)
        except AttributeError:
            l_xml = None
        return l_xml

    @staticmethod
    def get_any_field(p_xml, p_name):
        if p_xml == None:  #  We were passed XML without a tag of p_name
            return None
        l_xml = XML.get_element_field(p_xml, p_name)
        if l_xml == None:
            l_xml = XML.get_attribute_field(p_xml, p_name)
        if l_xml == None:
            if p_xml.tag == p_name:
                l_xml = p_xml.text
        return l_xml


class PutGetXML(object):
    """Protected put / get routines

    Try to be safe if a user edits (and screws up) the XML file.
    """
#-----
#  Bool
#-----
    @staticmethod
    def get_bool_from_xml(p_xml, p_name, _default = False):
        """Get a boolean from xml - element or attribute

        @param p_xml: is a parent element containing the item we are interested in.
        @param p_name: is the name or path of the item to find.
        @param default: is the default value
        @return: A Bool value - True or False
        """
        l_xml = XML.get_any_field(p_xml, p_name)
        if l_xml == 'True' or l_xml == True:
            return True
        if l_xml == "False" or l_xml == False:
            return False
        else:
            LOG.warning('Invalid bool value found for Field:{}; Value: {}==>False; Element:{}'.format(
                            p_name, l_xml, p_xml.tag))
        return False

    @staticmethod
    def put_bool_attribute(p_xml_element, p_name, p_bool = 'False'):
        l_bool = 'False'
        if p_bool == True or p_bool == 'True':
            l_bool = 'True'
        p_xml_element.set(p_name, l_bool)

    @staticmethod
    def put_bool_element(p_parent_xml, p_name, p_bool = 'False'):
        l_bool = 'False'
        if p_bool == True or p_bool == 'True':
            l_bool = 'True'
        ET.SubElement(p_parent_xml, p_name).text = l_bool

#-----
#  float
#-----
    @staticmethod
    def get_float_from_xml(p_xml, p_name, p_default = 0.0):
        l_xml = XML.get_any_field(p_xml, p_name)
        try:
            l_var = float(l_xml)
        except (ValueError, TypeError):
            l_var = float(p_default)
            LOG.warning('invalid float: {}; {}=>0.0'.format(p_name, l_xml))
        return l_var

    @staticmethod
    def put_float_attribute(p_xml_element, p_name, p_float):
        try:
            l_var = str(p_float)
        except (ValueError, TypeError):
            l_var = '0.0'
        p_xml_element.set(p_name, l_var)

    @staticmethod
    def put_float_element(p_parent_element, p_name, p_float):
        try:
            l_var = str(p_float)
        except (ValueError, TypeError):
            l_var = '0.0'
        ET.SubElement(p_parent_element, p_name).text = l_var

#-----
#  int
#-----
    @staticmethod
    def get_int_from_xml(p_xml, p_name, default = 0):
        l_xml = XML.get_any_field(p_xml, p_name)
        if l_xml == None:
            l_xml = default
        try:
            l_var = int(l_xml)
        except (ValueError, TypeError):
            l_var = int(default)
            #  LOG.warning('Invalid Int found for:{} - {}=>False'.format(p_name, l_xml))
        return l_var

    @staticmethod
    def put_int_attribute(p_xml_element, p_name, p_int):
        try:
            l_var = str(p_int)
        except (ValueError, TypeError):
            l_var = '0'
        p_xml_element.set(p_name, l_var)


    @staticmethod
    def put_int_element(p_parent_element, p_name, p_int):
        try:
            l_var = str(p_int)
        except (ValueError, TypeError):
            l_var = '0'
        ET.SubElement(p_parent_element, p_name).text = l_var

#-----
#  text
#-----
    @staticmethod
    def get_text_from_xml(p_xml, p_name, default = None):
        """
        @param p_xml: is the xml where we will find the field
        @param p_name: is the name of the field to fetch
        @return: the text contained in the field
        """
        l_xml = XML.get_any_field(p_xml, p_name)
        if l_xml == None:
            l_xml = default
        try:
            l_var = str(l_xml)
        except (ValueError, TypeError):
            l_var = str(default)
        return l_var

    @staticmethod
    def put_text_attribute(p_element, p_name, p_text):
        try:
            l_var = str(p_text)
        except (ValueError, TypeError):
            l_var = ''
        p_element.set(p_name, l_var)

    @staticmethod
    def put_text_element(p_parent_element, p_name, p_text):
        """
        @param p_parent_element: is the parent of this child element.
        @param p_name: is the name of this element.
        @param p_text: is the value to set into this element.
        """
        try:
            l_var = str(p_text)
        except (ValueError, TypeError):
            l_var = ''
        ET.SubElement(p_parent_element, p_name).text = l_var

#-----
#  UUID
#-----
    @staticmethod
    def get_uuid_from_xml(p_xml, p_name):
        """
        UUIDs are always an element.
        """
        l_xml = XML.get_any_field(p_xml, p_name)
        if l_xml == None:
            return str(uuid.uuid1())
        if len(l_xml) < 36:
            l_xml = str(uuid.uuid1())
            LOG.error("A valid UUID was not found - generating a new one. {}".format(p_xml))
        return l_xml

    @staticmethod
    def put_uuid_element(p_parent_element, p_name, p_uuid):
        """
        @param p_parent_element: is the parent of this child element.
        @param p_name: is the name of this element.
        @param p_text: is the value to set into this element.
        """
        PutGetXML.put_text_element(p_parent_element, p_name, p_uuid)


#-----
#  IP
#-----
    @staticmethod
    def get_ip_from_xml(p_xml, p_name):
        """
        Get either IPv4 or IPv6 from the xml file
        Return a (very) long Integer for the result
        """
        l_field = XML.get_any_field(p_xml, p_name)
        l_long = convert.str_to_long(l_field)
        return l_long

    @staticmethod
    def put_ip_element(p_parent_element, p_name, p_ip):
        pass

#-----
#  DateTime
#-----
    @staticmethod
    def get_date_time_from_xml(p_xml, p_name):
        l_field = XML.get_any_field(p_xml, p_name)
        l_ret = dparser.parse(l_field, fuzzy = True)
        return l_ret

    @staticmethod
    def put_date_time_element(p_parent_element, p_name, p_date_time):
        pass

#-----
#  Coords
#-----
    @staticmethod
    def get_coords_from_xml(p_xml, p_name):
        def _get_float(p_field):
            l_fld = str.strip(p_field, '" ')
            l_fld = str.strip(l_fld, "' ")
            l_flt = float(l_fld)
            return l_flt
        l_ret = CoordinateData()
        l_raw = XML.get_any_field(p_xml, p_name)
        #  LOG.info('Name:{};  Field:{}'.format(p_name, l_raw))
        try:
            l_raw = str.strip(l_raw, ' []')
            l_field = str.split(l_raw, ',')
            l_ret.X_Easting = _get_float(l_field[0])
            l_ret.Y_Northing = _get_float(l_field[1])
            l_ret.Z_Height = _get_float(l_field[2])
        except:
            l_ret.X_Easting = 0.0
            l_ret.Y_Northing = 0.0
            l_ret.Z_Height = 0.0
        return l_ret

    @staticmethod
    def put_coords_element(p_parent_element, p_name, p_coords):
        try:
            l_coord = '[{},{},{}]'.format(p_coords.X_Easting, p_coords.Y_Northing, p_coords.Z_Height)
        except Exception:
            l_coord = '[0.0,0.0,0.0]'
        ET.SubElement(p_parent_element, p_name).text = l_coord


class XmlConfigTools(object):

    @staticmethod
    def read_base_object_xml(p_base_obj, p_entry_element_xml, no_uuid = False):
        """Get the BaseObject entries from the XML element.
        @param p_base_obj: is the object into which we will put the data.
        @param p_entry_element_xml: is the element we will extract data from (including children).
        @return: A base object
        """
        try:
            p_base_obj.Name = PutGetXML.get_text_from_xml(p_entry_element_xml, 'Name')
            p_base_obj.Key = PutGetXML.get_int_from_xml(p_entry_element_xml, 'Key', 0)
            p_base_obj.Active = PutGetXML.get_bool_from_xml(p_entry_element_xml, 'Active', False)
        except Exception as e_err:
            LOG.error('{}'.format(e_err))
        if no_uuid == False:
            try:
                p_base_obj.UUID = PutGetXML.get_uuid_from_xml(p_entry_element_xml, 'UUID')
            except AttributeError:
                LOG.error('UUID missing for {}'.format(p_base_obj.Name))
                p_base_obj.pUUID = Uuid.make_valid('123')
        return p_base_obj

    @staticmethod
    def write_base_object_xml(p_element_name, p_object, no_uuid = False):
        """
        Note that UUID is optional.
        @param p_element_name: is the name of the XML element (Light, Button, etc.)
        @param p_object: is the device object that contains the info to be written.
        @return: An Element with Attributes filled in and perhaps sub-elements attached
        """
        l_elem = ET.Element(p_element_name)
        try:
            PutGetXML.put_text_attribute(l_elem, 'Name', p_object.Name)
            PutGetXML.put_int_attribute(l_elem, 'Key', p_object.Key)
            PutGetXML.put_bool_attribute(l_elem, 'Active', p_object.Active)
        except AttributeError as e_err:
            PutGetXML.put_text_attribute(l_elem, 'Error: ', e_err)
        if not no_uuid:
            try:
                PutGetXML.put_uuid_element(l_elem, 'UUID', p_object.UUID)
            except AttributeError:
                PutGetXML.put_uuid_element(l_elem, 'UUID', 'No UUID Given')
                LOG.error('UUID missing for {}'.format(p_object.Name))
                l_UUID = Uuid.make_valid('123')
                PutGetXML.put_uuid_element(l_elem, 'UUID', l_UUID)
        return l_elem

def stuff_new_attrs(p_target_obj, p_data_obj):
    """
    Put the NEW information from the data object into the target object.
    Preserve any attributes already in the target object.
    Skip system '__' and private '_' attributes

    @param p_target_obj: is the object that eill receive the attrs
    @param p_data_obj: is the obj whose public attrs will be pushed into the target obj
    """
    l_attrs = filter(lambda aname: not aname.startswith('_'), dir(p_data_obj))
    for l_attr in l_attrs:
        if not hasattr(p_target_obj, l_attr):
            setattr(p_target_obj, l_attr, getattr(p_data_obj, l_attr))

def XXXstuff_new_attr_values(p_target_obj, p_data_obj):
    """
    Put the NEW information from the data object into the target object.
    Preserve any attributes already in the target object.
    Skip system '__' and private '_' attributes

    setattr = Set a named attribute on an object; setattr(x, 'y', v) is equivalent to ``x.y = v''.

    @param p_target_obj: is the object that eill receive the attrs
    @param p_data_obj: is the obj whose public attrs will be pushed into the target obj
    """
    l_attrs = filter(lambda aname: not aname.startswith('_'), dir(p_data_obj))
    for l_attr in l_attrs:
        if not hasattr(p_target_obj, l_attr):
            setattr(p_target_obj, l_attr, getattr(p_data_obj, l_attr))

#  ## END
