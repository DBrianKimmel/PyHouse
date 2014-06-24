"""
-*- test-case-name: PyHouse.Modules.util.test.test_pyh_log -*-

@name: PyHouse/src/Modules/utils/pyh_log.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2010-2014 by D. Brian Kimmel
@note: Created on Jan 20, 2014
@license: MIT License
@summary: Log Module.

This is a Main Module - always present.

Default to /var/log/pyhouse/xxx
Be sure it exists and is read/write for the user running PyHouse.

This module sets up the logging used by PyHouse.
It configures PyHouse in the logging standard library module.
It has been redone to utilize twisted logging.
It has been a pain trying to write tests for other modules, hence the switch.
"""

# Import system type stuff
import logging
import xml.etree.ElementTree as ET
from twisted.python import log as tpLog
from twisted.python import util
from twisted.python.logfile import DailyLogFile

# Import PyMh files
from Modules.Core.data_objects import LogData
from Modules.utils import xml_tools
# from Modules.utils.tools import PrettyPrintAny


g_debug = 0


class Logger(object):
    """
    Wrapper of 'twisted.python.log.msg' function.
    Makes it easy to set log levels and 'system' channel to log messages.
    """
    def __init__(self, name):
        self.name = name

    def critical(self, message):
        """ Log message with CRITICAL level."""
        self._twisted_log(message, logging.CRITICAL)

    def error(self, message):
        """ Log message with ERROR level."""
        self._twisted_log(message, logging.ERROR)

    def warning(self, message):
        """ Log message with WARNING level."""
        self._twisted_log(message, logging.WARNING)

    def info(self, message):
        """ Log message with INFO level."""
        self._twisted_log(message, logging.INFO)

    def debug(self, message):
        """ Log message with DEBUG level."""
        self._twisted_log(message, logging.DEBUG)

    def _twisted_log(self, message, level):
        """ Helper method for enlogging message with specialized log level.
        """
        tpLog.msg(message, level = level, system = self.name)


class ReadWriteConfigXml(xml_tools.ConfigTools):
    """
    """

    def read_xml(self, p_pyhouse_obj):
        l_ret = LogData()
        try:
            l_computer = p_pyhouse_obj.Xml.XmlRoot.find('ComputerDivision')
            l_logs_xml = l_computer.find('LogSection')
            # PrettyPrintAny(l_logs_xml, 'read log xml A')
        except AttributeError as e_error:
            print("log.read_xml() - Warning - LogSection is missing - {0:}".format(e_error))
            l_logs_xml = ET.SubElement(p_pyhouse_obj.Xml.XmlRoot, 'Logs')
            ET.SubElement(l_logs_xml, 'Debug').text = 'None'
            ET.SubElement(l_logs_xml, 'Error').text = 'None'
        l_ret.Debug = self.get_text_from_xml(l_logs_xml, 'Debug')
        l_ret.Error = self.get_text_from_xml(l_logs_xml, 'Error')
        # PrettyPrintAny(l_ret, 'read log xml 2')
        return l_ret

    def write_xml(self, p_log_data):
        l_log_xml = ET.Element("Logs")
        self.put_text_element(l_log_xml, 'Debug', p_log_data.Debug)
        self.put_text_element(l_log_xml, 'Error', p_log_data.Error)
        return l_log_xml


class Utility(ReadWriteConfigXml):

    m_pyhouse_obj = None

    def setup_debug_log (self, p_pyhouse_obj):
        """Debug and more severe goes to the base logger
        """
        logging.basicConfig()
        l_file = p_pyhouse_obj.Computer.Logs.Debug
        self.m_pyhouse_obj = p_pyhouse_obj
        l_daily = DailyLogFile.fromFullPath(l_file)
        tpLog.startLogging(l_daily)
        observer = tpLog.PythonLoggingObserver()
        observer.start()

    def setup_error_log (self):
        pass


class API(Utility):

    def __init__(self):
        self.m_log_data = LogData()

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        p_pyhouse_obj.Computer.Logs = LogData()
        # PrettyPrintAny(p_pyhouse_obj, 'Logs 1')
        p_pyhouse_obj.Computer.Logs = self.read_xml(p_pyhouse_obj)
        # PrettyPrintAny(p_pyhouse_obj.Computer.Logs, 'Logs 2')
        self.setup_debug_log(p_pyhouse_obj)
        # PrettyPrintAny(p_pyhouse_obj.Computer.Logs, 'Logs 3')

    def Stop(self, p_xml):
        p_xml.append(self.write_xml(self.m_log_data))
        return p_xml

    def Update(self, p_entry):
        l_obj = LogData()
        l_obj.Debug = p_entry.Debug
        l_obj.Error = p_entry.Error
        self.m_pyhouse_obj.LogData = l_obj  # update schedule entry within a house


def getLogger(p_name):
    pass

LOG = getLogger('PyHouse.Logger      ')


class Manager(object):
    """
    Simplified version of 'logging.Manager'.
    """
    def __init__(self):
        self.loggers = {}

    def getLogger(self, name):
        """
        Get or create new logger with specisied name.
        """
        if not isinstance(name, basestring):
            raise TypeError("A logger name must be string or Unicode")
        if isinstance(name, unicode):
            name = name.encode("utf-8")
        logger = self.loggers.get(name)
        if logger is None:
            logger = Logger(name)
            self.loggers[name] = logger
        return logger

getLogger = Manager().getLogger



class LevelFileLogObserver(tpLog.FileLogObserver):
    """
    Log messages observer. Has internal logging level threshold. Adds log level to output messages.
    See 'twisted.python.log.FileLogObserver' for details.
    """

    def __init__(self, f, level = logging.INFO):
        tpLog.FileLogObserver.__init__(self, f)
        self.log_level = level

    def __call__(self, eventDict):
        self.emit(eventDict)

    def emit(self, eventDict):
        """
        Extends method of the base class by providing support for log level.
        """
        if eventDict['isError']:
            level = logging.ERROR
        elif 'level' in eventDict:
            level = eventDict['level']
        else:
            level = logging.INFO
        if level < self.log_level:
            return

        text = tpLog.textFromEventDict(eventDict)
        if text is None:
            return

        time_str = self.formatTime(eventDict['time'])
        fmt_dict = {
            'level': logging.getLevelName(level),
            'system': eventDict['system'],
            'text': text.replace("\n", "\n\t")
        }
        msg_str = tpLog._safeFormat("%(level)8s:[%(system)s]: %(text)s\n", fmt_dict)
        util.untilConcludes(self.write, "{0} {1}".format(time_str, msg_str))
        util.untilConcludes(self.flush)




class CollectingObserver(object):
    """
    """

    def __init__(self, level = logging.INFO):
        self.log = []
        self.log_level = level

    def __call__(self, eventDict):
        if eventDict['isError']:
            level = logging.ERROR
        elif 'level' in eventDict:
            level = eventDict['level']
        else:
            level = logging.INFO
        if level < self.log_level:
            return

        text = tpLog.textFromEventDict(eventDict)
        if text is None:
            return

        self.log.append({
            'level': level,
            'text': text,
            'system': eventDict['system'],
        })

# ## END DBK
