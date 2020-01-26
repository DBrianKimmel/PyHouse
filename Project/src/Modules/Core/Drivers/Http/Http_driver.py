"""
@name:      Modules/Core/Drivers/Http/Http_driver.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2020-2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jan 26, 2020
@summary:

"""
from Modules.Core.Utilities.debug_tools import PrettyFormatAny

__updated__ = '2020-01-26'
__version_info__ = (19, 5, 0)
__version__ = '.'.join(map(str, __version_info__))

#  Import system type stuff
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.HttpDriver     ')


class Api:
    """
    This is the standard Device Driver interface.
    """
    m_pyhouse_obj = None
    m_controller_obj = None
    m_active = False

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialize Http Driver')

    def Start(self):
        """
        @param p_controller_obj: is the ControllerInformation() object for a Http device to open.
        @return: a pointer to the Http interface or None
        """

    def Stop(self):
        """
        """
        self.close_device(self.m_controller_obj)
        _x = PrettyFormatAny.form(0, '')
        LOG.info('Stopped Http Driver for controller "{}"'.format(self.m_controller_obj.Name))

    def Read(self):
        """
        Non-Blocking read from the Http port.
        """
        # return self.fetch_read_data(self.m_controller_obj)

    def Write(self, p_message):
        """
        Non-Blocking write to the Http port
        """
        # LOG.debug('Writing - {}'.format(FormatBytes(p_message)))
        # self.write_device(p_message)

# ## END DBK
