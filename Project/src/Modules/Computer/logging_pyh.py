"""
name:      PyHouse/src/Modules/Computer/logging_pyh.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2014-2019 by D. Brian Kimmel
@note:      Created on Jan 20, 2014
@license:   MIT License
@summary:   Log Module.
#
Provides a Debug log and a Error log file to review.

Default to /var/log/pyhouse/xxx
Be sure it exists and is read/write for the user running PyHouse.
The reason for the pyhouse directory is to allow a non-root process access to the files.
Be sure that the pyhouse process has read/write privileges to the directory.

This module sets up the logging used by PyHouse.
It configures PyHouse in the logging standard library module plus twisted logging.

"""

__updated__ = '2019-07-05'

# Import system type stuff
import logging

# Import PyMh files


def getLogger(p_name):
    return logging.getLogger(p_name)


def addHandler(p_handler):
    logging.Logger.addHandler(p_handler)


class Utility(object):
    """
    """

    def add_twisted_log_to_pyhouse_log(self):
        pass

    def remove_twisted_log_to_pyhouse_log(self):
        self.m_tw_log.stop()


class API(Utility):

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

    def SaveXml(self, p_xml):
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
        print('Logger name = {} = {}'.format(p_name, logger))
        return logger

# ## END DBK
