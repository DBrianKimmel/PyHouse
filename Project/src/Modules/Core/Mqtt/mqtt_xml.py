"""
@name:      PyHouse/Project/src/Modules/Computer/Mqtt/mqtt_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 4, 2015
@Summary:

"""

__updated__ = '2019-07-06'

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files
from Modules.Core.Mqtt.mqtt_data import MqttInformation, MqttBrokerInformation
from Modules.Computer import logging_pyh as Logger
from Modules.Core.data_objects import HouseInformation
from Modules.Core.Utilities.xml_tools import PutGetXML, XmlConfigTools

LOG = Logger.getLogger('PyHouse.Mqtt_Xml       ')
DIVISION = 'ComputerDivision'
SECTION = 'MqttSection'
BROKER = 'Broker'


class Xml(object):

    @staticmethod
    def _read_computer_name(p_pyhouse_obj):
        l_obj = p_pyhouse_obj.Computer
        l_xml = XmlConfigTools.find_xml_section(p_pyhouse_obj, 'ComputerDivision')
        if l_xml is None:
            l_obj.Name = 'Default Name'
            l_obj.Key = 0
            l_obj.Active = True
            return l_obj
        XmlConfigTools.read_base_UUID_object_xml(l_obj, l_xml)
        return l_obj

    @staticmethod
    def _read_house_name(p_pyhouse_obj):
        l_obj = HouseInformation()
        l_xml = XmlConfigTools.find_xml_section(p_pyhouse_obj, 'HouseDivision')
        if l_xml is None:
            l_obj.Name = 'Default Name'
            l_obj.Key = 0
            l_obj.Active = True
            return l_obj
        XmlConfigTools.read_base_UUID_object_xml(l_obj, l_xml)
        return l_obj

    @staticmethod
    def X_read_one_broker(p_xml):
        """
        @param p_xml: XML information for one BrokerBroker
        @return: a b object filled in with data from the XML passed in
        """
        l_obj = MqttBrokerInformation()
        try:
            XmlConfigTools.read_base_UUID_object_xml(l_obj, p_xml)  # Name Key Active
            l_obj.BrokerHost = PutGetXML.get_text_from_xml(p_xml, 'BrokerHost')
            l_obj.BrokerAddress = PutGetXML.get_text_from_xml(p_xml, 'BrokerAddress')
            l_obj.BrokerPort = PutGetXML.get_int_from_xml(p_xml, 'BrokerPort')
            l_obj.UserName = PutGetXML.get_text_from_xml(p_xml, 'BrokerUser')
            l_obj.Password = PutGetXML.get_text_from_xml(p_xml, 'BrokerPassword')
            l_obj.Class = PutGetXML.get_text_from_xml(p_xml, 'Class', 'Local')
        except Exception:
            pass
        if l_obj.UserName == 'None':
            l_obj.UserName = None
        if l_obj.Password == 'None':
            l_obj.Password = None
        return l_obj

    @staticmethod
    def read_mqtt_xml(p_pyhouse_obj, p_api):
        """Read all the broker information.
        Allow for several brokers.
        @return: a dict of broker objects keys = 0, 1, 2...
        """
        l_mqtt = MqttInformation()
        l_count = 0
        l_house = Xml._read_house_name(p_pyhouse_obj).Name
        l_computer = Xml._read_computer_name(p_pyhouse_obj).Name
        l_section = XmlConfigTools.find_xml_section(p_pyhouse_obj, 'ComputerDivision/MqttSection')
        try:
            l_mqtt.ClientID = 'PyH-Comp-' + l_computer
            l_mqtt.Prefix = 'pyhouse/' + l_house
            for l_xml in l_section.iterfind('Broker'):
                l_broker = Xml._read_one_broker(l_xml)
                l_broker.Key = l_count
                l_broker._ClientAPI = p_api
                l_mqtt.Brokers[l_count] = l_broker
                l_count += 1
        except AttributeError as e_err:
            LOG.error('Mqtt Errors: {}'.format(e_err))
        return l_mqtt

    @staticmethod
    def _write_one_broker(p_mqtt):
        """
        @param p_obj: is one broker object.
        @return: the XML for one Broker System
        """
        l_entry = XmlConfigTools.write_base_UUID_object_xml('Broker', p_mqtt)
        PutGetXML().put_int_element(l_entry, 'BrokerAddress', p_mqtt.BrokerAddress)
        PutGetXML().put_int_element(l_entry, 'BrokerHost', p_mqtt.BrokerHost)
        PutGetXML().put_int_element(l_entry, 'BrokerPort', p_mqtt.BrokerPort)
        PutGetXML().put_text_element(l_entry, 'BrokerUser', p_mqtt.UserName)
        PutGetXML().put_text_element(l_entry, 'BrokerPassword', p_mqtt.Password)
        PutGetXML().put_text_element(l_entry, 'Class', p_mqtt.Class)
        return l_entry

    def write_mqtt_xml(self, p_obj):
        """
        @param p_obj: is the Mqtt sub-object in p_pyhouse_obj
        @return:  XML for the MqttSection
        """
        l_count = 0
        l_xml = ET.Element('MqttSection')
        if p_obj.Brokers == {}:
            LOG.info('No MQTT config to write.')
            return l_xml
        try:
            for l_obj in p_obj.Brokers.values():
                l_sys = Xml._write_one_broker(l_obj)
                l_xml.append(l_sys)
                l_count += 1
        except AttributeError as e_err:
            LOG.error('Writing MQTT XML {}'.format(e_err))
            return l_xml
        LOG.info('Wrote {} Mqtt XML entries'.format(l_count))
        return l_xml

#  ## END DBK
