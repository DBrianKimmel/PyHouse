"""
Created on Jun 3, 2013

@author: briank
"""
# Import system type stuff
from nevow import loaders
from nevow import rend

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils
from src.housing import rooms


g_debug = 0
# 0 = off
# 1 = log extra info
# 2 = major routine entry
# 3 = basic Data
# 4 = detail data
# + = NOT USED HERE


class RoomsPage(web_utils.ManualFormMixin):
    addSlash = True
    docFactory = loaders.xmlfile('rooms.xml', templateDir = 'src/web/template')

    def __init__(self, p_parent, p_name, p_house_obj):
        self.m_name = p_name
        self.m_parent = p_parent
        self.m_house_obj = p_house_obj
        if g_debug >= 2:
            print "web_rooms.RoomsPage()"
        if g_debug >= 4:
            print "    ", p_house_obj
        l_css = ['src/web/css/mainPage.css']
        l_js = ['src/web/js/ajax.js', 'src/web/js/floatingWindow.js',
                'src/web/js/roomPage.js']
        web_utils.add_attr_list(RoomsPage, l_css)
        web_utils.add_attr_list(RoomsPage, l_js)
        web_utils.add_float_page_attrs(RoomsPage)
        rend.Page.__init__(self)

    def data_roomslist(self, _context, _data):
        """Build up a list of schedule slots.
        @param _context: is a tag that we are building an object to render
        @param _data: is the page object we are extracting for.
        @return: an object to render.
        """
        if g_debug >= 4:
            print "web_rooms.data_roomlist() ", self.m_house_obj
        l_rooms = {}
        for l_key, l_obj in self.m_house_obj.Rooms.iteritems():
            l_rooms[l_key] = l_obj
        return l_rooms

    def render_action(self, _ctx, _data):
        return web_utils.action_url()

    def render_roomslist(self, _context, links):
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
            l_ret.append(T_input(type = 'button', value = l_obj.Key, name = BUTTON,
                    onclick = "createChangeRoomWindow('{0:}', \'{1:}\', \'{2:}\', \'{3:}\', \'{4:}\', \'{5:}\')".format(
                                                    l_obj.Name, l_obj.Key, l_obj.Active, l_obj.Size, l_obj.Corner, l_obj.Comment))
                         [ l_obj.Name, "\n" ])
            l_cnt += 1
        return l_ret

    def _store_rooms(self, **kwargs):
        if g_debug >= 3:
            print "web_rooms.RoomsPage._store_rooms() - ", kwargs
        l_obj = rooms.RoomData()
        for l_key, l_val in kwargs.iteritems():
            try:
                l_obj.l_key = l_val
            except KeyError:
                if g_debug >= 2:
                    print "web_rooms._store_rooms() - Error - bad key -", l_key, "=", l_val

    def form_post_add(self, **kwargs):
        """Add a new room to the house we selected earlier.
        """
        if g_debug >= 3:
            print "web_rooms.RoomsPage.form_post_add() - kwargs=", kwargs
        self._store_rooms(**kwargs)
        # TODO: we should write out the updated info.
        return RoomsPage(self, self.m_name, self.m_house_obj)

    def form_post_change(self, **kwargs):
        """Change a room in the house we selected earlier.
        """
        if g_debug >= 3:
            print "web_rooms.RoomsPage.form_post_change() - kwargs=", kwargs
        self._store_rooms(**kwargs)
        # TODO: we should write out the updated info.
        return RoomsPage(self, self.m_name, self.m_house_obj)

    def form_post_delete(self, **kwargs):
        """Delete a room from the house we selected earlier.
        """
        if g_debug >= 3:
            print "web_rooms.RoomsPage.form_post_delete() - kwargs=", kwargs
        del self.m_house_obj.Rooms[kwargs['Key']]
        # TODO: we should write out the updated info.
        return RoomsPage(self, self.m_name, self.m_house_obj)

    def form_post_back(self, **kwargs):
        if g_debug >= 3:
            print "web_rooms.form_post_back()", kwargs
        return self.m_parent(self, self.m_name, self.m_houses_obj.Object)

# ## END DBK
