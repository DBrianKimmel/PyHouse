"""
@name:      PyHouse/src/Modules/Utilities/user_validation.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Oct 30, 2015
@Summary:   Validate a user logging in to the web interface.

Also used to validate other (future) methods of accessing the PyHouse internals.


Validate against:
    Our own passwords in a dict like object.
    Standard Unix Passwords stored on this node
    Standard HTTP passwords ih a .htaccess file.

Resources
    http://blog.vrplumber.com/b/2004/09/27/adding-user-authentication-to/

"""

# Import system type stuff

# Import PyMh files and modules.
from twisted.cred import checkers, credentials, error as credError, portal
from twisted.internet import defer, protocol
from twisted.protocols import basic
from zope.interface import Interface, implements
from Modules.Computer import logging_pyh as Logger

LOG = Logger.getLogger('PyHouse.UserValidate   ')


class PyHouseRealm(object):
    """
    The realm is an interface which connects PyHouse's universe of “business objects” to the authentication system.

    """
    implements(portal.IRealm)

    def __init__(self, p_users):
        self.m_users = p_users

    def requestAvatar(self, p_avatarId, p_mind, *interfaces):
        """ The only method in the realm.
        This method will typically be called from ‘Portal.login’. The avatarId is the one returned by a CredentialChecker.

        @param p_avatarId: is the one returned by a CredentialChecker
        """
        if INamedUserAvatar in interfaces:
            l_fullname = self.m_users[p_avatarId]
            l_logout = lambda: None
            return (INamedUserAvatar(p_avatarId, l_fullname), l_logout)
        else:
            raise KeyError('None of the requested interfaces is supported.')


class DictPasswordChecker(object):
    """
    This is an object implementing ICredentialsChecker which resolves some credentials to an avatar ID.
    """
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (credentials.IUsernamePassword,)

    def __init__(self, p_passwords):
        """
        @param p_passwords: a dict like object mapping usernames to passwords.
        """
        self.m_passwords = p_passwords

    def requestAvatarId(self, p_credentials):
        l_username = p_credentials.username
        if self.m_passwords.has_key(l_username):
            if p_credentials.password == self.m_passwords[l_username]:
                return defer.succeed(l_username)
            else:
                return defer.fail(credError.UnauthorizedLogin('Bad Password.'))
        else:
            return defer.fail(credError.UnauthorizedLogin('No such user.'))


class UnixPasswordChecker(object):
    """
    """

    def __init__(self):
        pass

    def requestAvatarId(self, p_credentials):
        return defer.fail(credError.UnauthorizedLogin('Not yet working'))


class INamedUserAvatar(Interface):
    """ Should have attributes username abs fullname.
    """


class NamedUserAvatar(object):
    """
    """
    implements(INamedUserAvatar)
    def __init__(self, username, fullname):
        self.m_username = username
        self.m_fullname = fullname


class LoginTestProtocol(basic.LineReceiver):
    """
    """

    def lineReceived(self, line):
        l_cmd = getattr(self, 'handle_' + self.currentCommand)
        l_cmd(line.strip())

    def connectionMade(self):
        self.transport.write('User Name:')
        self.currentCommand = 'user'


class loginTestFactory(protocol.ServerFactory):
    """
    """
    protocol = LoginTestProtocol

    def __init__(self, p_portal):
        self.m_portal = p_portal




def wrapAuthorized(site):
    # force site to be nevow-compatible, using adapter for
    # twisted.web sites...
    site = inevow.IResource(site)
    realmObject = realm.CinemonRealm(site)
    portalObject = portal.Portal(realmObject)
    myChecker = checkers.InMemoryUsernamePasswordDatabaseDontUse()
    myChecker.addUser("user", "password")
    myChecker.addUser("fred", "flintstone")
    # Allow anonymous access.  Needed for access to loginform
    portalObject.registerChecker(
        checkers.AllowAnonymousAccess(), credentials.IAnonymous
    )
    # Allow users registered in the password file.
    portalObject.registerChecker(myChecker)
    site = appserver.NevowSite(
        resource = guard.SessionWrapper(portalObject)
    )
    return site

# ## END DBK
