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
from xml.dom import minidom

# Import PyMh files
from Modules.utils.tools import PrettyPrintAny

g_debug = 0


class PutGetXML(object):
    """Protected put / get routines

    Try to be safe if a user edits (and screws up) the XML file.
    """
#-----
# Bool
#-----
    def get_bool_from_xml(self, p_xml, p_name, p_default = False):
        """Get a boolean from xml - element or attribute

        @param p_xml: is a parent element containing the item we are interested in.
        @param p_name: is the name or path of the item to find.
        @param p_default: is the default value
        """
        try:
            l_xml = p_xml.find(p_name)  # Element
        except AttributeError:
            return None
        if l_xml == None:
            l_xml = p_xml.get(p_name)  # Attribute
        else:
            l_xml = l_xml.text
        l_ret = p_default
        if l_xml == 'True' or l_xml == True:
            l_ret = True
        if l_xml == "False" or l_xml == False:
            l_ret = False
        return l_ret

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
    def get_text_from_xml(self, p_xml, p_name, p_default = 'No Text'):
        try:
            l_xml = p_xml.find(p_name)  # Element
        except AttributeError:
            return None
        if l_xml == None:
            l_xml = p_xml.get(p_name, p_default)  # Attribute
        else:
            l_xml = l_xml.text
            # l_xml = p_default
        try:
            l_var = str(l_xml)
        except (ValueError, TypeError):
            l_var = str(p_default)
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


class ConfigTools(PutGetXML):

    def read_base_object_xml(self, p_base_obj, p_entry_element_xml):
        """Get the BaseObject entries from the XML element.
        Note that a UUID will be generated if one does not exist.

        @param p_base_obj: is the object into which we will put the data.
        @param p_entry_element_xml: is the element we will extract data from (including children).
        """
        p_base_obj.Name = self.get_text_from_xml(p_entry_element_xml, 'Name')
        p_base_obj.Key = self.get_int_from_xml(p_entry_element_xml, 'Key')
        p_base_obj.Active = self.get_bool_from_xml(p_entry_element_xml, 'Active')
        p_base_obj.UUID = self.get_uuid_from_xml(p_entry_element_xml, 'UUID')

    def write_base_object_xml(self, p_element_name, p_object):
        try:
            l_elem = ET.Element(p_element_name)
            l_elem.set('Active', self.put_bool(p_object.Active))
            l_elem.set('Name', p_object.Name)
            l_elem.set('Key', str(p_object.Key))
            self.put_text_element(l_elem, 'UUID', p_object.UUID)
        except AttributeError as e_error:
            print('ERROR in writeBaseObj {0:} {1:}'.format(e_error, PrettyPrintAny(p_object, 'Error in writeBaseObj')))
        return l_elem


class ConfigFile(PutGetXML):

    m_std_path = '/etc/pyhouse/', '~/.PyHouse/', '/var/PyHouse/'
    m_std_name = 'master.xml'

    def create_find_config_dir(self):
        """Check for directory existance.  If not, try creating one.
        If we can't create one, return a failure.

        @return: the path we created or found
        """
        for l_dir in self.m_std_path:
            l_dir = os.path.expanduser(l_dir)
            if os.path.exists(l_dir):
                return l_dir
        for l_dir in self.m_std_path:
            l_dir = os.path.expanduser(l_dir)
            try:
                os.mkdir(l_dir)
                return l_dir
            except OSError:
                pass
        print("Could not create any of the following {0:}".format(self.m_std_path))
        sys.exit(1)

    def find_config_file(self, p_dir):
        """Add a file name to the passed in dir to get the config file.
        """
        l_file_name = os.path.join(p_dir, self.m_std_name)
        try:
            open(l_file_name, mode = 'r')
        except IOError:
            self.create_empty_config_file(l_file_name)
        return l_file_name

    def create_empty_config_file(self, p_name):
        """Create an empty skeleton XML config file.

        @param p_name: the complete path and filename to create.
        """
        l_top = ET.Element('PyHouse')
        l_comment = ET.Comment('Generated by PyHouse {0:}'.format(datetime.datetime.now()))
        l_top.append(l_comment)
        open(os.path.expanduser(p_name), 'w')
        l_nice = PrettyPrintAny(l_top, 'XML_Tools - Create empty file')
        print(l_nice)
        ET.ElementTree(l_top).write(p_name)

    def XXXwrite_xml_file(self, p_xmltree, p_filename = ''):
        p_xmltree.write(p_filename, xml_declaration = True)


def stuff_new_attrs(p_target_obj, p_data_obj):
    """Put the NEW information from the data object into the target object.
    Preserve any attributes already in the target object.
    Skip system '__' and private '_' attributes
    """
    l_attrs = filter(lambda aname: not aname.startswith('_'), dir(p_data_obj))
    for l_attr in l_attrs:
        if not hasattr(p_target_obj, l_attr):
            setattr(p_target_obj, l_attr, getattr(p_data_obj, l_attr))

def open_config_file():
    """Open the master XML config file.

    If the file is not found, create a skeleton xml file to be populated by the user via the GUI.

    Search in several standard places for the config file;
    if not found create it after checking for read write permissions.

    @return: the open file name
    """
    l_cf = ConfigFile()
    l_dir = l_cf.create_find_config_dir()
    l_file_name = l_cf.find_config_file(l_dir)
    try:
        open(l_file_name, mode = 'r')
    except Exception as e:  # IOError:
        print(" -- Error in open_config_file {0:}".format(e))
        l_file_name = '/etc/pyhouse/master.xml'
        l_file_name = os.path.expanduser(l_file_name)
        ConfigFile().create_empty_config_file(l_file_name)
    # print('open_config_file {0:}'.format(l_file_name))
    return l_file_name

def write_xml_file(p_xmltree, p_filename):
    PrettyPrintAny(p_xmltree, 'XML_Tools - write_xml_file')
    l_tree = ET.ElementTree()
    l_tree._setroot(p_xmltree)
    l_tree.write(p_filename, xml_declaration = True)

# ## END
