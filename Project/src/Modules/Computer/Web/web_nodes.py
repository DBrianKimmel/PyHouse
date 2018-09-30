"""
@name:      PyHouse/src/Modules/Web/web_nodes.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Dec 11, 2014
@Summary:

"""

__updated__ = '2017-01-19'

# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.Core.data_objects import RoomData, NodeData
from Modules.Computer.Web.web_utils import GetJSONComputerInfo
from Modules.Computer import logging_pyh as Logger
from Modules.Core.Utilities import json_tools

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = Logger.getLogger('PyHouse.webNodes       ')


# ==============================================================================

class NodesElement(athena.LiveElement):
    jsClass = u'nodes.NodesWidget'
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'nodesElement.html'))

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getServerData(self):
        """
        Get a lot of server JSON data and pass it to the client browser.
        """
        l_json = GetJSONComputerInfo(self.m_pyhouse_obj)
        LOG.info('Fetched {}'.format(l_json))
        return l_json

    @athena.expose
    def saveNodeData(self, p_json):
        """A new/changed/deleted node is returned.  Process it and update the internal data.
        """
        l_json = json_tools.decode_json_unicode(p_json)
        l_ix = int(l_json['Key'])
        l_delete = l_json['Delete']
        if l_delete:
            try:
                del self.m_pyhouse_obj.Computer.Nodes[l_ix]
            except AttributeError:
                LOG.error("web_nodes - Failed to delete - JSON: {}".format(l_json))
            return
        try:
            l_obj = self.m_pyhouse_obj.Computer.Nodes[l_ix]
        except KeyError:
            l_obj = NodeData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_ix
        l_obj.Comment = l_json['Comment']
        self.m_pyhouse_obj.Computer.Nodes[l_ix] = l_obj

# ## END DBK
