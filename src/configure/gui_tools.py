#!/usr/bin/env python

from Tkinter import *
import Pmw


BG_BOTTOM = '#C0C090'
BG_TOP = '#E0F0E0'

class GuiTools(object):

    def columnize(self, p_count, p_cols = 4):
        l_row = p_count // p_cols
        l_col = p_count % p_cols
        return l_row, l_col

    def make_label(self, p_name):
        l_ret = Label(self.m_frame, text = p_name).grid(column = 0)
        return l_ret

    def make_entry_line(self, p_parent, p_label, p_field):
        l_1 = Label(p_parent, text = p_label)
        l_1.grid(row = 1, column = 0)
        self.m_name = Entry(p_parent, textvar = self.Name)
        self.m_name.grid(row = 1, column = 1)
        return

    def yes_no_radio(self, p_frame, p_var):
        _l_entry = int(p_var.get())
        #print "Creating Y/N buttons with value {0:} <{1:}>".format(p_var, _l_entry)
        l_frame = Frame(p_frame)
        Radiobutton(l_frame, text = "Yes", variable = p_var, value = True).grid(row = 0, column = 0)
        Radiobutton(l_frame, text = "No", variable = p_var, value = False).grid(row = 0, column = 1)
        return l_frame

    def frame_delete(self, p_frame):
        try:
            p_frame.grid_forget()
        except:
            pass

    def get_bool(self, p_arg):
        l_ret = False
        if p_arg == 'True' or p_arg == True:
            l_ret = True
        #print "get_bool ", p_arg, l_ret
        return l_ret

    def pulldown_box(self, p_parent, p_list, p_sel):
        """Create a Pmw combo pulldown box.

        @param p_parent: the parent container / frame
        @param p_list: a list of the items for the box
        @param p_sel: a variable holding the selection to be used
        @return: widget to be positioned in container.
        """
        l_entry = str(p_sel.get())
        #print "debug pulldown_box ", p_list, l_entry
        l_box = Pmw.ComboBox(p_parent,
                    scrolledlist_items = p_list,
                    )
        try:
            l_sel = p_list.index(l_entry)
            print "index = ", l_sel
        except ValueError:
            l_sel = p_list[0]
        l_box.selectitem(l_sel)
        return l_box

### END
