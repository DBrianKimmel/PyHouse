"""
-*- test-case-name: PyHouse.src.Modules.Computer.Web.test.test_web_clock -*-

@name:      PyHouse/src/Modules/Computer/Web/web_clock.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Sep 5, 2013
@summary:   Display a clock on the web page.

"""

__updated__ = '2017-01-19'

#  Import system type stuff
import os
import time
from nevow import loaders
from nevow import athena

#  Import PyMh files and modules.
from Modules.Computer import logging_pyh as Logger
from Modules.Core.Utilities import json_tools

#  Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webClock    ')


class ClockElement(athena.LiveElement):
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
    else:
        return msg

#  ## EBD DBK
