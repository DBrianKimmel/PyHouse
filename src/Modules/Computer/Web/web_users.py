"""
@name:      PyHouse/src/Modules/Web/web_users.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 23, 2015
@Summary:

"""

__updated__ = '2016-10-06'

# Import system type stuff
import os
from nevow import loaders
from nevow import athena

# Import PyMh files and modules.
from Modules.Core.data_objects import LoginData
from Modules.Computer import logging_pyh as Logger
from Modules.Utilities import json_tools

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')

LOG = Logger.getLogger('PyHouse.webUsers       ')

VALID_USER_ROLES = ['Admin', 'Adult', 'Child', 'Service']
# Admin can create new users, devices + all others
# Adult can change all schedules
# Child can change only some lighting
# Service is limited to turn on/off servicable items such as pool, irrigation


class UsersElement(athena.LiveElement):
    jsClass = u'users.UsersWidget'
    docFactory = loaders.xmlfile(os.path.join(templatepath, 'usersElement.html'))

    def __init__(self, p_workspace_obj, _p_params):
        self.m_workspace_obj = p_workspace_obj
        self.m_pyhouse_obj = p_workspace_obj.m_pyhouse_obj

    @athena.expose
    def getUsersData(self):
        """
        Get a lot of server JSON data and pass it to the client browser.
        """
        l_users = self.m_pyhouse_obj.Computer.Web.Logins
        # LOG.debug(PrettyFormatAny.form(l_users, 'Login users'))
        if l_users == {}:
            l_users[0] = LoginData()
            l_users[0].Name = 'admin'
            l_users[0].LoginPasswordCurrent = 'admin'
            l_users[0].LoginFullName = 'Administrator'
            l_users[0].LoginRole = 1
            self.m_pyhouse_obj.Computer.Web.Logins = l_users
            # LOG.debug('Creating fake user since there was none')
        l_json = unicode(json_tools.encode_json(l_users))
        # LOG.info('Fetched {}'.format(l_json))
        return l_json

    @athena.expose
    def putUsersData(self, p_json):
        """A new/changed/deleted user is returned.  Process it and update the internal data.
        """
        l_json = json_tools.decode_json_unicode(p_json)
        l_ix = int(l_json['Key'])
        l_delete = l_json['Delete']
        if l_delete:
            try:
                del self.m_pyhouse_obj.Computer.Web.Logins[l_ix]
            except AttributeError:
                LOG.error("Failed to delete user - JSON: {}".format(l_json))
            return
        try:
            l_obj = self.m_pyhouse_obj.Computer.Web.Logins[l_ix]
        except KeyError:
            l_obj = LoginData()
        l_obj.Name = l_json['Name']
        l_obj.Active = l_json['Active']
        l_obj.Key = l_ix
        l_obj.LoginFullName = l_json['FullName']
        l_obj.LoginPasswordCurrent = l_json['Password_1']
        l_obj.LoginRole = l_json['Role']
        self.m_pyhouse_obj.Computer.Web.Logins[l_ix] = l_obj


# ## END DBK
