#!/usr/bin/python

"""Log module.
This is a Main Module - always present.

Default to /var/log/pymh
Be sure it exists and is read/write for the user running PyMh.
"""

# Import system type stuff
import datetime
import logging
import logging.handlers

# Import PyMh files
import configure_mh


class LoggingUtility(object):

    def setup_debug_log (self):
        """Debug and more severe goes to the base logger
        """
        l_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')
        l_debug = logging.getLogger('PyHouse')
        l_debug.setLevel(logging.DEBUG)
        l_fh = logging.handlers.RotatingFileHandler(self.m_debug_name, maxBytes = 1000000, backupCount = 9)
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
        self.m_debug_name = '/var/log/pymh/debug.log'
        self.m_error_name = '/var/log/pymh/error.log'
        self.m_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s - %(message)s')

    def configure(self):
        self.m_config = configure_mh.ConfigureMain()
        l_dict = self.m_config.get_value('Logs')
        self.m_debug_name = l_dict['debug_log']
        self.m_error_name = l_dict['error_log']
        self.setup_debug_log()
        #self.setup_error_log()

### END
