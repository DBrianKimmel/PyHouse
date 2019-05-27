"""
@name:      PyHouse/Project/src/Modules/Web/web_mainpage.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 27, 2013
@Summary:

When a user wants to connect to PyHouse to monitor or control the system, they open a browser to the configured port (default is 8580).
Since internet access is possible, a login screen is presented first and authentication takes place.
Then a menu is presented that allows non house things to be selected or a the user may select to work with a house,
the house select screen also allows for a house to be added so starting with no houses is possible.

This module creates a main page and a workspace.
"""

__updated__ = '2019-05-23'

#  Import system type stuff
import gc
from twisted.web.template import Element, XMLFile
from twisted.python.filepath import FilePath
from twisted.web._element import renderer

#  Import PyMh files and modules.
# from Modules.Computer.Web import web_buttons
# from Modules.Computer.Web import web_clock
# from Modules.Computer.Web import web_computerMenu
# from Modules.Computer.Web import web_configMenu
# from Modules.Computer.Web import web_controllers
# from Modules.Computer.Web import web_controlLights
# from Modules.Computer.Web import web_garageDoors
# from Modules.Computer.Web import web_house
# from Modules.Computer.Web import web_houseMenu
# from Modules.Computer.Web import web_internet
# from Modules.Computer.Web import web_irrigation
# from Modules.Computer.Web import web_lights
from Modules.Computer.Web import web_login
# from Modules.Computer.Web import web_motionSensors
# from Modules.Computer.Web import web_mqtt
# from Modules.Computer.Web import web_nodes
from Modules.Computer.Web import web_rootMenu
# from Modules.Computer.Web import web_rooms
# from Modules.Computer.Web import web_schedules
# from Modules.Computer.Web import web_thermostats
# from Modules.Computer.Web import web_update
# from Modules.Computer.Web import web_users
# from Modules.Computer.Web import web_webs

# from Modules.Core.Utilities.debug_tools import PrettyFormatAny

from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.WebMainpage    ')

#  Handy helper for finding external resources nearby.
modulepath = FilePath('Modules/Computer/Web/')
templatepath = modulepath.child('template')
imagepath = modulepath.child('images')
csspath = modulepath.child('css')


class FileNoListDir(object):

    def directoryListing(self):
        print("ERROR - web_mainpage.directoryListing() - Forbidden resource")
        #  return error.ForbiddenResource()


class TheRoot(Element):
    """This is the root - given to the app server!
    """

    def __init__(self, p_pyhouse_obj, *args, **kw):
        super(TheRoot, self).__init__(*args, **kw)
        self.m_pyhouse_obj = p_pyhouse_obj
        self.children = {
          'resource'        : modulepath,
          'lcars.css'       : templatepath.child('lcars.css'),
          'Line.png'        : imagepath.child('Line.png'),
          'favicon.ico'     : imagepath.child('favicon.ico'),
          'waitroller.gif'  : imagepath.child('waitroller.gif')
        }

    def locateChild(self, ctx, segments):
        l_resource, l_segments = factory(ctx, segments, self.m_pyhouse_obj)
        if l_resource == None:
            l_resource, l_segments = super(TheRoot, self).locateChild(ctx, segments)
        return l_resource, l_segments

#==============================================================================


class mainPageFactory:
    """
    """

    def __init__(self):
        """
        The basic underlying plugin mechanism does not work in vhost situation where everything sits in the same basic namespace.
        The final trick was to update the module global mapping in jsDeps with my collections.
        """
        self.Clients = {}

    def addClient(self, client):
        l_clientID = self._newClientID()
        self.Clients[l_clientID] = client
        return l_clientID

    def getClient(self, p_clientID):
        return self.Clients[p_clientID]

    def removeClient(self, p_clientID):
        """
        State-tracking bugs may make it tempting to make the next line a 'pop', but it really shouldn't be;
        if the Page instance with this client ID is already gone, then it should be gone, which means that
        this method can't be called with that argument.
        """
        del self.Clients[p_clientID]

    def _newClientID(self):
        """Get a new UUID type id (dynamic) for the client.
        """
        return  # guard._sessionCookie()


#  This instance is built once
_mainPageFactory = mainPageFactory()

#==============================================================================

# COOKIEKEY = 'minimal'


class MainPage(Element):
    loader = XMLFile(templatepath.child('mainpage.html'))
    extraContent = XMLFile(csspath.child('lcars.css'))

    @renderer
    def css_spec(self, _request, tag):
        LOG.debug('In css_spec renderer')
        l_path = csspath.child('Simple.css')
        tag.fillSlots(css_filespec=l_path)
        return tag

#==============================================================================


REQ_404 = -1
REQ_ROOT = 0
REQ_WITHID = 2


class Workspace(Element):
    """
    WARNING:
        The names of the @athena.expose methods seem to have to match the js file name.
        They are called from browser when elements are attached to the workspace.
    """
    loader = XMLFile(templatepath.child('workspaceElement.html'))

