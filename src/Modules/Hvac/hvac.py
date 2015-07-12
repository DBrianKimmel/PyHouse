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
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.Hvac           ')


class Utility(object):
    """
    """

    def update_pyhouse_obj(self, p_pyhouse_obj):
        p_pyhouse_obj.House.DeviceOBJs.Thermostats = ThermostatData()

    def add_api_references(self, p_pyhouse_obj):
        pass

    def setup_xml(self, p_pyhouse_obj):
        try:
            l_xml = p_pyhouse_obj.Xml.XmlRoot.find('HouseDivision').find('ThermostatSection')
        except AttributeError as e_err:
            LOG.error('SetupXML ERROR {0:}'.format(e_err))
            l_xml = None
        return l_xml


class API(Utility):

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self):
        self.update_pyhouse_obj(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.DeviceOBJs.Thermostats = self.read_all_thermostats_xml(self.m_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self):
        LOG.info("Stopped.")

    def SaveXml(self, p_xml):
        l_xml = self.write_all_thermostats_xml(self.m_pyhouse_obj)
        p_xml.append(l_xml)
        LOG.info("Saved Hvac XML.")
        return l_xml

# ## END DBK
