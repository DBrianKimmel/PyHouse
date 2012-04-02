#!/usr/bin/python

"""Web server module.
This is a Main Module - always present.

TODO: format doc strings to Epydoc standards.
"""

# Import system type stuff
import datetime
import logging
import os
import random
#import time
import twisted.python.components as tpc
from nevow import appserver
from nevow import flat
from nevow import inevow
from nevow import loaders
from nevow import rend
from nevow import static
from nevow import tags as Tag
from nevow import url
from nevow import util
from nevow.rend import _CARRYOVER
from formless import iformless

# Import PyMh files
import configure_mh
import entertainment
import Device_Insteon
import lighting
import schedule



SUBMIT = '_submit'
BUTTON = 'post_btn'

Entertainment = {}
Lights = {}
Light_Data = {}
Scenes = {}
Schedule_Data = {}
g_lighting = None
g_schedule = None


class WebException(Exception):
    """Raised when there is a web error of some sort.
    """


class WebLightingData(lighting.LightingData):
    """
    """


class WebData(object):

    g_lighting = None
    g_schedule = None
    g_entertainment = None


class WebUtilities(WebData):
    """
    """

    def build_child_tree(self):
        """Build a tree of pages for nevow.
        """
        # These are real files on disk
        setattr(RootPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))
        setattr(RootPage, 'child_mainpage.js', static.File('web/js/mainpage.js'))
        #------------------------------------
        setattr(LightingPage, 'child_lightpage.css', static.File('web/css/lightpage.css'))

        setattr(LightingPage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(LightingPage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
        setattr(LightingPage, 'child_lightpage.js', static.File('web/js/lightpage.js'))

        setattr(LightingPage, 'child_close.gif', static.File('web/images/close.gif'))
        setattr(LightingPage, 'child_minimize.gif', static.File('web/images/minimize.gif'))
        setattr(LightingPage, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
        setattr(LightingPage, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
        setattr(LightingPage, 'child_topRight.gif', static.File('web/images/top_right.gif'))
        setattr(LightingPage, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
        setattr(LightingPage, 'child_handle.horizontal.png', static.File('web/images/handle.horizontal.png'))
        #------------------------------------
        setattr(SchedulePage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(SchedulePage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
        setattr(SchedulePage, 'child_schedpage.js', static.File('web/js/schedpage.js'))

        setattr(SchedulePage, 'child_close.gif', static.File('web/images/close.gif'))
        setattr(SchedulePage, 'child_minimize.gif', static.File('web/images/minimize.gif'))
        setattr(SchedulePage, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
        setattr(SchedulePage, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
        setattr(SchedulePage, 'child_topRight.gif', static.File('web/images/top_right.gif'))
        setattr(SchedulePage, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
        setattr(SchedulePage, 'child_handle.horizontal.png', static.File('web/images/handle.horizontal.png'))
        #------------------------------------
        setattr(ScenesPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))
        setattr(ScenesPage, 'child_scenepage.js', static.File('web/js/scenepage.js'))

    def lighting_sub_win(self):
        pass


class ManualFormMixin(rend.Page, WebUtilities):

    def locateChild(self, context, segments):
        """Add to the standard find child to handle POST of forms
        
        def form_post_lighting for a submit button valued 'lighting'
        def form_post for the form without a key
        """
        if segments[0].startswith(SUBMIT): # Handle the form post
            # Get a method name from the action in the form plus the first word in the button name,
            #  or simply the form action if no button name is specified
            kwargs = {}
            args = inevow.IRequest(context).args
            bindingName = ''
            for key in args:
                if key != BUTTON:
                    if args[key] != ['']:
                        kwargs[key] = (args[key][0], args[key])[len(args[key]) > 1]
                else:
                    bindingName = args[key][0]
            name_prefix = segments[0].split('!!')[1]
            if bindingName == '':
                name = name_prefix
            else:
                name = name_prefix + '_' + bindingName.split()[0].lower()
            method = getattr(self, 'form_' + name, None)
            if method is not None:
                return self.onManualPost(context, method, bindingName, kwargs)
            else:
                raise WebException("You should define a form_action_button method")
        (l_child, l_segments) = super(ManualFormMixin, self).locateChild(context, segments)
        return (l_child, l_segments)

    def onManualPost(self, ctx, method, bindingName, kwargs):
        """
        """

        def redirectAfterPost(aspects):
            """
            """
            l_handler = aspects.get(inevow.IHand)
            refpath = None
            ref = None
            if l_handler is not None:
                if isinstance(l_handler, rend.Page):
                    refpath = url.here
                    if 'freeform_hand' not in inevow.IRequest(ctx).prepath:
                        refpath = refpath.child('freeform_hand')
                if isinstance(l_handler, (url.URL, url.URLOverlay)):
                    refpath, l_handler = l_handler, None
            if refpath is None:
                redirectAfterPost = request.getComponent(iformless.IRedirectAfterPost, None)
                if redirectAfterPost is None:
                    ref = request.getHeader('referer')
                    if ref:
                        refpath = url.URL.fromString(ref)
                    else:
                        refpath = url.here
                else:
                    self.m_logger.warn("[0.5] IRedirectAfterPost is deprecated. Return a URL instance from your autocallable instead.", DeprecationWarning, 2)
                    ref = str(redirectAfterPost)
                    refpath = url.URL.fromString(ref)
            if l_handler is not None or aspects.get(iformless.IFormErrors) is not None:
                magicCookie = '%s%s%s' % (datetime.datetime.now(), request.getClientIP(), random.random())
                refpath = refpath.replace('_nevow_carryover_', magicCookie)
                _CARRYOVER[magicCookie] = C = tpc.Componentized()
                for k, v in aspects.iteritems():
                    C.setComponent(k, v)
            destination = flat.flatten(refpath, ctx)
            request.redirect(destination)
            return static.Data('You posted a form to %s' % bindingName, 'text/plain'), ()

        request = inevow.IRequest(ctx)
        return util.maybeDeferred(method, **kwargs
            ).addCallback(self.onPostSuccess, request, ctx, bindingName, redirectAfterPost
            ).addErrback(self.onPostFailure, request, ctx, bindingName, redirectAfterPost)


class LightingPage(ManualFormMixin):
    """Define the page layout of the lighting selection web page.
    """
    addSlash = True
    docFactory = loaders.stan(
        Tag.html["\n",
            Tag.head["\n",
                Tag.title['PyHouse - Lighting Page'],
                Tag.link(rel = 'stylesheet', type = 'text/css', href = url.root.child('mainpage.css'))["\n"],
                Tag.script(type = 'text/javascript', src = 'ajax.js')["\n"],
                Tag.script(type = 'text/javascript', src = 'floating_window.js'),
                Tag.script(type = 'text/javascript', src = 'lightpage.js')["\n"],
                ],
            Tag.body[
                Tag.h1['PyHouse Lighting'],
                Tag.p['\n'],
                Tag.p['Select the light to control:'],
                Tag.table(style = 'width: 100%;', border = 0)["\n",
                    Tag.invisible(data = Tag.directive('lightlist'), render = Tag.directive('lightlist'))
                    ],
                Tag.form(action = url.here.child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )["\n",
                    Tag.input(type = 'button', onclick = "createNewLightWindow('1234')", value = 'Add Light'),
                    Tag.input(type = 'submit', value = 'Scan Lights', name = BUTTON)
                    ]
                ]
            ]
        )

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name

    def data_lightlist(self, _context, _data):
        """Build up a list of lights.
        Omit controllers and buttons (scenes???)
        """
        #self.load_all_light_info()
        #global Light_Data
        l_light = {}
        for l_key, l_obj in lighting.Light_Data.iteritems():
            if lighting.LightingData.get_Family(l_obj) != 'Insteon': continue
            l_obj.CurLevel = lighting.Light_Status[l_key].CurLevel
            if l_obj.Type == 'Light':
                l_light[l_key] = l_obj
        return l_light

    def render_lightlist(self, _context, links):
        """Place buttons for each light on the page.
        """
        global l_ret
        l_ret = []
        l_cnt = 0
        for l_key, l_value in sorted(links.iteritems()):
            l_cur_lev = l_value.CurLevel
            l_family = l_value.Family
            l_type = l_value.Type
            l_name = l_value.Name
            if l_cnt % 2 == 0:
                l_ret.append(Tag.tr)
            l_ret.append(Tag.td)
            l_ret.append(Tag.input(type = 'submit', value = l_key, name = BUTTON, onclick = "createChangeLightWindow(\'{0:}\',\'{1:}\')".format(l_key, l_cur_lev, l_family))
                         [ l_family, '-', l_type, ' ', l_name, ' ', l_cur_lev, "\n" ])
            l_cnt += 1
        return l_ret

    def load_all_light_info(self):
        global Light_Data, g_lighting
        #Light_Data = g_lighting.get_light_tables()

    def _store_light(self, **kwargs):
        """Send the updated lighting info back to the lighting module.
        Update the lighting page with the new information.
        """
        global g_lighting, Lights
        l_name = kwargs['Name']
        Lights[l_name] = {}
        Lights[l_name]['Address'] = kwargs['Address']
        Lights[l_name]['Family'] = kwargs['Family']
        Lights[l_name]['Type'] = kwargs['Type']
        Lights[l_name]['Controller'] = kwargs['Controller']
        Lights[l_name]['Dimmable'] = kwargs['Dimmable']
        Lights[l_name]['Coords'] = kwargs['Coords']
        Lights[l_name]['Master'] = kwargs['Master']
        g_lighting.update_all_light_tables(Lights)

    def form_post_addlight(self, **kwargs):
        print " - form_post_add - ", kwargs
        self._store_light(**kwargs)
        return LightingPage(self.name)

    def form_post_changelight(self, **kwargs):
        """Browser user changed a light (on/off/dim)
        Now send the change to the light.
        """
        global g_lighting
        print " - form_post_changelight - kwargs=", kwargs
        g_lighting.change_light_setting(kwargs['Name'], kwargs['slider_val'], kwargs['Family'])
        g_lighting.update_all_light_tables(Lights)

    def form_post_deletelight(self, **kwargs):
        print " - form_post_delete - ", kwargs
        global g_lighting, Lights
        del Lights[kwargs['Name']]
        g_lighting.update_all_light_tables(Lights)
        return LightingPage(self.name)

    def form_post_scan(self, **kwargs):
        """Trigger a scan of all lights and then update light info.
        """
        print " - form_post_scan- ", kwargs
        global g_lighting, Lights
        g_lighting.scan_all_lighting(Lights)
        self.load_all_light_info()


class ScenesPage(LightingPage):
    addSlash = True
    docFactory = loaders.stan(
        Tag.html["\n",
            Tag.head["\n",
                Tag.title['PyHouse - Scenes Page'],
                Tag.link(rel = 'stylesheet', type = 'text/css', href = url.root.child('mainpage.css'))["\n"],
                Tag.script(type = 'text/javascript', src = 'ajax.js')["\n"],
                Tag.script(type = 'text/javascript', src = 'floating_window.js'),
                Tag.script(type = 'text/javascript', src = 'scenepage.js')["\n"],
                ],
            Tag.body[
                Tag.h1['PyHouse Scenes'],
                Tag.p['\n'],
                Tag.p['Select the scene:'],
                Tag.table(style = 'width: 100%;', border = 0)["\n",
                    Tag.invisible(data = Tag.directive('scenelist'), render = Tag.directive('scenelist'))
                    ],
                Tag.form(action = url.here.child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )["\n",
                    Tag.input(type = 'button', onclick = "createNewSceneWindow()", value = 'Add Scene'),
                    Tag.input(type = 'submit', value = 'Scan Lights', name = BUTTON)
                    ]
                ]
            ]
        )

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name

    def _store_scene(self, **kwargs):
        global g_lighting, Scenes
        l_name = kwargs['Name']
        Scenes[l_name] = {}
        Scenes[l_name]['Controller'] = kwargs['Controller']
        Scenes[l_name]['Responder'] = kwargs['Responder']
        Scenes[l_name]['Level'] = kwargs['Level']
        Scenes[l_name]['Ramp'] = kwargs['Ramp']
        g_lighting.update_scene_config(Scenes)

    def data_scenelist(self, _context, _data):
        """Build up a list of Scenes.
        """
        global Scenes
        l_scene = {}
        for l_key, l_value in Scenes.iteritems():
            l_scene[l_key] = l_value
        return l_scene

    def render_scenelist(self, _context, links):
        """Place buttons for each scene on the page.
        """
        global l_ret
        l_ret = []
        l_cnt = 0
        for l_key, l_value in sorted(links.iteritems()):
            if l_cnt % 2 == 0:
                l_ret.append(Tag.tr)
            l_ret.append(Tag.td)
            l_ret.append(Tag.input(type = 'submit', value = l_key, name = BUTTON, onclick = "createChangeSceneWindow(\'{0:}\', '100', '2s')".format(l_key))
                         [ l_value.get('Family', '.'), '-', l_value.get('Type', '-'), ' ', l_value.get('Name', '_'), "\n" ])
            l_cnt += 1
        return l_ret

    def form_post_addscene(self, **kwargs):
        print " - form_post_add - ", kwargs
        self._store_scene(**kwargs)
        return ScenesPage(self.name)

    def form_post_changescene(self, **kwargs):
        pass

    def form_post_deletescene(self, **kwargs):
        print " - form_post_deleteScene - ", kwargs
        global g_lighting, Scenes
        del Scenes[kwargs['Name']]
        g_lighting.update_scene_config(Scenes)
        return ScenesPage(self.name)


class SchedulePage(ScenesPage):
    """
    """
    addSlash = True
    docFactory = loaders.stan(
        Tag.html[
            Tag.head[
                Tag.title['PyHouse - Schedule Page'],
                Tag.link(rel = 'stylesheet', type = 'text/css', href = url.root.child('mainpage.css'))["\n"],
                Tag.script(type = 'text/javascript', src = 'ajax.js')["\n"],
                Tag.script(type = 'text/javascript', src = 'floating_window.js')["\n"],
                Tag.script(type = 'text/javascript', src = 'schedpage.js'),
                ],
            Tag.body[
                Tag.h1['PyHouse Schedule'],
                Tag.p['Select the schedule:'],
                Tag.table(style = 'width: 100%;', border = 0)["\n",
                    Tag.invisible(data = Tag.directive('schedlist'), render = Tag.directive('schedlist'))
                    ],
                Tag.input(type = "button", onclick = "createNewSchedule('1234')", value = "Add Slot")
                ]
            ]
        )

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name

    def data_schedlist(self, _context, _data):
        """Build up a list of schedule slots.
        @param _context: is a tag that we are building an object to render
        @param _data: is the page object we are extracting for.
        @return: an object to render.
        """
        l_sched_dict = {}
        for k, v in schedule.Schedule_Data.iteritems():
            l_sched_dict[k] = v
        return l_sched_dict

    def render_schedlist(self, _context, links):
        """
        @param: _context is ...
        @param: links are ...  
        @return: the list to be added into the stan.dom
        """
        global l_ret
        l_ret = []
        l_cnt = 0
        for l_key, l_value in sorted(links.iteritems()):
            if not 'Rate' in l_value:
                l_value['Rate'] = 0
            if l_cnt % 2 == 0:
                l_ret.append(Tag.tr)
            l_ret.append(Tag.td)
            l_ret.append(Tag.input(type = 'submit', value = l_key, name = BUTTON, onclick = "createChangeScheduleWindow(\'{0:}\', \'{1:}\', \'{2:}\', \'{3:}\', \'{4:}\', \'{5:}\')".format(
                                                    l_key, l_value['Type'], l_value['Name'], l_value['Time'], l_value['Level'], l_value['Rate']))
                         [ l_value['Name'], ' ', l_value['Type'], ' ', l_value['Time'], ' ', l_value['Level'], ' ', "\n" ])
            l_cnt += 1
        return l_ret

    def _store_schedule(self, **kwargs):
        #global g_schedule, Schedule
        l_slot = kwargs['Slot']
        schedule.Schedule_Data[l_slot] = {}
        schedule.Schedule_Data[l_slot]['Name'] = kwargs['Name']
        schedule.Schedule_Data[l_slot]['Type'] = kwargs['Type']
        schedule.Schedule_Data[l_slot]['Time'] = kwargs['Time']
        schedule.Schedule_Data[l_slot]['Level'] = kwargs['Level']
        schedule.Schedule_Data[l_slot]['Rate'] = kwargs['Rate']
        g_schedule.updateSchedule(schedule.Schedule_Data)

    def form_post_changesched(self, **kwargs):
        """Browser user changed a schedule
        Now send the change to the light.
        """
        print " - form_post_changesched - kwargs=", kwargs
        self._store_schedule(**kwargs)

    def form_post_addslot(self, **kwargs):
        print " - form_post_addslot - kwargs=", kwargs
        self._store_schedule(**kwargs)
        return SchedulePage(self.name)

    def form_post_changeschedule(self, **kwargs):
        print " - form_post_changeschedule (add) - kwargs=", kwargs
        self._store_schedule(**kwargs)
        g_schedule.updateSchedule(schedule.Schedule_Data)
        return SchedulePage(self.name)

    def form_post_deleteschedule(self, **kwargs):
        print " - form_post_deleteschedule - kwargs=", kwargs
        del schedule.Schedule_Data[kwargs['Slot']]
        g_schedule.updateSchedule(schedule.Schedule_Data)
        return SchedulePage(self.name)


class EntertainmentPage(SchedulePage):
    """
    """
    addSlash = True
    docFactory = loaders.stan(
        Tag.html[
            Tag.title['PyHouse - Entertainment Page'],
            Tag.body[
                Tag.h1['PyHouse Entertainment'],
                Tag.p['Select the entertainment:'],
                Tag.form(action = url.here.child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )[
                    Tag.input(type = 'submit', value = 'Add Entertainment', name = BUTTON),
                    Tag.input(type = 'submit', value = 'Delete Entertainment', name = BUTTON)
                    ]
                ]
            ]
        )

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name


#class RoomsPage(EntertainmentPage):

    #import ws_rooms

class RootPage(EntertainmentPage):
    """The main page of the web server.
    """
    addSlash = True
    docFactory = loaders.stan(
        Tag.html(xmlns = 'http://www.w3.org/1999/xhtml', lang = 'en')[
            Tag.head[
                Tag.title['PyHouse - Main Page'],
                Tag.link(rel = 'stylesheet', type = 'text/css', href = url.root.child('mainpage.css')),
                Tag.script(type = 'text/javascript', src = 'mainpage.js'),
                ],
            Tag.body[
                Tag.h1['PyHouse_2'],
                Tag.form(name = 'mainmenuofbuttons',
                    action = url.here.child('_submit!!post'),
                    enctype = "multipart/form-data",
                    method = 'post')
                    [
                    Tag.table(style = 'width: 100%;', border = 0)[
                        Tag.tr[
                            Tag.td[ Tag.input(type = 'submit', value = 'Entertainment', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = 'House', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = 'Weather', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = '1,4', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = '1,5', name = BUTTON), ],
                            ],
                        Tag.tr[
                            Tag.td[ Tag.input(type = 'submit', value = 'Lighting', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = 'Rooms', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = '2,3', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = '2,4', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = '2,5', name = BUTTON), ],
                            ],
                         Tag.tr[
                            Tag.td[ Tag.input(type = 'submit', value = 'Scenes', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = 'Location', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = '3,3', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = '3,4', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = '3,5', name = BUTTON), ],
                            ],
                        Tag.tr[
                            Tag.td[ Tag.input(type = 'submit', value = 'Schedule', name = BUTTON) ],
                            Tag.td[ Tag.input(type = 'submit', value = '4,2', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = '4,3', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = '4,4', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = '4,5', name = BUTTON), ],
                            ],
                        Tag.tr[
                            Tag.td[ Tag.input(type = 'submit', value = '5,1', name = BUTTON) ],
                            Tag.td[ Tag.input(type = 'submit', value = '5,2', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = '5,3', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = '5,4', name = BUTTON), ],
                            Tag.td[ Tag.input(type = 'submit', value = '5,5', name = BUTTON), ],
                            ],
                        ] # table
                    ] # form
                ] # body
            ] # html
        ) # stan

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name

    def form_post_lighting(self, **_kwargs):
        return LightingPage('lighting')

    def form_post_scenes(self, **_kwargs):
        return ScenesPage('scenes')

    def form_post_schedule(self, **_kwargs):
        return SchedulePage('schedule')

    def form_post_entertainment(self, **_kwargs):
        return EntertainmentPage('entertainment')

    def form_post_rooms(self, **_kwargs):
        return RoomsPage('rooms')

    def form_post(self, *args, **kwargs):
        print " - form_post - args={0:}, kwargs={1:}".format(args, kwargs)
        return LightingPage('Root')


class Web_ServerMain(ManualFormMixin):
    """This is the main web server.
    Other classes are to build pages and handle requests.
    """

    def __init__(self, p_debug = False):
        self.m_debug = p_debug
        self.m_logger = logging.getLogger('PyMh.WebServer')
        self.m_config = configure_mh.ConfigureMain()
        global g_lighting, g_schedule, g_entertainment
        g_lighting = lighting.LightingMain()
        g_schedule = schedule.ScheduleMain()
        g_entertainment = entertainment.EntertainmentMain()
        self.m_logger.info("Initialized.")

    def configure(self, p_port = 8080):
        self.m_port = p_port
        l_config = self.m_config.get_value()
        if 'web_server' in l_config:
            l_dict = l_config['web_server']
            if 'port' in l_dict:
                self.m_port = int(l_dict['port'])
        self.m_logger.info("Configured.  Start the web server on port {0:}".format(self.m_port))

    def start(self, p_reactor):
        self.m_reactor = p_reactor
        global Lights, Scenes, Schedule, Entertainment, g_lighting, g_schedule, g_entertainment
        #Lights = g_lighting.get_light_tables()
        Scenes = g_lighting.load_scene_data()
        Schedule_Data = g_schedule.get_all_schedule_slots()
        self.m_site_dir = os.path.split(os.path.abspath(__file__))[0]
        print "Webserver path = ", self.m_site_dir
        l_site = appserver.NevowSite(RootPage('/'))
        self.build_child_tree()
        p_reactor.listenTCP(self.m_port, l_site)
        self.m_logger.info("Started.")

### END
