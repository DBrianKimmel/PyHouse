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

# Import PyMh files
import configure


Log_Data = {}

class LogData(object):
    def __init__(self):
        self.Debug = None
        self.Error = None


class LoggingUtility(object):

    def setup_debug_log (self, p_filename):
        """Debug and more severe goes to the base logger
        """
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
        Log_Data[0] = LogData()
        configure.config_xml.ReadConfig().read_log_web()
        try:
            l_debug_name = Log_Data[0].Debug
        except:
            l_debug_name = '/var/log/pyhouse/debug'
            Log_Data[0].Debug = l_debug_name
        try:
            self.m_error_name = Log_Data[0].Error
        except:
            self.m_error_name = '/var/log/pyhouse/error'
        self.m_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')
        self.setup_debug_log(l_debug_name)

    def stop(self):
        logging.shutdown()

### END
