"""
Created on Jul 27, 2013

@author: briank
"""

# Import system type stuff
from twisted.python.filepath import FilePath
from nevow import loaders
from nevow import athena
import json

# Import PyMh files and modules.
from src.web import web_rootMenu
from src import web

# Handy helper for finding external resources nearby.
webdir = FilePath(web.__file__).parent().preauthChild

g_debug = 4
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# + = NOT USED HERE


class LoginData(object):
    """ Allowed logins

    Stage 1 - Username only.
    Stage 2 - Username and password (stored password will be encrypted)
    Stage 3 - Username and some sort of common login identifier from some secure external site.
    """

    def __init__(self):
        Username = ''
        Password = ''


class LoginElement(athena.LiveElement):
    """ a 'live' login element containing a username and password.
    """
    docFactory = loaders.xmlfile(webdir('template/loginElement.html').path)
    jsClass = u'login.LoginWidget'

    def __init__(self, p_playground_obj):
        self.m_pyhouses_obj = p_playground_obj
        if g_debug >= 2:
            print "web_login.LoginElement() - Playground:{0:}".format(p_playground_obj)

    @athena.expose
    def login(self, p_json):
        """ A JS receiver for login information from the client.
        """
        if g_debug >= 3:
            print "web_login.LoginElement.login() - Json:{0:}".format(p_json)
        Login().validate_user(p_json, self.m_pyhouses_obj)


class Login(object):
    """Actual login procedures.
    """

    def validate_user(self, p_login, p_pyhouses_obj):
        self.m_pyhouses_obj = p_pyhouses_obj
        #TODO: validate user - add password for security 
        l_json = json.loads(p_login)
        if g_debug >= 2:
            print "web_login.validate_user() ", l_json
        self.load_rootMenu_page()

    def load_rootMenu_page(self):
        if g_debug >= 2:
            print "web_login.load_rootMenu_page()"
        #web_rootMenu.RootMenuPage('Root_Menu_1', self.m_pyhouses_obj)


# ## END DBK
