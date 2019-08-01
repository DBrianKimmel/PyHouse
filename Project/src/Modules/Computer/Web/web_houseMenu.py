"""
-*- _test-case-name: PyHouse.src.Modules.Web._test.test_web_houseMenu -*-

@name:      PyHouse/src/Modules/Web/web_houseMenu.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on May 30, 2013
@summary:   Handle all of the information for a house.

"""

# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.webHMenu    ')

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')


class HouseMenuElement(athena.LiveElement):
    """
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'houseMenuElement.html'))
    jsClass = u'houseMenu.HouseMenuWidget'

    def __init__(self, p_workspace_obj):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

# ## END DBK
