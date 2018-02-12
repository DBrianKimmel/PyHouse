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

__updated__ = '2018-02-11'

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files
from Modules.Computer.Bridges import VALID_BRIDGE_TYPES
from Modules.Computer.Bridges.bridges_data import BridgeData
from Modules.Families.Hue.Hue_xml import Xml as hueXML
# from Modules.Computer.computer import COMPUTER_DIVISION
from Modules.Core.Utilities.xml_tools import PutGetXML, XmlConfigTools
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.BridgesXml     ')


class Xml(object):

    @staticmethod
    def _read_type(p_xml):
        l_type = PutGetXML.get_text_from_xml(p_xml, 'Type')
        if l_type not in VALID_BRIDGE_TYPES:
            LOG.error('Invalid bridge type: {} - Changed to: {}'.format(l_type, VALID_BRIDGE_TYPES[0]))
            l_type = VALID_BRIDGE_TYPES[0]
        return l_type

    @staticmethod
    def _read_one_bridge(p_xml):
        """ Read all the information for a single Bridge device.
        Call specific bridge information readers for some types of bridges.

        @param p_xml: XML information for one Bridge.
        @return: an Bridge object filled in with data from the XML passed in
        """
        l_obj = BridgeData()
        try:
            XmlConfigTools.read_base_UUID_object_xml(l_obj, p_xml)  # Name Key Active
            l_obj.Connection = PutGetXML.get_text_from_xml(p_xml, 'Connection')
            l_obj.Type = Xml._read_type(p_xml)
            l_obj.IPv4Address = PutGetXML.get_ip_from_xml(p_xml, 'IPv4Address')
            l_obj.TcpPort = PutGetXML.get_int_from_xml(p_xml, 'Port')
            l_obj.UserName = PutGetXML.get_text_from_xml(p_xml, 'UserName')
            l_obj.Password = PutGetXML.get_text_from_xml(p_xml, 'Password')
            if l_obj.Type == "Hue":
                hueXML.ReadXml(l_obj, p_xml)
        except Exception:
            pass
        return l_obj

    @staticmethod
    def _write_one_bridge(p_bridge_obj):
        """ Write all the information for a single Bridge device.

        @param p_obj: is one broker object.
        @return: the XML for one Broker System
        """
        l_entry = XmlConfigTools.write_base_UUID_object_xml('Bridge', p_bridge_obj)
        PutGetXML().put_text_element(l_entry, 'Connection', p_bridge_obj.Connection)
        PutGetXML().put_text_element(l_entry, 'Type', p_bridge_obj.Type)
        PutGetXML().put_ip_element(l_entry, 'IPv4Address', p_bridge_obj.IPv4Address)
        PutGetXML().put_int_element(l_entry, 'Port', p_bridge_obj.TcpPort)
        PutGetXML().put_text_element(l_entry, 'UserName', p_bridge_obj.UserName)
        PutGetXML().put_text_element(l_entry, 'Password', p_bridge_obj.Password)
        if p_bridge_obj.Type == "Hue":
            hueXML.WriteXml(l_entry, p_bridge_obj)
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
    def write_bridges_xml(p_pyhouse_obj):
        """
        @param p_obj: is the Bridges sub-object in p_pyhouse_obj
        @return:  XML for the BridgesSection
        """
        l_objs = p_pyhouse_obj.Computer.Bridges
        l_count = 0
        l_xml = ET.Element('BridgesSection')
        if l_objs == {}:
            LOG.info('No Bridges congig to write.')
            return l_xml
        try:
            for l_obj in l_objs.values():
                l_sys = Xml._write_one_bridge(l_obj)
                l_xml.append(l_sys)
                l_count += 1
        except AttributeError:  # No bridges
            pass
        LOG.info('Wrote {} Bridges XML entries'.format(l_count))
        return l_xml

# ## END DBK
