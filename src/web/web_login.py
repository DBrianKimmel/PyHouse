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
        """Login Data
        """
        self.Username = ''
        self.Password = ''
        self.Fullname = 'Not logged in'
        self.LoggedIn = False

    def __str__(self):
        l_ret = "LoginData:: "
        l_ret += "Username:{0:}, ".format(self.Username)
        l_ret += "Password:{0:}, ".format(self.Password)
        l_ret += "Fullname:{0:}, ".format(self.Fullname)
        l_ret += "LoggedIn:{0:}".format(self.LoggedIn)
        return l_ret

    def __repr__(self):
        """JSON representation of the data - encoding
        """
        l_ret = '{'
        l_ret += "'Username':'{0:}', ".format(self.Username)
        l_ret += "'Password':'{0:}', ".format(self.Password)
        l_ret += "'Fullname':'{0:}', ".format(self.Fullname)
        l_ret += "'LoggedIn':'{0:}'".format(self.LoggedIn)
        l_ret += "}"
        return l_ret

    def decode_login_json(self, p_json):
        l_obj = web_utils.JsonUnicode().decode_json(p_json)
        if l_obj['Username'] == 'briank':
            self.Username = l_obj['Username']
            self.Fullname = 'D. Brian Kimmel'
            self.Password = l_obj['Password']
            self.LoggedIn = True
        else:
            self.Username = l_obj['Username']
            self.Fullname = 'Invalid Login'
            self.Password = l_obj['Password']
            self.LoggedIn = False
        return self

    def encode_login_json(self, p_login):
        l_json = web_utils.JsonUnicode().encode_json(p_login)
        return l_json


class LoginElement(athena.LiveElement):
    """ a 'live' login element containing a username and password.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'loginElement.html'))
    jsClass = u'login.LoginWidget'

    def __init__(self, p_workspace_obj):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj
        if g_debug >= 2:
            print "web_login.LoginElement()"
            print "    self = ", self  #, vars(self)
            print "    workspace_obj = ", p_workspace_obj  #, vars(p_workspace_obj)

    @athena.expose
    def doLogin(self, p_json):
        """ A JS receiver for login information from the client.
        """
        if g_debug >= 3:
            print "web_login.LoginElement.doLogin() - Json:{0:}".format(p_json)
        g_logger.info("doLogin called {0:} {1:}".format(self, p_json))
        Login(p_json, self.m_workspace_obj, self.m_pyhouses_obj)

    def display_fullname(self, p_login, p_work):
        """The login was sucessful - un-display login and display logged in part.
        """
        if g_debug >= 3:
            print "web_login.LoginElement.display_fullname() - "
            print "    self = ", self # , vars(self)
            print "    work = ", p_work #, vars(p_work)  # Prints Workspace obj
            print "    p_login=", p_login # , vars(p_login)  # Prints json data with string keys and unicode data
        #p_work.callRemote('displayLoggedIn', p_login)
        #p_work.callRemote('displayLoggedIn', u'[u"Username":u"briank"]') #==>  workspase has no method displayLoggedIn
        #p_work.fragmentParent.callRemote('displayLoggedIn', u'[u"Username":u"briank"]') #==> TypeError: Cannot call method 'apply' of undefined
        # self.callRemote('displayLoggedIn', u'[u"Username":u"briank"]') #==> NonrType has no attribute callRemote
        #self.callRemote('displayLoggedIn', u'[u"Username":u"briank"]') #==> exceptions.AttributeError: 'NoneType' object has no attribute 'callRemote'
        athena.LiveElement().callRemote('displayLoggedIn', u'[u"Username":u"briank"]') #==> 


class Login(LoginElement):
    """Actual login procedures.
    """

    def __init__(self, p_json, p_work, p_pyhouses_obj):
        if g_debug >= 3:
            print "web_login.Login()"
            print "    p_json ", p_json
            #print "    p_work = ", p_work # , vars(p_work)
            #print "    p_pyhouses =", p_pyhouses_obj  # Prints Ok
        l_obj = self.validate_user(p_json, p_pyhouses_obj)
        if l_obj.LoggedIn:
            self.display_fullname(l_obj, p_work)
        else:  # login failed
            pass

    def validate_user(self, p_json, p_pyhouses_obj):
        """Validate the user and put all results into the LoginData object.
        """
        self.m_pyhouses_obj = p_pyhouses_obj
        #TODO: validate user - add password for security 
        l_obj = LoginData().decode_login_json(p_json)
        if g_debug >= 3:
            print "web_login.validate_user() ", p_json
            print "      obj:", l_obj
        return l_obj

# ## END DBK
