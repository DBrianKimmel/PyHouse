"""
-*- test-case-name: PyHouse.src.Modules.Families.test.test_family -*-

@name:      PyHouse/src/Modules/Families/family.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2016 by D. Brian Kimmel
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

    FamilyPackageName        Will point to the package directory 'Modules.Families.Insteon'
    FamilyDeviceModuleName   will contain 'Insteon_device'
    FamilyXmlModuleName      will contain 'Insteon_xml'

    FamilyModuleAPI          will point to Insteon_device.API() to allow API functions to happen.
    FamilyXmlModuleAPI       will point to Insteon_xml.API() where ReadXml

"""

# Import system type stuff
import importlib

# Import PyHouse files
from Modules.Core.data_objects import FamilyData
from Modules.Families import VALID_FAMILIES
from Modules.Computer import logging_pyh as Logging
LOG = Logging.getLogger('PyHouse.Family         ')


class Utility(object):
    """
    This will go thru every valid family and build a family entry for each one.
    It also imports the _device and _xml for each family and stores their API reference in the family object.
    """

    @staticmethod
    def _do_import(p_obj, p_module):
        """
        Import a module

        @param p_obj: is a family Object.
        @param p_module: is a name of a module that we want to import
        """
        l_ret = None
        l_device = p_obj.FamilyPackageName + '.' + p_module
        try:
            l_ret = importlib.import_module(l_device, p_obj.FamilyPackageName)
        except ImportError as e_err:
            l_msg = 'ERROR importing family:{} Module:{}\n   Err:{} .'.format(p_obj.Name, p_module, e_err)
            LOG.error(l_msg)
            l_ret = l_msg
        return l_ret

    @staticmethod
    def _create_api_instance(p_pyhouse_obj, p_module_name, p_module_ref):
        """
        Hopefully, this will catch errors when addingf new families.
        I had a very strange error when one module had a different number of params in the API.__init__ definition.

        @param p_pyhouse_obj: is the entire PyHouse Data
        @param p_module_name: is the name of the module for which we are creating the API instance.
        @param p_module_ref: is the module we just imported.
        """
        try:
            l_api = p_module_ref.API(p_pyhouse_obj)
        except Exception as e_err:
            LOG.error('ERROR - Module{} - {}'.format(p_module_name, e_err))
        return l_api

    @staticmethod
    def _create_xml_instance(p_module_name, p_module_ref):
        """
        @param p_module_name: is the name of the module for which we are creating the API instance.
        @param p_module_ref: is the module we just imported.
        """
        try:
            l_api = p_module_ref.Xml()
        except Exception as e_err:
            LOG.error('ERROR - Module{} - {}'.format(p_module_name, e_err))
        return l_api

    @staticmethod
    def _build_one_family_data(p_pyhouse_obj, p_name):
        """Build up the FamilyData names portion entry for a single family

        For the Instreon family:
            Insteon_device                   ==> FamilyDeviceModuleName
            Insteon_xml                      ==> FamilyXmlModuleName
            Modules.Families.Insteon         ==> FamilyPackageName

        @param p_name: a Valid Name such as "Insteon"
        @param p_count: an indexing number
        """
        l_family_obj = FamilyData()
        l_family_obj.Name = p_name
        LOG.info('Building Family: {}'.format(p_name))
        l_family_obj.Key = 0
        l_family_obj.Active = True
        l_family_obj.FamilyPackageName = 'Modules.Families.' + p_name
        l_family_obj.FamilyDeviceModuleName = p_name + '_device'
        l_family_obj.FamilyXmlModuleName = p_name + '_xml'
        l_dev_mod = Utility._do_import(l_family_obj, l_family_obj.FamilyDeviceModuleName)
        l_family_obj.FamilyModuleAPI = Utility._create_api_instance(p_pyhouse_obj, l_family_obj.FamilyDeviceModuleName, l_dev_mod)
        l_xml_mod = Utility._do_import(l_family_obj, l_family_obj.FamilyXmlModuleName)
        l_family_obj.FamilyXmlModuleAPI = Utility._create_xml_instance(l_family_obj.FamilyXmlModuleName, l_xml_mod)
        return l_family_obj

    @staticmethod
    def _init_component_apis(p_pyhouse_obj):
        pass
        """
        Used by many test modules.

        NOTE! - Any errors (syntax, etc) in the imported modules (or sub-modules) will cause the import to FAIL!

        This routine will go thru the valid families and create the structure to call each families device routine.
        This device routine is responsible for finding any controllers defined for this computer node and
         initializing the controller and starting anything needed for the given family.
        """
        l_family_data = {}
        l_count = 0
        for l_name in VALID_FAMILIES:
            l_family_obj = Utility._build_one_family_data(p_pyhouse_obj, l_name)
            l_family_obj.Key = l_count
            l_family_data[l_family_obj.Name] = l_family_obj
            l_count += 1
        LOG.info('Built {} families'.format(l_count))
        return l_family_data  # For testing


class API(object):

    m_count = 0

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_family = Utility._init_component_apis(p_pyhouse_obj)
        p_pyhouse_obj.House.FamilyData = self.m_family
        LOG.info('Initialized')

    def LoadXml(self, p_pyhouse_obj):
        """ The actual loading of the Families section of PyHouse_Obj os done in the constructor.
        """
        p_pyhouse_obj.House.FamilyData = self.m_family

    def Start(self):
        """
        Build p_pyhouse_obj.House.FamilyData
        """
        # self.m_pyhouse_obj.House.FamilyData = self.m_family
        return self.m_family

    def SaveXml(self, p_xml):
        """
        The family section is not saved.  it is rebuilt every Start() time from the lighting info
        """
        # LOG.info("Saved XML.")
        return p_xml

    def LoadFamilyTesting(self):
        """
        Load all the families for testing.
        """
        return Utility._init_component_apis(self.m_pyhouse_obj)

    def start_lighting_families(self, p_pyhouse_obj):
        """
        Load and start the family if there is a controller in the house for the family.
        Runs Device_<family>.API.Start()
        """
        LOG.info("Starting lighting families.")
        for l_family_obj in p_pyhouse_obj.House.FamilyData.itervalues():
            LOG.info('Starting Family {}'.format(l_family_obj.Name))
            l_family_obj.FamilyModuleAPI.Start()  # will run <family>_device.API().Start()
        LOG.info("Started all lighting families.")

# ## END DBK
