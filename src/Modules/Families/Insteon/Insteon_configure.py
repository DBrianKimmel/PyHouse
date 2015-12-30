"""
@name:      PyHouse/src/Modules/Families/Insteon.Insteon_configure.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created Dec 21, 2015
@Summary:   set and query the insteon configuration

"""

#  Import system type stuff

#  Import PyMh files
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.debug_tools import PrettyFormatAny

LOG = Logger.getLogger('PyHouse.Insteon_config ')


class Config(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def _get_aldb_l(self):
        """
        Read the Linear database.
        """

    def _get_aldb_t(self):
        """
        Read the Threaded database.
        """

    def get_config(self, p_controller_obj):
        l_msg = PrettyFormatAny.form(p_controller_obj, 'Controller')
        #  LOG.warning('Get config {}'.format(l_msg))

    def _set_aldb_l(self):
        """
        Write the Linear database.
        """
        pass

    def _set_aldb_t(self):
        """
        Write the Threaded database.
        """
        pass

    def set_config(self):
        pass

#  ## END DBK
