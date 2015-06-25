"""
-*- test-case-name: PyHouse.src.Modules.families.test.test_family -*-

@name:      PyHouse/src/Modules/families/family.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2015 by D. Brian Kimmel
@note:      Created on May 17, 2013
@license:   MIT License
@summary:   This module is for lighting families.

It is called from house.py and allows any number of different lighting families to be used.
So far Insteon and UPB are developed.  Many others may be added.

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
    def _build_one_family_data(p_name, p_count):
        """Build up the FamilyData entry for a single family
        """
        l_family_obj = FamilyData()
        l_family_obj.Name = p_name
        l_family_obj.Key = p_count
        l_family_obj.Active = True
        l_family_obj.FamilyPackageName = 'Modules.Families.' + p_name
        l_family_obj.FamilyDeviceModuleName = p_name + '_device'
        l_family_obj.FamilyXmlModuleName = p_name + '_xml'
        return l_family_obj

    @staticmethod
    def _import_one_module(p_family_obj):
        """
        This routine will attempt to import a module.

        Any errors, such as syntax errors, in the module will cause the import to fail.
        Hopefully, this method will detect all such errors and make the developers life much easier by reporting the error.
        """
        l_device = p_family_obj.FamilyPackageName + '.' + p_family_obj.FamilyDeviceModuleName
        try:
            l_module = importlib.import_module(l_device, p_family_obj.FamilyPackageName)
        except ImportError as l_error:
            l_msg = 'ERROR "{}" while trying to import module {}.'.format(l_error, p_family_obj.FamilyDeviceModuleName)
            print("ERROR - Cannot import:\n    Module: {}\n    Package: {}\n    Error: {}\n\n".format(p_family_obj.FamilyDeviceModuleName, p_family_obj.FamilyPackageName, l_msg))
            LOG.error(l_msg)
            l_module = None
        l_xml = p_family_obj.FamilyPackageName + '.' + p_family_obj.FamilyXmlModuleName
        try:
            l_xml_module = importlib.import_module(l_xml, p_family_obj.FamilyPackageName)
        except ImportError as l_error:
            l_msg = 'ERROR "{}" while trying to import XML_module {}.'.format(l_error, p_family_obj.FamilyXmlModuleName)
            print("ERROR - Cannot import:\n    XmlModule: {}\n    Package: {}\n    Error: {}\n\n".format(p_family_obj.FamilyXmlModuleName, p_family_obj.FamilyPackageName, l_msg))
            LOG.error(l_msg)
            l_module = None
        return l_module, l_xml_module

    @staticmethod
    def _initialize_one_module(p_module):
        try:
            l_api = p_module.API()
        except AttributeError as l_reason:
            l_api = None
            LOG.error("ERROR - Cannot get API - Module:{},   Reason: {}.".format(p_module, l_reason))
        return l_api


class API(Utility):

    m_count = 0

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj):
        """
        Build p_pyhouse_obj.House.RefOBJs.FamilyData
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        return self.build_lighting_family_info()

    def build_lighting_family_info(self):
        """
        Used by many test modules.

        NOTE! - Any errors (syntax, etc) in the imported modules (or sub-modules) will cause the import to FAIL!

        This routine will go thru the valid families and create the structure to call each families device routine.
        This device routine is responsible for finding any controllers defined for this computer node and
         initializing the controller and starting anything needed for the given family.
        """
        LOG.info('Starting build_lighting_family_info')
        l_family_data = {}
        self.m_count = 0
        for l_name in VALID_FAMILIES:
            LOG.info(' Building family {}'.format(l_name))
            l_family_obj = Utility._build_one_family_data(l_name, self.m_count)
            l_module, _l_xml_module = Utility._import_one_module(l_family_obj)
            l_api = Utility._initialize_one_module(l_module)
            l_family_obj.FamilyModuleAPI = l_api
            l_family_data[l_family_obj.Name] = l_family_obj
            self.m_count += 1
        return l_family_data

    def start_lighting_families(self, p_pyhouse_obj):
        """
        Load and start the family if there is a controller in the house for the family.

        Runs   <family>_device.API.Start  from Lighting/lighting.py
        """
        LOG.info("Starting lighting families.")
        for l_family_obj in p_pyhouse_obj.House.RefOBJs.FamilyData.itervalues():
            LOG.info('Starting Family {}'.format(l_family_obj.Name))
            l_family_obj.FamilyModuleAPI.Start(p_pyhouse_obj)  # will run <family>_device.API().Start()
        LOG.info("Started all lighting families.")

    def stop_lighting_families(self, p_house_obj):
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            l_family_obj.FamilyModuleAPI.Stop()

    def save_lighting_families(self, p_xml, p_house_obj):
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            l_family_obj.FamilyModuleAPI.SaveXml(p_xml)

    def ReadXml(self, p_device_obj, _p_device_xml):
        LOG.info('family ReadXml was called for device {}.'.format(p_device_obj.Name))
        pass

# ## END DBK

