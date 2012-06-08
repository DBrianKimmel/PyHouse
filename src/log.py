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
import platform

# Import PyMh files
import configure_mh


Configure_Data = configure_mh.Configure_Data


class LoggingUtility(object):

    def setup_debug_log (self):
        """Debug and more severe goes to the base logger
        """
        l_debug = logging.getLogger('PyHouse')
        l_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')
        l_debug.setLevel(logging.DEBUG)
        l_fh = logging.handlers.TimedRotatingFileHandler(self.m_debug_name, when = 'midnight', backupCount = 31)
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
        if platform.uname()[0] == 'Windows':
            self.m_debug_name = 'C:/var/debug.log'
            self.m_error_name = 'C:/var/error.log'
        else:
            self.m_debug_name = '/var/log/pymh/debug.log'
            self.m_error_name = '/var/log/pymh/error.log'
        self.m_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')
        l_dict = Configure_Data['Logs']
        self.m_debug_name = l_dict['debug_log']
        self.m_error_name = l_dict['error_log']
        self.setup_debug_log()

    def stop(self):
        logging.shutdown()

### END
