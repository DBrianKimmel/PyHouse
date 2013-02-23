'''
Gui to turn lights on/off or dim.

Created on Oct 7, 2012

@author: briank
'''
from Tkinter import Frame, Scale, Toplevel, Button, IntVar, DoubleVar, StringVar, W, DISABLED, SUNKEN, RAISED, HORIZONTAL
import lighting.lighting as lighting
import gui
import gui_tools
from configure.gui_tools import GuiTools
from main import houses
from house import house


g_debug = 5

House_Data = house.House_Data
Houses_Data = houses.Houses_Data

FG = 'red'
BG_LIGHT = '#C0C090'


class CtlLightsWindow(GuiTools):
    ''' Display a window showing all lights.
    '''

    def __init__(self, p_root, p_main_window):
        """Initialize then bring up the 'select house' menu.
        """
        if g_debug > 0:
            print "gui_ctl_lights - Show select house window"
        self.m_root = p_root
        self.main_window = p_main_window
        self.m_house_select_window = self.show_house_select_window(p_root, p_main_window)

    def show_buttons_for_one_house(self, p_ix, p_house_obj):
        """Display the light selection window with the lights for the selected house.

        @param p_house_obj: is one House_Data object (see house.py).
        """
        if g_debug > 1:
            print "gui_ctl_lights.show_buttons_for_one_house() - Ix:{0:}".format(p_ix)
        self.frame_delete(self.m_house_select_window)
        self.m_lights_frame = Frame(self.m_root)
        self.m_lights_frame.grid(padx = 5, pady = 5)
        self.m_ix = 0
        self.show_control_button(p_ix, p_house_obj)
        Button(self.m_lights_frame, text = "Back", fg = "red", bg = gui_tools.BG_BOTTOM,
               command = self.main_screen).grid(row = self.m_ix, column = 1)

    def show_control_button(self, p_ix, p_house_obj):
        """ Show all the lights for the selected house.

        @param p_house_obj: is one House_Data object (see house.py).
        """
        l_light = []
        self.m_max_light = 0
        for l_light_obj in p_house_obj.Lights.itervalues():
            if l_light_obj.Key > self.m_max_light: self.m_max_light = l_light_obj.Key
            l_relief = SUNKEN
            if l_light_obj.Active: l_relief = RAISED
            l_long = l_light_obj.RoomName + '-' + l_light_obj.Name
            l_bg, l_fg = self.color_button(int(l_light_obj.CurLevel))
            l = Button(self.m_lights_frame, text = l_long, bg = l_bg, fg = l_fg, relief = l_relief,
                       command = lambda x = p_house_obj, y = self.m_ix: self.ctl_lights(x, y))
            l_light.append(l)
            l_row, l_col = self.columnize(self.m_ix, 4)
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1

    def ctl_lights(self, p_house_obj, p_key):
        """
        @param p_house_obj: is the house object
        @param p_key: the key to look up the light info.
        """
        if g_debug > 0:
            print "Control lights", p_house_obj.Name
        LightingDialog(self.m_lights_frame, p_house_obj, p_key, "Editing Light")

    def main_screen(self):
        self.frame_delete(self.m_lights_frame)
        gui.MainWindow()


