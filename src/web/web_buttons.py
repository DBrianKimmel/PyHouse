'''
Created on Jun 3, 2013

@author: briank
'''

# Import system type stuff
import logging
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from src.web import web_utils
from src.lights import lighting_buttons

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Dump JSON
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.webButtn')


class ButtonsElement(athena.LiveElement):
    """ a 'live' login element containing a username and password.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'buttonsElement.html'))
    jsClass = u'buttons.ButtonsWidget'

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_buttons.ButtonsElement()"
            #print "    self = ", vars(self)
            #print "    workspace_obj = ", vars(p_workspace_obj)

    @athena.expose
    def getButtonData(self, p_index):
        """ A JS client has requested all the button information for a given house.

        Return the information via a remote call to the client.

        @param p_index: is the house index number.
        """
        if g_debug >= 3:
            print "web_buttons.ButtonsElement.getButtonData() - HouseIndex:", p_index
        g_logger.info("getButtonData called {0:}".format(self))
        l_buttons = self.m_pyhouses_obj.HousesData[int(p_index)].HouseObject.Buttons
        l_obj = {}
        for l_key, l_val in l_buttons.iteritems():
            l_obj[l_key] = l_val
        l_json = web_utils.JsonUnicode().encode_json(l_obj)
        if g_debug >= 3:
            print "web_buttons.ButtonsElement.getButtonData() - JSON:", l_json
        self.callRemote('displayButtonButtons', unicode(l_json))  # call client @ lighting_buttons.js
        return unicode(l_json)

    @athena.expose
    def doButtonSubmit(self, p_json):
        """A new/changed button is returned.  Process it and update the internal data via lighting_buttons.py
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_ix = int(l_json['HouseIx'])
        if g_debug >= 4:
            print "web_buttons.ButtonsElement.doButtonSubmit() - JSON:", l_json
            #print "    ", type(l_json)
            #print "  1 ", str(self.m_pyhouses_obj.HousesData)
            #print "  2 ", str(self.m_pyhouses_obj.HousesData[l_ix])
            #print "  3 ", str(self.m_pyhouses_obj.HousesData[l_ix].HouseObject)
            #print "  4 ", dir(self.m_pyhouses_obj.HousesData[l_ix].HouseObject)
        l_obj = lighting_buttons.ButtonData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_json['Key']
        l_obj.Level = l_json['Level']
        self.m_pyhouses_obj.HousesData[l_ix].HouseObject.LightingAPI.update_data(l_obj)

# ## END DBK
