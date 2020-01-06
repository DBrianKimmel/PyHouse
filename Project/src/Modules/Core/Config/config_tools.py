"""
@name:      Modules/Core/Config/config_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 15, 2014
@Summary:   This handles config files.

"""

__updated__ = '2020-01-06'
__version_info__ = (20, 1, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import os
import datetime
import importlib
from typing import Any, List, Optional, Union
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO
from ruamel.yaml.comments import CommentedMap

#  Import PyMh files
from Modules.Core.Config.login import LoginInformation
from Modules.Core.data_objects import HostInformation
from Modules.Core.Utilities.debug_tools import PrettyFormatAny
from Modules.House.Family.family import DeviceFamilyInformation, FamilyInformation

from Modules.Core.Drivers.interface import DriverInterfaceInformation, get_device_driver_Api

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.ConfigTools    ')

CONFIG_SUFFIX = '.yaml'


class ConfigInformation:
    """ A collection of Yaml data used for Configuration

    ==> PyHouse._Config.xxx
    """

    def __init__(self):
        self.YamlFileName = None
        # self.YamlTree = {}  # ConfigFileInformation()


class ConfigFileInformation:
    """ ==? pyhouse_obj._Config {}

    Used to record where each confile is located so it can be updated.
    """

    def __init__(self) -> None:
        self.Name: Optional[str] = None  # LowerCase filemane without .yaml
        self.Path: Optional[str] = None  # Full path to file


class RoomLocationInformation:
    """
    """

    def __init__(self):
        self.Name = None


class AccessInformation:
    """
    """

    def __init__(self):
        """
        """
        self.Name = None  # Username
        self.Password = None
        self.ApiKey = None
        self.AccessKey = None


class MyYAML(YAML):

    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()


yaml = MyYAML()  # or typ='safe'/'unsafe' etc

cm = CommentedMap()


class Tools:
    """
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj) -> None:
        LOG.debug('Init')
        self.m_pyhouse_obj = p_pyhouse_obj

    def _get_config_dir(self) -> str:
        """
        @return: The configuration Directory ('/etc/pyhouse' is the default)
        """
        return '/etc/pyhouse'

    def _find_file(self, p_name: str, p_dir: str) -> Union[None, str]:
        """
        @param p_name: is the file to find
        @param p_dir: is the dir tree to search for the file
        @return: the absolute path of the file or None if not found.
        """
        # LOG.debug('Finding file:"{}" In dir:"{}"'.format(p_name, p_dir))
        # print('Looking for:"{}"; in Dir:"{}"'.format(p_name, p_dir))
        for l_root, _l_dirs, l_files in os.walk(p_dir):
            # print('Root:{}; Dirs:{}; Files:{}'.format(l_root, _l_dirs, l_files))
            if p_name in l_files:
                l_path = os.path.join(l_root, p_name)
                return l_path
        # LOG.warning('Not Found "{}"'.format(p_name))
        return None

    def find_config_file(self, p_name):
        """ Given a name like 'computer' or 'Computer', find any config file 'computer.yaml'.
        @return: the absolute path of the file or None if not found.
        """
        # LOG.debug('Finding Config file:"{}"'.format(p_name))
        l_filename = p_name + CONFIG_SUFFIX
        l_ret = self._find_file(l_filename, self._get_config_dir())
        return l_ret

    def get_modules_api(self, p_module_list, p_path):
        """ import a list of modules all within the same path
        @param p_module_list: is a list of config files to look for and import their modules
        @param p_path: is the starting point to look for rhe module to import.
        """

    def extract_fields(self, p_obj, p_config, required_list=None, allowed_list=None, groupfield_list=[]):
        """
        @param p_obj: is the python object that will contain the config information
        @param p_config: is the yaml(json) fragment that contains the data
        @param required_list: is a list of fields that must be in the config data
        @param allowed_list: additional fields that may be in the config data.
        @param groupfield_list: are fields that have sub-entries
        """
        for l_key, l_value in p_config.items():
            # LOG.debug('Key: {}; Value: {}'.format(l_key, l_value))
            if l_key in groupfield_list:
                l_extr = 'extract_' + l_key
                LOG.debug('Groupfield Extracting ', l_extr)
                continue
            # LOG.debug('Extract - Key:"{}"; Value:"{}" '.format(l_key, l_value))
            setattr(p_obj, l_key, l_value)
        #
        for l_key in [l_attr for l_attr in dir(p_obj) if not l_attr.startswith('_') and not callable(getattr(p_obj, l_attr))]:
            # LOG.debug('Now checking key: {}'.format(l_key))
            if getattr(p_obj, l_key) == None:  # Key is missing
                # LOG.debug('No key defined: {}'.format(l_key))
                if l_key in required_list:
                    LOG.warning('Config entry "{}" is missing.'.format(l_key))
                    continue
            else:  # Key is Present
                # LOG.debug('Key defined: {}; Value: {}'.format(l_key, l_value))
                if l_key in allowed_list:
                    LOG.warning('Config entry "{}" is not permitted.'.format(l_key))
                    continue
            return p_obj

    def find_module_list(self, p_modules: List) -> List:
        """ Find python modules (or packages) that have a config file.
        If it has a config file, it will be imported later, otherwise it is not loaded therefore saving memory.
        @param p_modules: is a list of Module/Package names to search for config files.
        """
        l_list = []
        LOG.info('Search for config files for: {}'.format(p_modules))
        for l_part in p_modules:
            l_path = self.find_config_file(l_part.lower())
            if l_path != None:
                l_list.append(l_part)
                LOG.info(' Found  config file for "{}"'.format(l_part))
            else:
                LOG.info('Missing config file for "{}"'.format(l_part))
        # LOG.debug('Found config files for: {}'.format(l_list))
        return l_list

    def _do_import(self, p_name, p_path):
        """ This will import a module.
        Used when we discover that the module is needed because:
            It is required
            Configuration calles for it.
        @param p_name: is the name of the module ('pandora')
        @param p_path: is the relative path to the module ('Modules.House.Entertainment')
        @return: a pointer to the module or None
        """
        l_path = p_path + '.' + p_name.lower()
        LOG.debug('Importing\n\tModule:  {}\n\tPath:    {}'.format(p_name, l_path))
        try:
            l_ret = importlib.import_module(l_path)
        except ImportError as e_err:
            l_msg = 'PROG ERROR importing module: "{}"\n\tErr:{}.'.format(p_name, e_err)
            LOG.error(l_msg)
            l_ret = None
        # LOG.info('Imported "{}" ({})'.format(p_name, l_path))
        return l_ret

    def import_module_get_api(self, p_module, p_path):
        """ import a module with a path
        @param p_module: is a module name ("Cameras")
        @param p_path: is the starting point to look for the module to import.
        @return: an initialized Api
        """
        l_module_name = p_module
        LOG.info('Get Module pointer for "{}" on path "{}"'.format(l_module_name, p_path))
        l_ret = self._do_import(l_module_name, p_path)
        try:
            # LOG.debug(PrettyFormatAny.form(l_ret, 'Module'))
            l_api = l_ret.Api(self.m_pyhouse_obj)
        except Exception as e_err:
            LOG.error('ERROR - Initializing Module: "{}"\n\tError: {}'.format(p_module, e_err))
            # LOG.error('Ref: {}'.format(PrettyFormatAny.form(l_ret, 'ModuleRef')))
            l_api = None
        # LOG.debug('Imported: {}'.format(l_ret))
        return l_api

    def import_module_list(self, p_modules: List, p_module_path: str):
        """
        This is seperate from find_module_list because sometimes extra modules have to be imported but have no config file.

        @param p_module_path: the place to find the modules - e.g. 'Modules.House'
        """
        l_modules = {}
        for l_part in p_modules:
            l_path = p_module_path
            if l_path.endswith('.'):
                l_path = p_module_path + l_part
            # LOG.debug('Starting import of Part: "{}" at "{}"'.format(l_part, l_path))
            l_api = self.import_module_get_api(l_part, l_path)
            l_modules[l_part] = l_api
        LOG.info('Loaded Module: {}'.format(l_modules))
        return l_modules

    def yaml_dump_struct(self, p_yaml: Any) -> str:
        """
        """
        l_ret = '-Start- {}\n'.format(type(p_yaml))
        if isinstance(p_yaml, dict):
            l_ret += '-Dict- {}\tLen: {}\n'.format(type(p_yaml), len(p_yaml))
            l_ret += '-Attr- {}\n'.format(dir(p_yaml))
            if hasattr(p_yaml, 'ca'):
                l_ret += '-attr:ca- {}\n'.format(p_yaml.ca)
            elif hasattr(p_yaml, 'fa'):
                l_ret += '-attr:fa- {}\n'.format(p_yaml.fa)
            elif hasattr(p_yaml, 'lc'):
                l_ret += '-attr:lc- {}\n'.format(p_yaml.lc)
            elif hasattr(p_yaml, 'items'):
                l_ret += '-attr:items- {}\n'.format(p_yaml.items)
            elif hasattr(p_yaml, 'anchor'):
                l_ret += '-attr:anchor- {}\n'.format(p_yaml.anchor)
            elif hasattr(p_yaml, 'keys'):
                l_ret += '-attr:keys- {}\n'.format(p_yaml.keys)
            elif hasattr(p_yaml, 'tag'):
                l_ret += '-attr:tag- {}\n'.format(p_yaml.tags)
            elif hasattr(p_yaml, 'values'):
                l_ret += '-attr:values- {}\n'.format(p_yaml.values)
            else:
                l_ret += '-noattr- {}\n'.format(dir(p_yaml))
            for l_yaml in p_yaml:
                self.yaml_dump_struct(p_yaml[l_yaml])
        elif isinstance(p_yaml, list):
            l_ret += '-List- {}\n'.format(type(p_yaml))
            if hasattr(p_yaml, 'ca'):
                l_ret += '-Attr:ca- {}\n'.format(p_yaml.ca)
                for _idx, l_yaml in enumerate(p_yaml):
                    self.yaml_dump_struct(l_yaml)
            else:
                l_ret += '-4- {}\n'.format(p_yaml)
                for l_yaml in p_yaml:
                    self.yaml_dump_struct(p_yaml[l_yaml])
        else:
            l_ret += '-Unk-\n'
            l_ret += '-5- {}\n'.format(p_yaml)
        return l_ret


class SubFields(Tools):
    """ Get config sub-fields such as Hosts:, Access:, Rooms: etc.
    """

    def _get_name_password(self, p_config):
        """
        """
        l_required = ['Name', 'Password']
        l_obj = LoginInformation()
        for l_key, l_value in p_config.items():
            setattr(l_obj, l_key, l_value)
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('Pandora Yaml is missing an entry for "{}"'.format(l_key))
        return l_obj

    def extract_access_group(self, p_config):
        """
        """
        # LOG.debug('Getting Access')
        l_obj = AccessInformation()
        l_required = ['Name', 'Password']
        l_allowed = ['ApiKey', 'AccessKey']
        self.extract_fields(l_obj, p_config, l_required, l_allowed)
        return l_obj

    def extract_family_group(self, p_config):
        """
        Extract the family information when it is given.
        Also, create a PyHouse_obj.House.Family entry so we can load the families that were defined in the config files.
        @param p_config: is the 'Family' ordereddict
        @return: the device object
        """
        # LOG.debug('Getting Family')
        l_family_obj = FamilyInformation()
        l_device_obj = DeviceFamilyInformation()
        l_required = ['Name', 'Address']
        l_allowed = ['Type']
        self.extract_fields(l_device_obj, p_config, l_required, l_allowed)
        l_device_obj.Name = l_device_obj.Name
        l_key = l_device_obj.Name
        l_family_obj.Name = l_device_obj.Name
        # LOG.debug(PrettyFormatAny.form(l_device_obj, 'Device'))
        # LOG.debug(PrettyFormatAny.form(l_family_obj, 'Family'))
        self.m_pyhouse_obj.House.Family[l_key] = l_family_obj
        return l_device_obj

    def extract_host_group(self, p_config):
        """
        @param p_config: is the 'Host' ordereddict
        """
        # LOG.debug('Getting Host')
        l_obj = HostInformation()
        l_required = ['Name', 'Port']
        l_allowed = ['IPv4', 'IPv6']
        self.extract_fields(l_obj, p_config, l_required, l_allowed)
        return l_obj

    def extract_interface_group(self, p_config):
        """ Get the Interface sub-fields
        Yaml:
           - Name: TestPlm
             Interface:
                Type: Serial
                Baud: 19200,8,N,1
                Port: /dev/ttyUSB0
                Host: Laptop-05
        """
        # LOG.debug('Getting Interface')
        l_obj = DriverInterfaceInformation()
        l_required = ['Type', 'Host', 'Port']
        l_allowed = ['ApiKey', 'AccessKey']
        self.extract_fields(l_obj, p_config, l_required, l_allowed)
        #
        # LOG.debug('Getting driver Api')
        if l_obj.Host.lower() == self.m_pyhouse_obj.Computer.Name.lower():
            l_obj._isLocal = True
            l_driver = get_device_driver_Api(self.m_pyhouse_obj, l_obj)
            l_obj._DriverApi = l_driver
        # LOG.debug(PrettyFormatAny.form(l_obj, 'Interface'))
        return l_obj

    def extract_room_group(self, p_config):
        """
        """
        # LOG.debug('Getting Room')
        l_obj = RoomLocationInformation()
        try:
            for l_key, l_value in p_config.items():
                # LOG.debug('RoomKey:{}; Value:{}'.format(l_key, l_value))
                setattr(l_obj, l_key, l_value)
            return l_obj
        except:
            l_obj.Name = p_config
        return l_obj


class YamlCreate:
    """ For creating and appending to yaml files.
    """

    def _create_yaml(self, p_tag: str):
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
        l_yaml = MyYAML()
        l_yaml.indent(mapping=2, sequence=4, offset=2)
        l_data = l_yaml.load(YAML_STR)
        return l_data

    def XXXadd_key_value_to_map(self, p_yaml, p_key, _p_value):
        """ Add a key,Value pair to a map
        Test:
           Key: Value
           New Key: New Value  <== Added

        @param p_yaml: is the fragment where the addition is to go.
        @param p_tag: is a list of tags to add the K,V entry below.  The tags are relative to the top of the yaml fragment.
        """
        p_yaml.append(p_key)
        # print('Yaml: {}'.format(p_yaml))

    def XXXadd_dict(self, p_yaml, _p_key, p_add_dict):
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

    def XXXadd_list(self, p_yaml, p_key, p_add_obj):
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

    def XXXadd_obj(self, p_yaml, p_key, _p_tag):
        """ Add a new ordereddict to the yaml after the Key location
        @param p_yaml: is the yaml fragment that contains p_key (Rooms)
        @param p_key: is the key we will add a new tag into (Room)
        @param p_tag: is the
        """
        l_working = p_yaml[p_key]
        p_obj = l_working
        print('Working: {}'.format(l_working))
        for l_key in [l_attr for l_attr in dir(p_obj) if not l_attr.startswith('_')  and not callable(getattr(l_working, l_attr))]:
            _l_val = getattr(l_working, l_key)
            # setattr(l_config, l_key, l_val)
        pass

    def XXXadd_to_obj(self, p_yaml, p_key, p_obj):
        """
        """
        l_working = p_yaml[p_key]
        # print('Working: {}'.format(l_working))
        for l_key in [l_attr for l_attr in dir(p_obj) if not l_attr.startswith('_')  and not callable(getattr(l_working, l_attr))]:
            _l_val = getattr(l_working, l_key)
            # setattr(l_config, l_key, l_val)


class YamlRead:
    """
    """


class YamlWrite:
    """
    """

    def add_updated_comment(self, p_contents):
        """ Add or modify a comment for when the yaml file was last updated / written.

        Light:  # Updated 2020-01-02
            - Name: Light-01
              Room: Kitchen

        @param p_contents: is the formatted yaml contents.
        @return: the updated contents with the added information
        """
        l_ret = p_contents
        # Find existing comments if any
        # Insert missing comment
        # Update the updated comment
        return l_ret


class Yaml(YamlRead, YamlWrite, YamlCreate, Tools):

    def __init__(self, p_pyhouse_obj):
        """
        """
        # LOG.debug('Initializing')
        self.m_pyhouse_obj = p_pyhouse_obj

    def _find_config_node(self, p_filename):
        """ Search the config dir to find the yaml config file.
        If unit testing, we must find the file in the source tree.

        @return: a ConfigFileInformation() filled in.
        """
        # LOG.debug('Progress')
        l_filename = p_filename.lower()
        l_node = ConfigFileInformation()
        l_node.Name = l_filename
        l_node.Path = self.find_config_file(l_filename)
        self.m_pyhouse_obj._Config[l_filename] = l_node
        return l_node

    def find_first_element(self, p_ordered):
        """ Return the first element from an ordered collection
           or an arbitrary element from an unordered collection.
           Raise StopIteration if the collection is empty.
        """
        return next(iter(p_ordered))

    def _read_yaml(self, p_filename):
        """ Find the Yaml file and read it in.
        Save file location

        @return: a ConfigFileInformation() filled in
        """
        l_node = self._find_config_node(p_filename.lower())
        if l_node == None:
            LOG.warning('Config file "{}" not found.'.format(p_filename))
            return None
        l_yaml = MyYAML(typ='rt')
        l_yaml.allow_duplicate_keys = True
        try:
            with open(l_node.Path, 'r') as l_file:
                l_data = l_yaml.load(l_file)
        except Exception as e_err:
            LOG.error('Config file read error; {}\n\tFile: "{}"'.format(e_err, p_filename))
            LOG.error(PrettyFormatAny.form(l_node, 'Node'))
            return None
        # LOG.info('Loaded config file "{}" '.format(p_filename))
        return l_data

    def _write_yaml(self, p_filename, p_data, addnew=False):
        """
        @param p_data: is the yaml data to be written.
        @param p_filename: is the name of the read in yaml file 'rooms.yaml'
        @param addnew: defaults to false, will add '-new' to the saved filename.
        """
        try:
            l_path = self.m_pyhouse_obj._Config[p_filename].Path
        except Exception as e_err:
            l_path = '/etc/pyhouse/'
            LOG.error('Bad file {}'.format(e_err))
        l_now = datetime.datetime.now()
        p_data.insert(0, 'Skip', 'x', comment="Updated: " + str(l_now))
        if addnew:
            l_path += '-new'
        l_yaml = MyYAML(typ='rt')
        l_yaml.indent(mapping=2, sequence=4, offset=2)
        l_yaml.version = (1, 2)
        with open(l_path, 'w+') as l_file:
            l_yaml.dump(p_data, l_file)
        LOG.debug('Saved Yaml file "{}"'.format(l_path))

    def _x(self):
        LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj, 'Dummy'))


class Api(SubFields, Tools):
    """ This is the interface to the config system.
    """

    m_pyhouse_obj = None
    m_yaml = None

    def __init__(self, p_pyhouse_obj):
        # LOG.debug('Initializing')
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_yaml = Yaml(p_pyhouse_obj)

    def read_config_file(self, p_filename):
        """ Main config file read routine
        @param  p_filename: is the name of the config file to read (without .yaml)
        @return: the yaml file string or None if no such config file
        """
        l_ret = self.m_yaml._read_yaml(p_filename.lower())
        # LOG.debug(PrettyFormatAny.form(l_ret, 'Config'))
        return l_ret

    def write_config_file(self, p_filename, p_data, addnew=False):
        """ Main config file write routine
        """
        l_ret = self.m_yaml._write_yaml(p_filename, p_data, addnew)
        return l_ret

#  ## END DBK
