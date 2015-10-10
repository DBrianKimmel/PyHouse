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
    """This will filter out all the HTTP log messages added by twisted (Athena/Nevow).
    """

    def __init__(self, p_param = None):
        self.m_param = p_param

    def filter(self, p_record):
        if self.m_param is None:
            allow = True
        else:
            # allow = self.m_param not in p_record.msg
            allow = False
        # if allow:
        #    p_record.msg = 'changed: ' + p_record.msg
        return allow


LOGGING_DICT = {
    'version' : 1,
    'disable_existing_loggers' : False,

    'filters': {
        'http': {
            '()': DropHttpFilter,
            'p_param': '/transport ',
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
        'console' : {
            'class':'logging.StreamHandler',
            'level' : 'DEBUG',
            'formatter' : 'standard',
        },
        'debug' : {
            'class':'logging.handlers.TimedRotatingFileHandler',
            'level' : 'DEBUG',
            'filters': ['http'],
            'formatter' : 'verbose',
            'filename' : DEBUG_LOG_LOCTION,
            'when' : 'midnight',
        },
        'error' : {
            'class':'logging.handlers.TimedRotatingFileHandler',
            'level' : 'ERROR',
            'formatter' : 'standard',
            'filename' : ERROR_LOG_LOCTION,
            'when' : 'midnight',
        },
    },

    'root': {
        'handlers': ['debug', 'error'],
        'level' : 'DEBUG',
    },
    'PyHouse': {
        'handlers': ['console'],
        'level' : 'DEBUG',
    },
}

logging.getLogger(LOGGER_NAME)
logging.config.dictConfig(LOGGING_DICT)
logging.info('PyHouse Starting\n')

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

    def Start(self):
        # PrettyPrintAny(self.m_pyhouse_obj.Twisted, 'PyHouseObj.Twisted')
        DeleteOldLogs.run_at_12_05(self.m_pyhouse_obj)
        pass

# ## END DBK
