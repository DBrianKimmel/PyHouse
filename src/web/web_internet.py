'''
Created on Jun 3, 2013

@author: briank
'''

# Import system type stuff
import logging
import os
from nevow import athena
from nevow import loaders

# Import PyMh files and modules.
from src.web import web_utils
from src.housing import internet

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
g_logger = logging.getLogger('PyHouse.webInternet ')

class InternetElement(athena.LiveElement):
    """ a 'live' internet element.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'internetElement.html'))
    jsClass = u'internet.InternetWidget'

    def __init__(self, p_workspace_obj, p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_internet.InternetElement()"

    @athena.expose
    def getHouseData(self, p_index):
        """ A JS client has requested all the information for a given house.

        @param p_index: is the house index number.
        """
        l_ix = int(p_index)
        l_house = self.m_pyhouses_obj.HousesData[l_ix].HouseObject
        if g_debug >= 3:
            print "web_internet.getHouseData() - HouseIndex:", p_index
        l_json = unicode(web_utils.JsonUnicode().encode_json(l_house))
        return l_json

    @athena.expose
    def saveInternetData(self, p_json):
        """Internet data is returned, so update the house info.
        """
        l_json = web_utils.JsonUnicode().decode_json(p_json)
        l_house_ix = int(l_json['HouseIx'])
        l_dyndns_ix = int(l_json['Key'])
        if g_debug >= 0:
            print "web_internet.saveInternetData() - JSON:", l_json
        try:
            l_obj = self.m_pyhouses_obj.HousesData[l_house_ix].HouseObject.Internet
        except KeyError:
            l_obj = internet.InternetData()
            l_obj.DynDns = {}
        l_obj.Name = l_json['Name']
        l_obj.Key = l_dyndns_ix
        l_obj.Active = l_json['Active']
        l_obj.ExternalDelay = 0
        l_obj.ExternalIP = None # returned from url to check our external IP address
        l_obj.UrlExternalIP = None
        l_obj.DynDns[l_dyndns_ix].Name = 'No Name'
        l_obj.DynDns[l_dyndns_ix].Key = l_dyndns_ix
        l_obj.DynDns[l_dyndns_ix].Active = True
        l_obj.DynDns[l_dyndns_ix].Interval = l_json['Interval']
        l_obj.DynDns[l_dyndns_ix].Url = l_json['Url']
        self.m_pyhouses_obj.HousesData[l_house_ix].HouseObject.Internet = l_obj

# ## END DBK
