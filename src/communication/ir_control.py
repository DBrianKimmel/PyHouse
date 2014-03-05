"""
Created on Jan 26, 2014

Name: ir_control.py
@author: briank

Lirc connection.

Allow various IR receivers to collect signals from various IR remotes.

"""

# Import system type stuff
import logging


g_debug = 0
g_logger = logging.getLogger('PyHouse.CoreSetup   ')


LIRC_SOCKET = 'unix:path=/var/run/lirc/lircd'

class IrDispatch(object):
    """
    """

class API(object):

    def __init__(self):
        pass

    def Start(self, _p_pyhouses_obj):
        pass

    def Stop(self):
        pass

# ## END DBK
