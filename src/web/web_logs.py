'''
Created on Jun 1, 2013

@author: briank
'''

# Import system type stuff
from nevow import loaders
from nevow import rend

# Import PyMh files and modules.
from src.web.web_tagdefs import *
from src.web import web_utils


g_debug = 8
# 0 = off
# 1 = major routine entry
# 2 = Basic data


class LogsPage(web_utils.ManualFormMixin):
    addSlash = True
    docFactory = loaders.stan(
        T_html["\n",
            T_head["\n",
                T_title['PyHouse - Logs Page'],
                T_link(rel = 'stylesheet', type = 'text/css', href = U_R_child('mainpage.css'))["\n"],
                T_script(type = 'text/javascript', src = 'ajax.js')["\n"],
                T_script(type = 'text/javascript', src = 'floating_window.js'),
                T_script(type = 'text/javascript', src = 'logspage.js')["\n"],
                ],
            T_body[
                T_h1['PyHouse Logs'],
                T_p['\n'],
                T_p['abc'],
                T_table(style = 'width: 100%;', border = 0)["\n",
                    T_invisible(data = T_directive('houselist'), render = T_directive('houselist'))
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

    def __init__(self, name, p_pyhouse_obj):
        if g_debug >= 1:
            print "web_logs.LogsPage.__init__()"
        rend.Page.__init__(self)
        self.name = name

# ## END DBK
