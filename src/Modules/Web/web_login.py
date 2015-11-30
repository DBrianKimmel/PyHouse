"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_data_objects -*-

@name:      PyHouse/src/Modules/Web/web_login.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2014 by D. Brian Kimmel
@note:      Created on Jul 27, 2013
@license:   MIT License
@summary:   Handle the web server login.

Server side code.

Handles the login page.
This page is presented when the browser connects to the server.
The user is required to login to allow further access to the PyHouse controls.
After the user is authenticated, this element is converted to a "loged in as" entry near the
 top of the screen and has no further interactions with the user.

"""


# Import system type stuff
import os
from nevow import loaders
from nevow import athena
# from passlib.hash import pbkdf2_sha256
from zope.interface import implements
from twisted.cred.portal import IRealm
from twisted.cred import checkers, credentials, error as credError
from twisted.internet import defer

# Import PyMh files and modules.
from Modules.Core.data_objects import LoginData
from Modules.Web import web_utils
from Modules.Drivers import VALID_INTERFACES, VALID_PROTOCOLS
from Modules.Hvac import VALID_TEMP_SYSTEMS, VALID_THERMOSTAT_MODES
from Modules.Families import VALID_FAMILIES, VALID_DEVICE_TYPES
from Modules.Housing import VALID_FLOORS
from Modules.Lighting import VALID_LIGHTING_TYPE
from Modules.Scheduling import VALID_SCHEDULING_TYPES, VALID_SCHEDULE_MODES
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities.debug_tools import PrettyFormatAny
from Modules.Web.web_users import VALID_USER_ROLES
from Modules.Utilities import json_tools

LOG = Logger.getLogger('PyHouse.webLogin       ')

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')


class LoginElement(athena.LiveElement):
    """ a 'live' login element containing a username and password.
    """
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'loginElement.html'))
    jsClass = u'login.LoginWidget'

    def __init__(self, p_workspace_obj):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def doLogin(self, p_json):
        """ This will receive json of username, password when the user clicks on the login button in the browser.

            First, we validate the user
            If valid, display the user and then the root menu.
            If not - allow the user to retry the login.

            also

            allow user to check the change button and apply the change after logging in the user.

            @param p_json: is the username and password passed back by the client.
        """
        LOG.info("doLogin called {}.".format(PrettyFormatAny.form(p_json, 'Login From Browser')))
        l_obj = web_utils.JsonUnicode().decode_json(p_json)
        l_login_obj = self.validate_user(l_obj)
        l_json = json_tools.encode_json(l_login_obj)
        return unicode(l_json)

    @athena.expose
    def getValidLists(self):
        """ A JS request for various validating information has been received from the client.

        Return via JSON:
            VALID_DEVICE_TYPES
            VALID_FAMILIES
            VALID_FLOORS
            VALID_INTERFACES
            VALID_LIGHTING_TYPES
            VALID_PROTOCOLS
            VALID_SCHEDULING_TYPES
            VALID_SCHEDULE_MODES
            VALID_TEMP_SYSTEMS
            VALID_THERMOSTAT_MODES
        """
        l_obj = dict(
                     Devices = VALID_DEVICE_TYPES,
                     Families = VALID_FAMILIES,
                     Floors = VALID_FLOORS,
                     InterfaceType = VALID_INTERFACES,
                     LightType = VALID_LIGHTING_TYPE,
                     ProtocolType = VALID_PROTOCOLS,
                     ScheduleType = VALID_SCHEDULING_TYPES,
                     ScheduleMode = VALID_SCHEDULE_MODES,
                     TempSystem = VALID_TEMP_SYSTEMS,
                     ThermostatModes = VALID_THERMOSTAT_MODES,
                     UserRoles = VALID_USER_ROLES
                     )
        l_json = json_tools.encode_json(l_obj)
        return unicode(l_json)

    def validate_user(self, p_obj):
        """
        TODO - swithc to twisted.cred and validate the user using twisted.
                we will get an avatar (twisted definition)
        @param p_obj: is from the browser login screen
        """
        l_login_obj = LoginData()
        l_login_obj.LoginName = p_obj['LoginName']
        l_login_obj.LoginPasswordCurrent = p_obj['PasswordCurrent']
        LOG.info('Login Attempt using: {}'.format(PrettyFormatAny.form(l_login_obj, 'Login Obj')))
        #
        if l_login_obj.LoginName in self.m_pyhouse_obj.Computer.Web.Logins:
            pass
        for l_user in self.m_pyhouse_obj.Computer.Web.Logins.itervalues():
            LOG.debug(PrettyFormatAny.form(l_user, 'User Obj'))
            if l_user.Name == l_login_obj.LoginName:
                LOG.debug('User Matched')
                if l_user.LoginPasswordCurrent == l_login_obj.LoginPasswordCurrent:
                    LOG.debug('Password Matched')
                    l_login_obj.IsLoggedIn = True
                    l_login_obj.LoginRole = l_user.LoginRole
                    l_login_obj.LoginFullName = l_user.LoginFullName
                    # LOG.debug(PrettyFormatAny.form(l_login_obj, 'Login Obj'))
                return l_login_obj
            # pbkdf2_sha256.verify("password", hash)
        # Default for development - allow us in.
        # l_login_obj.LoginFullName = 'Administrator'
        # l_login_obj.IsLoggedIn = True
        # l_login_obj.ServerState = web_utils.WS_LOGGED_IN
        return l_login_obj


class PasswordDictChecker:
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,)

    def __init__(self, passwords):
        "passwords: a dict-like object mapping usernames to passwords"
        self.passwords = passwords

    def requestAvatarId(self, credentials):
        username = credentials.username
        if self.passwords.has_key(username):
            if credentials.password == self.passwords[username]:
                return defer.succeed(username)
            else:
                return defer.fail(
                    credError.UnauthorizedLogin("Bad password"))
        else:
            return defer.fail(
                credError.UnauthorizedLogin("No such user"))


class PyHouseRealm(object):
    implements(IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if pb.IPerspective in interfaces:
            avatar = SimplePerspective()
            return pb.IPerspective, avatar, avatar.logout
        else:
            LOG.error('No Interface.')


# ## END DBK
