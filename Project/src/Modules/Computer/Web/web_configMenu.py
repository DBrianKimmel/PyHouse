"""
-*- test-case-name: PyHouse.src.Modules.Web.test.test_web_configMenu -*-

@name:      PyHouse/src/Modules/Web/web_configMenu.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 23, 2015
@Summary:

"""

__updated__ = '2017-01-20'


# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.Core import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.webCfgMenu  ')

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')


class ConfigMenuElement(athena.LiveElement):
    """
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'configMenuElement.html'))
    jsClass = u'configMenu.ConfigMenuWidget'

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj
        self.m_params = p_params

# ## END DBK
