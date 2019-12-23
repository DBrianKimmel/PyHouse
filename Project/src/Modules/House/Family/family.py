"""
@name:      Modules/House/Family/family.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@note:      Created on May 17, 2013
@license:   MIT License
@summary:   This module is for *BUILDING/loading* device families.

Families are a way of abstracting the difference between different "Device Families".
Device families are things such as Insteon, X10, Zigby and many others.
Each family has a different syntax for communicating with the various devices in that family.

Insteon, for example, has light switches, dimmers, light bulbs, thermostats, cameras to name a few.

So far Insteon and UPB are developed.  Many others may be added.

The goal of this module is to fill in enough info in each family object to allow information that is specific
 to a family to be loaded/saved between a device object and the config file.

The Family specific information is used to control and monitor the different devices within the family.

An Insteon_device module is used to read and write information to an Insteon controller connected to the computer.

    PackageName         Will point to the package directory 'Modules.House.Family.insteon'
    DeviceName          will contain 'Insteon_device'
    _Api                will point to Insteon_device.Api() to allow Api functions to happen.
"""

__updated__ = '2019-12-22'
__version_info__ = (19, 11, 28)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff

# Import PyHouse files
from Modules.Core.Config import config_tools
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Family         ')

CONFIG_NAME = 'families'

MODULES = [
    'Acurite',
    'Hue',
    'Insteon',
    'Lutron',
    'Sonoff',
    'Upb',
    'X10',
    'Zwave',
    'Null'
    ]


class FamilyInformation:
    """ Info about a family
    This points to the
    ==> PyHouse_obj.House.Family[<familyname>]
    indexed by lowercased family name "insteon"
    """

    def __init__(self):
        self.Name = None  # Family Name
        self.Module = None  # FamilyModuleInformation()
        self._Api = None  # of the family_device.py file


class DeviceFamilyInformation:
    """ This is used for things like Lights
    """

    def __init__(self):
        self.Name = None
        self.Type = None
        self.Address = None


class FamilyModuleInformation:
    """ A container for every family that has been defined in modules.

    PyHouse_obj.House.Family.()
    PyHouse_obj.House.Family is a dict indexed by lower() family name.

    Each entry is an object of this class.
    """

    def __init__(self):
        self.Name = None  # Insteon
        # self.Address = None
        self.DeviceName = None  # insteon_device
        self.PackageName = None  # Modules.House.Family.insteon
        self._Api = None  # insteon_device()


