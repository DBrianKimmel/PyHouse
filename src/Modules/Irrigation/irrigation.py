"""
-*- test-case-name: PyHouse.src.Modules.irrigation.test.test_irrigation -*-

@name: PyHouse/src/Modules/irrigation/test/irrigation.py
@author: briank
@contact: <d.briankimmel@gmail.com>
@Copyright: (c)  2014 by briank
@license: MIT License
@note: Created on Jul 4, 2014
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import IrrigationData
from Modules.Utilities import xml_tools
from Modules.Computer import logging_pyh as Logging
# from Modules.Utilities.tools import PrettyPrintAny

g_debug = 0
LOG = Logging.getLogger('PyHouse.Irrigation  ')


class ReadWriteConfigXml(xml_tools.XmlConfigTools):
    """
    """
    m_count = 0

    def _read_irrigation_data(self, p_obj, p_xml):
        """
        @return: a IrrigationData object.
        """
        p_obj.ControllerFamily = self.get_text_from_xml(p_xml, 'ControllerFamily')
        return p_obj

    def _read_family_data(self, p_obj, p_xml):
        try:
            l_family = p_obj.ControllerFamily
            l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[l_family].FamilyModuleAPI
            l_api.extract_device_xml(p_obj, p_xml)
        except KeyError:
            pass

    def read_one_irrigation_xml(self, p_item_element):
        """
        @return: an IrrigationData object
        """
        l_obj = IrrigationData()
        self.read_base_object_xml(l_obj, p_item_element)
        l_obj.Key = self.m_count  # Renumber
        self._read_irrigation_data(l_obj, p_item_element)
        self._read_family_data(l_obj, p_item_element)
        return l_obj

    def read_all_irrigation_xml(self, p_sect_element):
        """
        """
        l_xml_sect = self.setup_xml(self.m_pyhouse_obj)
        l_ret = {}
        self.m_count = 0
        if l_xml_sect == None:
            return l_ret
        try:
            for l_xml in p_sect_element.iterfind('Irrigation'):
                l_obj = self.read_one_irrigation_xml(l_xml)
                l_ret[self.m_count] = l_obj
                self.m_count += 1
        except AttributeError as e:
            LOG.error('ERROR is Reading irrigation information - {0:}'.format(e))
        # PrettyPrintAny(self.m_pyhouse_obj.House.OBJs.Irrigation, 'irrigation - ReadAll ', 100)
        return l_ret


    def _write_irrigation_data(self, p_obj, p_xml):
        pass

    def _write_family_data(self, p_obj, p_xml):
        try:
            l_api = self.m_pyhouse_obj.House.OBJs.FamilyData[p_obj.ControllerFamily].FamilyModuleAPI
            l_api.insert_device_xml(p_xml, p_obj)
        except KeyError:
            pass

    def write_one_thermostat_xml(self, p_thermostat_obj):
        """
        """
        l_xml = self.write_base_object_xml('Irrigation', p_thermostat_obj)
        self._write_irrigation_data(p_thermostat_obj, l_xml)
        self._write_family_data(p_thermostat_obj, l_xml)
        return l_xml

    def write_all_irrigation_xml(self, p_thermostat_sect_obj):
        """Create a sub tree for 'Irrigation' - the sub elements do not have to be present.
        @return: a sub tree ready to be appended to "something"
        """
        l_xml = ET.Element('IrrigationSection')
        self.m_count = 0
        try:
            for l_obj in p_thermostat_sect_obj.itervalues():
                l_entry = self.write_one_thermostat_xml(l_obj)
                l_xml.append(l_entry)
                self.m_count += 1
        except AttributeError as e:
            LOG.error('ERROR in saving irrigation data - {0:}'.format(e))
        return l_xml


class Utility(ReadWriteConfigXml):
    """
    """

    def update_pyhouse_obj(self, p_pyhouse_obj):
        p_pyhouse_obj.House.OBJs.Irrigation = IrrigationData()

    def add_api_references(self, p_pyhouse_obj):
        pass

    def setup_xml(self, p_pyhouse_obj):
        l_xml = p_pyhouse_obj.Xml.XmlRoot
        try:
            l_xml = l_xml.find('HouseDivision')
            l_xml = l_xml.find('IrrigationSection')
        except AttributeError:
            pass
        return l_xml


class API(Utility):

    m_pyhouse_obj = None

    def Start(self, p_pyhouse_obj):
        self.update_pyhouse_obj(p_pyhouse_obj)
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.House.OBJs.Irrigation = self.read_all_irrigation_xml(self.setup_xml(p_pyhouse_obj))

    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        l_xml = self.write_all_irrigation_xml(self.m_pyhouse_obj.House.OBJs.Irrigation)
        p_xml.append(l_xml)
        return l_xml

# ## END DBK
