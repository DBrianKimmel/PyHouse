"""
-*- test-case-name: PyHouse.Modules.families.test.test_family -*-

@name: PyHouse/Modules/families/family.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on May 17, 2013
@license: MIT License
@summary: This module is for lighting familyies.
"""

# Import system type stuff
import importlib

# Import PyHouse files
from Modules.Core.data_objects import FamilyData
from Modules.families import VALID_FAMILIES
from Modules.utils import pyh_log

g_debug = 1
LOG = pyh_log.getLogger('PyHouse.Family      ')


class API(object):
    """
    """

    def build_one_family(self, p_family, p_count):
        l_family_obj = FamilyData()
        l_family_obj.Name = p_family
        l_family_obj.Key = p_count
        l_family_obj.PackageName = 'Modules.families.' + p_family
        l_family_obj.ModuleName = 'Device_' + p_family
        return l_family_obj

    def import_module(self, p_family_obj):
        try:
            l_module = importlib.import_module(p_family_obj.PackageName + '.' + p_family_obj.ModuleName, p_family_obj.PackageName)
        except ImportError as l_error:
            l_module = None
            print("Cannot import:\n    Module: {0:}\n    Package: {1:}\n    Error: {2:}<<".format(p_family_obj.ModuleName, p_family_obj.PackageName, l_error))
        return l_module

    def build_lighting_family_info(self, p_house_obj):
        """NOTE!
        Any errors in the imported modules (or sub-modules) will cause the import to FAIL!
        """
        l_family_data = {}
        l_count = 0
        for l_family in VALID_FAMILIES:
            l_family_obj = self.build_one_family(l_family, l_count)
            l_module = self.import_module(l_family_obj)
            try:
                l_family_obj.API = l_module.API(p_house_obj)
            except AttributeError:
                l_family_obj.API = None
                LOG.error("Cannot get API - Module:{0:}, House:{1:}.".format(l_module, p_house_obj.Name))
            l_family_data[l_count] = l_family_obj
            l_count += 1
        return l_family_data

    def start_lighting_families(self, p_house_obj):
        """Load and start the family if there is a controller in the house for the family.
        Runs Device_<family>.API.Start()
        """
        LOG.info("Starting lighting families for house {0:}.".format(p_house_obj.Name))
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            l_family_obj.API.Start(p_house_obj)  # will run Device_<family>.API.Start()
            LOG.info("Started lighting family {0:}.".format(l_family_obj.Name))

    def stop_lighting_families(self, p_xml, p_house_obj):
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            l_family_obj.API.Stop(p_xml)

# ## END DBK

