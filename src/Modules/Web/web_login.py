"""
-*- test-case-name: PyHouse.src.Modules.Core.test.test_data_objects -*-

@name: PyHouse/src/Modules/Web/web_login.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@copyright: 2013-2014 by D. Brian Kimmel
@note: Created on Jul 27, 2013
@license: MIT License
@summary: Handle the web server login.

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

# Handy helper for finding external resources nearby.
webpath = os.path.join(os.path.split(__file__)[0])
templatepath = os.path.join(webpath, 'template')



LOG = Logger.getLogger('PyHouse.webLogin       ')


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

            @param p_json: is the username and password passed back by the client.
        """
        LOG.info("doLogin called {}.".format(p_json))
        l_obj = web_utils.JsonUnicode().decode_json(p_json)
        l_login_obj = self.validate_user(l_obj)
        l_json = web_utils.JsonUnicode().encode_json(l_login_obj)
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
                     ThermostatModes = VALID_THERMOSTAT_MODES
                     )
        l_json = web_utils.JsonUnicode().encode_json(l_obj)
        return unicode(l_json)

    def validate_user(self, p_obj):
        """Validate the user and put all results into the LoginData object.

        TODO: validate user - add password check for security
        """
        l_login_obj = LoginData()
        l_login_obj.LoginName = p_obj['LoginName']
        l_login_obj.LoginEncryptedPassword = p_obj['Password']
        # if p_login_obj.LoginName == 'briank' and p_login_obj.Password == 'nitt4agmtc':
        if l_login_obj.LoginName == 'briank' and l_login_obj.LoginEncryptedPassword == 'd':
            l_login_obj.LoginFullName = 'D. Brian Kimmel'
            l_login_obj.IsLoggedIn = True
            l_login_obj.ServerState = web_utils.WS_LOGGED_IN
            # web_server.API().add_browser(p_login_obj)
        else:
            l_login_obj.IsLoggedIn = False
            l_login_obj.LoginFullName = 'Not logged In'
            l_login_obj.ServerState = 0
        return l_login_obj

# ## END DBK
