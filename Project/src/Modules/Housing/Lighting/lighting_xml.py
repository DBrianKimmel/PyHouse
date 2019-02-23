"""
-*- test-case-name: /home/briank/workspace/PyHouse/Project/src/Modules/Housing/Lighting/lighting_xml.py -*-

@name:      /home/briank/workspace/PyHouse/Project/src/Modules/Housing/Lighting/lighting_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@note:      Created on Jan 21, 2019
@license:   MIT License
@summary:

"""

__updated__ = '2019-02-21'

#  Import system type stuff
# import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
# from Modules.Core.data_objects import ControllerData, UuidData
from Modules.Families.family_utils import FamUtil
from Modules.Computer import logging_pyh as Logger
# from Modules.Drivers.interface import Xml as interfaceXML
from Modules.Core.Utilities.device_tools import XML as deviceXML
# from Modules.Core.Utilities.uuid_tools import Uuid as UtilUuid
# from Modules.Core.Utilities.xml_tools import PutGetXML

LOG = Logger.getLogger('PyHouse.LightingXml    ')


class LightingXML:

    def _read_base_device(self, p_obj, p_xml):
        """
        @param p_obj: is basic controller object
        @param p_xml: is the XML Element for the entire device
        @return: a Controller data object with the base info filled in
        """
        deviceXML.read_base_device_object_xml(p_obj, p_xml)
        return p_obj

    def _write_base_device(self, p_name, p_obj):
        """
        @param p_name: is the xml name such as 'Controller', 'Light', etc.
        """
        l_xml = deviceXML.write_base_device_object_xml(p_name, p_obj)
        return l_xml

    def _read_family_data(self, p_pyhouse_obj, p_obj, p_xml):
        """Read the family specific data for this controller.
        """
        l_api = FamUtil.read_family_data(p_pyhouse_obj, p_obj, p_xml)
        return l_api  # for testing

    def _write_family_data(self, p_pyhouse_obj, p_controller_obj, p_xml):
        try:
            l_family = p_controller_obj.DeviceFamily
            l_family_obj = p_pyhouse_obj.House.FamilyData[l_family]
            l_api = l_family_obj.FamilyXml_ModuleAPI
            l_api.WriteXml(p_xml, p_controller_obj)
        except Exception as e_err:
            LOG.error('ERROR - Family: {} - Err: {}'.format(l_family_obj.Name, e_err))

# ## END DBK
