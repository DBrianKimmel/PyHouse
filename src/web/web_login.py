"""
Created on Jul 27, 2013

@author: briank

Server side code.

Handles the login page.
This page is presented when the browser connects to the server.
The user is required to login to allow further access to the PyHouse controls.
After the user is authenticated, this element is converted to a "loged in as" entry near the
 top of the screen and has no further interactions with the user.
"""


# Import system type stuff
import logging
from twisted.python.filepath import FilePath
from nevow import loaders
from nevow import athena
import json

# Import PyMh files and modules.
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
g_logger = logging.getLogger('PyHouse.webLogin')


class LoginData(object):
    """ Allowed logins

    Stage 1 - Username only.
    Stage 2 - Username and password (stored password will be encrypted)
    Stage 3 - Username and some sort of common login identifier from some secure external site.
    """

    def __init__(self):
        Username = ''
        Password = ''
        Fullname = 'Not logged in'


class LoginElement(athena.LiveElement):
    """ a 'live' login element containing a username and password.


    """
    docFactory = loaders.xmlfile(webdir('template/loginElement.html').path)
    jsClass = u'login.LoginWidget'

    def __init__(self, p_workspace_obj):
        self.m_pyhouses_obj = p_workspace_obj
        if g_debug >= 2:
            print "web_login.LoginElement() - Workspace:{0:}".format(p_workspace_obj)

    @athena.expose
    def login(self, p_params):
        if g_debug >= 3:
            print "web_login.LoginElement.login() - called from browser ", self
        g_logger.info("login called")

    @athena.expose
    def doLogin(self, p_json):
        """ A JS receiver for login information from the client.
        """
        if g_debug >= 3:
            print "web_login.LoginElement.doLogin() - Json:{0:}".format(p_json)
        g_logger.info("doLogin called {0:} {1:}".format(self, p_json))
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


# ## END DBK
