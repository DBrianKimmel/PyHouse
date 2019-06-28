"""
@name:      PyHouse/Project/src/Modules/Core/Utilities.config_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 15, 2014
@Summary:   This handles config files.

"""

__updated__ = '2019-06-26'
__version_info__ = (19, 6, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import datetime
import os
from xml.etree import ElementTree as ET
from ruamel.yaml import YAML

#  Import PyMh files
from Modules.Core.Utilities.xml_tools import PutGetXML
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.ConfigTools    ')


class ConfigInformation:
    """ A collection of Yaml data used for Configuration

    ==> PyHouse._Config.xxx
    """

    def __init__(self):
        self.ConfigDir = None
        self.XmlRoot = None
        self.XmlTree = None
        self.YamlFileName = None
        self.YamlTree = {}  # ConfigYamlNodeInformation()


class ConfigYamlNodeInformation:

    def __init__(self):
        self.Yaml = None
        self.YamlPath = None
        self.FileName = None


class Yaml:

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def generate_running_key_value(self, p_object):
        """ get key, value of pyhouse object
        Iterable.

        This will take a pyhouse object and return each data storage item
        """
        l_obj = p_object
        for l_key in [l_attr for l_attr in dir(l_obj) if not callable(getattr(l_obj, l_attr)) and not l_attr.startswith('_')]:
            l_value = getattr(l_obj, l_key)
            yield (l_key, l_value)
        return

    def _find_config_file(self, p_filename):
        """ Search the config dir to find the yaml config file.
        If unit testing, we must find the file in the source tree.
        @return: a ConfigYamlNodeInformation filled in.
        """
        l_node = ConfigYamlNodeInformation()
        l_node.FileName = p_filename
        l_dir = self.m_pyhouse_obj._Config.ConfigDir
        # print('ConfigDir: ', l_dir, p_filename)
        for l_root, _l_dirs, l_files in os.walk(l_dir):
            if p_filename in l_files:
                l_path = os.path.join(l_root, p_filename)
                # print('Path: ', l_path)
                l_node.YamlPath = l_path
                return l_node
        return l_node

    def read_yaml(self, p_filename):
        """ Find the Yaml file and read it in.
        Save file location and source YAML

        @return: a ConfigYamlNodeInformation() filled in
        """
        l_node = self._find_config_file(p_filename)
        if l_node.YamlPath == None:
            LOG.error('Config file "{}" was not found within the config dir "{}".'.format(l_node.FileName, l_node.YamlPath))
            return l_node
        l_yaml = YAML(typ='rt')
        l_yaml.allow_duplicate_keys = True
        # ruamel.yaml.add_constructor(u'!Ref', your_ref_constructor, constructor=ruamel.yaml.SafeConstructor)
        with open(l_node.YamlPath) as l_file:
            l_data = l_yaml.load(l_file)
            l_node.Yaml = l_data
        self.m_pyhouse_obj._Config.YamlTree[p_filename] = l_node
        LOG.info('Loaded config file "{}" '.format(p_filename))
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj._Config.YamlTree, 'Tree', 190))
        return l_node

    def write_yaml(self, p_data, p_filename, addnew=False):
        """
        @param p_data: is the yaml data to be written.
        @param p_filename: is the name of the read in yaml file
        @param addnew: defaults to false, will add '-new' to the saved filename.
        """
        l_node = self.m_pyhouse_obj._Config.YamlTree[p_filename]
        l_filename = l_node.YamlPath
        if addnew:
            l_filename += '-new'
        l_yaml = YAML(typ='rt')
        l_yaml.indent(mapping=2, sequence=4, offset=2)
        l_yaml.version = (1, 2)
        with open(l_filename, 'w+') as l_file:
            l_yaml.dump(p_data, l_file)


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

#  ## END DBK
