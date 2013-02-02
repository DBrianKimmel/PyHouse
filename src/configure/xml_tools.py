#!/usr/bin/env python

"""This module only used by config_xml to access or create an empty config file.1
0
"""

# Import system type stuff
import os, sys
from xml.etree import ElementTree as ET
from xml.dom import minidom


g_debug = 0


class XmlFileTools(object):

    def __init__(self):
        """Open the xml config file.

        If the file is missing, an empty minimal skeleton is created.
        """
        global g_xmltree
        self.m_filename = open_config()
        try:
            g_xmltree = ET.parse(self.m_filename)
        except SyntaxError:
            ConfigFile().create_empty_config_file(self.m_filename)
            g_xmltree = ET.parse(self.m_filename)
        self.m_root = g_xmltree.getroot()


class ConfigTools(XmlFileTools):

    def get_bool(self, p_arg):
        l_ret = False
        if p_arg == 'True' or p_arg == True:
            l_ret = True
        return l_ret

    def get_float(self, p_obj, p_name):
        l_var = p_obj.findtext(p_name)
        try:
            l_var = float(l_var)
        except (ValueError, TypeError):
            l_var = 0.0
        return l_var

    def get_int(self, p_obj, p_name):
        l_var = p_obj.findtext(p_name)
        try:
            l_var = int(l_var)
        except (ValueError, TypeError):
            l_var = 0
        return l_var

    def get_text(self, p_obj, p_name):
        l_var = p_obj.findtext(p_name)
        try:
            l_var = str(l_var)
        except (ValueError, TypeError):
            l_var = ''
        return l_var


    def put_bool(self, p_arg):
        l_text = 'False'
        if p_arg != False: l_text = 'True'
        return l_text

    def put_str(self, p_obj):
        try:
            l_var = str(p_obj)
        except AttributeError:
            l_var = 'no str value'
        return l_var

    def build_common(self, p_parent, p_title, p_obj):
        """Build a common entry.

        <p_parent>
            <p_title Name=p_obj.Name Key=p_obj.Key Active=o_obj.Active>
            </p_title>
        """
        l_ret = ET.SubElement(p_parent, p_title)
        l_ret.set('Name', p_obj.Name)
        l_ret.set('Key', str(p_obj.Key))
        l_ret.set('Active', self.put_bool(p_obj.Active))
        return l_ret

    def read_common(self, p_obj, p_entry):
        """Get the common (Name, Key, Active) information from an XML sub-tree.

        @param p_obj: is the object we are updating the common information for.
        @param p_entry: is the XML subtree that we are extracting the information from.
        """
        if g_debug > 1:
            print "xml_tools.read_common()", p_entry
        p_obj.Name = p_entry.get('Name')
        try:
            p_obj.Key = int(p_entry.get('Key'))
        except (AttributeError, TypeError):
            p_obj.Key = 0
        p_obj.Active = self.get_bool(p_entry.get('Active'))

    def write_file(self, p_xmltree, p_filename = ''):
        if g_debug > 0:
            print "xml_tools.write_file() Filename:{0:}".format(p_filename), p_xmltree
        p_xmltree.write(p_filename, xml_declaration = True)


class ConfigEtc(object):
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
        if g_debug > 0:
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
                if g_debug > 1:
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
        # print "Create_config_dir()"
        for l_dir in self.m_std_path:
            # print "1. Processing dir ", l_dir
            l_dir = os.path.expanduser(l_dir)
            if os.path.exists(l_dir):
                # print "Found directory path ", l_dir
                return l_dir
        print "No directory found, try creating one."
        for l_dir in self.m_std_path:
            # print "2, Processing dir ", l_dir
            l_dir = os.path.expanduser(l_dir)
            try:
                os.mkdir(l_dir)
                # print "Directory created - ", l_dir
                return l_dir
            except OSError:
                # print "Could not make a directory -", l_dir
                pass
        print "Could not create any of the following ", self.m_std_path
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
        print "xml_tools create_empty_config_file"
        l_top = ET.Element('PyHouse')
        l_comment = ET.Comment('Generated by PyHouse')
        l_top.append(l_comment)
        open(os.path.expanduser(p_name), 'w')
        l_nice = prettify(l_top)
        print l_nice
        ET.ElementTree(l_top).write(p_name)


def prettify(elem):
    """Return a pretty-printed XML string for the Element.

    @param elem: an element to format as a readable xml tree.
    @return: a string formatted with indeentation and newlines.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent = "  ")

def open_config():
    """Open the PyHouse config xml file.

    If the file is not found, create a skeleton xml file to be populated by the user via the GUI.

    Search in several standard places for the config file;
    if not found create it after checking for read write permissions.

    @return: the open file name
    """
    l_cf = ConfigFile()
    l_dir = l_cf.create_find_config_dir()
    l_file = l_cf.find_config_file(l_dir)
    try:
        open(l_file, mode = 'r')
    except Exception, e:  # IOError:
        print " -- Error in open_config ", sys.exc_info(), e
        l_file = '~/.PyHouse/PyHouse.xml'
        l_file = os.path.expanduser(l_file)
        ConfigFile().create_empty_config_file(l_file)
    return l_file

# ## END