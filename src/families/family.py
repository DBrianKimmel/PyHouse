'''
Created on May 17, 2013

@author: briank
'''

# Import system type stuff
import logging
import importlib

# Import PyHouse files
from src.families import VALID_FAMILIES


g_debug = 3
# 0 = off
# 1 = major routine entry

g_logger = logging.getLogger('PyHouse.Family  ')


class FamilyData(object):
    """A container for every family that has been defined.
    """

    def __init__(self):
        self.Active = False
        self.API = None
        self.ModuleName = ''
        self.Key = 0
        self.ModuleRef = ''
        self.Name = ''
        self.PackageName = ''

    def __str__(self):
        l_ret = "FamilyData:: "
        l_ret += "Name:{0:}, ".format(self.Name)
        l_ret += "Key:{0:}, ".format(self.Key)
        l_ret += "Active:{0:}, ".format(self.Active)
        l_ret += "PackageName:{0:}, ".format(self.PackageName)
        l_ret += "ModuleName:{0:}, ".format(self.ModuleName)
        l_ret += "ModuleRef:{0:}, ".format(self.ModuleRef)
        l_ret += "API:{0:}".format(self.API)
        return l_ret


class LightingUtility(FamilyData):
    """
    """

    def build_lighting_family_info(self, p_house_obj):
        """NOTE!
        Any errors in the imported modules (or sub-modules) will cause the import to FAIL!
        """
        l_family_data = {}
        l_count = 0
        for l_family in VALID_FAMILIES:
            if g_debug >= 2:
                print "family.build_lighting_family_info() - House:{0:}, Name:{1:}".format(p_house_obj.Name, l_family)
            l_family_obj = FamilyData()
            l_family_obj.Active = True
            l_family_obj.Name = l_family
            l_family_obj.Key = l_count
            l_family_obj.PackageName = 'src.families.' + l_family
            l_family_obj.ModuleName = 'Device_' + l_family
            try:
                l_module = importlib.import_module(l_family_obj.PackageName + '.' + l_family_obj.ModuleName, l_family_obj.PackageName)
            except ImportError:
                if g_debug >= 1:
                    print "    family.build_lighting_family_info() - ERROR - Cannot import module {0:}".format(l_family_obj.ModuleName)
                l_module = None
                g_logger.error("Cannot import - Module:{0:}, Package:{1:}.".format(l_family_obj.ModuleName, l_family_obj.PackageName))
            l_family_obj.ModuleRef = l_module
            try:
                l_family_obj.API = l_module.API(p_house_obj)
            except AttributeError:
                if g_debug >= 1:
                    print "    family.build_lighting_family_info() - ERROR - NO API"
                l_family_obj.API = None
                g_logger.error("Cannot get API - Module:{0:}, House:{1:}.".format(l_module, p_house_obj.Name))
            if g_debug >= 2:
                print "   from {0:} import {1:}".format(l_family_obj.PackageName, l_family_obj.ModuleName)
                print "   l_family_data  Key:{0:} -".format(l_count), l_family_obj
            l_family_data[l_count] = l_family_obj
            l_count += 1
        return l_family_data

    def start_lighting_families(self, p_house_obj):
        """Load and start the family if there is a controller in the house for the family.
        Runs Device_<family>.API.Start()
        """
        if g_debug >= 2:
            print "family.start_lighting_families()", p_house_obj.FamilyData
        g_logger.info("Starting lighting families.")
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            if g_debug >= 3:
                print "family.start_lighting_families() - Starting {0:}".format(l_family_obj.Name), l_family_obj
            l_family_obj.API.Start(p_house_obj)  # will run Device_<family>.API.Start()
            g_logger.info("Started lighting family {0:}.".format(l_family_obj.Name))

    def stop_lighting_families(self, p_xml, p_house_obj):
        if g_debug >= 2:
            print "family.stop_lighting_families()"
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            l_family_obj.API.Stop(p_xml)

# ## END DBK

