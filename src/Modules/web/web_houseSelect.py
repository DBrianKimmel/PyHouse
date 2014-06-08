'''
Created on Jun 1, 2013

@author: briank
'''

# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.web import web_utils
from Modules.housing import house
from Modules.utils import pyh_log
# from src.Modules.utils.tools import PrettyPrintAny


# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 0
LOG = pyh_log.getLogger('PyHouse.webHouseSel ')


class WebHouseData(object):
    def __init__(self):
        self.House = house.HouseData()

    def reprJSON(self):
        return dict(House = self.House)


class HouseSelectElement(athena.LiveElement):
    """
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'houseSelectElement.html'))
    jsClass = u'houseSelect.HouseSelectWidget'

    def __init__(self, p_workspace_obj):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getHousesToSelect(self, _p_dummy):
        """This is called from the client when the widget is activated by selecting the select house button on the root menu.

        Gather the top level data for houses and send it back to the client for building a house select page.
        """
        l_house = self.m_pyhouse_obj.HouseData
        l_obj = {}
        l_obj[0] = {}
        l_obj[0]['Name'] = l_house.Name
        l_obj[0]['Key'] = l_house.Key
        l_obj[0]['Active'] = l_house.Active
        # PrettyPrintAny(l_obj, 'Json 1A ')
        l_json = web_utils.JsonUnicode().encode_json(l_obj)
        # rettyPrintAny(l_json, 'Json 1B ')
        return unicode(l_json)

    @athena.expose
    def getSelectedHouseData(self, p_index):
        """This is called from the client when a house was selected.

        Gather the data for house and send it back to the client.
        """
        l_ix = int(p_index)
        l_house = self.m_pyhouse_obj.HouseData
        l_json = web_utils.JsonUnicode().encode_json(l_house)
        # PrettyPrintAny(l_json, 'Json 2 ')
        if g_debug >= 1:
            LOG.debug("HouseIx:{0:}, JSON{1:}".format(l_ix, l_json))
        return unicode(l_json)

# ## END DBK
