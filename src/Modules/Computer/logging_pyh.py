"""
-*- test-case-name: PyHouse.Modules.Computer.test.test_logging_pyh -*-

@name:      PyHouse/src/Modules/Computer/logging_pyh.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2014-2015 by D. Brian Kimmel
@note:      Created on Jan 20, 2014
@license:   MIT License
@summary:   Log Module.

Provides a Debug log and a Error log file to review.

Default to /var/log/pyhouse/xxx
Be sure it exists and is read/write for the user running PyHouse.
The reason for the pyhouse directory is to allow a non-root process access to the files.
Be sure that the pyhouse process has read/write privileges to the directory.

This module sets up the logging used by PyHouse.
It configures PyHouse in the logging standard library module plus twisted logging.


"""

# Import system type stuff
import logging
import xml.etree.ElementTree as ET

# Import PyMh files
# from Modules.Utilities.xml_tools import XmlConfigTools


def getLogger(p_name):
    return logging.getLogger(p_name)

def addHandler(p_handler):
    logging.Logger.addHandler(p_handler)


class ReadWriteConfigXml(object):
    """
    """

    def read_xml(self, p_pyhouse_obj):
        pass

    def write_xml(self, p_log_data):
        l_log_xml = ET.Element("LogSection")
        self.put_text_element(l_log_xml, 'Debug', p_log_data.Debug)
        self.put_text_element(l_log_xml, 'Error', p_log_data.Error)
        return l_log_xml


class Utility(object):
    """
    """

    def add_twisted_log_to_pyhouse_log(self):
        # self.m_tw_log = log_twisted.PythonLoggingObserver(loggerName = 'PyHouse.tw          ')
        # self.m_tw_log.start()
        # log_twisted.startLoggingWithObserver(self.m_tw_log)
        pass

    def remove_twisted_log_to_pyhouse_log(self):
        self.m_tw_log.stop()


class API(Utility, ReadWriteConfigXml):

    m_pyhouse_obj = None

    def __init__(self):
        # self.m_log_data = LogData()
        pass

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        # self.add_twisted_log_to_pyhouse_log()
        l_ret = self.read_xml(p_pyhouse_obj)
        try:
            self.m_pyhouse_obj.Computer.Logs = l_ret
        except AttributeError:
            pass
        return l_ret

    def Stop(self):
        self.remove_twisted_log_to_pyhouse_log()
        pass

    def SaveXml(self, p_xml):
        # p_xml.append(self.write_xml(self.m_pyhouse_obj.Computer.Logs))
        return p_xml


class Manager(object):
    """
    Simplified version of 'logging.Manager'.
    """
    def __init__(self):
        self.loggers = {}

    def mgr_getLogger(self, p_name):
        """
        Get or create new logger with specified name.
        """
        if not isinstance(p_name, basestring):
            raise TypeError("A logger name must be string or Unicode")
        if isinstance(p_name, unicode):
            p_name = p_name.encode("utf-8")
        logger = self.loggers.get(p_name)
        # if logger is None:
        #    logger = Logger(p_name)
        #    self.loggers[p_name] = logger
        print('Logger name = {} = {}'.format(p_name, logger))
        return logger

# ## END DBK
