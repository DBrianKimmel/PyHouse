"""
-*- test-case-name: PyHouse.src.Modules.Web.test.test_web_clock -*-

@name: PyHouse/src/Modules/Web/web_clock.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2013-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Sep 5, 2013
@summary: Display a clock on the web page.

"""

# Import system type stuff
import os
import time
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.Utilities import pyh_log

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.webClock    ')


class ClockElement(athena.LiveElement):
    jsClass = u'clock.ClockWidget'
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'clockElement.html'))

    @athena.expose
    def getTimeOfDay(self):
        return uc(time.strftime("%I:%M:%S", time.localtime(time.time())))

def uc(msg):
    if type(msg) == type(''):
        return unicode(msg, 'iso-8859-1')
    else:
        return msg

# ## EBD DBK
