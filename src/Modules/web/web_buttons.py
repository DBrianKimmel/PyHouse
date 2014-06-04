'''
Created on Jun 3, 2013

@author: briank
'''

# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.web import web_utils
from Modules.lights import lighting_buttons
from Modules.utils import pyh_log

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
LOG = pyh_log.getLogger('PyHouse.webButton   ')


class ButtonsElement(athena.LiveElement):
    """ a 'live' login element containing a username and password.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'buttonsElement.html'))
    jsClass = u'buttons.ButtonsWidget'

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print("web_buttons.ButtonsElement()")

    @athena.expose
    def getHouseData(self, p_index):
        """ A JS client has requested all the House information for a given house.

        Return the information via a remote call to the client.

        @param p_index: is the house index number.
        """
        l_ix = int(p_index)
        l_house = self.m_pyhouses_obj.HouseData
        l_json = web_utils.JsonUnicode().encode_json(l_house)
        if g_debug >= 3:
            print("web_buttons.getHouseData() - JSON: {0:}".format(l_json))
        return unicode(l_json)

    @athena.expose
    def saveButtonData(self, p_json):
        """A new/changed button is returned.
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_ix = int(l_json['HouseIx'])
        if g_debug >= 4:
            print("web_buttons.ButtonsElement.saveButtonData() - JSON:{0:}".format(l_json))
        l_obj = lighting_buttons.ButtonData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_json['Key']
        l_obj.Level = l_json['Level']

# ## END DBK
