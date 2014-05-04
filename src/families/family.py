'''
Created on May 17, 2013

@author: briank
'''

# Import system type stuff
import importlib

# Import PyHouse files
from src.families import VALID_FAMILIES
from src.utils import pyh_log


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# + = NOT USED HERE
LOG = pyh_log.getLogger('PyHouse.Family      ')


class FamilyData(object):
    """A container for every family that has been defined.
    Usually called 'l_family_obj'
    Since they contain API instances, each house has it's own collection of Family Dicts.
    """

    def __init__(self):
        self.Name = ''
        self.Key = 0
        self.Active = True
        self.API = None  # Device_Insteon.API()
        self.ModuleName = ''  # Device_Insteon
        self.PackageName = ''  # src.families.Insteon

    def reprJSON(self):
        l_ret = dict(Name = self.Name, Key = self.Key, Active = self.Active,
            ModuleName = self.ModuleName,
            PackageName = self.PackageName
            )
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
            LOG.info("Adding lighting Family:{0:} for House:{1:}".format(l_family, p_house_obj.Name))
            l_family_obj = FamilyData()
            l_family_obj.Name = l_family
            l_family_obj.Key = l_count
            l_family_obj.PackageName = 'src.families.' + l_family
            l_family_obj.ModuleName = 'Device_' + l_family
            try:
                l_module = importlib.import_module(l_family_obj.PackageName + '.' + l_family_obj.ModuleName, l_family_obj.PackageName)
            except ImportError as e:
                l_module = None
                LOG.error("Cannot import - Module:{0:}, Package:{1:}. {2:}".format(l_family_obj.ModuleName, l_family_obj.PackageName, e))
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

