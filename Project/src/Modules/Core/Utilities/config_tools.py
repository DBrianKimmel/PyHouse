"""
@name:      Modules/Core/Utilities/config_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 15, 2014
@Summary:   This handles config files.

"""

__updated__ = '2019-08-03'
__version_info__ = (19, 6, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import datetime
import os
from xml.etree import ElementTree as ET
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedSeq as cs
from ruamel.yaml.comments import TaggedScalar as ts
from ruamel.yaml.scalarstring import SingleQuotedScalarString as sq
from ruamel.yaml.comments import CommentedMap as ordereddict

#  Import PyMh files
from Modules.Core.Utilities.xml_tools import PutGetXML
from Modules.Core.data_objects import HostInformation
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.ConfigTools    ')


class ConfigInformation:
    """ A collection of Yaml data used for Configuration

    ==> PyHouse._Config.xxx
    """

    def __init__(self):
        self.ConfigDir = None
        # self.XmlRoot = None
        # self.XmlTree = None
        self.YamlFileName = None
        self.YamlTree = {}  # ConfigYamlNodeInformation()


class ConfigYamlNodeInformation:

    def __init__(self):
        self.FileName = None
        self.Yaml = None
        self.YamlPath = None
        self._Error = None


class SecurityInformation:
    """
    """

    def __init__(self):
        """
        """
        self.Name = None  # Username
        self.Passwoed = None
        self.ApiKey = None
        self.AccessKey = None


class Tools:
    """
    """

    def read_coords(self, p_yaml):
        """ Read a set of room co-ordinates
        Written as "[1.2, 3.4, 5.6]"
        """
        l_coord = []
        _l_x = p_yaml
        return l_coord


class YamlCreate:
    """ For creating and appending to yaml files.
    """

    def create_yaml(self, p_tag: str):
        """ create a yaml structure with a nested-map.

        Yaml = ordereddict([('p_tag', None)])
        p_tag:
            <empty position>

        @param p_tag: is the top level map string
        """
        if p_tag == None:
            LOG.error('Create requires a concrete tag (not "None") "ERROR_TAG" is used as the tag instead !')
            p_tag = 'ERROR_TAG'
        YAML_STR = p_tag + ':'
        l_yaml = YAML()
        l_yaml.indent(mapping=2, sequence=4, offset=2)
        l_data = l_yaml.load(YAML_STR)
        return l_data

    def add_key_value_to_map(self, p_yaml, p_key, p_value):
        """ Add a key,Value pair to a map
        Test:
           Key: Value
           New Key: New Value  <== Added

        @param p_yaml: is the fragment where the addition is to go.
        @param p_tag: is a list of tags to add the K,V entry below.  The tags are relative to the top of the yaml fragment.
        """
        p_yaml.append(p_key)
        # print('Yaml: {}'.format(p_yaml))

    def add_dict(self, p_yaml, p_key, p_add_dict):
        """ Add a key,Value pair to a map
        Test:
           Key: Value
           New Key: New Value  <== Added

        @param p_yaml: is the fragment where the addition is to go.
        @param p_add_dict: is the dict to add
        """
        # print('Yaml: {}'.format(p_yaml))
        for l_key, l_val in p_add_dict.items():
            # print('Adding: {} : {}'.format(l_key, l_val))
            setattr(p_yaml, l_key, l_val)
        return p_yaml

    def add_list(self, p_yaml, p_key, p_add_obj):
        """
        Insert a list entry into the list fragment that is the surrounding yaml.

        @param p_yaml_frag: is the list fragment where the addition is to go.
        @param p_add: is the object to add
        """
        if p_yaml == None:
            p_yaml = p_add_obj
        else:
            l_ix = len(p_yaml) - 2  # This is the Index where the object object needs to be inserted.
            p_yaml.insert(l_ix, p_key, p_add_obj)
            # p_yaml[-1] = p_add_obj
        return p_yaml

    def add_obj(self, p_yaml, p_key, p_tag):
        """ Add a new ordereddict to the yaml after the Key location
        @param p_yaml: is the yaml fragment that contains p_key (Rooms)
        @param p_key: is the key we will add a new tag into (Room)
        @param p_tag: is the
        """
        l_working = p_yaml[p_key]
        p_obj = l_working
        # print('Working: {}'.format(l_working))
        for l_key in [l_attr for l_attr in dir(p_obj) if not l_attr.startswith('_')  and not callable(getattr(l_working, l_attr))]:
            l_val = getattr(l_working, l_key)
            # setattr(l_config, l_key, l_val)

    def add_to_obj(self, p_yaml, p_key, p_obj):
        """
        """
        l_working = p_yaml[p_key]
        # print('Working: {}'.format(l_working))
        for l_key in [l_attr for l_attr in dir(p_obj) if not l_attr.startswith('_')  and not callable(getattr(l_working, l_attr))]:
            l_val = getattr(l_working, l_key)
            # setattr(l_config, l_key, l_val)


class YamlFetch:
    """
    """

    def fetch_host_info(self, p_yaml):
        """
        @param p_yaml: is the 'Host' ordereddict
        """
        l_obj = HostInformation()
        for l_key, l_val in p_yaml.items():
            setattr(l_obj, l_key, l_val)
        return l_obj

    def fetch_security_info(self, p_yaml):
        """
        """
        l_obj = SecurityInformation()
        for l_key, l_val in p_yaml.items():
            setattr(l_obj, l_key, l_val)
        if l_obj.Name == None:
            l_obj.Name = l_obj.UserName
        else:
            l_obj.UserName = l_obj.Name
        return l_obj


class Yaml(YamlCreate, YamlFetch):

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj

    def create_yaml_node(self, p_tag):
        """ Create a node for a yaml config file
        @param p_tag: is the name to be used
        """
        LOG.debug(self.m_pyhouse_obj)
        l_filename = p_tag.lower() + '.yaml'
        l_node = ConfigYamlNodeInformation()
        l_node._Error = None
        l_node.FileName = l_filename
        l_node.YamlPath = self.m_pyhouse_obj._Config.ConfigDir + '/' + l_filename
        l_node.Yaml = self.create_yaml(p_tag)
        self.m_pyhouse_obj._Config.YamlTree[l_filename] = l_node
        return l_node

    def find_first_element(self, p_ordered):
        """ Return the first element from an ordered collection
           or an arbitrary element from an unordered collection.
           Raise StopIteration if the collection is empty.
        """
        return next(iter(p_ordered))

    def validate_yaml_in_main(self, p_info_obj, p_yaml_def):
        """
        @param p_info_obj: is the xxxInformation() object we are getting the config data for.
        @param p_yaml_def: is the yaml from the config file that we are extracting for the info_obj.
        """
        for l_yaml_key, l_yaml_value in p_yaml_def.items():
            try:
                _l_x = getattr(p_info_obj, l_yaml_key)
            except AttributeError:
                LOG.warn('floors.yaml contains a bad floor item "{}" = {} - Ignored.'.format(l_yaml_key, l_yaml_value))
                continue
            setattr(p_info_obj, l_yaml_key, l_yaml_value)
        return p_info_obj  # For testing

    def generate_running_key_value(self, p_object):
        """ get key, value of pyhouse object Iterable.

        This will take a pyhouse object and return each data storage item as a key, value tuple.
        """
        l_obj = p_object
        for l_key in [l_attr for l_attr in dir(l_obj) if not callable(getattr(l_obj, l_attr)) and not l_attr.startswith('_')]:
            l_value = getattr(l_obj, l_key)
            yield (l_key, l_value)
        return

    def require_config_file(self, p_filename):
        try:
            l_node = self.read_yaml(p_filename)
        except:
            LOG.error('Required YAML config file is missing: "{}"'.format(p_filename))
            return None
        return l_node

    def find_config_node(self, p_filename):
        """ Search the config dir to find the yaml config file.
        If unit testing, we must find the file in the source tree.

        @return: a ConfigYamlNodeInformation() filled in.
        """
        l_node = ConfigYamlNodeInformation()
        l_node.FileName = p_filename
        l_dir = self.m_pyhouse_obj._Config.ConfigDir
        for l_root, _l_dirs, l_files in os.walk(l_dir):
            if p_filename in l_files:
                l_path = os.path.join(l_root, p_filename)
                l_node.YamlPath = l_path
                return l_node
        return None  # Not Found

    def read_yaml(self, p_filename):
        """ Find the Yaml file and read it in.
        Save file location and source YAML

        @return: a ConfigYamlNodeInformation() filled in
        """
        l_node = self.find_config_node(p_filename)
        if l_node.YamlPath == None:
            LOG.error('Config file "{}" was not found within the config dir "{}".'.format(
                        l_node.FileName, self.m_pyhouse_obj._Config.ConfigDir))
            return l_node
        l_yaml = YAML(typ='rt')
        l_yaml.allow_duplicate_keys = True
        with open(l_node.YamlPath, 'r') as l_file:
            l_data = l_yaml.load(l_file)
            l_node.Yaml = l_data
        self.m_pyhouse_obj._Config.YamlTree[p_filename] = l_node
        # LOG.info('Loaded config file "{}" '.format(p_filename))
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj._Config.YamlTree, 'Tree', 190))
        return l_node

    def write_yaml(self, p_data, p_filename, addnew=False):
        """
        @param p_data: is the yaml data to be written.
        @param p_filename: is the name of the read in yaml file 'rooms.yaml'
        @param addnew: defaults to false, will add '-new' to the saved filename.
        """
        l_now = datetime.datetime.now()
        l_node = self.m_pyhouse_obj._Config.YamlTree[p_filename]
        l_filename = l_node.YamlPath
        l_node.Yaml.insert(0, 'Skip', 'x', comment="Updated: " + str(l_now))
        if addnew:
            l_filename += '-new'
        l_yaml = YAML(typ='rt')
        l_yaml.indent(mapping=2, sequence=4, offset=2)
        l_yaml.version = (1, 2)
        with open(l_filename, 'w+') as l_file:
            l_yaml.dump(p_data, l_file)
        LOG.debug('Saved Yaml file "{}"'.format(p_filename))

    def dump_string(self, p_data):
        """
        """
        l_yaml = YAML(typ='rt')
        l_data = l_yaml.dump(p_data, None, transform=print)
        return l_data


