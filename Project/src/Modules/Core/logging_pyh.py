"""
name:       Modules/Core/logging_pyh.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2014-2019 by D. Brian Kimmel
@note:      Created on Jan 20, 2014
@license:   MIT License
@summary:   Log Module.

This configures the logger used in PyHouse.ything.
It is used during import to set up the logging name used for each module that will log an

"""

__updated__ = '2019-10-04'

# Import system type stuff
import logging

# Import PyMh files


def getLogger(p_name):
    return logging.getLogger(p_name)


def addHandler(p_handler):
    logging.Logger.addHandler(p_handler)


class lightingUtility(object):
    """
    """

    def add_twisted_log_to_pyhouse_log(self):
        pass

    def remove_twisted_log_to_pyhouse_log(self):
        self.m_tw_log.stop()


class Api(lightingUtility):

    m_pyhouse_obj = None

    def __init__(self):
        pass

    def Start(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        try:
            self.m_pyhouse_obj.Computer.Logs = None
        except AttributeError:
            pass

    def Stop(self):
        self.remove_twisted_log_to_pyhouse_log()
        pass


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
        p_name = p_name.encode("utf-8")
        logger = self.loggers.get(p_name)
        print('Logger name = {} = {}'.format(p_name, logger))
        return logger

# ## END DBK
