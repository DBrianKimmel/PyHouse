#!/usr/bin/env python

"""This module used to access or create an empty config file.1
0
"""

# Import system type stuff
import datetime
import os
import sys
import uuid
from xml.etree import ElementTree as ET
from xml.dom import minidom

# Import PyMh files


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 - Config file handling
# 4 = Debug do get_xxx_element
# + = NOT USED HERE
g_xmltree = None


class XmlFileTools(object):

    def __init__(self):
        """Open the xml config file.

        If the file is missing, an empty minimal skeleton is created.
        """
        if g_debug >= 2:
            print "xml_tools.XmlFileTools()"
        global g_xmltree
        self.m_xml_filename = open_config_file()
        try:
            g_xmltree = ET.parse(self.m_xml_filename)
        except SyntaxError:
            ConfigFile().create_empty_config_file(self.m_xml_filename)
            g_xmltree = ET.parse(self.m_xml_filename)
        self.m_xmltree_root = g_xmltree.getroot()


class PutGetXML(XmlFileTools):
    """Protected put / get routines

    Try to be safe if a user edits the XML file.
    """
#-----
# Bool
#-----
    def get_bool_from_xml(self, p_xml, p_name):
        l_xml = p_xml.find(p_name)
        if l_xml == None:
            l_xml = p_xml.get(p_name)
        else:
            l_xml = l_xml.text
        l_ret = False
        if l_xml == 'True' or l_xml == True:
            l_ret = True
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
    def get_float_from_xml(self, p_xml, p_name):
        l_xml = p_xml.find(p_name)
        if l_xml == None:
            l_xml = p_xml.get(p_name)
        else:
            l_xml = l_xml.text
        try:
            l_var = float(l_xml)
        except (ValueError, TypeError):
            l_var = 0.0
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
    def get_int_from_xml(self, p_xml, p_name):
        l_xml = p_xml.find(p_name)
        if l_xml == None:
            l_xml = p_xml.get(p_name)
        else:
            l_xml = l_xml.text
        try:
            l_var = int(l_xml)
        except (ValueError, TypeError):
            l_var = 0
        if g_debug >= 4:
            print "xml_tools.get_int_from_xml() Int:'{0:}'".format(l_var)
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
    def get_text_from_xml(self, p_xml, p_name):
        l_xml = p_xml.find(p_name)
        if l_xml == None:
            l_xml = p_xml.get(p_name)
        else:
            l_xml = l_xml.text
        return str(l_xml)

    def put_text_attribute(self, p_element, p_name, p_text):
        try:
            l_var = str(p_text)
        except (ValueError, TypeError):
            l_var = ''
        p_element.set(p_name, l_var)

    def put_text_element(self, p_parent_element, p_name, p_text):
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
        l_xml = p_xml.find(p_name)
        if l_xml == None:
            l_xml = str(p_xml.get(p_name))
        else:
            l_xml = str(l_xml.text)
        if len(l_xml) < 8:
            l_xml = str(uuid.uuid1())
        return l_xml

#-----

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

    def xml_create_common_element(self, p_title, p_obj):
        """Build a common entry.
        """
        if g_debug >= 3:
            print "xml_tools.xml_create_common_element() - Title:{0:}, Name:{1:} ".format(p_title, p_obj.Name)
        l_elem = ET.Element(p_title)
        l_elem.set('Name', p_obj.Name)
        l_elem.set('Key', str(p_obj.Key))
        l_elem.set('Active', self.put_bool(p_obj.Active))
        return l_elem

    def xml_read_common_info(self, p_obj, p_entry_xml):
        """Get the common (Name, Key, Active) information from an XML sub-tree.

        @param p_obj: is the object we are updating the common information for.
        @param p_entry_xml: is the XML subtree that we are extracting the information from.
        """
        if g_debug >= 3:
            print "xml_tools.xml_read_common_info()", p_entry_xml, p_entry_xml.items()
        p_obj.Name = self.get_text_from_xml(p_entry_xml, 'Name')
        p_obj.Key = self.get_int_from_xml(p_entry_xml, 'Key')
        p_obj.Active = self.get_bool_from_xml(p_entry_xml, 'Active')
        if g_debug >= 3:
            print "    Name:{0:}, Key:{1:}, Active:{2:}".format(p_obj.Name, p_obj.Key, p_obj.Active)


