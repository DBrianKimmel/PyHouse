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
from Modules.utils import xml_tools
from Modules.utils import pyh_log
# from Modules.utils.tools import PrettyPrintAny

g_debug = 1
LOG = pyh_log.getLogger('PyHouse.Family      ')


class ReadWriteConfigXml(xml_tools.XmlConfigTools):
    """Read and write the interface information based in the interface type.
    """

    def read_family_xml(self, p_controller_obj, p_controller_xml):
        """Update the controller object by extracting the passed in XML.
        """
        pass

    def write_family_xml(self, p_controller_obj, p_xml):
        pass


class Utility(ReadWriteConfigXml):
    """
    """

    def _build_one_family_data(self, p_family_name):
        """Build up the FamilyData entry for a single family
        """
        l_family_obj = FamilyData()
        l_family_obj.Name = p_family_name
        l_family_obj.Key = self.m_count
        l_family_obj.Active = True
        l_family_obj.FamilyPackageName = 'Modules.families.' + p_family_name
        l_family_obj.FamilyDeviceModuleName = p_family_name + '_device'
        l_family_obj.FamilyXmlModuleName = p_family_name + '_xml'
        return l_family_obj

    def _import_one_module(self, p_family_obj):
        """
        This routine will attempt to import a module.

        Any errors, such as syntax errors, in the module will cause the import to fail.
        Hopefully, this method will detect all such errors and make the developers life much easier by reporting the error.
        """
        l_device = p_family_obj.FamilyPackageName + '.' + p_family_obj.FamilyDeviceModuleName
        l_xml = p_family_obj.FamilyPackageName + '.' + p_family_obj.FamilyXmlModuleName
        try:
            l_module = importlib.import_module(l_device, p_family_obj.FamilyPackageName)
        except ImportError as l_error:
            l_msg = 'ERROR "{0:}" while trying to import module {1:}.'.format(l_error, p_family_obj.FamilyDeviceModuleName)
            print("ERROR - Cannot import:\n    Module: {0:}\n    Package: {1:}\n    Error: {2:}\n\n".format(p_family_obj.FamilyDeviceModuleName, p_family_obj.FamilyPackageName, l_msg))
            LOG.error(l_msg)
            l_module = None
        return l_module

    def _initialize_one_module(self, p_module):
        """
        """
        try:
            l_api = p_module.API()
        except AttributeError as l_reason:
            l_api = None
            LOG.error("ERROR - Cannot get API - Module:{0:},   Reason: {1:}.".format(p_module, l_reason))
        return l_api


class API(Utility):
    """
    """

    m_count = 0

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        return self.build_lighting_family_info()

    def build_lighting_family_info(self):
        """
        Called from Lighting.

        NOTE! - Any errors (syntax, etc) in the imported modules (or sub-modules) will cause the import to FAIL!
        """
        if g_debug >= 1:
            LOG.debug('Starting build_lighting_family_info')
        l_family_data = {}
        self.m_count = 0
        for l_family in VALID_FAMILIES:
            l_family_obj = self._build_one_family_data(l_family)
            l_module = self._import_one_module(l_family_obj)
            l_api = self._initialize_one_module(l_module)
            l_family_obj.FamilyModuleAPI = l_api
            l_family_data[l_family_obj.Name] = l_family_obj
            self.m_count += 1
        return l_family_data

    def start_lighting_families(self, p_pyhouse_obj, p_house_obj):
        """
        Load and start the family if there is a controller in the house for the family.
        Runs Device_<family>.API.Start()
        """
        if g_debug >= 1:
            LOG.info("Starting lighting families.")
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            if g_debug >= 1:
                LOG.debug('Starting Family {0:}'.format(l_family_obj.Name))
            l_family_obj.FamilyModuleAPI.Start(p_pyhouse_obj)  # will run Device_<family>.API.Start()
        if g_debug >= 1:
            LOG.info("Started all lighting families.")

    def stop_lighting_families(self, p_house_obj):
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            l_family_obj.FamilyModuleAPI.Stop()

    def save_lighting_families(self, p_xml, p_house_obj):
        for l_family_obj in p_house_obj.FamilyData.itervalues():
            l_family_obj.FamilyModuleAPI.SaveXml(p_xml)

    def ReadXml(self, p_device_obj, p_device_xml):
        LOG.info('family ReadXml was called for device {0:}.'.format(p_device_obj.Name))
        pass

# ## END DBK

