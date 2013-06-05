"""
Created on Jun 3, 2013

@author: briank
"""
# Import system type stuff
from nevow import loaders
from nevow import rend
from nevow import static

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils
from src.housing import rooms


g_debug = 8
# 0 = off
# 1 = major routine entry
# 2 = Basic data


class RoomsPage(web_utils.ManualFormMixin):
    addSlash = True
    docFactory = loaders.stan(
        T_html[
            T_head[
                T_title['PyHouse - Schedule Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js')["\n"],
                T_script(type = 'text/javascript', src = 'roompage.js'),
                ],  # # head
            T_body[
                T_h1['PyHouse Schedule'],
                T_p['Select the schedule:'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    T_invisible(data = T_directive('roomlist'), render = T_directive('roomlist'))
                    ],  # body
                T_input(type = "button", onclick = "createNewRoomWindow('-1', )", value = "Add Room"),
                # T_input(type = "submit", value = "Back", name = BUTTON),)
                ]
            ]  # html
        )  # stan

    def __init__(self, name, p_house_obj):
        self.name = name
        self.m_house_obj = p_house_obj
        if g_debug >= 1:
            print "web_rooms.RoomsPage.__init__()"
        if g_debug >= 5:
            print "web_rooms.RoomsPage()", self.m_house_obj
        rend.Page.__init__(self)
        setattr(RoomsPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))
        setattr(RoomsPage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(RoomsPage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
        setattr(RoomsPage, 'child_roompage.js', static.File('web/js/roompage.js'))
        #------------------------------------
        setattr(RoomsPage, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
        setattr(RoomsPage, 'child_close.gif', static.File('web/images/close.gif'))
        setattr(RoomsPage, 'child_minimize.gif', static.File('web/images/minimize.gif'))
        setattr(RoomsPage, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
        setattr(RoomsPage, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
        setattr(RoomsPage, 'child_topRight.gif', static.File('web/images/top_right.gif'))
        setattr(RoomsPage, 'child_handle.horizontal.png', static.File('web/images/handle.horizontal.png'))

    def data_roomlist(self, _context, _data):
        """Build up a list of schedule slots.
        @param _context: is a tag that we are building an object to render
        @param _data: is the page object we are extracting for.
        @return: an object to render.
        """
        if g_debug >= 5:
            print "web_rooms.data_roomlist() ", self.m_house_obj
        l_rooms = {}
        for l_key, l_obj in self.m_house_obj.Rooms.iteritems():
            l_rooms[l_key] = l_obj
        return l_rooms

    def render_roomlist(self, _context, links):
        """
        @param: _context is ...
        @param: links are ...
        @return: the list to be added into the stan.dom
        """
        global l_ret
        l_ret = []
        l_cnt = 0
        for l_obj in sorted(links.itervalues()):
            if l_cnt % 2 == 0:
                l_ret.append(T_tr)
            l_ret.append(T_td)
            l_ret.append(T_input(type = 'submit', value = l_obj.Key, name = BUTTON,
                    onclick = "createChangeRoomWindow('{0:}', \'{1:}\', \'{2:}\', \'{3:}\', \'{4:}\', \'{5:}\')".format(
                                                    l_obj.Name, l_obj.Key, l_obj.Active, l_obj.Size, l_obj.Corner, l_obj.Comment))
                         [ l_obj.Name, "\n" ])
            l_cnt += 1
        return l_ret

    def _store_rooms(self, **kwargs):
        if g_debug >= 1:
            print "web_rooms.RoomsPage._store_rooms() - ", kwargs
        l_obj = rooms.RoomData()
        for l_key, l_val in kwargs.iteritems():
            try:
                l_obj.l_key = l_val
            except KeyError:
                if g_debug >= 1:
                    print "web_rooms._store_rooms() - Error - bad key -", l_key, "=", l_val

    def form_post_add(self, **kwargs):
        """Add a new room to the house we selected earlier.
        """
        print "web_rooms.RoomsPage.form_post_add() - kwargs=", kwargs
        self._store_rooms(**kwargs)
        # TODO: we should write out the updated info.
        return RoomsPage(self.name, self.m_house_obj)

    def form_post_change(self, **kwargs):
        """Change a room in the house we selected earlier.
        """
        print "web_rooms.RoomsPage.form_post_change() - kwargs=", kwargs
        self._store_rooms(**kwargs)
        # TODO: we should write out the updated info.
        return RoomsPage(self.name, self.m_house_obj)

    def form_post_delete(self, **kwargs):
        """Delete a room from the house we selected earlier.
        """
        print "web_rooms.RoomsPage.form_post_delete() - kwargs=", kwargs
        del self.m_house_obj.Rooms[kwargs['Key']]
        # TODO: we should write out the updated info.
        return RoomsPage(self.name, self.m_house_obj)

# ## END DBK
