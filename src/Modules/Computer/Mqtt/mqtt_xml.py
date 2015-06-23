"""
@name:      PyHouse/src/Modules/Computer/Mqtt/mqtt_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@Copyright: (c)  2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 4, 2015
@Summary:

"""

# Import system type stuff
import xml.etree.ElementTree as ET

# Import PyMh files
from Modules.Core.data_objects import MqttBrokerData
from Modules.Utilities.xml_tools import XmlConfigTools
from Modules.Computer import logging_pyh as Logger


g_debug = 1
LOG = Logger.getLogger('PyHouse.MqttXml        ')


class ReadWriteConfigXml(XmlConfigTools):
    """
    """

    def _read_one_broker(self, p_broker_element):
        l_obj = MqttBrokerData()
        self.read_base_object_xml(l_obj, p_broker_element)
        l_obj.BrokerAddress = self.get_text_from_xml(p_broker_element, 'BrokerAddress')
        l_obj.BrokerPort = self.get_int_from_xml(p_broker_element, 'BrokerPort')
        return l_obj

    def read_mqtt_xml(self, p_pyhouse_obj):
        """Read all the broker information.
        Allow for several brokers - Use the first one '[0]'.
        """
        self.m_count = 0
        l_dict = {}
        l_dict = MqttBrokerData()
        # PrettyPrintAny(l_dict, "l_dict")
        try:
            l_xml = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision').find('MqttSection')
            for l_entry in l_xml.iterfind('Broker'):
                l_obj = self._read_one_broker(l_entry)
                l_obj.Key = self.m_count  # Renumber
                l_dict = l_obj
                self.m_count += 1
        except AttributeError as e_err:
            LOG.error('ERROR in mqtt_xml.read_xml() - {0:}'.format(e_err))
        return l_dict


    def _write_one_broker(self, p_mqtt):
        l_entry = self.write_base_object_xml('Broker', p_mqtt)
        self.put_text_element(l_entry, 'BrokerAddress', p_mqtt.BrokerAddress)
        self.put_text_element(l_entry, 'BrokerPort', p_mqtt.BrokerPort)
        return l_entry

    def write_mqtt_xml(self, p_pyhouse_obj):
        l_mqtt = p_pyhouse_obj.Computer.Mqtt[0]
        self.m_count = 0
        l_xml = ET.Element('MqttSection')
        l_entry = self._write_one_broker(l_mqtt)
        l_xml.append(l_entry)
        self.m_count += 1
        return l_xml

# ## END DBK
