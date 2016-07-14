"""
@name:      PyHouse/src/Modules/Hvac/hvac.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 12, 2015
@Summary:

This is the controlling portion of a complete HVAC system.

PyHouse.House.Hvac.
                   Thermostats

"""

__updated__ = '2016-07-14'

#  Import system type stuff

#  Import PyMh files
from Modules.Computer import logging_pyh as Logger
from Modules.Core.data_objects import ThermostatData
from Modules.Housing.Hvac.hvac_xml import XML as hvacXML

LOG = Logger.getLogger('PyHouse.Hvac           ')


class Utility(object):
    """
    """


class API(Utility):

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info("Initialized.")

    def LoadXml(self, p_pyhouse_obj):
        l_obj = hvacXML.read_hvac_xml(p_pyhouse_obj)
        p_pyhouse_obj.House.Hvac = l_obj
        return l_obj

    def Start(self):
        LOG.info("Started.")

    def Stop(self):
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        l_xml = hvacXML.write_hvac_xml(self.m_pyhouse_obj, p_xml)
        p_xml.append(l_xml)
        LOG.info("Saved Hvac XML.")
        return l_xml

#  ## END DBK
