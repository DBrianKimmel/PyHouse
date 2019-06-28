'''
Created on Jun 9, 2019

@author: briank
'''
"""
@name:      PyHouse/Project/src/Modules/Core/Utilities/Node_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun  9, 2019
@Summary:   Routines to

"""

__updated__ = '2019-06-09'

#  Import system type stuff

#  Import PyHouse files
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.NodeTools      ')


def get_node_name(p_pyhhouse_obj):
    return p_pyhhouse_obj.Computer.Name

# ## END DBK

