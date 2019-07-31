"""
-*- test-case-name: PyHouse.Modules.Web.test.test_web_xml -*-

@name:      PyHouse/src/Modules/Web/web_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 17, 2014
@Summary:

This is used to load and save the XML definitions.

PyHouse.Computer.Web
            Logins
            Port
            SecurePort
"""

__updated__ = '2019-07-05'

#  Import system type stuff
import xml.etree.ElementTree as ET

#  Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger
from Modules.Core.data_objects import LoginData, WebInformation
from Modules.Core.Utilities.uuid_tools import Uuid
from Modules.Core.Utilities.xml_tools import PutGetXML, XmlConfigTools
LOG = Logger.getLogger('PyHouse.WebXml         ')


class Xml(object):
    """
    """

    @staticmethod
    def _read_ports(p_xml):
        """
        @param p_xml: is the web section
        @return: the Port Number
        """
        l_port = PutGetXML.get_int_from_xml(p_xml, 'WebPort', 8580)
        l_secure = PutGetXML.get_int_from_xml(p_xml, 'SecurePort', 8588)
        l_socket = PutGetXML.get_int_from_xml(p_xml, 'SocketPort', 8581)
        return l_port, l_secure, l_socket

    @staticmethod
    def _write_ports(p_obj, p_xml):
        """
        @param p_obj: is the Computer.Web object
        """
        PutGetXML.put_int_element(p_xml, 'Port', p_obj.WebPort)
        PutGetXML.put_int_element(p_xml, 'SecurePort', p_obj.SecurePort)
        PutGetXML.put_int_element(p_xml, 'SocketPort', p_obj.WebSocketPort)
        return p_xml

    @staticmethod
    def _read_one_login(p_xml):
        """
        @param p_xml: is the element of one login
        """
        l_obj = LoginData()
        XmlConfigTools.read_base_UUID_object_xml(l_obj, p_xml)
        l_obj.LoginFullName = PutGetXML.get_text_from_xml(p_xml, 'FullName')
        l_obj.LoginPasswordCurrent = PutGetXML.get_text_from_xml(p_xml, 'Password')
        l_obj.LoginRole = PutGetXML.get_text_from_xml(p_xml, 'Role')
        LOG.info('Loaded login "{}"'.format(l_obj.LoginFullName))
        return l_obj

    @staticmethod
    def _write_one_login(p_obj):
        """
        @param p_obj: is one login object
        """
        l_xml = XmlConfigTools.write_base_UUID_object_xml('Login', p_obj)
        PutGetXML().put_text_element(l_xml, 'FullName', p_obj.LoginFullName)
        PutGetXML().put_text_element(l_xml, 'Password', p_obj.LoginPasswordCurrent)
        PutGetXML().put_text_element(l_xml, 'Role', p_obj.LoginRole)
        return l_xml

    @staticmethod
    def _add_default_login():
        l_obj = LoginData()
        l_obj.Name = 'admin'
        l_obj.Key = 0
        l_obj.Active = True
        l_obj.UUID = Uuid.create_uuid()
        l_obj.LoginFullName = 'Administrator'
        l_obj.LoginPasswordCurrent = 'admin'
        l_obj.LoginPasswordNew = ''
        l_obj.LoginPasswordChangeFlag = False
        l_obj.LoginRole = 1
        LOG.info('Adding admin login.')
        return l_obj

    @staticmethod
    def _read_all_logins(p_xml):
        """
        @param p_xml: is the WebSection XML element.
        @return: A dict of all logins.
        """
        l_dict = {}
        l_count = 0
        l_xml = p_xml.find('LoginSection')
        if l_xml is None:
            l_dict[0] = Xml._add_default_login()
            return l_dict, 1
        LOG.info('Reading Logins')
        try:
            for l_log_xml in l_xml.iterfind('Login'):
                l_obj = Xml._read_one_login(l_log_xml)
                l_dict[l_count] = l_obj
                l_count += 1
        except Exception as e_err:
            LOG.error('Reading web logins {}'.format(e_err))
        if l_count == 0:
            l_dict[0] = Xml._add_default_login()
            l_count = 1
        return l_dict, l_count

    @staticmethod
    def _write_all_logins(p_obj):
        """
        @param p_obj: is the object with all logins
        @return: The entire LoginSection XML element tree
        """
        l_count = 0
        l_xml = ET.Element('LoginSection')
        if p_obj == {}:
            return l_xml
        try:
            for l_obj in p_obj.values():
                l_sys = Xml._write_one_login(l_obj)
                l_xml.append(l_sys)
                l_count += 1
        except AttributeError as e_err:
            LOG.error('{}'.format(e_err))
        LOG.info('Wrote {} Logins'.format(l_count))
        return l_xml

    @staticmethod
    def read_web_xml(p_pyhouse_obj):
        """
        PyHouse.Computer.Web.
                Logins
                WebPort

        @param p_pyhouse_xml: is the entire PyHouse Object
        """
        l_obj = WebInformation()
        l_obj.Logins = Xml._add_default_login()
        l_obj.WebPort = 8580
        l_obj.SecurePort = 8588
        l_obj.WebSocketPort = 8581
        l_xml = XmlConfigTools.find_xml_section(p_pyhouse_obj, 'ComputerDivision/WebSection')
        if l_xml == None:
            return l_obj
        l_obj.Logins, l_count = Xml._read_all_logins(l_xml)
        l_obj.WebPort, l_obj.SecurePort, l_obj.WebSocketPort = Xml._read_ports(l_xml)
        LOG.info('Loaded {} logins.'.format(l_count))
        return l_obj

    @staticmethod
    def write_web_xml(p_pyhouse_obj):
        """
        @param p_pyhouse_obj: Is the entire PyHouse object
        @return: the WebSection XNL element tree
        """
        l_obj = p_pyhouse_obj.Computer.Web
        l_web_xml = ET.Element("WebSection")
        Xml._write_ports(l_obj, l_web_xml)
        l_web_xml.append(Xml._write_all_logins(l_obj.Logins))
        return l_web_xml

#  ## END DBK
