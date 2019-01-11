"""
-*- test-case-name: PyHouse/Project/src/Modules/Core/Utilities/update_tools.py -*-

@name:      PyHouse/Project/src/Modules/Core/Utilities/update_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@note:      Created on Jan 11, 2019
@license:   MIT License
@summary:

"""

__updated__ = '2019-01-11'

#  Import system type stuff

#  Import PyMh files
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.CoreUpdateTool ')


def is_update_needed(p_local_obj, p_remote_obj):
    """ If the remote (Mqtt) site is Later then Update
    """
    try:
        if p_local_obj.LastUpdate < p_remote_obj.LastUpdate:
            return True
        else:
            return False
    except Exception:
        LOG.warn('No LastUpdate found.')
        return False

# ## END DBK
