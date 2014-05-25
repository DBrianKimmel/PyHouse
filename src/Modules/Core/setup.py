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
from Modules.Core.data_objects import CoreServicesData
from Modules.Core import nodes
from Modules.entertain import entertainment
from Modules.housing import houses
from Modules.web import web_server
from Modules.utils import pyh_log

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
        self.m_entertainment = entertainment.API()
        self.m_nodes = nodes.API()

    def Start(self, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        p_pyhouses_obj.CoreServicesData = CoreServicesData()
        self.m_nodes.Start(p_pyhouses_obj)
        # House
        self.m_pyhouses_obj.HousesAPI = houses.API()
        # SubSystems
        self.m_pyhouses_obj.WebAPI = web_server.API()
        self.m_entertainment.Start(p_pyhouses_obj)
        LOG.info("Started.")

    def Stop(self, p_xml):
        # SubSystems
        self.m_entertainment.Stop(p_xml)
        # House
        self.m_nodes.Stop(p_xml)
        LOG.info("Stopped.")

# ## END DBK
