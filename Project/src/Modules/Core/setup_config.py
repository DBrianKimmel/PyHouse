"""
@name:      Modules/Core/setup_config.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@note:      Created on Aug 20, 2019
@license:   MIT License
@summary:   This module sets up the Core part of PyHouse.

"""

__updated__ = '2019-08-20'
__version_info__ = (19, 8, 1)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
import os
import pathlib

#  Import PyMh files and modules.

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.CoreSetup      ')


class CheckInitialSetup:
    """
    """

    def __init__(self):
        """
        """
        self.check_venv()
        self.check_etc()
        self.check_log()

    def check_venv(self):
        """ Be sure we are running in a Virtual python environment.
        """
        LOG.info('File: {}'.format(__file__))

    def check_etc(self):
        """
        """
        if not pathlib.Path('/etc/pyhouse').isdir():
            try:
                pass
            except:
                pass

    def check_log(self):
        """
        """
        if not pathlib.Path('/var/log/pyhouse').isdir():
            pass

# ## END DBK
