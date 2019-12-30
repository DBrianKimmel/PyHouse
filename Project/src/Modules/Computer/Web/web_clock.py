"""
@name:      Modules/Computer/Web/web_clock.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 5, 2013
@summary:   Display a clock on the web page.

"""

__updated__ = '2019-12-30'

#  Import system type stuff
import os
import time
from twisted.web._element import Element

#  Import PyMh files and modules.
from Modules.Core.Utilities import json_tools

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.webClock    ')

#  Handy helper for finding external resources nearby.
modulepath = FilePath('Modules/Computer/Web/')
templatepath = modulepath.child('template')


class ClockElement(Element):
    jsClass = u'clock.ClockWidget'
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'clockElement.html'))

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getTimeOfDay(self):
        return uc(time.strftime("%I:%M:%S", time.localtime(time.time())))

    @athena.expose
    def getServerInfo(self):
        """ A JS request
        """
        l_obj = dict(
            ServerName=self.m_pyhouse_obj.Computer.Name
            )
        l_json = json_tools.encode_json(l_obj)
        return unicode(l_json)


def uc(msg):
    if type(msg) == type(''):
        return unicode(msg, 'iso-8859-1')
        return msg

#  ## EBD DBK
