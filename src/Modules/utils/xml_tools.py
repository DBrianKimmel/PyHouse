"""
-*- test-case-name: PyHouse.src.Modules.util.test.test_xml_tools -*-

@name: PyHouse/src/Modules/utils/xml_tools.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2012-2014 by D. Brian Kimmel
@note: Created on Jun 2, 2012
@license: MIT License
@summary: Various XML functions and utility methods.

"""

# Import system type stuff
import datetime
import os
import sys
import uuid
from xml.etree import ElementTree as ET

# Import PyMh files
from Modules.utils.tools import PrettyPrintAny
# from Modules.utils import pyh_log

g_debug = 0
# LOG = pyh_log.getLogger('PyHouse.XMLTools     ')


class PutGetXML(object):
    """Protected put / get routines

    Try to be safe if a user edits (and screws up) the XML file.
    """
#-----
# Bool
#-----
    def get_bool_from_xml(self, p_xml, p_name, default = False):
        """Get a boolean from xml - element or attribute

        @param p_xml: is a parent element containing the item we are interested in.
        @param p_name: is the name or path of the item to find.
        @param default: is the default value
        """
        try:
            l_xml = p_xml.find(p_name)  # Element
        except AttributeError as e_err:
            print('XMLTools - GetBool - Name:{0:}, ERROR-AttributeError {1:} - XML:{2:}'.format(p_name, e_err, p_xml))
            return False
        if l_xml == None:
            l_xml = p_xml.get(p_name)  # Attribute
        else:
            l_xml = l_xml.text
        if l_xml == 'True' or l_xml == True:
            return True
        if l_xml == "False" or l_xml == False:
            return False
        else:
            print('XMLTools - GetBool - ERROR invalid bool value found for:{0:} - {1:}=>False'.format(p_name, l_xml))
        return False

    def put_bool_attribute(self, p_xml_element, p_bool = 'False'):
        l_bool = 'False'
        if p_bool == True or p_bool == 'True':
            l_bool = 'True'
        p_xml_element.put(l_bool)

    def put_bool_element(self, p_parent_xml, p_name, p_bool = 'False'):
        l_bool = 'False'
        if p_bool == True or p_bool == 'True':
            l_bool = 'True'
        ET.SubElement(p_parent_xml, p_name).text = l_bool

#-----
# float
#-----
    def get_float_from_xml(self, p_xml, p_name, p_default = 0.0):
        try:
            l_xml = p_xml.find(p_name)  # Element
        except AttributeError:
            return None
        if l_xml == None:
            l_xml = p_xml.get(p_name)  # Attribute
        else:
            l_xml = l_xml.text
        try:
            l_var = float(l_xml)
        except (ValueError, TypeError):
            l_var = p_default
        return l_var

    def put_float_attribute(self, p_xml_element, p_name, p_float):
        try:
            l_var = str(p_float)
        except (ValueError, TypeError):
            l_var = '0.0'
        p_xml_element.set(p_name, l_var)

    def put_float_element(self, p_parent_element, p_name, p_float):
        try:
            l_var = str(p_float)
        except (ValueError, TypeError):
            l_var = '0.0'
        ET.SubElement(p_parent_element, p_name).text = l_var

#-----
# int
#-----
    def get_int_from_xml(self, p_xml, p_name, p_default = 0):
        try:
            l_xml = p_xml.find(p_name)  # Element
        except AttributeError:
            return None
        if l_xml == None:
            l_xml = p_xml.get(p_name, p_default)  # Attribute
        else:
            l_xml = l_xml.text
        try:
            l_var = int(l_xml)
        except (ValueError, TypeError):
            l_var = p_default
        return l_var

    def put_int_attribute(self, p_xml_element, p_name, p_int):
        try:
            l_var = str(p_int)
        except (ValueError, TypeError):
            l_var = '0'
        p_xml_element.set(p_name, l_var)

    def put_int_element(self, p_parent_element, p_name, p_int):
        try:
            l_var = str(p_int)
        except (ValueError, TypeError):
            l_var = '0'
        ET.SubElement(p_parent_element, p_name).text = l_var

