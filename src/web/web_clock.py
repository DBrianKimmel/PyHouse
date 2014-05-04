"""
Created on Sep 5, 2013

@author: briank
"""

# Import system type stuff
import os
import time
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from src.utils import pyh_log

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# + = NOT USED HERE
LOG = pyh_log.getLogger('PyHouse.webClock    ')

#==============================================================================

class ClockElement(athena.LiveElement):
    jsClass = u'clock.ClockWidget'
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'clockElement.html'))

    @athena.expose
    def getTimeOfDay(self):
        if g_debug >= 2:
            print("web_mainpage.Clock.getTimeOfDay() - called from browser")
        return uc(time.strftime("%I:%M:%S", time.localtime(time.time())))

def uc(msg):
    if type(msg) == type(''):
        return unicode(msg, 'iso-8859-1')
    else:
        return msg

# ## EBD DBK
