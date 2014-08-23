"""
-*- test-case-name: PyHouse.Modules.Computer.test.test_logging_pyh -*-

@name: PyHouse/src/Modules/Computer/logging_pyh.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2010-2014 by D. Brian Kimmel
@note: Created on Jan 20, 2014
@license: MIT License
@summary: Log Module.

This is a Main Module - always present.

Isolates PyHouse from the logging libraries used.
Provides a number of logging levels: Error, Warning, Info and Debug.
Provides 'getLogger' to return the actual logger.
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
# from twisted.python import log as tp_logging
# from twisted.python import util
# from twisted.python.logfile import DailyLogFile

# Import PyMh files
from Modules.Core.data_objects import LogData
from Modules.Utilities.xml_tools import XmlConfigTools
# from Modules.Utilities.tools import PrettyPrintAny

def getLogger(p_name):
    return logging.getLogger(p_name)

LOG = getLogger('PyHouse.Logger      ')


class ReadWriteConfigXml(XmlConfigTools):
    """
    """

    def read_xml(self, p_pyhouse_obj):
        l_ret = LogData()
        try:
            l_computer = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
            l_logs_xml = l_computer.find('LogSection')
            l_ret.Debug = self.get_text_from_xml(l_logs_xml, 'Debug')
            l_ret.Error = self.get_text_from_xml(l_logs_xml, 'Error')
        except AttributeError:
            l_ret.Debug = '/tmp/debug'
            l_ret.Error = '/tmp/error'
        return l_ret

    def write_xml(self, p_log_data):
        l_log_xml = ET.Element("LogSection")
        self.put_text_element(l_log_xml, 'Debug', p_log_data.Debug)
        self.put_text_element(l_log_xml, 'Error', p_log_data.Error)
        return l_log_xml


class Utility(object):
    """
    """


class API(Utility, ReadWriteConfigXml):

    m_pyhouse_obj = None

    def __init__(self):
        self.m_log_data = LogData()

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        l_ret = self.read_xml(p_pyhouse_obj)
        try:
            self.m_pyhouse_obj.Computer.Logs = l_ret
        except AttributeError:
            pass
        return l_ret

    def Stop(self):
        pass

    def SaveXml(self, p_xml):
        p_xml.append(self.write_xml(self.m_pyhouse_obj.Computer.Logs))
        return p_xml

    # def Update(self):
        # l_obj = LogData()
        # l_obj.Debug = p_entry.Debug
        # l_obj.Error = p_entry.Error
        # self.m_pyhouse_obj.LogData = l_obj


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
        print('Logger name = {0:} = {1:}'.format(p_name, logger))
        return logger

# getLogger = Manager().mgr_getLogger



# class LevelFileLogObserver(tp_logging.FileLogObserver):
#    """
#    Log messages observer. Has internal logging level threshold. Adds log level to output messages.
#    See 'twisted.python.log.FileLogObserver' for details.
#    """

#    def __init__(self, f, level = L_INFO):
#        tp_logging.FileLogObserver.__init__(self, f)
#        self.log_level = level

#    def __call__(self, eventDict):
#        self.emit(eventDict)

#    def emit(self, eventDict):
#        """
#        Extends method of the base class by providing support for log level.
#        """
#        if eventDict['isError']:
#            level = lib_logging.ERROR
#        elif 'level' in eventDict:
#            level = eventDict['level']
#        else:
#            level = lib_logging.INFO
#        if level < self.log_level:
#            return

#        text = tp_logging.textFromEventDict(eventDict)
#        if text is None:
#            return

#        time_str = self.formatTime(eventDict['time'])
#        fmt_dict = {
#            'level': lib_logging.getLevelName(level),
#            'system': eventDict['system'],
#            'text': text.replace("\n", "\n\t")
#        }
#        msg_str = tp_logging._safeFormat("%(level)8s:[%(system)s]: %(text)s\n", fmt_dict)
#        util.untilConcludes(self.write, "{0} {1}".format(time_str, msg_str))
#        util.untilConcludes(self.flush)



# class Logger(object):
#    """
#    Wrapper of 'twisted.python.log.msg' function.
#    Makes it easy to set log levels and 'system' channel to log messages.
#    """
#    def __init__(self, name):
#        self.name = name

#    def critical(self, message):
#        """ Log message with CRITICAL level."""
#        self._twisted_log(message, logging.CRITICAL)

#    def error(self, message):
#        """ Log message with ERROR level."""
#        self._twisted_log(message, logging.ERROR)

#    def warning(self, message):
#        """ Log message with WARNING level."""
#        self._twisted_log(message, logging.WARNING)

#    def info(self, message):
#        """ Log message with INFO level."""
#        self._twisted_log(message, logging.INFO)

#    def debug(self, message):
#        """ Log message with DEBUG level."""
#        self._twisted_log(message, logging.DEBUG)

#    def _twisted_log(self, message, level):
#        """ Helper method for enlogging message with specialized log level.
#        """
#        tp_logging.msg(message, level = level, system = self.name)



# class CollectingObserver(object):
#    """
#    """

#    def __init__(self, level = L_INFO):
#        self.log = []
#        self.log_level = level

#    def __call__(self, eventDict):
#        if eventDict['isError']:
#            level = lib_logging.ERROR
#        elif 'level' in eventDict:
#            level = eventDict['level']
#        else:
#            level = lib_logging.INFO
#        if level < self.log_level:
#            return

#        text = tp_logging.textFromEventDict(eventDict)
#        if text is None:
#            return

#        self.log.append({
#            'level': level,
#            'text': text,
#            'system': eventDict['system'],
#        })

# ## END DBK
