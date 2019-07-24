"""
@name:      PyHouse/Project/src/Modules/Housing/Lighting/lighting_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@note:      Created on Jan 21, 2019
@license:   MIT License
@summary:

"""

__updated__ = '2019-07-22'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Families.family_utils import FamUtil
from Modules.Computer import logging_pyh as Logger
from Modules.Core.Utilities.device_tools import XML as deviceXML

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
        l_api = None  # FamUtil.read_family_data(p_pyhouse_obj, p_obj, p_xml)
        return l_api  # for testing

    def _write_family_data(self, p_pyhouse_obj, p_controller_obj, p_xml):
        try:
            l_family = p_controller_obj.Family.Name
            l_family_obj = p_pyhouse_obj._Families[l_family]
            l_api = l_family_obj.FamilyXml_ModuleAPI
            l_api.WriteXml(p_xml, p_controller_obj)
        except Exception as e_err:
            LOG.error('ERROR - Family: {} - Err: {}'.format(l_family_obj.Name, e_err))

# ## END DBK
