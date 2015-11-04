"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_setup_logging -*-

@name:      PyHouse/src/Modules/Core/setup_logging.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@note:      Created on Aug 22, 2014
@license:   MIT License
@summary:   This module sets up logging.

This needs to be run before anything else gets set up so everything can be logged.

Log file paths are hard coded therefore.

Log directories must exist and be writable by the PyHouse process as it begins.

"""
from Modules.Utilities.debug_tools import PrettyFormatAny

LOGGER_NAME = 'PyHouse                '
LOGGER_NAME_TWISTED = 'PyHouse.Twisted.....   '

LOG_DIRECTORY = '/var/log/pyhouse/'
DEBUG_LOG_NAME = 'debug'
DEBUG_LOG_LOCTION = LOG_DIRECTORY + DEBUG_LOG_NAME
ERROR_LOG_NAME = 'error'
ERROR_LOG_LOCTION = LOG_DIRECTORY + ERROR_LOG_NAME

# Import system type stuff
import datetime
import logging.config
from twisted.python import log


class DropHttpFilter(object):
    """ This will filter out the HTTP log messages added by twisted (Athena/Nevow).
    """

    def __init__(self, p_param = None):
        """ Save the list of strings to filter the log message
        """
        self.m_param = p_param

    def filter(self, p_record):
        """ Should we filter this record out of the logs?
        """
        l_allow = True
        if self.m_param is None:
            return l_allow
        else:
            try:
                for l_entry in self.m_param:
                    if l_entry in p_record.msg:
                        l_allow = False
            except Exception as e_err:
                print('ERROR in setup_logging DropHttpFilter - {}'.format(e_err))
                print(PrettyFormatAny.form(self.m_param, 'Params'))
        return l_allow


LOGGING_DICT = {
    'version'                  : 1,
    'disable_existing_loggers' : False,

    'filters' : {
        'http' : {
            '()'      : DropHttpFilter,
            'p_param' : ['/transport', '/jsmodule/'],
        }
    },

    'formatters' : {
        'standard' : {
            'format' : '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'verbose' : {
            'format' : '%(asctime)s [%(levelname)s] %(name)s: %(funcName)s %(lineno)s: - %(message)s'
        },
    },

    'handlers' : {
        'debug'   : {
            'class'       : 'logging.handlers.TimedRotatingFileHandler',
            'level'       : 'DEBUG',
            'formatter'   : 'verbose',
            'filename'    : '/var/log/pyhouse/debug',
            'when'        : 'midnight',
            'filters'     : ['http'],
            'backupCount' : '20',
        },
        'error'   : {
            'class'       : 'logging.handlers.TimedRotatingFileHandler',
            'level'       : 'ERROR',
            'formatter'   : 'standard',
            'filename'    : ERROR_LOG_LOCTION,
            'when'        : 'midnight',
            'backupCount' : '20',
        },
        'console' : {
            'class'       : 'logging.StreamHandler',
            'level'       : 'DEBUG',
            'filters'     : ['http'],
            'formatter'   : 'standard',
        },
    },

    'root' : {
        'handlers' : ['debug', 'error'],
        'level'    : 'DEBUG',
    },
    'PyHouse' : {
        'handlers' : ['console'],
        'level'    : 'DEBUG',
    },
}

logging.getLogger(LOGGER_NAME)
logging.config.dictConfig(LOGGING_DICT)
# logging.debug('PyHouse Debug Starting\n')
logging.info('PyHouse Info Starting\n')
# logging.warn('PyHouse Warn Starting\n')
# logging.error('PyHouse Error Starting\n')
# logging.critical('PyHouse Critical Starting\n')
# print('setup_logging-122')
# print(PrettyFormatAny.form(logging, 'Logging'))

l_observer = log.PythonLoggingObserver(loggerName = LOGGER_NAME_TWISTED)
l_observer.start()


class DeleteOldLogs(object):
    """
    """

    @staticmethod
    def run_daily(p_pyhouse_obj):
        l_delay = 60 * 60 * 24
        p_pyhouse_obj.Twisted.Reactor.callLater(l_delay, DeleteOldLogs.run_daily, p_pyhouse_obj)
        pass

    @staticmethod
    def run_at_12_05(p_pyhouse_obj):
        l_now = datetime.datetime.now()
        l_1205 = datetime.time(0, 5, 0)
        if l_now == l_1205:
            pass
        l_delay = 1
        p_pyhouse_obj.Twisted.Reactor.callLater(l_delay, DeleteOldLogs.run_daily, p_pyhouse_obj)


class API(object):  # To remove eclipse warnings.

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        # print('setup_logging-153')

    def Start(self):
        # PrettyPrintAny(self.m_pyhouse_obj.Twisted, 'PyHouseObj.Twisted')
        DeleteOldLogs.run_at_12_05(self.m_pyhouse_obj)
        pass

# ## END DBK