class ConfigEtc(ConfigTools):
    '''
    classdocs
    '''

    def __init__(self):
        pass

    def find_etc_config_file(self):
        """Check for /etc/pyhouse.conf existence.
        If not, ABORT and do not become a daemon.

        @return: the filename we found.
        """
        if g_debug >= 2:
            print "config_etc.find_etc_config_file()"
        l_file_name = 'C:/etc/pyhouse.conf'
        try:
            l_file = open(l_file_name, mode = 'r')
        except IOError:
            self.config_abort()
        l_text = l_file.readlines()
        for l_line in l_text:
            if l_line == '':
                continue
            elif l_line[0] == '#':
                continue
            else:
                l_ret = l_line
                if g_debug >= 3:
                    print "config_etc.find_etc_config_file() found", l_ret
                return l_ret
        return None

    def config_abort(self):
        print "Could not find or read '/etc/pyhouse.conf'.  Please create it and rerun PyHouse!"
        sys.exit(1)


class ConfigFile(ConfigEtc):

    m_std_path = '/etc/pyhouse/', '~/.PyHouse/', '/var/PyHouse/'
    m_std_name = 'PyHouse.xml'

    def __init__(self):
        pass

    def create_find_config_dir(self):
        """Check for directory existance.  If not, try creating one.
        If we can't create one, return a failure.

        @return: the path we created or found
        """
        if g_debug >= 3:
            print "xml_tools create_find_config_dir"
        for l_dir in self.m_std_path:
            l_dir = os.path.expanduser(l_dir)
            if os.path.exists(l_dir):
                if g_debug >= 3:
                    print "xml_tools.create_find_config_dir() - Found:{0:}".format(l_dir)
                return l_dir
        print "No directory found, try creating one."
        for l_dir in self.m_std_path:
            l_dir = os.path.expanduser(l_dir)
            try:
                os.mkdir(l_dir)
                if g_debug >= 3:
                    print "xml_tools.create_find_config_dir() - Created:{0:}".format(l_dir)
                return l_dir
            except OSError:
                pass
        print "Could not create any of the following ", self.m_std_path
        sys.exit(1)

    def find_config_file(self, p_dir):
        """Add a file name to the passed in dir to get the config file.
        """
        if g_debug >= 3:
            print "xml_tools find_config_file()"
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
        if g_debug >= 3:
            print "xml_tools create_empty_config_file"
        l_top = ET.Element('PyHouse')
        l_comment = ET.Comment('Generated by PyHouse {0:}'.format(datetime.datetime.now()))
        l_top.append(l_comment)
        open(os.path.expanduser(p_name), 'w')
        l_nice = prettify(l_top)
        print l_nice
        ET.ElementTree(l_top).write(p_name)

    def write_xml_file(self, p_xmltree, p_filename = ''):
        if g_debug >= 2:
            print "xml_tools.write_xml_file() Filename:{0:}".format(p_filename)
        p_xmltree.write(p_filename, xml_declaration = True)


def prettify(p_element):
    """Return a pretty-printed XML string for the Element.

    @param p_element: an element to format as a readable XML tree.
    @return: a string formatted with indentation and newlines.
    """
    if g_debug >= 3:
        print "xml_tools.pretify()"
    rough_string = ET.tostring(p_element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent = "    ")

def open_config_file():
    """Open the PyHouse config xml file.

    If the file is not found, create a skeleton xml file to be populated by the user via the GUI.

    Search in several standard places for the config file;
    if not found create it after checking for read write permissions.

    @return: the open file name
    """
    if g_debug >= 1:
        print "xml_tools.open_config_file()"
    l_cf = ConfigFile()
    l_dir = l_cf.create_find_config_dir()
    l_file_name = l_cf.find_config_file(l_dir)
    try:
        open(l_file_name, mode = 'r')
    except Exception, e:  # IOError:
        print " -- Error in open_config_file ", sys.exc_info(), e
        l_file_name = '~/.PyHouse/PyHouse.xml'
        l_file_name = os.path.expanduser(l_file_name)
        ConfigFile().create_empty_config_file(l_file_name)
    return l_file_name

def write_xml_file(p_xmltree, p_filename):
    if g_debug >= 2:
        print "xml_tools.write_xml_file() Filename:{0:}".format(p_filename)
    l_tree = ET.ElementTree()
    l_tree._setroot(p_xmltree)
    l_tree.write(p_filename, xml_declaration = True)

# ## END
