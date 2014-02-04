'''
Created on Jun 1, 2013

@author: briank
'''

# Import system type stuff
import logging
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from src.web import web_utils
from src.housing import house

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

g_debug = 1
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# 5 = Detailed Data
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.webHouseSel ')


class WebHouseData(object):
    def __init__(self):
        self.House = house.HouseData()

    def reprJSON(self):
        # print "web_house.reprJSON(1)"
        return dict(House = self.House)


class HouseSelectElement(athena.LiveElement):
    """
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'houseSelectElement.html'))
    jsClass = u'houseSelect.HouseSelectWidget'

    def __init__(self, p_workspace_obj):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_houseSelect.houseSelectElement()"

    @athena.expose
    def getHousesToSelect(self, _p_dummy):
        """This is called from the client when the widget is activated by selecting the select house button on the root menu.

        Gather the top level data for houses and send it back to the client for building a house select page.
        """
        l_houses = self.m_pyhouses_obj.HousesData
        l_obj = {}
        if g_debug >= 3:
            print "web_houseSelect.getHousesToSelect() "
        for l_key, l_val in l_houses.iteritems():
            l_obj[l_key] = {}
            l_obj[l_key]['Name'] = l_val.HouseObject.Name
            l_obj[l_key]['Key'] = l_key
            l_obj[l_key]['Active'] = l_val.HouseObject.Active
        l_json = web_utils.JsonUnicode().encode_json(l_obj)
        return unicode(l_json)

    @athena.expose
    def getSelectedHouseData(self, p_index):
        """This is called from the client when a house was selected.

        Gather the data for house and send it back to the client.
        """
        l_ix = int(p_index)
        l_house = self.m_pyhouses_obj.HousesData[l_ix].HouseObject
        l_json = web_utils.JsonUnicode().encode_json(l_house)
        if g_debug >= 1:
            g_logger.debug("HouseIx:{0:}, JSON{1:}".format(l_ix, l_json))
        return unicode(l_json)

# ## END DBK
