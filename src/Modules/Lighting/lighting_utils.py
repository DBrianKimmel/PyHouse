"""
-*- test-case-name: PyHouse.src.Modules.Lighting.test.test_lighting_utils -*-

@name: PyHouse/src/Modules/Lighting/lighting_utils.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Aug 9, 2011
@license: MIT License
@summary: This module

"""

# Import system type stuff

# Import PyHouse files
from Modules.Computer import logging_pyh as Logger
# from Modules.Utilities.tools import PrettyPrintAny

g_debug = 0
LOG = Logger.getLogger('PyHouse.LightgUtils ')


class Utility(object):

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def read_family_data(self, p_obj, p_xml):
        l_api = None
        try:
            l_family = p_obj.ControllerFamily
            l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[l_family].FamilyModuleAPI
            l_api.ReadXml(p_obj, p_xml)
        except Exception as e_err:
            l_msg = 'ERROR in lighting_utils.read_family_data() - {0:} {1:} {2:}'.format(e_err, p_obj.Name, l_family)
            LOG.error(l_msg)
            print(l_msg)
        return l_api  # for testing

# ## END DBK