class API:

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    @staticmethod
    def create_xml_config_foundation(p_pyhouse_obj):
        """
        Create the "PyHouse" top element of the XML config file.
        The other divisions are appended to this foundation.
        """
        l_xml = ET.Element("PyHouse")  # The root element.
        # PutGetXML.put_text_attribute(l_xml, 'Version', p_pyhouse_obj.Xml.XmlVersion)
        PutGetXML.put_text_attribute(l_xml, 'xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        PutGetXML.put_text_attribute(l_xml, 'xsi:schemaLocation', 'http://PyHouse.org schemas/PyHouse.xsd')
        PutGetXML.put_text_attribute(l_xml, 'xmlns:comp', 'http://PyHouse.Org/ComputerDiv')
        l_xml.append(ET.Comment(' Updated by PyHouse {} '.format(datetime.datetime.now())))
        p_pyhouse_obj._Config.XmlTree = l_xml
        return

    @staticmethod
    def write_xml_config_file(p_pyhouse_obj):
        """
        Note!
        @param p_xml_tree: is the tree body part to write
        """
        l_file = p_pyhouse_obj._Config.ConfigDir + 'master.xml'
        try:
            l_tree = ET.ElementTree()
            l_tree._setroot(p_pyhouse_obj._Config.XmlTree)
            l_tree.write(l_file, xml_declaration=True)
            l_size = os.stat(l_file).st_size
            LOG.info('Wrote config File - XML={}-bytes'.format(l_size))
        except AttributeError as e_err:
            LOG.error('Err:{}'.format(e_err))

    def _Stop(self):
        LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj, 'Dummy', 190))
#  ## END DBK