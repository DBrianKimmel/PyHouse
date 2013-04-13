#!/usr/bin/env python

"""Superclass

Handle the controller component of the lighting system.

"""

import lighting_tools
from utils.tools import PrintBytes
from drivers import interface

g_debug = 9

Controller_Data = {}
ControllerCount = 0


class ControllerData(lighting_tools.CoreData):

    def __init__(self):
        global ControllerCount
        ControllerCount += 1
        super(ControllerData, self).__init__()
        self.Type = 'Controller'
        self.Command = None
        self.Interface = ''
        self.Message = ''
        self.Port = ''

    def __str__(self):
        l_ret = "LightingController:: Name:{0:}, Family:{1:}, Interface:{2:}, Port:{3:}, Type:{4:}, Message:{5:}, ".format(
                self.Name, self.Family, self.Interface, self.Port, self.Type, PrintBytes(self.Message))
        return l_ret


class ControllersAPI(lighting_tools.CoreAPI):

    def __init__(self):
        super(ControllersAPI, self).__init__()

# ## END
