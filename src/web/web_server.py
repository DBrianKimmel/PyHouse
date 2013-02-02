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
import twisted.python.components as tpc
from twisted.internet import reactor
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

from lighting import lighting


g_debug = 0
g_port = 8080
g_logger = None

SUBMIT = '_submit'
BUTTON = 'post_btn'

Entertainment = {}
Lights = {}
XLight_Data = {}

# Only to move the eclipse error flags to one small spot
T_p = Tag.p
T_h1 = Tag.h1
T_td = Tag.td
T_tr = Tag.tr
T_html = Tag.html
T_head = Tag.head
T_body = Tag.body
T_form = Tag.form
T_link = Tag.link
T_table = Tag.table
T_title = Tag.title
T_input = Tag.input
T_script = Tag.script
U_R_child = url.root.child
U_H_child = url.here.child

class WebLightData(lighting.LightData): pass
class WebLightingAPI(lighting.LightingAPI): pass
class WebLightingStatusData(lighting.LightingStatusData): pass
class WebLightingStatusAPI(lighting.LightingStatusAPI): pass

class WebSceneData(lighting.SceneData): pass
class WebSceneAPI(lighting.SceneAPI): pass


class WebException(Exception):
    """Raised when there is a web error of some sort.
    """

class WebData(object):
    """
    """
    def __init__(self):
        self.WebPort = 8080

