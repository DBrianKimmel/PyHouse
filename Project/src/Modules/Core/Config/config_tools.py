"""
@name:      Modules/Core/Config/config_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 15, 2014
@Summary:   This handles config files.

"""

__updated__ = '2019-11-29'
__version_info__ = (19, 11, 4)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import os
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO

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

    def __init__(self):
        self.Name = None  # LowerCase without .yaml
        self.Path = None


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


class SubFields:
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
        Tools(self.m_pyhouse_obj).extract_fields(l_obj, p_config, l_required, l_allowed)
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
        Tools(self.m_pyhouse_obj).extract_fields(l_device_obj, p_config, l_required, l_allowed)
        l_key = l_device_obj.Name.lower()
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
        Tools(self.m_pyhouse_obj).extract_fields(l_obj, p_config, l_required, l_allowed)
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
        Tools(self.m_pyhouse_obj).extract_fields(l_obj, p_config, l_required, l_allowed)
        #
        # LOG.debug('Getting driver Api')
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


class Tools:
    """
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _get_config_dir(self):
        """
        @return: The configuration Directory ('/etc/pyhouse' is the default)
        """
        return '/etc/pyhouse'
        # return self.m_pyhouse_obj._Config.ConfigDir

    def _find_file(self, p_name, p_dir):
        """
        @param p_name: is the file to find
        @param p_dir: is the dir tree to search for the file
        @return: the absolute path of the file or None if not found.
        """
        # LOG.debug('Finding file:"{}" In dir:"{}"'.format(p_name, p_dir))
        # print('Looking for:{}; in Dir:{}'.format(p_name, p_dir))
        for l_root, _l_dirs, l_files in os.walk(p_dir):
            # print('Root:{}; Dirs:{}; Files:{}'.format(l_root, _l_dirs, l_files))
            if p_name in l_files:
                l_path = os.path.join(l_root, p_name)
                return l_path
        # LOG.warn('Not Found "{}"'.format(p_name))
        return None

    def find_config_file(self, p_name):
        """ Given a name like 'computer' or 'Computer', find any config file 'computer.yaml'.
        @return: the absolute path of the file or None if not found.
        """
        # LOG.debug('Finding Config file:"{}"'.format(p_name))
        l_filename = p_name.lower() + CONFIG_SUFFIX
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
                    LOG.warn('Config entry "{}" is missing.'.format(l_key))
                    continue
            else:  # Key is Present
                # LOG.debug('Key defined: {}; Value: {}'.format(l_key, l_value))
                if l_key in allowed_list:
                    LOG.warn('Config entry "{}" is not permitted.'.format(l_key))
                    continue
            return p_obj


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


class YamlFetch(Tools):
    """
    """

    def XXXvalidate_yaml_in_main(self, p_info_obj, p_yaml_def):
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

    def XXXgenerate_running_key_value(self, p_object):
        """ get key, value of pyhouse object Iterable.

        This will take a pyhouse object and return each data storage item as a key, value tuple.
        """
        l_obj = p_object
        for l_key in [l_attr for l_attr in dir(l_obj) if not callable(getattr(l_obj, l_attr)) and not l_attr.startswith('_')]:
            l_value = getattr(l_obj, l_key)
            yield (l_key, l_value)
        return


class Yaml(YamlCreate, YamlFetch, Tools):

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
        l_node = ConfigFileInformation()
        l_node.FileName = p_filename
        l_node.YamlPath = self.find_config_file(p_filename)
        return l_node

    def find_first_element(self, p_ordered):
        """ Return the first element from an ordered collection
           or an arbitrary element from an unordered collection.
           Raise StopIteration if the collection is empty.
        """
        return next(iter(p_ordered))

    def read_yaml(self, p_filename):
        """ Find the Yaml file and read it in.
        Save file location and source YAML

        @return: a ConfigFileInformation() filled in
        """
        l_node = self._find_config_node(p_filename)
        if l_node == None:
            LOG.warn('Config file "{}" not found.'.format(p_filename))
            return None
        l_yaml = MyYAML(typ='rt')
        l_yaml.allow_duplicate_keys = True
        try:
            with open(l_node.YamlPath, 'r') as l_file:
                l_data = l_yaml.load(l_file)
        except Exception as e_err:
            LOG.error('Config file read error; {}'.format(e_err))
            return None
        # LOG.info('Loaded config file "{}" '.format(p_filename))
        return l_data

    def _write_yaml(self, p_filename, p_data, addnew=False):
        """
        @param p_data: is the yaml data to be written.
        @param p_filename: is the name of the read in yaml file 'rooms.yaml'
        @param addnew: defaults to false, will add '-new' to the saved filename.
        """
        # l_now = datetime.datetime.now()
        # l_node = self.m_pyhouse_obj._Config.YamlTree[p_filename]
        # l_filename = l_node.YamlPath
        # l_node.Yaml.insert(0, 'Skip', 'x', comment="Updated: " + str(l_now))
        # if addnew:
        # #   l_filename += '-new'
        # l_yaml = MyYAML(typ='rt')
        # l_yaml.indent(mapping=2, sequence=4, offset=2)
        # l_yaml.version = (1, 2)
        # with open(l_filename, 'w+') as l_file:
        #    l_yaml.dump(p_data, l_file)
        LOG.debug('Saved Yaml file "{}"'.format(p_filename))

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

    def read_config(self, p_filename):
        """ Main config file read routine
        @param  p_filename: is the name of the config file to read (without .yaml)
        @return: the yaml file string or None if no such config file
        """
        l_ret = self.m_yaml.read_yaml(p_filename.lower())
        # LOG.debug(PrettyFormatAny.form(l_ret, 'Config'))
        return l_ret

    def write_config(self, p_filename, p_data, addnew=False):
        """ Main config file write routine
        """
        l_ret = self.m_yaml._write_yaml(p_filename, p_data, addnew)
        return l_ret

    def find_config(self, p_name):
        """ Given a name like 'computer' or 'Computer', find any config file 'computer.yaml'.
        @return: the absolute path of the file or None if not found.
        """
        l_ret = Tools(self.m_pyhouse_obj).find_config_file(p_name)
        return l_ret

    def look_for_all_configed_modules(self, p_modules):
        """ Find all modules to find config files for.
        @param p_modules: is a list of module names to check for.
        @return: a dict of module names that have config files.
        """
        l_modules = {}
        for l_module in p_modules:
            l_path = self.find_config_file(l_module.lower())
            if l_path == None:
                continue
            l_modules[l_module] = l_path
        return l_modules

#  ## END DBK