#-----------------
#  Calls from browser JS to load an element (fragment)

    """
    #  NOTE!  Tne name of the def MUST be the same as the widget name as used in workspace.js attachWidget's first argument.
    """

    def inject_404(self):
        LOG.info("404 called from browser")
        # f = FourOfour()
        # f.setFragmentParent(self)
        # return f

    @renderer
    def login(self, _p_params):
        l_element = web_login.LoginElement(self)
        l_element.setFragmentParent(self)
        return l_element

    @renderer
    def rootMenu(self, _p_params):
        l_element = web_rootMenu.RootMenuElement(self)
        l_element.setFragmentParent(self)
        return l_element

"""
    def buttons(self, p_params):
        l_element = web_buttons.ButtonsElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def clock(self, p_params):
        l_element = web_clock.ClockElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def computerMenu(self, _p_params):
        l_element = web_computerMenu.ComputerMenuElement(self)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def configMenu(self, p_params):
        l_element = web_configMenu.ConfigMenuElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def controllers(self, p_params):
        l_element = web_controllers.ControllersElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def controlLights(self, p_params):
        l_element = web_controlLights.ControlLightsElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def garageDoors(self, p_params):
        l_element = web_garageDoors.GarageDoorsElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def house(self, _p_params):
        l_element = web_house.HouseElement(self)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def houseMenu(self, _p_params):
        l_element = web_houseMenu.HouseMenuElement(self)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def internet(self, p_params):
        l_element = web_internet.InternetElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def irrigation(self, p_params):
        l_element = web_irrigation.IrrigationElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def lights(self, p_params):
        l_element = web_lights.LightsElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def login(self, _p_params):
        l_element = web_login.LoginElement(self)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def motionSensors(self, p_params):
        l_element = web_motionSensors.MotionSensorsElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def mqtt(self, p_params):
        l_element = web_mqtt.MqttElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def nodes(self, p_params):
        l_element = web_nodes.NodesElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def rooms(self, p_params):
        l_element = web_rooms.RoomsElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def rootMenu(self, _p_params):
        l_element = web_rootMenu.RootMenuElement(self)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def schedules(self, p_params):
        l_element = web_schedules.SchedulesElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def thermostats(self, p_params):
        l_element = web_thermostats.ThermostatsElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def users(self, p_params):
        l_element = web_users.UsersElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def update(self, p_params):
        l_element = web_update.UpdateElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

    @athena.expose
    def webs(self, p_params):
        l_element = web_webs.WebsElement(self, p_params)
        l_element.setFragmentParent(self)
        return l_element

"""
#==============================================================================


def factory(_ctx, segments, p_pyhouse_obj):
    """ If segments contains a liveID (len = 32) the page stored in self.Clients will be returned.
    Status of the given page is stored in the page object itself and nowhere else.
    """
    seg0 = segments[0]
    if seg0 == '':
        #  Starting page - no segments yet
        return MainPage(p_pyhouse_obj), segments[1:]
    elif _mainPageFactory.Clients.has_key(seg0):
        #  xxx
        return _mainPageFactory.Clients[seg0], segments[1:]
    elif len(seg0) == 32:
        #  We have a liveID
        # IRequest(ctx).addCookie(COOKIEKEY, seg0, http.datetimeToString(time.time() + 30.0))
        # return url.URL.fromString('/'), ()
        pass
    else:
        #
        return None, segments

#==============================================================================

"""
helper funcs and classes

author   : Werner Thie, wth
last edit: wth, 20.01.2011
modhistory:
  20.01.2011 - wth, pruned for minimal
"""


def uc(msg):
    if type(msg) == type(''):
        return msg.encode('iso-8859-1')
    else:
        return msg


def dc(msg):
    if type(msg) == type(''):
        return msg
    else:
        return msg.encode('iso-8859-1')


def dumpObjects(delta=True, limit=0, include=[], exclude=[]):
    global prev
    if include != [] and exclude != []:
        return
    objects = {}
    gc.collect()
    oo = gc.get_objects()
    for o in oo:
        if getattr(o, "__class__", None):
            name = o.__class__.__name__
            if ((exclude == [] and include == [])       or \
                (exclude != [] and name not in exclude) or \
                (include != [] and name in include)):
                objects[name] = objects.get(name, 0) + 1
    pk = prev.keys()
    pk.sort()
    names = objects.keys()
    names.sort()
    for name in names:
        if limit == 0 or objects[name] > limit:
            if not prev.has_key(name):
                prev[name] = objects[name]
            dt = objects[name] - prev[name]
            if delta or dt != 0:
                print('%0.6d -- %0.6d -- ' % (dt, objects[name]), name)
            prev[name] = objects[name]


def getObjects(oname):
    """
    gets an object list with all the named objects out of the sea of gc'ed objects
    """
    l_obj_list = []
    gc.collect()
    oo = gc.get_objects()
    for o in oo:
        if getattr(o, "__class__", None):
            name = o.__class__.__name__
            if (name == oname):
                l_obj_list.append(o)
    return l_obj_list

#  ## END DBK
