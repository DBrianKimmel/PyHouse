"""
-*- test-case-name: PyHouse.src.Modules.Irrigation.test.test_irrigation -*-

@name:      PyHouse/src/Modules/Irrigation/irrigation.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com>
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 4, 2014
@Summary:

"""

# Import system type stuff

# Import PyMh files
from Modules.Core.data_objects import IrrigationData
from Modules.Irrigation.irrigation_xml import IrrigationXmlAPI
from Modules.Computer import logging_pyh as Logging

LOG = Logging.getLogger('PyHouse.Irrigation     ')


class Utility(object):
    """
    """

    def update_pyhouse_obj(self, p_pyhouse_obj):
        p_pyhouse_obj.House.DeviceOBJs.Irrigation = IrrigationData()

    def add_api_references(self, p_pyhouse_obj):
        pass

    def setup_xml(self, p_pyhouse_obj):
        l_xml = p_pyhouse_obj.Xml.XmlRoot
        try:
            l_xml = l_xml.find('HouseDivision')
            l_xml = l_xml.find('IrrigationSection')
        except AttributeError as e_err:
            LOG.error('Error {}'.format(e_err))
        return l_xml


class API(Utility):

    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self):
        l_obj = IrrigationXmlAPI().read_irrigation_xml(self.m_pyhouse_obj)
        self.m_pyhouse_obj.House.DeviceOBJs.Irrigation = l_obj

    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        (l_xml, l_count) = IrrigationXmlAPI().write_irrigation_xml(self.m_pyhouse_obj.House.DeviceOBJs.Irrigation)
        p_xml.append(l_xml)
        LOG.info("Saved {} Irrigation XML.".format(l_count))
        return p_xml

# ## END DBK
