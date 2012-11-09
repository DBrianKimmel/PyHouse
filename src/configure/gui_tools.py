#!/usr/bin/env python

from Tkinter import *
import Pmw

ComboBox = Pmw.ComboBox

g_debug = 0
BG_BOTTOM = '#C0C090'
BG_TOP = '#E0F0E0'

class GuiTools(object):

    def _yes_no_radio(self, p_parent, p_var):
        _l_entry = int(p_var.get())
        l_frame = Frame(p_parent)
        Radiobutton(l_frame, text = "Yes", variable = p_var, value = True).grid(row = 0, column = 0)
        Radiobutton(l_frame, text = "No", variable = p_var, value = False).grid(row = 0, column = 1)
        return l_frame

    def columnize(self, p_count, p_cols = 4):
        l_row = p_count // p_cols
        l_col = p_count % p_cols
        return l_row, l_col

    def make_label(self, p_parent, p_row, p_label):
        l_ret = Label(p_parent, text = p_label).grid(row = p_row, column = 0, sticky = E)
        return l_ret

    def get_entry_str(self, p_parent, p_row, p_label, p_field, **kwargs):
        Label(p_parent, text = p_label).grid(row = p_row, column = 0, sticky = E)
        l_name = Entry(p_parent, textvar = p_field, **kwargs)
        l_name.grid(row = p_row, column = 1, sticky = W)
        return l_name

    def get_entry_bol(self, p_parent, p_row, p_label, p_var):
        Label(p_parent, text = p_label).grid(row = p_row, column = 0, sticky = E)
        l_frame = self._yes_no_radio(p_parent, p_var)
        l_frame.grid(row = p_row, column = 1, sticky = W)

    def get_entry_pdb(self, p_parent, p_row, p_label, p_var, p_list, p_sel, p_func, **kwargs):
        Label(p_parent, text = p_label).grid(row = p_row, column = 0, sticky = E)
        l_pdb = self.pulldown_box(p_parent, p_var, p_list, p_sel, p_func, **kwargs)
        l_pdb.grid(row = p_row, column = 1, sticky = W)

    def get_entry_btn(self, p_parent, p_row, p_col, p_label, p_func, **kwargs):
        l_butn = Button(p_parent, text = p_label, command = p_func, **kwargs)
        l_butn.grid(row = p_row, column = p_col)

    def frame_delete(self, p_frame):
        try:
            p_frame.grid_forget()
        except:
            pass

    def get_bool(self, p_arg):
        l_ret = False
        if p_arg == 'True' or p_arg == True:
            l_ret = True
        # print "get_bool ", p_arg, l_ret
        return l_ret

    def get_true(self, p_arg):
        """Return 1 if a filed is true, 0 otherwise.
        """
        l_arg = p_arg.lower()
        if l_arg == 'true' or l_arg == 'yes' or l_arg != 0:
            return 1
        return 0

    def build_names(self, p_dict):
        if g_debug > 0: print "Build_Names ", p_dict
        l_ret = []
        for l_obj in p_dict.itervalues():
            l_ret.append(l_obj.Name)
        return l_ret

    def pulldown_box(self, p_parent, p_var, p_list, p_sel, p_fun):
        """Create a Pmw combo pulldown box.

        @param p_parent: the parent container / frame
        @param p_var: The variable to be updated
        @param p_list: a list of the items for the box
        @param p_sel: a variable holding the selection to be used
        @param p_fun: is the callback to be used when the var is changed
        @return: widget to be positioned in container.

        FIXME: does not properly update the calling variable with a new selection.
        """
        try:
            l_entry = str(p_sel.get())
        except AttributeError:
            l_entry = ''
        l_box = ComboBox(p_parent, scrolledlist_items = p_list, selectioncommand = p_fun)
        try:
            l_sel = p_list.index(l_entry)
            if g_debug > 0: print "index = ", l_sel
        except ValueError:
            l_sel = 0
        l_box.selectitem(l_sel)
        p_var.set(p_list[l_sel])
        if g_debug > 0: print "gui_tools.pulldown_box() ", p_list, l_sel, p_list[l_sel]
        return l_box

# ## END
