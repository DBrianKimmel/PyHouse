"""
-*- test-case-name: PyHouse.src.Modules.families.test.test_family -*-

@name:      PyHouse/src/Modules/families/family.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@note:      Created on May 17, 2013
@license:   MIT License
@summary:   This module is for building device families.

Families are a way of abstracting the difference between different "Devices Families".

Device families are things such as Insteon, X10, Zigby and many others.
Each family has a different protocol for communicating with the various devices in that family.
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
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Family         ')


class Utility(object):

    @staticmethod
    def _do_import(p_obj, p_module):
        l_ret = None
        l_device = p_obj.FamilyPackageName + '.' + p_module
        try:
            l_ret = importlib.import_module(l_device, p_obj.FamilyPackageName)
        except ImportError as e_err:
            l_msg = 'ERROR importing family:{} Module:{}\n   Err:{} .'.format(p_obj.Name, p_module, e_err)
            LOG.error(l_msg)
        return l_ret

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
        l_family_obj.Key = 0
        l_family_obj.Active = True
        l_family_obj.FamilyPackageName = 'Modules.Families.' + p_name
        l_family_obj.FamilyDeviceModuleName = p_name + '_device'
        l_family_obj.FamilyXmlModuleName = p_name + '_xml'
        l_family_obj.FamilyModuleAPI = Utility._do_import(l_family_obj, l_family_obj.FamilyDeviceModuleName).API(p_pyhouse_obj)
        l_family_obj.FamilyXmlModuleAPI = Utility._do_import(l_family_obj, l_family_obj.FamilyXmlModuleName).API(p_pyhouse_obj)
        return l_family_obj

    def start_lighting_families(self, p_pyhouse_obj):
        """
        Load and start the family if there is a controller in the house for the family.

        Runs   <family>_device.API.Start  from Lighting/lighting.py
        """
        LOG.info("Starting lighting families.")
        for l_family_obj in p_pyhouse_obj.House.RefOBJs.FamilyData.itervalues():
            LOG.info('Starting Family {}'.format(l_family_obj.Name))
            l_family_obj.FamilyModuleAPI.Start()  # will run <family>_device.API().Start()
        LOG.info("Started all lighting families.")

    def XXXstop_lighting_families(self, p_house_obj):
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            l_family_obj.FamilyModuleAPI.Stop()

    def XXXsave_lighting_families(self, p_xml, p_house_obj):
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            l_family_obj.FamilyModuleAPI.SaveXml(p_xml)

    def XXXReadXml(self, p_device_obj, _p_device_xml):
        LOG.info('family ReadXml was called for device {}.'.format(p_device_obj.Name))
        pass

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
            LOG.info(' Building family {}'.format(l_name))
            l_family_obj = Utility._build_one_family_data(p_pyhouse_obj, l_name)
            l_family_obj.Key = l_count
            l_family_data[l_family_obj.Name] = l_family_obj
            l_count += 1
        return l_family_data  # For testing


class API(Utility):

    m_count = 0

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_family = Utility._init_component_apis(p_pyhouse_obj)
        LOG.info('Started')

    def Start(self):
        """
        Build p_pyhouse_obj.House.RefOBJs.FamilyData
        """
        self.m_pyhouse_obj.House.RefOBJs.FamilyData = self.m_family
        return self.m_family

    def SaveXml(self, p_xml):
        """
        The family section is not saved.  it is rebuilt every Start() time from the lighting info
        """
        LOG.info("Saved XML.")
        return p_xml

    def LoadFamilyTesting(self):
        """
        Load all the families for testing.
        """
        return Utility._init_component_apis(self.m_pyhouse_obj)

# ## END DBK

