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
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from src.web import web_utils

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')


g_debug = 3
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# 5 = Detailed Data
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.webLogin')


class LoginData(object):
    """ Allowed logins

    Stage 1 - Username only.
    Stage 2 - Username and password (stored password will be encrypted)
    Stage 3 - Username and some sort of common login identifier from some secure external site.
    """

    def __init__(self):
        """Login Data
        """
        self.Username = ''
        self.Password = ''
        self.Fullname = 'Not logged in'
        self.LoggedIn = False
        self.ServerState = web_utils.WS_IDLE

    def __str__(self):
        l_ret = "LoginData:: "
        l_ret += "Username:{0:}, ".format(self.Username)
        l_ret += "Password:{0:}, ".format(self.Password)
        l_ret += "Fullname:{0:}, ".format(self.Fullname)
        l_ret += "LoggedIn:{0:}, ".format(self.LoggedIn)
        l_ret += "ServerState:{0:}".format(self.ServerState)
        return l_ret

    def __repr__(self):
        """JSON representation of the data - encoding
        """
        l_ret = u'{'
        l_ret += u'"Username": "{0:}", '.format(self.Username)
        l_ret += u'"Password": "{0:}", '.format(self.Password)
        l_ret += u'"Fullname": "{0:}", '.format(self.Fullname)
        l_ret += u'"LoggedIn": "{0:}", '.format(self.LoggedIn)
        l_ret += u'"ServerState": "{0:}"'.format(self.ServerState)
        l_ret += u'}'
        return l_ret


class LoginElement(athena.LiveElement):
    """ a 'live' login element containing a username and password.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'loginElement.html'))
    jsClass = u'login.LoginWidget'

    def __init__(self, p_workspace_obj):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        self.m_login_data = LoginData()
        if g_debug >= 3:
            print "web_login.LoginElement()"
        if g_debug >= 5:
            print "    self = ", self  #, vars(self)
            print "    workspace_obj = ", p_workspace_obj  #, vars(p_workspace_obj)

    @athena.expose
    def doLogin(self, p_json):
        """ This will receive json of username, password when the user clicks on the login button in the browser.

            First, we validate the user
            If valid, display the user and then the root menu.
            If not - allow the user to retry the login.

            @param p_json: is the username and password passed back by the client.
        """
        g_logger.info("doLogin called {0:}.".format(p_json))
        self.validate_user(p_json)
        if g_debug >= 5:
            print "web_login.LoginElement.doLogin()"
            print "    json-in", p_json
        if self.m_login_data.LoggedIn:
            l_json = unicode(repr(self.m_login_data))
            self.display_fullname(l_json)
        else:  # login failed
            pass

    def validate_user(self, p_json):
        """Validate the user and put all results into the LoginData object.

        TODO: validate user - add password check for security
        """
        l_obj = web_utils.JsonUnicode().decode_json(p_json)
        self.m_login_data.Username = l_obj['Username']
        self.m_login_data.Password = l_obj['Password']
        if self.m_login_data.Username == 'briank':
            self.m_login_data.Fullname = 'D. Brian Kimmel'
            self.m_login_data.LoggedIn = True
            self.m_login_data.ServerState = web_utils.WS_LOGGED_IN
        if g_debug >= 5:
            print "web_login.validate_user() ", self.m_login_data

    def display_fullname(self, p_login):
        """The login was sucessful - un-display login and display logged in part.
        """
        if g_debug >= 5:
            print "web_login.LoginElement.display_fullname() - "
            print "    p_login=", p_login
        self.callRemote('displayFullname', p_login)

# ## END DBK
