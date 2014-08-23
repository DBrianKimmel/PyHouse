"""
-*- test-case-name: PyHouse.src.Modules.web.test.test_web_logs -*-

@name: PyHouse/src/Modules/web/web_logs.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jun 1, 2013
@summary: Handle all of the information for a house.

"""

# Import system type stuff
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from Modules.Core.data_objects import LogData
from Modules.Web import web_utils
from Modules.Computer import logging_pyh as Logger

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')


g_debug = 0
LOG = Logger.getLogger('PyHouse.webLogs    ')


class LogsElement(athena.LiveElement):
    """ a 'live' schedules element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'logsElement.html'))
    jsClass = u'logs.LogsWidget'

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getLogData(self):
        """ A JS client has requested all the Logger information.
        """
        l_obj = self.m_pyhouse_obj.Computer.Logs
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_obj))
        return l_json

    @athena.expose
    def saveLogData(self, p_json):
        """A new/changed Log is returned.  Process it and update the internal data via ???.py
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_obj = LogData()
        l_obj.Debug = l_json['Debug']
        l_obj.Error = l_json['Error']
        self.m_pyhouse_obj.LogsAPI.SaveXml(l_obj)

# ## END DBK
