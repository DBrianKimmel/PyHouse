#!/usr/bin/env python

from Tkinter import *
import Pmw

from housing import houses

g_debug = 0

BG_BOTTOM = '#C0C090'
BG_TOP = '#E0F0E0'
BG_UNDONE = '#F0C0C0'

FG_ACTIVE = '#000000'
BG_ACTIVE = '#F0C0C0'

FG_INACTIVE = "#000000"
BG_INACTIVE = "#E04040"

ComboBox = Pmw.ComboBox


class GuiData(object):

    def __init__(self):
        self.RootWindow = None
        self.HouseSelectFrame = None  # Frame of RootWindow
        self.MainMenuFrame = None  # Frame of RootWindow
        self.ModuleMenuFrame = None  # Frame of RootWindow
        self.DialogWindow = None
        self.ModuleDialogFrame = None  # Frame of DialogWindow
        self.SecondDialogWindow = None
        self.SecondDialogFrame = None

    def __repr__(self):
        l_ret = "GuiData:: RootWindow:{0:}, MainMenuFrame:{1:}, HouseSelectFrame:{2:}".format(self.RootWindow, self.MainMenuFrame, self.HouseSelectFrame)
        l_ret += ", ModuleMenuFrame:{0:}, DialogWindow:{1:}".format(self.ModuleMenuFrame, self.DialogWindow)
        return l_ret


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
        except AttributeError:
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

    m_house_select_frame = None

    def show_house_select_window(self, p_gui_obj, p_houses_obj):
        """This will show a house select window for various modules.
        @param p_gui_obj: is
        @return: the house object for the house selected.
        In addition, returns the house index and house object as parameters for the callback
        """
        if g_debug > 0:
            print "gui_tools.show_house_select_window() - {0:}".format(p_gui_obj)
        p_gui_obj.HouseSelectFrame = Frame(p_gui_obj.RootWindow)
        p_gui_obj.RootWindow.title('Select House')
        p_gui_obj.HouseSelectFrame.grid(padx = 5, pady = 5)
        l_ix = 0
        l_house = []
        for l_house_obj in p_houses_obj.itervalues():
            l_relief = SUNKEN
            l_bg = BG_INACTIVE
            l_fg = FG_INACTIVE
            if l_house_obj.Object.Active:
                l_relief = RAISED
                l_bg = BG_ACTIVE
                l_fg = FG_ACTIVE
            l_row, l_col = self.columnize(l_ix, 4)
            l = Button(p_gui_obj.HouseSelectFrame, text = l_house_obj.Object.Name,
                      relief = l_relief, bg = l_bg, fg = l_fg,
                      command = lambda x = p_gui_obj, y = l_house_obj.Object: self.show_buttons_for_one_house(x, y))
            l_house.append(l)
            l_house[l_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            l_ix += 1
        Button(p_gui_obj.HouseSelectFrame, text = "Back", fg = "red", bg = BG_BOTTOM,
               command = lambda x = p_gui_obj: self.show_main_menu(x)).grid(row = l_ix, column = 1)

    def show_main_menu(self, p_gui_obj):
        """Exit the schedule screen.
        """
        if g_debug > 0:
            print "gui_tools.show_main_menu() - main_menu_frame:{0:}".format(p_gui_obj)
        try:
            self.frame_delete(p_gui_obj.HouseSelectFrame)
        except AttributeError:
            pass
        p_gui_obj.MainMenuFrame.grid()


class GuiTools(HouseSelect):
    """
    """


# ## END
