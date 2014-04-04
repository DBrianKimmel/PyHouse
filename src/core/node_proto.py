"""
Created on Apr 3, 2014

# -*- test-case-name: PyHouse.src.core.test.test_node_proto -*-

@author: briank

@copyright: 2014 by D. Brian Kimmel

@summary: This module is for AMP request/response protocol

"""

# Import system type stuff
import logging

from twisted.protocols.amp import AMP, Integer, String, Command

from src.core.nodes import NodeData


g_debug = 0
g_logger = logging.getLogger('PyHouse.Node_proto  ')


class NodeInfoError(Exception): pass


class ReqNodeInfo(Command):
    """Ask a node for its node information.
    """

    arguments = [('Command', Integer()),
                 ('Address', String())]
    response = [('Name', String()),
                ('Active', String()),
                ('Address', String()),
                ('Role', Integer())]
    errors = {NodeInfoError: 'Node information unavailable.'}


class NodeInfoResponse(AMP):
    def NodeInfo(self, p_name, p_active, p_address, p_role):
        Name = p_name
        Active = p_active
        Address = p_address
        Role = p_role
        return {'Name': Name,
                'Active': Active,
                'Address': Address,
                'Role': Role}

    ReqNodeInfo.responder(NodeInfo)

# ## END DBK