#-----
# text
#-----
    def get_text_from_xml(self, p_xml, p_name, default = 'No Text'):
        # print('XmlTools - GetText - Name:{0:} - {1:}'.format(p_name, default))
        try:
            l_xml = p_xml.find(p_name)  # Element
        except AttributeError as e_err:
            print('XMLTools - getText - Name:{0:}, ERROR-AttributeError {1:} - XML:{2:}'.format(p_name, e_err, p_xml))
            return None
        if l_xml == None:
            l_xml = p_xml.get(p_name, default)  # Attribute
        else:
            l_xml = l_xml.text
            # l_xml = default
        try:
            l_var = str(l_xml)
        except (ValueError, TypeError):
            l_var = str(default)
        return l_var

    def put_text_attribute(self, p_element, p_name, p_text):
        try:
            l_var = str(p_text)
        except (ValueError, TypeError):
            l_var = ''
        p_element.set(p_name, l_var)

    def put_text_element(self, p_parent_element, p_name, p_text):
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
# UUID
#-----
    def get_uuid_from_xml(self, p_xml, p_name):
        """Always return an UUID - generate one if it is missing.
        """
        try:
            l_xml = p_xml.find(p_name)
        except AttributeError:
            return None
        if l_xml == None:
            l_xml = str(p_xml.get(p_name))
        else:
            l_xml = str(l_xml.text)
        if len(l_xml) < 8:
            l_xml = str(uuid.uuid1())
        return l_xml

    def put_str(self, p_obj):
        try:
            l_var = str(p_obj)
        except AttributeError:
            l_var = 'no str value'
        return l_var

    def put_bool(self, p_arg):
        l_text = 'False'
        if p_arg != False: l_text = 'True'
        return l_text


class XmlConfigTools(PutGetXML):

    def read_base_object_xml(self, p_base_obj, p_entry_element_xml):
        """Get the BaseObject entries from the XML element.
        Note that a UUID will be generated if one does not exist.

        @param p_base_obj: is the object into which we will put the data.
        @param p_entry_element_xml: is the element we will extract data from (including children).
        """
        try:
            p_base_obj.Name = self.get_text_from_xml(p_entry_element_xml, 'Name', 'Missing Name')
            p_base_obj.Key = self.get_int_from_xml(p_entry_element_xml, 'Key', 0)
            p_base_obj.Active = self.get_bool_from_xml(p_entry_element_xml, 'Active', False)
            p_base_obj.UUID = self.get_uuid_from_xml(p_entry_element_xml, 'UUID')
        except Exception as e_err:
            print('Read error in read_base_obj - {0:}'.format(e_err))

    def write_base_object_xml(self, p_element_name, p_object):
        """
        Note that UUID is optional.
        """
        l_elem = ET.Element(p_element_name)
        try:
            l_elem.set('Active', self.put_bool(p_object.Active))
        except AttributeError:
            l_elem.set('Active', self.put_bool(True))
        try:
            l_elem.set('Name', p_object.Name)
        except AttributeError:
            l_elem.set('Name', self.put_str('No Name Given'))
        try:
            l_elem.set('Key', str(p_object.Key))
        except AttributeError:
            l_elem.set('Key', '123456')

        try:
            self.put_text_element(l_elem, 'UUID', p_object.UUID)
        except AttributeError as e_err:
            self.put_text_element(l_elem, 'UUID', 'No UUID Given')
            # print('ERROR in writeBaseObj {0:} {1:}'.format(e_err, PrettyPrintAny(p_object, 'Error in writeBaseObj', 120)))
            print('ERROR in writeBaseObj {0:}'.format(e_err))
        return l_elem


def stuff_new_attrs(p_target_obj, p_data_obj):
    """Put the NEW information from the data object into the target object.
    Preserve any attributes already in the target object.
    Skip system '__' and private '_' attributes
    """
    l_attrs = filter(lambda aname: not aname.startswith('_'), dir(p_data_obj))
    for l_attr in l_attrs:
        if not hasattr(p_target_obj, l_attr):
            setattr(p_target_obj, l_attr, getattr(p_data_obj, l_attr))

# ## END