class LightingDialog(gui_tools.GuiTools):
    """Create a dialog window to control a light.

    @param p_parent: The parent widget for this dialog.
    @param p_house_obj: is the house object.
    @param p_key: is the index of the light to control
    @param p_title:
    """
    def __init__(self, p_parent, p_house_obj, p_key, p_title = None):
        self.m_top = Toplevel(p_parent)
        if p_title:
            self.m_top.title(p_title)
        self.m_parent = p_parent
        self.l_result = None
        self.create_vars()
        l_light_obj = self.load_vars(p_house_obj, p_key)
        l_res = 100
        if self.Dimmable.get() == 1: l_res = 1
        self.m_frame = Frame(self.m_top)
        self.m_frame.grid_columnconfigure(0, minsize = 130)
        self.m_frame.grid_columnconfigure(1, minsize = 300)
        self.m_frame.grid(padx = 5, pady = 5)
        #
        self.get_entry_str(self.m_frame, 1, 'Key', self.Key, state = DISABLED)
        self.get_entry_str(self.m_frame, 2, 'House Name', self.HouseName, state = DISABLED)
        self.get_entry_str(self.m_frame, 3, 'Room Name', self.RoomName, state = DISABLED)
        self.get_entry_str(self.m_frame, 4, 'Light Name', self.Name, state = DISABLED)
        self.level = Scale(self.m_frame, from_ = 0, to = 100, orient = HORIZONTAL, resolution = l_res)
        self.level.grid(row = 11, column = 1, sticky = W)
        self.level.set(l_light_obj.CurLevel)
        Button(self.m_frame, text = 'Change', fg = "blue", bg = gui_tools.BG_BOTTOM, command = lambda x = p_house_obj, y = p_key: self.change_light(x, y)).grid(row = 91, column = 0)
        Button(self.m_frame, text = "Cancel", fg = "red", bg = gui_tools.BG_BOTTOM, command = self.quit_dialog).grid(row = 91, column = 2)
        if g_debug > 0:
            print "Resolution: {0:}, CurLevel: {1:}".format(l_res, l_light_obj.CurLevel)

    def create_vars(self):
        """Create everything - used or not.
        """
        # Common / Lights, Buttons
        self.Active = IntVar()
        self.Comment = StringVar()
        self.Coords = StringVar()
        self.Dimmable = IntVar()
        self.Family = StringVar()
        self.Key = IntVar()
        self.Name = StringVar()
        self.HouseName = StringVar()
        self.RoomName = StringVar()
        self.Type = StringVar()
        # Controllers
        self.Interface = StringVar()
        self.Port = StringVar()
        # Interface USB
        self.Vendor = IntVar()
        self.Product = IntVar()
        # Interface Serial
        self.BaudRate = IntVar()
        self.ByteSize = IntVar()
        self.Parity = StringVar()
        self.StopBits = DoubleVar()
        self.Timeout = DoubleVar()
        # Family - UPB
        self.NetworkID = IntVar()
        self.Password = IntVar()
        self.UnitID = IntVar()
        # Family - Insteon
        self.Address = StringVar()
        self.Controller = IntVar()
        self.DevCat = StringVar()
        self.GroupList = StringVar()
        self.GroupNumber = StringVar()
        self.Master = IntVar()
        self.ProductKey = IntVar()
        self.Responder = IntVar()

    def load_vars(self, p_house_obj, p_key):
        """
        @param p_house_obj: is the house object.
        @param p_key: is the index of the light to control
        """
        if g_debug > 0:
            print "gui_ctl_lights.load_vars() "
        l_light_obj = p_house_obj.Lights[p_key]
        l_light_obj.Key = p_key
        l_family = l_light_obj.Family
        l_type = l_light_obj.Type
        self.Active.set(self.get_bool(l_light_obj.Active))
        self.Comment.set(l_light_obj.Comment)
        self.Coords.set(l_light_obj.Coords)
        self.Dimmable.set(self.get_bool(l_light_obj.Dimmable))
        self.Family.set(l_family)
        self.Key.set(l_light_obj.Key)
        self.Name.set(l_light_obj.Name)
        self.HouseName.set(l_light_obj.HouseName)
        self.RoomName.set(l_light_obj.RoomName)
        self.Type.set(l_type)
        if g_debug > 0:
            print "Dim ", l_light_obj.Dimmable, self.Dimmable.get()
        return l_light_obj

    def get_vars(self):
        pass

    def change_light(self, p_house_obj, p_key):
        """

        @param p_house_obj: is the house object
        """
        l_light = self.Name.get()
        l_level = self.level.get()
        l_key = self.Key.get()
        l_light_obj = p_house_obj.Lights[l_key]
        if g_debug > 0:
            print "gui_ctl_lights.change_light() - Name:{0:}, Level:{1}, Key:{2:} ".format(l_light, l_level, p_key)
        p_house_obj.LightingAPI.change_light_setting(p_house_obj, p_key, l_level)

    def quit_dialog(self):
        self.m_top.destroy()

# ## END
