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
from utils import xml_tools


g_debug = 0
Log_Data = {}

class LogData(object):
    def __init__(self):
        self.Debug = None
        self.Error = None


class LoggingUtility(object):

    def read_log(self):
        if g_debug > 8:
            print "Debug - reading log_web"
            print xml_tools.prettify(self.m_root)
        try:
            l_sect = self.m_root.find('Logs')
            l_sect.find('Debug')
        except AttributeError:
            print "Warning - Logs section is missing - Adding empty values now."
            l_sect = ET.SubElement(self.m_root, 'Logs')
            ET.SubElement(l_sect, 'Debug').text = 'None'
            ET.SubElement(l_sect, 'Error').text = 'None'
        l_obj = LogData()
        l_obj.Debug = l_sect.findtext('Debug')
        l_obj.Error = l_sect.findtext('Error')
        Log_Data[0] = l_obj
        try:
            l_sect = self.m_root.find('Web')
            l_sect.find('WebPort')
        except AttributeError:
            l_sect = ET.SubElement(self.m_root, 'Web')
            ET.SubElement(l_sect, 'WebPort').text = 'None'

    def write_log(self):
        if g_debug > 1:
            print "Write log_web", Log_Data[0], vars(Log_Data[0])
        l_sect = self.write_create_empty('Logs')
        l_obj = Log_Data[0]
        # l_entry = self.build_common(l_sect, 'Log', l_obj)
        ET.SubElement(l_sect, 'Debug').text = str(l_obj.Debug)
        ET.SubElement(l_sect, 'Error').text = str(Log_Data[0].Error)
        l_sect = self.write_create_empty('Web')

    def setup_debug_log (self, p_filename):
        """Debug and more severe goes to the base logger
        """
        if g_debug > 0:
            print "log.setup_debug_log() - Name: {0:}".format(p_filename)
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


class LoggingMain(LoggingUtility):

    def __init__(self):
        if g_debug > 0:
            print "log.LoggingMain()"
        Log_Data[0] = LogData()
        try:
            l_debug_name = Log_Data[0].Debug
        except AttributeError:
            l_debug_name = '/var/log/pyhouse/debug'
            Log_Data[0].Debug = l_debug_name
        if l_debug_name == None:
            l_debug_name = '/var/log/pyhouse/debug'
        if g_debug > 4:
            print "log.LoggingMain() debug name ", l_debug_name
        try:
            self.m_error_name = Log_Data[0].Error
        except AttributeError:
            self.m_error_name = '/var/log/pyhouse/error'
        self.m_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')
        self.setup_debug_log(l_debug_name)

    def stop(self):
        logging.shutdown()

# ## END
