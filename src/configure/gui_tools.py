#!/usr/bin/env python

from Tkinter import *
import Pmw

from main import houses

g_debug = 1

Houses_Data = houses.Houses_Data


BG_BOTTOM = '#C0C090'
BG_TOP = '#E0F0E0'
BG_UNDONE = '#F0C0C0'

ComboBox = Pmw.ComboBox


class GuiUtils(object):

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

    def get_entry_hex(self, p_parent, p_row, p_label, p_field, **kwargs):
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
        if g_debug > 1:
            print "gui_tools.get_entry_btn()"
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

    def get_int(self, p_arg):
        l_ret = int(p_arg, 0)
        return l_ret

    def get_hex(self, p_arg):
        l_ret = int(p_arg, 16)
        return l_ret

    def get_true(self, p_arg):
        """Return 1 if a filed is true, 0 otherwise.
        """
        l_arg = p_arg.lower()
        if l_arg == 'true' or l_arg == 'yes' or l_arg != 0:
            return 1
        return 0

    def put_hex(self, p_arg):
        """Convert an int to a hex string with 0x
        """
        l_ret = hex(p_arg)
        return l_ret

    def get_grid(self, p_count):
            l_row = p_count // 4
            l_col = p_count % 4
            return l_row, l_col

    def color_button(self, p_level):
        """Select the colors for a light button based on passed in level.
        """
        # First the foreground to contrast with the background
        if p_level < 70:
            l_fg = 'white'
        else:
            l_fg = 'black'
        # Next the background in 10% steps.
        if p_level < 10:  # Dark
            l_bg = '#505010'
        elif p_level <= 20:  # Dark Yellow
            l_bg = '#585820'
        elif p_level <= 30:  # Dark Yellow
            l_bg = '#606028'
        elif p_level <= 40:  # Dark Yellow
            l_bg = '#707030'
        elif p_level <= 50:  # Dark Yellow
            l_bg = '#808040'
        elif p_level <= 60:  # Dark Yellow
            l_bg = '#909050'
        elif p_level <= 70:  # Dark Yellow
            l_bg = '#A0A060'
        elif p_level <= 80:  # Dark Yellow
            l_bg = '#B0B070'
        elif p_level < 90:  # Medium Yellow
            l_bg = '#D0D080'
        else:
            l_bg = '#FFFFD0'  # Very Light yellow - full on
        return l_bg, l_fg
    def build_names(self, p_dict):
        if g_debug > 1:
            print "gui_tools.build_names() ", p_dict
        l_ret = []
        for l_obj in p_dict.itervalues():
            l_ret.append(l_obj.Name)
        if g_debug > 1:
            print "      List=", l_ret
        return l_ret

    def pulldown_box(self, p_parent, p_tkvar, p_list, p_sel, p_fun):
        """Create a Pmw combo pulldown box.

        @param p_parent: the parent container / frame
        @param p_tkvar: The variable to be updated
        @param p_list: a list of the items for the box
        @param p_sel: a variable holding the selection to be used
        @param p_fun: is the callback to be used when the var is changed
        @return: widget ready to be positioned in container.

        FIXME: does not properly update the calling variable with a new selection.
        """
        if g_debug > 1:
            print "gui_tools.pulldown_box()  - Parent=", p_parent
            print "                  TkInter variable=", p_tkvar
            print "                              List=", p_list
            print "                Selection Variable=", p_sel
            print "                    Callback Funct=", p_fun
        try:
            l_entry = str(p_sel.get())
        except AttributeError:
            l_entry = ''
        l_box = ComboBox(p_parent, scrolledlist_items = p_list, selectioncommand = p_fun)
        try:
            l_sel = p_list.index(l_entry)
            if g_debug > 0:
                print "gui_tools.pulldown_box() - index = ", l_sel
        except ValueError:
            l_sel = 0
        l_box.selectitem(l_sel)
        p_tkvar.set(p_list[l_sel])
        if g_debug > 0:
            print "gui_tools.pulldown_box() ", p_list, l_sel, p_list[l_sel]
        return l_box

class HouseSelect(GuiUtils):

    m_house_select_window = None

    def show_house_select_window(self, p_root, p_main_window):
        """This will show a house select window for various modules.
        @param p_root: is the Tk() root instance.
        @return: the house object for the house selected.
        """
        if g_debug > 0:
            print "gui_tools.show_house_select_window()  - Root=", p_root
        self.m_main_window = p_main_window
        self.m_house_select_window = Frame(p_root)
        p_root.title('Select House')
        self.m_root = p_root
        self.m_house_select_window.grid(padx = 5, pady = 5)
        l_ix = 0
        l_house = []
        for l_obj in Houses_Data.itervalues():
            l_relief = SUNKEN
            if l_obj.Object.Active: l_relief = RAISED
            l_row, l_col = self.get_grid(l_ix)
            l = Button(self.m_house_select_window, text = l_obj.Object.Name,
                      relief = l_relief,
                      command = lambda x = l_ix, y = l_obj.Object: self.show_buttons_for_one_house(x, y))
            l_house.append(l)
            l_house[l_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            l_ix += 1
        Button(self.m_house_select_window, text = "Back", fg = "red", bg = BG_BOTTOM, command = self.show_main_menu).grid(row = l_ix, column = 1)
        return self.m_house_select_window

    def show_main_menu(self):
        """Exit the schedule screen.
        """
        if g_debug > 0:
            print "gui_tools.show_main_menu()"
        self.frame_delete(self.m_house_select_window)
        self.m_main_window.grid()


class GuiTools(HouseSelect):
    """
    """


# ## END