class WebUtilities(WebData):
    """
    """

    def build_child_tree(self):
        """Build a tree of pages for nevow.
        """
        # These are real files on disk
        setattr(RootPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))
        setattr(RootPage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(RootPage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
        setattr(RootPage, 'child_housepage.js', static.File('web/js/housepage.js'))
        setattr(RootPage, 'child_lightpage.js', static.File('web/js/lightpage.js'))
        setattr(RootPage, 'child_mainpage.js', static.File('web/js/mainpage.js'))
        setattr(RootPage, 'child_schedpage.js', static.File('web/js/schedpage.js'))
        setattr(RootPage, 'child_scenepage.js', static.File('web/js/scenepage.js'))
        #------------------------------------
        setattr(RootPage, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
        setattr(RootPage, 'child_close.gif', static.File('web/images/close.gif'))
        setattr(RootPage, 'child_minimize.gif', static.File('web/images/minimize.gif'))
        setattr(RootPage, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
        setattr(RootPage, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
        setattr(RootPage, 'child_topRight.gif', static.File('web/images/top_right.gif'))
        setattr(RootPage, 'child_handle.horizontal.png', static.File('web/images/handle.horizontal.png'))

        setattr(LightingPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))
        setattr(LightingPage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(LightingPage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
        setattr(LightingPage, 'child_lightpage.js', static.File('web/js/lightpage.js'))
        setattr(LightingPage, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
        setattr(LightingPage, 'child_close.gif', static.File('web/images/close.gif'))
        setattr(LightingPage, 'child_minimize.gif', static.File('web/images/minimize.gif'))
        setattr(LightingPage, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
        setattr(LightingPage, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
        setattr(LightingPage, 'child_topRight.gif', static.File('web/images/top_right.gif'))

        setattr(HousePage, 'child_mainpage.css', static.File('web/css/mainpage.css'))
        setattr(HousePage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(HousePage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
        setattr(HousePage, 'child_housepage.js', static.File('web/js/housepage.js'))
        setattr(HousePage, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
        setattr(HousePage, 'child_close.gif', static.File('web/images/close.gif'))
        setattr(HousePage, 'child_minimize.gif', static.File('web/images/minimize.gif'))
        setattr(HousePage, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
        setattr(HousePage, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
        setattr(HousePage, 'child_topRight.gif', static.File('web/images/top_right.gif'))

    def lighting_sub_win(self):
        pass


class ManualFormMixin(rend.Page, WebUtilities):
    """
    This came from 404 code in rend.py


xxx cookies []
xxx code 404
xxx received_headers {'accept-language': 'en-US,en;q=0.8', 'accept-encoding': 'gzip,deflate,sdch', 'host': 'localhost:8080', 'accept': '*/*', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5', 'accept-charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'connection': 'keep-alive', 'referer': 'http://localhost:8080/freeform_hand/?_nevow_carryover_=2012-06-28%2014%3A28%3A52.124743127.0.0.10.879904703826', 'cookie': 'good_id2_attr=1200%2C50%2C250%2C120%2C10008%2C0; good_id3_attr=1200%2C50%2C300%2C350%2C10010%2C0; good_id1_attr=1200%2C50%2C400%2C350%2C10002%2C0; TWISTED_SESSION=56503d0ede2321ea2672c167d565c643'}
xxx site <nevow.appserver.NevowSite instance at 0x158d8c0>
xxx session <twisted.web.server.Session instance at 0x172a7e8>
xxx responseHeaders Headers({'date': ['Thu, 28 Jun 2012 18:28:52 GMT'], 'content-type': ['text/html; charset=UTF-8'], 'server': ['TwistedWeb/11.0.0']})
xxx transport <HTTPChannel #6 on 8080>
xxx deferred <Deferred at 0x17595a8>
xxx requestHeaders Headers({'accept-language': ['en-US,en;q=0.8'], 'accept-encoding': ['gzip,deflate,sdch'], 'connection': ['keep-alive'], 'accept': ['*/*'], 'user-agent': ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5'], 'accept-charset': ['ISO-8859-1,utf-8;q=0.7,*;q=0.3'], 'host': ['localhost:8080'], 'referer': ['http://localhost:8080/freeform_hand/?_nevow_carryover_=2012-06-28%2014%3A28%3A52.124743127.0.0.10.879904703826'], 'cookie': ['good_id2_attr=1200%2C50%2C250%2C120%2C10008%2C0; good_id3_attr=1200%2C50%2C300%2C350%2C10010%2C0; good_id1_attr=1200%2C50%2C400%2C350%2C10002%2C0; TWISTED_SESSION=56503d0ede2321ea2672c167d565c643']})
xxx content <cStringIO.StringO object at 0x17bc148>
xxx code_message Not Found
xxx method GET
xxx channel <twisted.web.http.HTTPChannel instance at 0x16ba950>
xxx args {}
xxx notifications []
xxx host IPv4Address(TCP, '127.0.0.1', 8080)
xxx path /freeform_hand/schedpage.js
xxx postpath ['schedpage.js']
xxx sitepath []
xxx stack []
xxx _adapterCache {}
xxx clientproto HTTP/1.1
xxx prepath ['freeform_hand']
xxx received_cookies {'good_id2_attr': '1200%2C50%2C250%2C120%2C10008%2C0', 'good_id1_attr': '1200%2C50%2C400%2C350%2C10002%2C0', 'good_id3_attr': '1200%2C50%2C300%2C350%2C10010%2C0', 'TWISTED_SESSION': '56503d0ede2321ea2672c167d565c643'}
xxx uri /freeform_hand/schedpage.js
xxx headers {'date': 'Thu, 28 Jun 2012 18:28:52 GMT', 'content-type': 'text/html; charset=UTF-8', 'server': 'TwistedWeb/11.0.0'}
xxx client IPv4Address(TCP, '127.0.0.1', 51383)
xxx queued 0
    """

    def locateChild(self, context, segments):
        """Add to the standard find child to handle POST of forms

        def form_post_lighting for a submit button valued 'lighting'
        def form_post for the form without a key
        """
        if segments[0].startswith(SUBMIT):  # Handle the form post
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
            # print "locateChild - name:", name
            method = getattr(self, 'form_' + name, None)
            print "locateChild - method:", method
            if method is not None:
                return self.onManualPost(context, method, bindingName, kwargs)
            else:
                raise WebException("You should define a form_action_button method for {0:}".format(name))
        (l_child, l_segments) = super(ManualFormMixin, self).locateChild(context, segments)
        return (l_child, l_segments)

    def onManualPost(self, ctx, method, bindingName, kwargs):
        """
        """

        def redirectAfterPost(aspects):
            """See: nevow.rend.Page.WebFormPost
            """
            print " -- Start - ctx:", ctx, ", method:", method, ", bindingName:", bindingName, ", kwargs", kwargs
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
            # print " -- refpath-1:", refpath
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
                    # # Use the redirectAfterPost url
                    ref = str(redirectAfterPost)
                    refpath = url.URL.fromString(ref)
            # print " -- refpath-2:", refpath
            if l_handler is not None or aspects.get(iformless.IFormErrors) is not None:
                magicCookie = '%s%s%s' % (datetime.datetime.now(), request.getClientIP(), random.random())
                refpath = refpath.replace('_nevow_carryover_', magicCookie)
                _CARRYOVER[magicCookie] = C = tpc.Componentized()
                for k, v in aspects.iteritems():
                    C.setComponent(k, v)
            destination = flat.flatten(refpath, ctx)
            request.redirect(destination)
            print "Posted a form to >", bindingName, "<"
            return static.Data('You posted a form to %s' % bindingName, 'text/plain'), ()

        request = inevow.IRequest(ctx)
        print " --  defer ", kwargs
        return util.maybeDeferred(method, **kwargs
            ).addCallback(self.onPostSuccess, request, ctx, bindingName, redirectAfterPost
            ).addErrback(self.onPostFailure, request, ctx, bindingName, redirectAfterPost)

class ControllersPage(rend.Page):

    addSlash = True
    docFactory = loaders.stan(
        T_html[
            T_title['PyHouse - Controller Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
            T_body[
                T_h1['PyHouse Controllers'],
                T_p['Select the controller:'],
                T_form(action = U_H_child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )[
                    T_input(type = 'submit', value = 'Add Controller', name = BUTTON),
                    T_input(type = 'submit', value = 'Delete Controller', name = BUTTON)
                    ]
                ]
            ]
        )

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name

class EntertainmentPage(rend.Page):
    """
    """
    addSlash = True
    docFactory = loaders.stan(
        T_html[
            T_title['PyHouse - Entertainment Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
            T_body[
                T_h1['PyHouse Entertainment'],
                T_p['Select the entertainment:'],
                T_form(action = U_H_child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )[
                    T_input(type = 'submit', value = 'Add Entertainment', name = BUTTON),
                    T_input(type = 'submit', value = 'Delete Entertainment', name = BUTTON)
                    ]
                ]
            ]
        )

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name

class HousePage(rend.Page):
    """
    """
    addSlash = True
    docFactory = loaders.stan(
        T_html["\n",
            T_head["\n",
                T_title['PyHouse - House Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js'),
                T_script(type = 'text/javascript', src = 'housepage.js')["\n"],
                ],
            T_body[
                T_h1['PyHouse Houses'],
                T_p['\n'],
                T_p['Select the house to control:'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    Tag.invisible(data = Tag.directive('houselist'), render = Tag.directive('houselist'))
                    ],
                T_form(action = U_H_child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )["\n",
                    T_input(type = 'button', onclick = "createNewHouseWindow('1')", value = 'add')
                    ]
                ]
            ]
        )

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name

    def data_houselist(self, _context, _data):
        l_house = {}
        for l_key, l_obj in House_Data.iteritems():
            l_house[l_key] = l_obj
        return l_house

    def render_houselist(self, _context, links):
        l_ret = []
        l_cnt = 0
        for l_key, l_value in sorted(links.iteritems()):
            l_name = l_value.Name
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON, onclick = "createChangeHouseWindow(\'{0:}\', \'{1:}\', \'{2:}\', \'{3:}\', \'{4:}\', \'{5:}\', \'{6:}\', \'{7:}\', \'{8:}\', \'{9:}\' )".format(
                        l_value.Name, l_value.Active, l_value.Street, l_value.City, l_value.State, l_value.ZipCode, l_value.Latitude, l_value.Longitude, l_value.TimeZone, l_value.SavingTime))
                         [ l_name])
            l_cnt += 1
        return l_ret

    def form_post_add(self, **kwargs):
        print "form_post_addhouse (HousePage)", kwargs
        return HousePage(self.name)

    def form_post_change_house(self, **kwargs):
        print "form_post_change_house (HousePage)", kwargs
        return HousePage(self.name)

    def form_post_deletehouse(self, **kwargs):
        print "form_post_deletehouse (HousePage)", kwargs
        return HousePage(self.name)

    def form_post_house(self, **kwargs):
        print "form_post_house (HousePage)", kwargs
        return HousePage(self.name)

class LightingPage(rend.Page, WebLightData, WebLightingAPI, WebLightingStatusData, WebLightingStatusAPI):
    """Define the page layout of the lighting selection web page.
    """
    addSlash = True
    docFactory = loaders.stan(
        T_html["\n",
            T_head["\n",
                T_title['PyHouse - Lighting Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js'),
                T_script(type = 'text/javascript', src = 'lightpage.js')["\n"],
                ],
            T_body[
                T_h1['PyHouse Lighting'],
                T_p['\n'],
                T_p['Select the light to control:'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    Tag.invisible(data = Tag.directive('lightlist'), render = Tag.directive('lightlist'))
                    ],
                T_form(action = U_H_child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )["\n",
                    T_input(type = 'button', onclick = "createNewLightWindow('1234')", value = 'Add Light'),
                    T_input(type = 'submit', value = 'Scan Lights', name = BUTTON)
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
        l_light = {}
        for l_key, l_obj in lighting.Light_Data.iteritems():
            if l_obj.Family != 'Insteon': continue
            if l_obj.Type != 'Light': continue
            # l_obj.CurLevel = lighting.Light_Data[l_key].CurLevel
            # if l_obj.Type == 'Light':
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
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON, onclick = "createChangeLightWindow(\'{0:}\',\'{1:}\',\'{2:}\')".format(l_key, l_cur_lev, l_family))
                         [ l_family, '-', l_type, ':', l_name, ' ', l_cur_lev])
            l_cnt += 1
        return l_ret

    def load_all_light_info(self):
        global Light_Data
        pass

    def _store_light(self, **kwargs):
        """Send the updated lighting info back to the lighting module.
        Update the lighting page with the new information.
        """
        global Lights
        l_name = kwargs['Name']
        Lights[l_name] = {}
        Lights[l_name]['Address'] = kwargs['Address']
        Lights[l_name]['Family'] = kwargs['Family']
        Lights[l_name]['Type'] = kwargs['Type']
        Lights[l_name]['Controller'] = kwargs['Controller']
        Lights[l_name]['Dimmable'] = kwargs['Dimmable']
        Lights[l_name]['Coords'] = kwargs['Coords']
        Lights[l_name]['Master'] = kwargs['Master']
        lighting.LightingUtility().update_all_lighting_families()

    def form_post_addlight(self, **kwargs):
        print " - form_post_addlight - ", kwargs
        self._store_light(**kwargs)
        return LightingPage(self.name)

    def form_post_changelight(self, **kwargs):
        """Browser user changed a light (on/off/dim)
        Now send the change to the light.
        """
        print " - form_post_changelight - kwargs=", kwargs
        return LightingPage(self.name)

    def form_post_deletelight(self, **kwargs):
        print " - form_post_delete - ", kwargs
        global Lights
        del Lights[kwargs['Name']]
        lighting.LightingUtility().update_all_lighting_families()
        return LightingPage(self.name)

    def form_post_scan(self, **kwargs):
        """Trigger a scan of all lights and then update light info.
        """
        print " - form_post_scan- ", kwargs
        return LightingPage(self.name)

    def form_post_lighting(self, **kwargs):
        print " - form_post_lighting - ", kwargs
        return LightingPage(self.name)

class LocationPage(rend.Page): pass

class RoomsPage(rend.Page): pass

class ScenesPage(rend.Page):
    addSlash = True
    docFactory = loaders.stan(
        T_html["\n",
            T_head["\n",
                T_title['PyHouse - Scenes Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js'),
                T_script(type = 'text/javascript', src = 'scenepage.js')["\n"],
                ],
            T_body[
                T_h1['PyHouse Scenes'],
                T_p['\n'],
                T_p['Select the scene:'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    Tag.invisible(data = Tag.directive('scenelist'), render = Tag.directive('scenelist'))
                    ],
                T_form(action = U_H_child('_submit!!post'),
                       enctype = "multipart/form-data",
                       method = 'post'
                      )["\n",
                    T_input(type = 'button', onclick = "createNewSceneWindow()", value = 'Add Scene'),
                    T_input(type = 'submit', value = 'Scan Lights', name = BUTTON)
                    ]
                ]
            ]
        )

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name

    def _store_scene(self, **kwargs):
        pass

    def data_scenelist(self, _context, _data):
        """Build up a list of Scenes.
        """
        l_scene = {}
        for l_key, l_obj in lighting.Scene_Data.iteritems():
            l_scene[l_key] = l_obj
        return l_scene

    def render_scenelist(self, _context, links):
        """Place buttons for each scene on the page.
        """
        global l_ret
        l_ret = []
        l_cnt = 0
        for l_key, l_value in sorted(links.iteritems()):
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON, onclick = "createChangeSceneWindow(\'{0:}\', '100', '2s')".format(l_key))
                         [ l_value.Name, "\n" ])
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

class SchedulePage(rend.Page):
    addSlash = True
    docFactory = loaders.stan(
        T_html[
            T_head[
                T_title['PyHouse - Schedule Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js')["\n"],
                T_script(type = 'text/javascript', src = 'schedpage.js'),
                ],
            T_body[
                T_h1['PyHouse Schedule'],
                T_p['Select the schedule:'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    Tag.invisible(data = Tag.directive('schedlist'), render = Tag.directive('schedlist'))
                    ],
                T_input(type = "button", onclick = "createNewSchedule('1234')", value = "Add Slot")
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
        l_sched = {}
        for l_key, l_obj in schedule.Schedule_Data.iteritems():
            l_sched[l_key] = l_obj
        return l_sched

    def render_schedlist(self, _context, links):
        """
        @param: _context is ...
        @param: links are ...
        @return: the list to be added into the stan.dom
        """
        global l_ret
        l_ret = []
        l_cnt = 0
        for l_key, l_obj in sorted(links.iteritems()):
            l_level = l_obj.Level
            l_name = l_obj.Name
            l_rate = l_obj.Rate
            l_time = l_obj.Time
            l_type = l_obj.Type
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_key, name = BUTTON, onclick = "createChangeScheduleWindow(\'{0:}\', \'{1:}\', \'{2:}\', \'{3:}\', \'{4:}\', \'{5:}\')".format(
                                                    l_key, l_type, l_name, l_time, l_level, l_rate))
                         [ l_name, ' ', l_type, ' ', l_time, ' ', l_level, ' ', "\n" ])
            l_cnt += 1
        return l_ret

    def _store_schedule(self, **kwargs):
        # FIXME this is old - change to new format schedule
        l_slot = kwargs['Slot']
        schedule.Schedule_Data[l_slot] = {}
        schedule.Schedule_Data[l_slot]['Name'] = kwargs['Name']
        schedule.Schedule_Data[l_slot]['Type'] = kwargs['Type']
        schedule.Schedule_Data[l_slot]['Time'] = kwargs['Time']
        schedule.Schedule_Data[l_slot]['Level'] = kwargs['Level']
        schedule.Schedule_Data[l_slot]['Rate'] = kwargs['Rate']

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
        schedule.ScheduleAPI().update_schedule(schedule.Schedule_Data)
        return SchedulePage(self.name)

    def form_post_deleteschedule(self, **kwargs):
        print " - form_post_deleteschedule - kwargs=", kwargs
        del schedule.Schedule_Data[kwargs['Slot']]
        schedule.ScheduleAPI().update_schedule(schedule.Schedule_Data)
        return SchedulePage(self.name)

class WeatherPage(rend.Page): pass

class RootPage(ManualFormMixin, EntertainmentPage, HousePage, LightingPage, LocationPage, RoomsPage, ScenesPage, SchedulePage, WeatherPage):
    """The main page of the web server.
    """
    addSlash = True
    docFactory = loaders.stan(
        T_html(xmlns = 'http://www.w3.org/1999/xhtml', lang = 'en')[
            T_head[
                T_title['PyHouse - Main Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css')),
                T_script(type = 'text/javascript', src = 'mainpage.js'),
                ],
            T_body[
                T_h1['PyHouse_2'],
                T_form(name = 'mainmenuofbuttons',
                    action = U_H_child('_submit!!post'),
                    enctype = "multipart/form-data",
                    method = 'post')
                    [
                    T_table(style = 'width: 100%;', border = 0)[
                        T_tr[
                            T_td[ T_input(type = 'submit', value = 'Entertainment', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'House', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Weather', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = '1,4', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Controllers', name = BUTTON), ],
                            ],
                        T_tr[
                            T_td[ T_input(type = 'submit', value = 'Lighting', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Rooms', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = '2,3', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = '2,4', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Buttons', name = BUTTON), ],
                            ],
                         T_tr[
                            T_td[ T_input(type = 'submit', value = 'Scenes', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = 'Location', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = '3,3', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = '3,4', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = '3,5', name = BUTTON), ],
                            ],
                        T_tr[
                            T_td[ T_input(type = 'submit', value = 'Schedule', name = BUTTON) ],
                            T_td[ T_input(type = 'submit', value = '4,2', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = '4,3', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = '4,4', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = '4,5', name = BUTTON), ],
                            ],
                        T_tr[
                            T_td[ T_input(type = 'submit', value = '5,1', name = BUTTON) ],
                            T_td[ T_input(type = 'submit', value = '5,2', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = '5,3', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = '5,4', name = BUTTON), ],
                            T_td[ T_input(type = 'submit', value = '5,5', name = BUTTON), ],
                            ],
                        ]  # table
                    ]  # form
                ]  # body
            ]  # html
        )  # stan

    def __init__(self, name):
        rend.Page.__init__(self)
        self.name = name

    def form_post_controllers(self, **_kwargs):
        return ControllersPage('controllers')

    def form_post_entertainment(self, **_kwargs):
        return EntertainmentPage('entertainment')

    def form_post_house(self, **kwargs):
        print "form_post_house (RootPage)", kwargs
        return HousePage('House')

    def form_post_lighting(self, **kwargs):
        print "form_post_lighting (RootPage)", kwargs
        return LightingPage('Lighting')

    def form_post_rooms(self, **_kwargs):
        return RoomsPage('rooms')

    def form_post_scenes(self, **_kwargs):
        return ScenesPage('scenes')

    def form_post_schedule(self, **_kwargs):
        return SchedulePage('schedule')

    def form_post(self, *args, **kwargs):
        print " - form_post - args={0:}, kwargs={1:}".format(args, kwargs)
        return RootPage('Root')


def Init():
    return
    global g_logger
    Web_Data[0] = WebData()
    Web_Data[0].WebPort = 8080
    g_logger = logging.getLogger('PyHouse.WebServer')
    entertainment.Init()
    # config_xml.ReadConfig().read_log_web()
    g_logger.info("Initialized - Start the web server on port {0:}".format(g_port))

def Start():
    return
    g_site_dir = os.path.split(os.path.abspath(__file__))[0]
    print "Webserver path = ", g_site_dir
    l_site = appserver.NevowSite(RootPage('/'))
    WebUtilities().build_child_tree()
    reactor.listenTCP(g_port, l_site)
    g_logger.info("Started.")

def Stop():
    pass

# Import PyMh files
from entertainment import entertainment
# from main.house import Location_Data
from schedule import schedule

Light_Data = lighting.Light_Data
# Location_Data = house.Location_Data
# Room_Data = house.Room_Data
# Schedule_Data = schedule.Schedule_Data
Web_Data = {}



# ## END
