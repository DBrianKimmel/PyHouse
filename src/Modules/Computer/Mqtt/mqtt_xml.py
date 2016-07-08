"""
@name:      PyHouse/src/Modules/Computer/Mqtt/mqtt_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 4, 2015
@Summary:

"""

__updated__ = '2016-07-06'

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files
from Modules.Core.data_objects import MqttBrokerData
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.xml_tools import PutGetXML, XmlConfigTools

LOG = Logger.getLogger('PyHouse.Mqtt_Xml       ')
DIVISION = 'ComputerDivision'
SECTION = 'MqttSection'
BROKER = 'Broker'


class Xml(object):

    @staticmethod
    def _read_one_broker(p_xml):
        """
        @param p_xml: XML information for one Broker.
        @return: an IrrigationZone object filled in with data from the XML passed in
        """
        l_obj = MqttBrokerData()
        try:
            XmlConfigTools.read_base_object_xml(l_obj, p_xml)
            l_obj.BrokerAddress = PutGetXML.get_text_from_xml(p_xml, 'BrokerAddress')
            l_obj.BrokerPort = PutGetXML.get_int_from_xml(p_xml, 'BrokerPort')
            l_obj.UserName = PutGetXML.get_text_from_xml(p_xml, 'BrokerUser')
            l_obj.Password = PutGetXML.get_text_from_xml(p_xml, 'BrokerPassword')
        except Exception:
            pass
        return l_obj

    @staticmethod
    def read_mqtt_xml(p_pyhouse_obj):
        """Read all the broker information.
        Allow for several brokers.
        @return: a dict of broker objects keys = 0, 1, 2...
        """
        l_dict = {}
        l_count = 0
        try:
            l_section = p_pyhouse_obj.Xml.XmlRoot.find(DIVISION)
            if l_section == None:
                return l_dict
            l_section = l_section.find(SECTION)
            if l_section == None:
                return l_dict
        except AttributeError as e_err:
            LOG.error('Reading MQTT Configuration information - {}'.format(e_err))
            l_section = None
        try:
            for l_xml in l_section.iterfind(BROKER):
                l_broker = Xml._read_one_broker(l_xml)
                l_broker.Key = l_count
                l_dict[l_count] = l_broker
                l_count += 1
        except AttributeError as e_err:
            LOG.error('Mqtt Errors: {}'.format(e_err))
        return l_dict


    @staticmethod
    def _write_one_broker(p_mqtt):
        """
        @param p_obj: is one broker object.
        @return: the XML for one Broker System
        """
        l_entry = XmlConfigTools.write_base_object_xml('Broker', p_mqtt)
        PutGetXML().put_int_element(l_entry, 'BrokerAddress', p_mqtt.BrokerAddress)
        PutGetXML().put_int_element(l_entry, 'BrokerPort', p_mqtt.BrokerPort)
        PutGetXML().put_text_element(l_entry, 'BrokerUser', p_mqtt.UserName)
        PutGetXML().put_text_element(l_entry, 'BrokerPassword', p_mqtt.Password)
        return l_entry

    def write_mqtt_xml(self, p_obj):
        """
        @param p_obj: is the Mqtt sub-object in p_pyhouse_obj
        @return:  XML for the MqttSection
        """
        l_count = 0
        l_xml = ET.Element(SECTION)
        if p_obj == {}:
            LOG.info('No MQTT congig to write.')
            return l_xml
        try:
            for l_obj in p_obj.itervalues():
                l_sys = Xml._write_one_broker(l_obj)
                l_xml.append(l_sys)
                l_count += 1
        except AttributeError as e_err:
            LOG.error('Writing MQTT XML {}'.format(e_err))
            return l_xml
        LOG.info('Wrote {} Mqyy XML entries'.format(l_count))
        return l_xml

#  ## END DBK
