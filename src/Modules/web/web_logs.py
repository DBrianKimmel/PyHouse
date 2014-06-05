'''
Created on Jun 1, 2013

@author: briank
'''

# Import system type stuff
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from Modules.web import web_utils
from Modules.utils import pyh_log

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')


g_debug = 0
# 0 = off
# 1 = major routine entry
# 2 = Basic data
LOG = pyh_log.getLogger('PyHouse.webLogs    ')


class LogsElement(athena.LiveElement):
    """ a 'live' schedules element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'logsElement.html'))
    jsClass = u'logs.LogsWidget'

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getLogData(self):
        """ A JS client has requested all the pyh_log information.
        """
        l_obj = self.m_pyhouse_obj.LogsData
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_obj))
        return l_json

    @athena.expose
    def saveLogData(self, p_json):
        """A new/changed Log is returned.  Process it and update the internal data via ???.py
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_obj = pyh_log.LogData()
        l_obj.Debug = l_json['Debug']
        l_obj.Error = l_json['Error']
        self.m_pyhouse_obj.LogsAPI.Update(l_obj)

# ## END DBK
