'''
Created on May 30, 2013

@author: briank
'''

# Import system type stuff
from nevow import tags as _Tag
from nevow import url as _Url


SUBMIT = '_submit'
BUTTON = 'post_btn'

T_p = _Tag.p
T_h1 = _Tag.h1
T_h2 = _Tag.h2
T_td = _Tag.td
T_tr = _Tag.tr
T_div = _Tag.div
T_html = _Tag.html
T_head = _Tag.head
T_body = _Tag.body
T_form = _Tag.form
T_link = _Tag.link
T_table = _Tag.table
T_title = _Tag.title
T_input = _Tag.input
T_script = _Tag.script
T_invisible = _Tag.invisible
T_directive = _Tag.directive

U_R_child = _Url.root.child
U_H_child = _Url.here.child

class WebException(Exception):
    """Raised when there is a web error of some sort.
    """

# ## END DBK

