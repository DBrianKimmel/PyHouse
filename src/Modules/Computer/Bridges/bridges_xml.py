"""
-*- test-case-name: PyHouse/src/Modules/Computer/Bridges/bridges_xml.py -*-

@name:      PyHouse/src/Modules/Computer/Bridges/bridges_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2018 by D. Brian Kimmel
@note:      Created on Dec 24, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2017-12-27'

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files
from Modules.Core.data_objects import BridgesData
from Modules.Computer.Bridges.bridges_data import BridgeData
from Modules.Core.Utilities.xml_tools import XmlConfigTools
from Modules.Core.Utilities import uuid_tools
# from Modules.Computer.computer import COMPUTER_DIVISION
from Modules.Core.Utilities.xml_tools import PutGetXML, XmlConfigTools
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.BridgesXml     ')


class Xml(object):

    @staticmethod
    def _read_one_bridge(p_xml):
        """
        @param p_xml: XML information for one Bridge.
        @return: an Bridge object filled in with data from the XML passed in
        """
        l_obj = BridgeData()
        try:
            XmlConfigTools.read_base_UUID_object_xml(l_obj, p_xml)  # Name Key Active
            l_obj.Connection = PutGetXML.get_text_from_xml(p_xml, 'Connection')
            l_obj.Type = PutGetXML.get_text_from_xml(p_xml, 'Type')
            l_obj.IPv4Address = PutGetXML.get_ip_from_xml(p_xml, 'IPv4Address')
            l_obj.TcpPort = PutGetXML.get_int_from_xml(p_xml, 'Port')
            l_obj.UserName = PutGetXML.get_text_from_xml(p_xml, 'UserName')
            l_obj.Password = PutGetXML.get_text_from_xml(p_xml, 'Password')
        except Exception:
            pass
        return l_obj

    @staticmethod
    def _write_one_bridge(p_bridge_obj):
        """
        @param p_obj: is one broker object.
        @return: the XML for one Broker System
        """
        l_entry = XmlConfigTools.write_base_UUID_object_xml('Broker', p_bridge_obj)
        PutGetXML().put_text_element(l_entry, 'Connection', p_bridge_obj.Connection)
        PutGetXML().put_text_element(l_entry, 'Type', p_bridge_obj.Type)
        PutGetXML().put_ip_element(l_entry, 'IPv4Address', p_bridge_obj.IPv4Address)
        PutGetXML().put_int_element(l_entry, 'Port', p_bridge_obj.TcpPort)
        PutGetXML().put_text_element(l_entry, 'UserName', p_bridge_obj.UserName)
        PutGetXML().put_text_element(l_entry, 'Password', p_bridge_obj.Password)
        return l_entry

    @staticmethod
    def read_bridges_xml(p_pyhouse_obj, p_api):
        """ Read all the BridgesSection XML information and populate the master obj with the data
        Allow for several bridges.

        @param p_pyhouse_obj: The master obj.
        @param p_api: self of the caller - Where to find the bridges api
        @return: a dict of bridge objects keys = 0, 1, 2...
        """
        l_dict = {}
        l_count = 0
        try:
            l_section = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
            if l_section == None:
                return l_dict
            l_section = l_section.find('BridgesSection')
            if l_section == None:
                return l_dict
        except AttributeError as e_err:
            LOG.error('Reading Bridges Configuration information - {}'.format(e_err))
            l_section = None
        try:
            for l_xml in l_section.iterfind('Bridge'):
                l_bridge = Xml._read_one_bridge(l_xml)
                l_bridge.Key = l_count
                l_bridge._ClientAPI = p_api
                l_dict[l_count] = l_bridge
                l_count += 1
        except AttributeError as e_err:
            LOG.error('Bridge Errors: {}'.format(e_err))
        LOG.info('Read {} Bridges'.format(l_count))
        return l_dict

    @staticmethod
    def write_bridges_xml(p_pyhouse_obj, p_api):
        """ Write all the bridges information.
        Allow for several bridges.

        @return:  l_xml - XML for BridgesSection
        """
        l_xml = XmlConfigTools.write_base_UUID_object_xml(COMPUTER_DIVISION, p_pyhouse_obj.Computer)
        return l_xml

    @staticmethod
    def write_bridges_xml(p_pyhouse_obj, p_obj):
        """
        @param p_obj: is the Bridges sub-object in p_pyhouse_obj
        @return:  XML for the BridgesSection
        """
        l_count = 0
        l_xml = ET.Element('BridgesSection')
        if p_obj == {}:
            LOG.info('No Bridges congig to write.')
            return l_xml
        try:
            for l_obj in p_obj.values():
                l_sys = Xml._write_one_bridge(l_obj)
                l_xml.append(l_sys)
                l_count += 1
        except AttributeError as e_err:
            LOG.error('Writing MQTT XML {}'.format(e_err))
            return l_xml
        LOG.info('Wrote {} Mqtt XML entries'.format(l_count))
        return l_xml

# ## END DBK
