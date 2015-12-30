"""
-*- test-case-name: PyHouse.Modules.Web.test.test_web_xml -*-

@name:      PyHouse/src/Modules/Web/web_xml.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 17, 2014
@Summary:

"""


#  Import system type stuff
from Modules.Computer import logging_pyh as Logger
from Modules.Core.data_objects import LoginData, WebData
from Modules.Core.setup_logging import l_observer
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Utilities.xml_tools import PutGetXML, XmlConfigTools
import xml.etree.ElementTree as ET


#  Import PyMh files and modules.
LOG = Logger.getLogger('PyHouse.WebXml         ')


class Xml(object):
    """
    """

    @staticmethod
    def _read_port(p_xml):
        """
        @param p_xml: is the web section
        @return: the Port Number
        """
        l_port = PutGetXML.get_int_from_xml(p_xml, 'WebPort', 8580)
        return l_port

    @staticmethod
    def _write_port(p_obj, p_xml):
        """
        @param p_obj: is the Computer.Web object
        """
        l_xml = PutGetXML.put_int_element(p_xml, 'Port', p_obj.WebPort)
        return l_xml

    @staticmethod
    def _read_one_login(p_xml):
        """
        @param p_xml: is the element of one login
        """
        l_obj = LoginData()
        XmlConfigTools.read_base_object_xml(l_obj, p_xml)
        l_obj.LoginFullName = PutGetXML.get_text_from_xml(p_xml, 'FullName')
        l_obj.LoginPasswordCurrent = PutGetXML.get_text_from_xml(p_xml, 'Password')
        l_obj.LoginRole = PutGetXML.get_text_from_xml(p_xml, 'Role')
        return l_obj

    @staticmethod
    def _write_one_login(p_obj):
        """
        @param p_obj: is one login object
        """
        l_xml = XmlConfigTools.write_base_object_xml('Login', p_obj, no_uuid = True)
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
        l_obj.LoginFullName = 'Administrator'
        l_obj.LoginPasswordCurrent = 'admin'
        l_obj.LoginPasswordNew = ''
        l_obj.LoginPasswordChangeFlag = False
        l_obj.LoginRole = 1
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
        LOG.info('Reading Logins')
        try:
            for l_log_xml in l_xml.iterfind('Login'):
                l_obj = Xml._read_one_login(l_log_xml)
                #  LOG.debug('  Reading {}'.format(l_obj.Name))
                l_dict[l_count] = l_obj
                l_count += 1
        except:
            LOG.warn('No Logins found - Adding admin')
            l_obj = Xml._add_default_login()
            l_dict[l_count] = l_obj
            l_count += 1
        if l_count == 0:
            l_dict[0] = Xml._add_default_login()
            l_count += 1
        return l_dict, l_count

    @staticmethod
    def _write_all_logins(p_obj):
        """
        @param p_obj: is the object with all logins
        @return: The entire LoginSection XML element tree
        """
        l_xml = ET.Element('LoginSection')
        if p_obj == {}:
            return l_xml
        try:
            for l_obj in p_obj.itervalues():
                l_sys = Xml._write_one_login(l_obj)
                l_xml.append(l_sys)
        except AttributeError as e_err:
            LOG.error('{}'.format(e_err))
        return l_xml

    @staticmethod
    def read_web_xml(p_pyhouse_obj):
        """
        @param p_pyhouse_xml: is the entire PyHouse Object
        """
        l_obj = WebData()
        l_obj.Logins = {}
        try:
            l_xml = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision').find('WebSection')
            l_obj.Logins, l_count = Xml._read_all_logins(l_xml)
        except Exception as e_err:
            LOG.error('ERROR reading web : {}'.format(e_err))
            l_xml = None
            #  l_login_xml = None
            l_count = 0
        if l_xml == None:
            l_obj.WebPort = 8580
        else:
            l_obj.WebPort = Xml._read_port(l_xml)
        LOG.info('Loaded {} logins.'.format(l_count))
        return l_obj

    @staticmethod
    def write_web_xml(p_pyhouse_obj):
        """
        @param p_pyhouse_obj: Is the entire PyHouse object
        @return: the WebSection XNL element tree
        """
        l_obj = p_pyhouse_obj.Computer.Web
        #  print(PrettyFormatAny.form(l_obj, 'Obj'))
        l_web_xml = ET.Element("WebSection")
        Xml._write_port(l_obj, l_web_xml)
        l_xml = Xml._write_all_logins(l_obj.Logins)
        l_web_xml.append(l_xml)
        return l_web_xml

#  ## END DBK
