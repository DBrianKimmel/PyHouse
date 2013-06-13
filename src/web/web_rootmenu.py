'''
Created on May 30, 2013

@author: briank
'''

# Import system type stuff
from nevow import loaders
from nevow import rend
from nevow import static
import json

# Import PyMh files and modules.
from src.utils import config_xml
from src.web.web_tagdefs import *
from src.web import web_utils
from src.web import web_selecthouse
from src.utils import log


g_debug = 5
# 0 = off
# 1 = major routine entry
# 2 = Basic data


class RootPage(web_utils.ManualFormMixin):
    """The main page of the web server.
    """
    addSlash = True
    docFactory = loaders.stan(
        T_html(xmlns = 'http://www.w3.org/1999/xhtml', lang = 'en')[
            T_head[
                T_title['PyHouse - Main Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css')),
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js')["\n"],
                T_script(type = 'text/javascript', src = 'addhouse.js'),
                T_script(type = 'text/javascript', src = 'webserver.js'),
                T_script(type = 'text/javascript', src = 'logs.js'),
                ],
            T_body[
                T_h1['PyHouse'],
                T_form(name = 'mainmenuofbuttons',
                    action = U_H_child('_submit!!post'),
                    enctype = "multipart/form-data",
                    method = 'post')
                    [
                    T_table(style = 'width: 100%;', border = 0)[
                        # T_invisible(data = T_directive('logslist'), render = T_directive('logslist')),
                        T_tr[
                            T_td[ T_input(type = 'submit', value = 'Select House', name = BUTTON), ],
                            T_td[ T_input(type = 'button', onclick = "createNewHouseWindow('NewName')", value = 'Add House') ],
                            T_td[ T_input(type = 'button', onclick = "createChangeWebServerWindow('" + '' + "')", value = 'Web Server') ],
                            T_td[ T_input(type = 'button', onclick = "createChangeLogsWindow(" + json.dumps('x') + ")", value = 'Logs') ],
                            ],
                         T_tr[
                            T_td[ T_input(type = 'submit', value = 'Quit', name = BUTTON) ],
                            T_td[ T_input(type = 'submit', value = 'Reload', name = BUTTON), ],
                            ],
                        ]  # table
                    ]  # form
                ]  # body
            ]  # html
        )  # stan

    def __init__(self, name, p_pyhouses_obj):
        self.name = name
        self.m_pyhouses_obj = p_pyhouses_obj
        if g_debug >= 1:
            print "web_rootmenu.RootPage()"
        if g_debug >= 2:
            print "    ", p_pyhouses_obj
        rend.Page.__init__(self)

        """Build a tree of pages for nevow.
        """
        # These are real files on disk
        setattr(RootPage, 'child_mainpage.css', static.File('web/css/mainpage.css'))
        setattr(RootPage, 'child_ajax.js', static.File('web/js/ajax.js'))
        setattr(RootPage, 'child_floating_window.js', static.File('web/js/floating-window.js'))
        setattr(RootPage, 'child_addhouse.js', static.File('web/js/addhouse.js'))
        setattr(RootPage, 'child_webserver.js', static.File('web/js/webserver.js'))
        setattr(RootPage, 'child_logs.js', static.File('web/js/logs.js'))
        #------------------------------------
        setattr(RootPage, 'child_bottomRight.gif', static.File('web/images/bottom_right.gif'))
        setattr(RootPage, 'child_close.gif', static.File('web/images/close.gif'))
        setattr(RootPage, 'child_minimize.gif', static.File('web/images/minimize.gif'))
        setattr(RootPage, 'child_topCenter.gif', static.File('web/images/top_center.gif'))
        setattr(RootPage, 'child_topLeft.gif', static.File('web/images/top_left.gif'))
        setattr(RootPage, 'child_topRight.gif', static.File('web/images/top_right.gif'))
        setattr(RootPage, 'child_handle.horizontal.png', static.File('web/images/handle.horizontal.png'))


    def form_post_select(self, **kwargs):
        """Select House button post processing.
        """
        if g_debug >= 2:
            print "web_rootmenu.form_post_select()", kwargs
        return web_selecthouse.SelectHousePage('House', self.m_pyhouses_obj)

    def form_post_add(self, **kwargs):
        """Add House button post processing.
        """
        if g_debug >= 2:
            print "web_rootmenu.form_post_add()", kwargs
        # TODO: validate and create a new house.
        return RootPage('House', self.m_pyhouses_obj)

    def form_post_change_web(self, **kwargs):
        """Web server button post processing.
        """
        if g_debug >= 2:
            print "web_rootmenu.form_post_change_web()", kwargs
        self.m_pyhouses_obj.WebData.WebPort = kwargs['WebPort']
        return RootPage('House', self.m_pyhouses_obj)

    def form_post_change_logs(self, **kwargs):
        """Log change form.
        """
        if g_debug >= 2:
            print "web_rootmenu.form_post_change_logs()", kwargs
        return RootPage('House', self.m_pyhouses_obj)

    def form_post(self, *args, **kwargs):
        print "web_rootmenu.form_post() - args={0:}, kwargs={1:}".format(args, kwargs)
        return RootPage('Root', self.m_pyhouses_obj)

    def form_post_quit(self, *args, **kwargs):
        if g_debug >= 2:
            print "web_rootmenu.form_post_quit() - args={0:}, kwargs={1:}".format(args, kwargs)
        """Quit the GUI - this also means quitting all of PyHouse !!
        """
        config_xml.WriteConfig()
        self.m_pyhouses_obj.API.Quit()

    def form_post_reload(self, *args, **kwargs):
        if g_debug >= 2:
            print "web_rootmenu.form_post_reload() - args={0:}, kwargs={1:}".format(args, kwargs)
        self.m_pyhouses_obj.API.Reload(self.m_pyhouses_obj)
        return RootPage('Root', self.m_pyhouses_obj)

# ## END DBK
