"""
@name:      Modules/Core/setup_logging.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@note:      Created on Aug 22, 2014
@license:   MIT License
@summary:   This module sets up logging.

This needs to be run before anything else gets set up so everything can be logged.

Log file paths are hard coded therefore.

Log directories must exist and be writable by the PyHouse process as it begins.

"""

__updated__ = '2019-09-05'

#  Import system type stuff
import logging.config
from twisted.python import log

#  Import PyMh files and modules.
#  from Modules.Core.Utilities.debug_tools import PrettyFormatAny

LOGGER_NAME = 'PyHouse                '
LOGGER_NAME_TWISTED = 'PyHouse._Twisted.......'

LOG_DIRECTORY = '/var/log/pyhouse/'
DEBUG_LOG_NAME = 'debug'
DEBUG_LOG_LOCTION = LOG_DIRECTORY + DEBUG_LOG_NAME
ERROR_LOG_NAME = 'error'
ERROR_LOG_LOCTION = LOG_DIRECTORY + ERROR_LOG_NAME


class DropHttpFilter(object):
    """ This will filter out the HTTP log messages added by twisted (Athena/Nevow).
    """

    def __init__(self, p_param=None):
        """ Save the list of strings to filter the log message
        """
        self.m_param = p_param

    def filter(self, p_record):
        """ Should we filter this record out of the logs?
        @param p_record: is the message object
        """
        l_allow = True
        if self.m_param is None:
            return True
        #  l_list = self.m_param
        try:
            l_str = str(p_record.msg)
            if l_str.find('/transport') > 0:
                l_allow = False
            elif l_str.find('/jsmodule/') > 0:
                l_allow = False
        except Exception as e_err:
            p_record.msg = '\n\n{}\n\t{}\n'.format(p_record.msg, e_err)
        return l_allow


LOGGING_DICT = {
    'version'                  : 1,
    'disable_existing_loggers' : False,

    'filters' : {
        'http' : {
            '()'      : DropHttpFilter,
            'p_param' : ['/transport'],
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
            'filename'    : LOG_DIRECTORY + 'debug',
            'when'        : 'midnight',
            'filters'     : ['http'],
            'backupCount' : 2,
        },
        'info'   : {
            'class'       : 'logging.handlers.TimedRotatingFileHandler',
            'level'       : 'INFO',
            'formatter'   : 'standard',
            'filename'    : LOG_DIRECTORY + 'info',
            'when'        : 'midnight',
            'filters'     : ['http'],
            'backupCount' : 20,
        },
        'warning'   : {
            'class'       : 'logging.handlers.TimedRotatingFileHandler',
            'level'       : 'WARNING',
            'formatter'   : 'verbose',
            'filename'    : LOG_DIRECTORY + 'warning',
            'when'        : 'midnight',
            'filters'     : ['http'],
            'backupCount' : 20,
        },
        'error'   : {
            'class'       : 'logging.handlers.TimedRotatingFileHandler',
            'level'       : 'ERROR',
            'formatter'   : 'verbose',
            'filename'    : ERROR_LOG_LOCTION,
            'when'        : 'midnight',
            'backupCount' : 30,
        },
        'console' : {
            'class'       : 'logging.StreamHandler',
            'level'       : 'DEBUG',
            'filters'     : ['http'],
            'formatter'   : 'standard',
        },
    },

    'root' : {
        'handlers' : ['debug', 'info', 'warning', 'error'],
        'level'    : 'DEBUG',
    },
    'PyHouse' : {
        'handlers' : ['console'],
        'level'    : 'DEBUG',
    },
}

logging.getLogger(LOGGER_NAME)
logging.config.dictConfig(LOGGING_DICT)
logging.info('PyHouse Logging Starting. (setup_logging.py)\n------------------------- Loggomg --------------------------------\n')

l_observer = log.PythonLoggingObserver(loggerName=LOGGER_NAME_TWISTED)
l_observer.start()


class API:  #  To remove eclipse warnings.

    def __init__(self):
        pass

#  ## END DBK
