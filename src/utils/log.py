#!/usr/bin/python

"""Log module.
This is a Main Module - always present.

Default to /var/log/pymh
Be sure it exists and is read/write for the user running PyHouse.

This module sets up the logging used by PyHouse.
It configures 'PyHouse' in the logging standard library module.
"""

# Import system type stuff
import logging.handlers
import xml.etree.ElementTree as ET

# Import PyMh files
from src.utils import xml_tools


g_debug = 3
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 - Config file handling
# + = NOT USED HERE


class LogData(object):

    def __init__(self):
        self.Debug = None
        self.Error = None

    def __str__(self):
        l_ret = "Logs:: "
        l_ret += "Debug:{0:}, ".format(self.Debug)
        l_ret += "Error:{0:};".format(self.Error)
        return l_ret


class LoggingUtility(xml_tools.ConfigFile):

    def read_xml_config_logfiles(self, p_log_obj, p_xml_root):
        try:
            l_sect = p_xml_root.find('Logs')
            l_sect.find('Debug')
        except AttributeError:
            print "log.read_xml_config_logfiles() - Warning - Logs section is missing - Adding empty values now."
            l_sect = ET.SubElement(p_xml_root, 'Logs')
            ET.SubElement(l_sect, 'Debug').text = 'None'
            ET.SubElement(l_sect, 'Error').text = 'None'
        p_log_obj.Debug = l_sect.findtext('Debug')
        p_log_obj.Error = l_sect.findtext('Error')
        if g_debug >= 3:
            print "log.read_xml_config_logfiles() - Debug:{0:}, Error:{1:}".format(p_log_obj.Debug, p_log_obj.Error)

    def write_log_xml(self, p_log_data):
        l_log_xml = ET.Element("Logs")
        self.put_text_element(l_log_xml, 'Debug', p_log_data.Debug)
        self.put_text_element(l_log_xml, 'Error', p_log_data.Error)
        if g_debug >= 3:
            print "Write log_web", p_log_data, l_log_xml
            print xml_tools.prettify(l_log_xml)
        return l_log_xml

    def setup_debug_log (self, p_filename):
        """Debug and more severe goes to the base logger
        """
        if g_debug >= 2:
            print "log.setup_debug_log() - FileName:{0:}".format(p_filename)
        l_debug = logging.getLogger('PyHouse')
        l_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')
        l_debug.setLevel(logging.DEBUG)
        l_fh = logging.handlers.TimedRotatingFileHandler(p_filename, when = 'midnight', backupCount = 31)
        l_fh.setLevel(logging.DEBUG)
        l_fh.setFormatter(l_formatter)
        l_debug.addHandler(l_fh)

    def setup_error_log (self):
        self.m_logger_error = logging.getLogger('PyHouseError')
        self.m_logger_error.setLevel(logging.DEBUG)
        self.fh_error = logging.FileHandler(self.m_error_name)
        self.fh_error.setFormatter(self.m_formatter)
        l_handler = logging.handlers.RotatingFileHandler(self.m_error_name, maxBytes = 1000000, backupCount = 9)
        self.m_logger_error.addHandler(l_handler)


class API(LoggingUtility):

    def __init__(self):
        if g_debug >= 2:
            print "log.API.__init__()"
        self.m_log_data = LogData()

    def Start(self, p_pyhouse_obj):
        if g_debug >= 2:
            print "log.API.Start()"
        self.read_xml_config_logfiles(self.m_log_data, p_pyhouse_obj.XmlRoot)
        self.setup_debug_log(self.m_log_data.Debug)
        return self.m_log_data

    def Stop(self):
        if g_debug >= 2:
            print "log.API.Stop()"
        l_xml = self.write_log_xml(self.m_log_data)
        return l_xml
        #logging.shutdown()

# ## END DBK
