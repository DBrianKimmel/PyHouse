'''
Gui to turn lights on/off or dim.

Created on Oct 7, 2012

@author: briank
'''

# Import system type stuff
from Tkinter import Frame, Scale, Toplevel, Button, IntVar, StringVar, W, DISABLED, SUNKEN, RAISED, HORIZONTAL

# Import PyMh files and modules.
from src.configure import gui_tools
from src.configure.gui_tools import GuiTools

g_debug = 4
# 0 = off
# 1 = major routine entry
# 2 = Startup Details
# 3 = setting details
# 4 =

FG = 'red'
BG_LIGHT = '#C0C090'


class CtlLightsWindow(GuiTools):
    ''' Display a window showing all lights.
    '''

    m_gui_obj = None
    m_ix = 0

    def __init__(self, p_gui_obj, p_houses_obj):
        """Initialize then bring up the 'select house' menu.
        """
        if g_debug >= 1:
            print "gui_ctl_lights - Show select house window - {0:}".format(p_gui_obj)
        self.m_gui_obj = p_gui_obj
        self.show_house_select_window(p_gui_obj, p_houses_obj)

    def show_buttons_for_one_house(self, p_gui_obj, p_house_obj):
        """Display the light selection window with the lights for the selected house.
        Display this frame within the root window.

        This is a callback from gui_tools house select window

        @param p_house_obj: is the house object of the selected house.
        """
        self.m_house_obj = p_house_obj
        self.m_gui_obj = p_gui_obj
        if g_debug >= 2:
            print "gui_ctl_lights.show_buttons_for_one_house() - House:{0:}".format(p_house_obj.Name)
        self.frame_delete(p_gui_obj.HouseSelectFrame)
        self.frame_delete(p_gui_obj.ModuleMenuFrame)
        p_gui_obj.ModuleMenuFrame = Frame(self.m_gui_obj.RootWindow)
        p_gui_obj.ModuleMenuFrame.grid(padx = 5, pady = 5)
        p_gui_obj.RootWindow.title('Control Lights')
        self.m_ix = 0
        self.show_control_button(p_house_obj)
        Button(p_gui_obj.ModuleMenuFrame, text = "Back", fg = "red", bg = gui_tools.BG_BOTTOM,
               command = self.main_screen).grid(row = self.m_ix, column = 1)

    def show_control_button(self, p_house_obj):
        """ Show all the lights for the selected house.

        @param p_house_obj: is one House_Data object (see house.py).
        """
        l_light = []
        self.m_max_light = 0
        for l_light_obj in p_house_obj.Lights.itervalues():
            if l_light_obj.Key > self.m_max_light:
                self.m_max_light = l_light_obj.Key
            l_relief = SUNKEN
            l_bg = gui_tools.BG_INACTIVE
            l_fg = gui_tools.FG_INACTIVE
            if l_light_obj.Active:
                l_relief = RAISED
                l_bg, l_fg = self.color_button(int(l_light_obj.CurLevel))
            l_long = l_light_obj.RoomName + '-' + l_light_obj.Name
            l = Button(self.m_gui_obj.ModuleMenuFrame, text = l_long, bg = l_bg, fg = l_fg, relief = l_relief,
                       command = lambda x = p_house_obj, y = self.m_ix: self.ctl_lights(x, y))
            l_light.append(l)
            l_row, l_col = self.columnize(self.m_ix, 4)
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1

    def ctl_lights(self, p_house_obj, p_light_key):
        """
        @param p_house_obj: is the house object
        @param p_light_key: the key to look up the light info.
        """
        if g_debug >= 4:
            print "gui_ctl_lights.ctl_lights() - House:{0:}".format(p_house_obj.Name)
        CtlLightsDialog(self.m_gui_obj, p_house_obj, p_light_key, "Editing Light")

    def main_screen(self):
        self.frame_delete(self.m_gui_obj.ModuleMenuFrame)
        self.m_gui_obj.MainMenuFrame.grid()


