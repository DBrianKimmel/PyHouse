'''
Gui to turn lights on/off or dim.

Created on Oct 7, 2012

@author: briank
'''
from Tkinter import *
import lighting.lighting as lighting
import gui
import gui_tools
from configure.gui_tools import GuiTools


Light_Data = lighting.Light_Data
g_debug = 0

FG = 'red'
BG_LIGHT = '#C0C090'


class CtlLightsWindow(GuiTools):
    '''
    Display a window showing all lights.
    '''

    def __init__(self, p_root):
        '''
        Constructor
        '''
        self.m_frame = Frame(p_root)
        self.m_ix = 0
        self.m_frame.grid()
        self.show_all_lights()
        Button(self.m_frame, text = "Back", fg = FG, bg = gui_tools.BG_BOTTOM, command = self.main_screen).grid(row = self.m_ix, column = 1)

    def show_all_lights(self):
        l_light = []
        self.m_max_light = 0
        for l_obj in Light_Data.itervalues():
            if l_obj.Key > self.m_max_light: self.m_max_light = l_obj.Key
            l_relief = SUNKEN
            if l_obj.Active: l_relief = RAISED
            l_long = l_obj.HouseName + '-' + l_obj.RoomName + '-' + l_obj.Name
            l = Button(self.m_frame, text = l_long, bg = BG_LIGHT, relief = l_relief,
                       command = lambda x = l_obj.Key, y = 1: self.ctl_lights(x, y))
            l_light.append(l)
            l_row, l_col = self.columnize(self.m_ix, 4)
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1

    def ctl_lights(self, p_key, p_kind):
        """
        @param p_key: the key to look up the light info.
        """
        if g_debug > 0:
            print "Control lights", p_key, p_kind
        LightingDialog(self.m_frame, p_key, p_kind, "Editing Light")

    def main_screen(self):
        self.frame_delete(self.m_frame)
        gui.MainWindow()


class LightingDialog(gui_tools.GuiTools):
    """Create a dialog window o control a light.

    @param p_parent: The parent widget for this dialog.
    @param p_key:
    @param p_kind:
    @param p_title:
    """
    def __init__(self, p_parent, p_key, p_kind, p_title = None):
        self.m_top = Toplevel(p_parent)
        if p_title:
            self.m_top.title(p_title)
        self.m_parent = p_parent
        self.l_result = None
        self.create_vars()
        _l_type, _l_family, l_obj = self.load_vars(p_key, p_kind)
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
        self.level.set(l_obj.CurLevel)
        Button(self.m_frame, text = 'Change', fg = "blue", bg = gui_tools.BG_BOTTOM, command = lambda k = self.Key: self.change_light(k)).grid(row = 91, column = 0)
        Button(self.m_frame, text = "Cancel", fg = "red", bg = gui_tools.BG_BOTTOM, command = self.quit_dialog).grid(row = 91, column = 2)
        if g_debug > 0:
            print "Resolution: {0:}, CurLevel: {1:}".format(l_res, l_obj.CurLevel)

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

    def load_vars(self, p_key, _p_kind):
        if g_debug > 0:
            print "LoadVars key, Kind = {0:} - {1:}".format(p_key, _p_kind)
        try:
            l_obj = Light_Data[p_key]
        except:
            l_obj = lighting.LightingData()
            l_obj.Key = p_key
        l_family = l_obj.Family
        l_type = l_obj.Type
        self.Active.set(self.get_bool(l_obj.Active))
        self.Comment.set(l_obj.Comment)
        self.Coords.set(l_obj.Coords)
        self.Dimmable.set(self.get_bool(l_obj.Dimmable))
        self.Family.set(l_family)
        self.Key.set(l_obj.Key)
        self.Name.set(l_obj.Name)
        self.HouseName.set(l_obj.HouseName)
        self.RoomName.set(l_obj.RoomName)
        self.Type.set(l_type)
        if g_debug > 0:
            print "Dim ", l_obj.Dimmable, self.Dimmable.get()
        return l_type, l_family, l_obj

    def get_vars(self):
        pass

    def change_light(self, p_key):
        l_key = p_key.get()
        l_obj = Light_Data[l_key]
        l_light = self.Name.get()
        l_level = self.level.get()
        l_family = self.Family.get()
        if g_debug > 0:
            print "change_light()", l_level, l_light, l_family, l_obj
        lighting.LightingUtility().change_light_setting(l_obj, l_level)

    def quit_dialog(self):
        self.m_top.destroy()

# ## END
