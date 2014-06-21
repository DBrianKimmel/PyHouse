"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_setup -*-

@name: PyHouse/src/Modules/Core/setup.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@copyright: 2014 by D. Brian Kimmel
@note: Created on Mar 1, 2014
@license: MIT License
@summary: This module sets up the Core part of PyHouse.


This will set up this node and then find all other nodes in the same domain (House).

Then start the House and all the sub systems.
"""

# Import system type stuff

# Import PyMh files and modules.
from Modules.Core import nodes
from Modules.entertain import entertainment
from Modules.housing import house
from Modules.web import web_server
from Modules.utils import pyh_log
# from Modules.utils.tools import PrettyPrintAny

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.CoreSetup   ')

INTER_NODE = 'tcp:port=8581'
INTRA_NODE = 'unix:path=/var/run/pyhouse/node:lockfile=1'


class Utility(object):

    def dispatch(self):
        pass


class API(object):

    m_entertainment = None
    m_nodes = None

    def __init__(self):
        LOG.info("\n------------------------------------------------------------------\n\n")
        self.m_nodes = nodes.API()

    def Start(self, p_pyhouse_obj):
        # PrettyPrintAny(p_pyhouse_obj, 'Core setup - PyHouse Obj')
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_nodes.Start(p_pyhouse_obj)
        # House
        p_pyhouse_obj.House.APIs.HouseAPI = house.API()
        p_pyhouse_obj.House.APIs.HouseAPI.Start(p_pyhouse_obj)
        # SubSystems
        p_pyhouse_obj.House.APIs.WebAPI = web_server.API()
        p_pyhouse_obj.House.APIs.WebAPI.Start(p_pyhouse_obj)
        p_pyhouse_obj.House.APIs.EntertainmentAPI = entertainment.API()
        p_pyhouse_obj.House.APIs.EntertainmentAPI.Start(p_pyhouse_obj)
        LOG.info("Started.")

    def Stop(self, p_xml):
        # SubSystems
        self.m_pyhouse_obj.House.APIs.EntertainmentAPI.Stop(p_xml)
        self.m_pyhouse_obj.House.APIs.WebAPI.Stop(p_xml)
        # House
        self.m_pyhouse_obj.House.APIs.HouseAPI.Stop(p_xml)
        self.m_nodes.Stop(p_xml)
        LOG.info("Stopped.")

# ## END DBK