class CtlLightsDialog(CtlLightsWindow):
    """Create a dialog window to control a light.
    """

    def __init__(self, p_gui_obj, p_house_obj, p_lights_key, p_title = None):
        """
        @param p_parent: The parent widget for this dialog.
        @param p_house_obj: is the house object.
        @param p_light_key: is the index of the light to control
        @param p_title:
        """
        self.m_gui_obj = p_gui_obj
        p_gui_obj.DialogWindow = Toplevel(p_gui_obj.RootWindow)
        if p_title:
            p_gui_obj.DialogWindow.title(p_title)
        self.l_result = None
        self.create_room_vars()
        l_light_obj = self.load_house_vars(p_house_obj, p_lights_key)
        l_res = 100
        if self.Dimmable.get() == 1: l_res = 1
        p_gui_obj.ModuleDialogFrame = Frame(p_gui_obj.DialogWindow)
        p_gui_obj.ModuleDialogFrame.grid_columnconfigure(0, minsize = 130)
        p_gui_obj.ModuleDialogFrame.grid_columnconfigure(1, minsize = 300)
        p_gui_obj.ModuleDialogFrame.grid(padx = 5, pady = 5)
        #
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 1, 'Key', self.Key, state = DISABLED)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 3, 'Room Name', self.RoomName, state = DISABLED)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 4, 'Light Name', self.Name, state = DISABLED)
        self.level = Scale(p_gui_obj.ModuleDialogFrame, from_ = 0, to = 100, orient = HORIZONTAL, resolution = l_res)
        self.level.grid(row = 11, column = 1, sticky = W)
        self.level.set(l_light_obj.CurLevel)
        Button(p_gui_obj.ModuleDialogFrame, text = 'Change', fg = "blue", bg = gui_tools.BG_BOTTOM,
               command = lambda x = p_house_obj, y = p_lights_key: self.change_light(x, y)).grid(row = 91, column = 0)
        Button(p_gui_obj.ModuleDialogFrame, text = "Cancel", fg = "red", bg = gui_tools.BG_BOTTOM,
               command = lambda x = p_gui_obj, y = p_house_obj: self.quit_dialog(x, y)).grid(row = 91, column = 2)
        if g_debug >= 4:
            print "gui_ctl_lights.CtlLightsDialog.__init__() - Resolution: {0:}, CurLevel: {1:}".format(l_res, l_light_obj.CurLevel)

    def create_room_vars(self):
        """Create everything - used or not.
        """
        # Common / Lights, Buttons
        self.Dimmable = IntVar()
        self.Family = StringVar()
        self.Key = IntVar()
        self.Name = StringVar()
        self.RoomName = StringVar()
        self.Type = StringVar()

    def load_house_vars(self, p_house_obj, p_light_key):
        """
        @param p_house_obj: is the house object.
        @param p_light_key: is the index of the light to control
        """
        if g_debug >= 1:
            print "gui_ctl_lights.load_house_vars() "
        l_light_obj = p_house_obj.Lights[p_light_key]
        l_light_obj.Key = p_light_key
        l_family = l_light_obj.Family
        l_type = l_light_obj.Type
        self.Dimmable.set(self.get_bool(l_light_obj.Dimmable))
        self.Family.set(l_family)
        self.Key.set(l_light_obj.Key)
        self.Name.set(l_light_obj.Name)
        self.RoomName.set(l_light_obj.RoomName)
        self.Type.set(l_type)
        if g_debug >= 8:
            print "gui_ctl_lights.load_house_vars() - Dim ", l_light_obj.Dimmable, self.Dimmable.get()
        return l_light_obj

    def get_vars(self):
        pass

    def change_light(self, p_house_obj, p_light_key):
        """

        @param p_house_obj: is the house object
        """
        l_light = self.Name.get()
        l_level = self.level.get()
        l_key = self.Key.get()
        l_light_obj = p_house_obj.Lights[l_key]
        if g_debug >= 3:
            print "gui_ctl_lights.change_light() - House:{0:}".format(p_house_obj.Name), p_house_obj
            print "                              - Name:{0:}, Level:{1}, Key:{2:} ".format(l_light, l_level, p_light_key)

    def quit_dialog(self, p_gui_obj, p_house_obj):
        if g_debug >= 2:
            print "gui_ctl_lights.quit_dialog()"
        p_gui_obj.DialogWindow.destroy()
        p_gui_obj.ModuleDialogFrame.destroy()
        self.show_buttons_for_one_house(p_gui_obj, p_house_obj)

# ## END DBK
