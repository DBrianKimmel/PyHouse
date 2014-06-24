"""
-*- test-case-name: PyHouse.src.Modules.families.test.test_family -*-

@name: PyHouse/src/Modules/families/family.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on May 17, 2013
@license: MIT License
@summary: This module is for lighting families.

It is called from lighting.py and allows any number of different lighting families to be used.
So far Insteon and UPB are developed.  Many others may be added.


"""

# Import system type stuff
import importlib

# Import PyHouse files
from Modules.Core.data_objects import FamilyData
from Modules.families import VALID_FAMILIES
from Modules.utils import pyh_log
# from Modules.utils.tools import PrettyPrintAny

g_debug = 9
LOG = pyh_log.getLogger('PyHouse.Family      ')


class ReadWriteConfigXml(object):
    """
    """


class API(ReadWriteConfigXml):
    """
    """

    m_count = 0

    def build_one_family(self, p_family_name):
        l_family_obj = FamilyData()
        l_family_obj.Name = p_family_name
        l_family_obj.Key = self.m_count
        l_family_obj.Active = True
        l_family_obj.PackageName = 'Modules.families.' + p_family_name
        l_family_obj.ModuleName = 'Device_' + p_family_name
        return l_family_obj

    def XXXimport_one_module(self, p_family_name):
        l_family_obj = self.build_one_family(p_family_name)
        try:
            l_module = importlib.import_module(l_family_obj.PackageName + '.' + l_family_obj.ModuleName, l_family_obj.PackageName)
        except ImportError as l_error:
            l_msg = 'Found error "{0:}" while trying to import module {1:}.'.format(l_error, l_family_obj.ModuleName)
            print("Cannot import:\n    Module: {0:}\n    Package: {1:}\n    Error: {2:}\n\n".format(l_family_obj.ModuleName, l_family_obj.PackageName, l_msg))
            LOG.error(l_msg)
            l_module = None
        return l_module

    def import_module(self, p_family_obj):
        """This routine will attempt to import a module.
        Any errors, such as syntax errors, in the module will cause the import to fail.
        Hopefully, this will detect all such errors and make the developers life much easier by reporting the error.
        """
        try:
            l_module = importlib.import_module(p_family_obj.PackageName + '.' + p_family_obj.ModuleName, p_family_obj.PackageName)
        except ImportError as l_error:
            l_msg = 'Found error "{0:}" while trying to import module {1:}.'.format(l_error, p_family_obj.ModuleName)
            print("Cannot import:\n    Module: {0:}\n    Package: {1:}\n    Error: {2:}\n\n".format(p_family_obj.ModuleName, p_family_obj.PackageName, l_msg))
            LOG.error(l_msg)
            l_module = None
        return l_module

    def initialize_module(self, p_module):
        try:
            l_api = p_module.API()
        except AttributeError as l_reason:
            l_api = None
            LOG.error("Cannot get API - Module:{0:},   Reason: {1:}.".format(p_module, l_reason))
        return l_api

    def build_lighting_family_info(self):
        """
        Called from Lighting.

        NOTE! - Any errors (syntax, etc) in the imported modules (or sub-modules) will cause the import to FAIL!
        """
        l_family_data = {}
        self.m_count = 0
        for l_family in VALID_FAMILIES:
            l_family_obj = self.build_one_family(l_family)
            l_module = self.import_module(l_family_obj)
            try:
                l_family_obj.ModuleAPI = l_module.API()
            except AttributeError as l_reason:
                l_family_obj.ModuleAPI = None
                LOG.error("Cannot get API - Module:{0:},   Reason: {1:}.".format(l_module, l_reason))
            l_family_data[l_family_obj.Name] = l_family_obj
            self.m_count += 1
        return l_family_data

    def XXXstart_one_lighting_family(self, p_x):
        pass

    def start_lighting_families(self, p_pyhouse_obj, p_house_obj):
        """
        Load and start the family if there is a controller in the house for the family.
        Runs Device_<family>.API.Start()
        """
        LOG.info("---Starting lighting families for house {0:}.".format(p_pyhouse_obj.House.Name))
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            l_family_obj.ModuleAPI.Start(p_pyhouse_obj)  # will run Device_<family>.API.Start()
            LOG.info("Started lighting family {0:}.".format(l_family_obj.Name))

    def stop_lighting_families(self, p_xml, p_house_obj):
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            l_family_obj.ModuleAPI.Stop(p_xml)

# ## END DBK

