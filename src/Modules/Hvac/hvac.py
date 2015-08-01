"""
@name:      PyHouse/src/Modules/Hvac/hvac.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 12, 2015
@Summary:

This is the controlling portion of a complete HVAC system.

"""


# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import ThermostatData
from Modules.Hvac.hvac_xml import XML as hvacXML
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Hvac           ')


class Utility(object):
    """
    """


class API(Utility):

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self):
        hvacXML.read_hvac_xml(self.m_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        l_xml = self.write_all_thermostats_xml(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Saved Hvac XML.")
        return l_xml

# ## END DBK
