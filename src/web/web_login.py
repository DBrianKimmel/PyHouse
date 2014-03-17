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
from src.families import VALID_FAMILIES
from src.drivers import VALID_INTERFACES
from src.drivers import VALID_PROTOCOLS
from src.scheduling import VALID_SCHEDULING_TYPES
from src.lights import VALID_LIGHTS_TYPE

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = Config file handling
# 4 = Basic data
# 5 = Detailed Data
# + = NOT USED HERE
g_logger = logging.getLogger('PyHouse.webLogin    ')


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

    def reprJSON(self):
        return dict(Username = self.Username, Password = self.Password, Fullname = self.Fullname,
                    LoggedIn = self.LoggedIn, ServerState = self.ServerState)


class LoginElement(athena.LiveElement):
    """ a 'live' login element containing a username and password.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'loginElement.html'))
    jsClass = u'login.LoginWidget'

    def __init__(self, p_workspace_obj):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouses_obj = p_workspace_obj.m_pyhouses_obj

    @athena.expose
    def doLogin(self, p_json):
        """ This will receive json of username, password when the user clicks on the login button in the browser.

            First, we validate the user
            If valid, display the user and then the root menu.
            If not - allow the user to retry the login.

            @param p_json: is the username and password passed back by the client.
        """
        g_logger.info("doLogin called {0:}.".format(p_json))
        l_obj = web_utils.JsonUnicode().decode_json(p_json)
        self.m_login_obj = LoginData()
        l_login_obj = self.validate_user(l_obj, self.m_login_obj)
        l_json = web_utils.JsonUnicode().encode_json(l_login_obj)
        return unicode(l_json)

    @athena.expose
    def getValidLists(self):
        """ A JS request for various validating information has been received from the client.

        Return via JSON:
            VALID_INTERFACES
            VALID_FAMILIES
            VALID_LIGHTS_TYPES
            VALID_SCHEDULING_TYPES
        """
        l_obj = dict(Interfaces = VALID_INTERFACES, Protocols = VALID_PROTOCOLS, Families = VALID_FAMILIES,
                     Lights = VALID_LIGHTS_TYPE, Scheduling = VALID_SCHEDULING_TYPES)
        l_json = web_utils.JsonUnicode().encode_json(l_obj)
        return unicode(l_json)

    def validate_user(self, p_obj, p_login_obj):
        """Validate the user and put all results into the LoginData object.

        TODO: validate user - add password check for security
        """
        p_login_obj.Username = p_obj['Username']
        p_login_obj.Password = p_obj['Password']
        # if p_login_obj.Username == 'briank' and p_login_obj.Password == 'nitt4agmtc':
        if p_login_obj.Username == 'briank' and p_login_obj.Password == 'd':
            p_login_obj.Fullname = 'D. Brian Kimmel'
            p_login_obj.LoggedIn = True
            p_login_obj.ServerState = web_utils.WS_LOGGED_IN
            # web_server.API().add_browser(p_login_obj)
        else:
            p_login_obj.LoggedIn = False
            p_login_obj.Fullname = 'Not logged In'
        return p_login_obj


# ## END DBK
