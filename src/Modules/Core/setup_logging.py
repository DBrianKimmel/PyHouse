"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_setup_logging -*-

@name: PyHouse/src/Modules/Core/setup_logging.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Aug 22, 2014
@license: MIT License
@summary: This module sets up logging.

This needs to be run before anything else gets set up so everything can be logged.

Log file paths are hard coded therefore.

Log directories must exist and be writable by the PyHouse process as it begins.

"""

LOGGING_DICT = {
    'version' : 1,
    'disable_existing_loggers' : False,

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
            'formatter' : 'verbose',
            'filename' : '/var/log/pyhouse/debug',
            'when' : 'midnight',
        },
        'error' : {
            'class':'logging.handlers.TimedRotatingFileHandler',
            'level' : 'ERROR',
            'formatter' : 'standard',
            'filename' : '/var/log/pyhouse/error',
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

LOGGER_NAME = 'PyHouse                '
LOGGER_NAME_TWISTED = 'PyHouse.Twisted.....   '

# Import system type stuff
import logging.config
from twisted.python import log



logging.getLogger(LOGGER_NAME)
logging.config.dictConfig(LOGGING_DICT)
logging.info('PyHouse Starting\n')

l_observer = log.PythonLoggingObserver(loggerName = LOGGER_NAME_TWISTED)
l_observer.start()

class API(object):  # To remove eclipse warnings.
    def NotUsed(self):
        pass

# ## END DBK