class Utility:
    """
    This will go thru every valid family and build a family entry for each one.
    It also imports the _device and _xml for each family and stores their Api reference in the family object.

    This should operate more as a plug-in loader rather than loading everything.
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _create_api_instance(self, p_pyhouse_obj, p_module_name, p_module_ref):
        """
        Hopefully, this will catch errors when adding new families.
        I had a very strange error when one module had a different number of params in the Api.__init__ definition.

        @param p_pyhouse_obj: is the entire PyHouse Data
        @param p_module_name: is the name of the module for which we are creating the Api instance.
        @param p_module_ref: is a reference to the module we just imported.
        """
        LOG.info('Starting')
        # LOG.debug(PrettyFormatAny.form(p_module_ref, 'Ref'))
        try:
            l_api = p_module_ref.Api(p_pyhouse_obj)
            l_api.LoadConfig()
            l_api.Start()
        except Exception as e_err:
            LOG.error('ERROR - Module: {}\n\t{}'.format(p_module_name, e_err))
            # LOG.error('Ref: {}'.format(PrettyFormatAny.form(p_module_ref, 'ModuleRef', 190)))
            l_api = None
        return l_api

    def _create_config_instance(self, _p_pyhouse_obj, p_module_name, p_module_ref):
        """
        @param p_module_name: is the name of the module for which we are creating the Api instance.
        @param p_module_ref: is the module we just imported.
        """
        try:
            l_api = p_module_ref.Config()
            return l_api
        except Exception as e_err:
            LOG.error('ERROR - Module:{} - {}'.format(p_module_name, e_err))
        return None


class LocalConfig:
    """
    """

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def extract_family_group(self, p_config):
        """
        @param p_config: is the 'Family' ordereddict
        """
        l_obj = DeviceFamilyInformation()
        l_required = ['Name', 'Address']
        l_allowed = ['Type']
        config_tools.Tools(self.m_pyhouse_obj).extract_fields(l_obj, p_config, l_required, l_allowed)
        # LOG.debug('Family "{}"'.format(l_obj.Name))
        # LOG.debug(PrettyFormatAny.form(l_obj, 'Family'))
        return l_obj

    def XXXload_family_config(self, p_config, p_pyhouse_obj):
        """ Get the yaml config information.

        This is called from many different modules.
        It loads the appropriate information for the different families supported by PyHouse

        Family:
           Name: Insteon
           Address: 11.44.33

        """
        l_module = FamilyModuleInformation()
        l_required = ['Name']
        #
        # Load specific family information dispatched from here
        #
        for l_key, l_value in p_config.items():
            print('Family Key {}'.format(l_key))
            if l_key == 'Name':
                l_value = l_value.lower()
                p_pyhouse_obj.House.Family[l_value] = l_module
            setattr(l_module, l_key, l_value)
        # Check for data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_module) if not l_attr.startswith('_') and not callable(getattr(l_module, l_attr))]:
            if getattr(l_module, l_key) == None and l_key in l_required:
                LOG.warning('Controller Yaml is missing an entry for "{}"'.format(l_key))
        # Now build the families actually called for in the config files.
        # LOG.debug(PrettyFormatAny.form(p_pyhouse_obj.House.Family, 'House.Family', 190))
        try:
            _l_test = p_pyhouse_obj.House.Family[l_module.Name]
        except Exception as e_err:
            LOG.debug('Config family "{}" Update family.\n\tError: {}'.format(l_module.Name, e_err))
            LOG.debug(PrettyFormatAny.form(p_pyhouse_obj, 'PyHouse'))
            LOG.debug(PrettyFormatAny.form(p_pyhouse_obj.House, 'House'))
            LOG.debug(PrettyFormatAny.form(p_pyhouse_obj.House.Family, 'Family'))
            l_module.Name = l_module.Name
            p_pyhouse_obj.House.Family[l_module.Name.lower()] = l_module
        return l_module


class Api:

    m_config_tools = None
    m_family = {}  # type: ignore
    m_local_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        self.m_config_tools = config_tools.Api(p_pyhouse_obj)
        self._add_storage()
        LOG.info("Initialized - Version:{}".format(__version__))

    def _add_storage(self):
        self.m_pyhouse_obj.House.Family = {}  #

    def _build_one_family_data(self, p_name):
        """Build up the FamilyModuleInformation names portion entry for a single family

        For the Insteon family:
            insteon_device                   ==> FamilyDevice_ModuleName
            Modules.House.Family.insteon         ==> PackageName

        @param p_name: a Valid Name such as "Insteon"
        """
        LOG.info('Building Family "{}"'.format(p_name))
        l_path = 'Modules.House.Family'
        l_obj = FamilyInformation()
        l_key = p_name.lower()
        l_module = l_key + '.' + l_key + '_device'
        self.m_pyhouse_obj.House.Family[l_key] = l_obj
        l_obj.Name = p_name
        l_obj.Module = l_module
        l_obj._Api = self.m_config_tools.import_module_get_api(l_module, l_path)
        LOG.debug(PrettyFormatAny.form(l_obj, 'Family'))
        return l_obj

    def LoadConfig(self):
        """
        This is run after all other config files are loaded so we only have the configured familys now.
        """
        # LOG.debug('Loading Families')
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Family, 'Families'))
        l_dict = {}
        for l_key, l_family_obj in self.m_pyhouse_obj.House.Family.items():
            LOG.info('Loading Family "{}"'.format(l_key))
            # LOG.debug(PrettyFormatAny.form(l_family_obj, 'Family'))
            l_family_obj = self._build_one_family_data(l_key)
            l_dict[l_key] = l_family_obj
        LOG.info('Loaded {} Families'.format(len(self.m_pyhouse_obj.House.Family)))
        self.m_pyhouse_obj.House.Family = l_dict

    def Start(self):
        """ Start each family we have registered.

        This will import the the family_device and start the family device.
        """
        LOG.info('Starting {} families.'.format(len(self.m_pyhouse_obj.House.Family)))
        # LOG.debug(PrettyFormatAny.form(self.m_pyhouse_obj.House.Family, 'Family'))
        for l_key, l_family_obj in self.m_pyhouse_obj.House.Family.items():
            LOG.info('Starting Family "{}"'.format(l_key))
            # LOG.debug(PrettyFormatAny.form(l_family_obj, 'Family'))
            l_api = l_family_obj._Api
            if l_api != None:
                l_api.Start()
        LOG.info('Started {} families.'.format(len(self.m_pyhouse_obj.House.Family)))
        return self.m_family

    def SaveConfig(self):
        pass

# ## END DBK
