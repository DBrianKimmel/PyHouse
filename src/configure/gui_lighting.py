#!/usr/bin/env python

from Tkinter import Frame, Toplevel, Button, IntVar, DoubleVar, StringVar, W, DISABLED, SUNKEN, RAISED

import sys
from operator import attrgetter

import gui_tools
from lights import lighting
from utils import config_xml


g_debug = 5

VAL_FAM = lighting.VALID_FAMILIES
VAL_INTER = lighting.VALID_INTERFACES
BG_LIGHT = '#C0C090'
BG_CTLR = '#90C090'
BG_BUTTN = '#C09090'

class LightingWindow(gui_tools.GuiTools):

    m_gui_obj = None
    m_ix = 0

    def __init__(self, p_gui_obj, p_houses_obj):
        """Initialize then bring up the 'select house' menu.
        """
        if g_debug > 0:
            print "gui_lighting - Show select house window"
        self.m_gui_obj = p_gui_obj
        self.show_house_select_window(p_gui_obj, p_houses_obj)

    def show_buttons_for_one_house(self, p_gui_obj, p_house_obj):
        """Display the lighting menu with the lights for the selected house.

        This is a callback from gui_tools house select window

        @param p_house_obj: is the house object of the selected house.
        """
        self.m_gui_obj = p_gui_obj
        if g_debug > 1:
            print "gui_lighting.show_buttons_for_one_house() - House:{0:}".format(p_house_obj.Name)
        self.frame_delete(p_gui_obj.HouseSelectFrame)
        self.frame_delete(p_gui_obj.ModuleMenuFrame)
        p_gui_obj.ModuleMenuFrame = Frame(self.m_gui_obj.RootWindow)
        p_gui_obj.ModuleMenuFrame.grid(padx = 5, pady = 5)
        p_gui_obj.RootWindow.title('Add / Edit Lighting Device')
        self.m_ix = 0
        self.show_device_buttons(p_gui_obj, p_house_obj)
        Button(p_gui_obj.ModuleMenuFrame, text = "ADD New Light", bg = BG_LIGHT,
               command = lambda x = p_gui_obj, y = p_house_obj: self.add_light(x, y)).grid(row = self.m_ix, column = 0)
        Button(p_gui_obj.ModuleMenuFrame, text = "ADD New Controller", bg = BG_CTLR,
               command = lambda x = p_gui_obj, y = p_house_obj: self.add_controller(x, y)).grid(row = self.m_ix, column = 1)
        Button(p_gui_obj.ModuleMenuFrame, text = "ADD New Button", bg = BG_BUTTN,
               command = lambda x = p_gui_obj, y = p_house_obj: self.add_button(x, y)).grid(row = self.m_ix, column = 2)
        Button(p_gui_obj.ModuleMenuFrame, text = "Back", fg = "red", bg = gui_tools.BG_BOTTOM,
               command = lambda x = p_gui_obj: self.save_lighting_and_exit(x)).grid(row = self.m_ix, column = 3)

    def show_device_buttons(self, p_gui_obj, p_house_obj):
        """
        """
        if g_debug > 0:
            print "gui_lighting.show_device_buttons()"
        l_light = []
        self.m_max_light = 0
        for l_light_obj in sorted(p_house_obj.Lights.itervalues(), key = attrgetter('Name')):
            if l_light_obj.Key > self.m_max_light:
                self.m_max_light = l_light_obj.Key
            l_relief = SUNKEN
            if l_light_obj.Active:
                l_relief = RAISED
            l = Button(p_gui_obj.ModuleMenuFrame, text = l_light_obj.Name, bg = BG_LIGHT, relief = l_relief,
                       command = lambda w = p_gui_obj, x = l_light_obj.Key, y = 1, z = p_house_obj: self.edit_lights(w, x, y, z))
            l_light.append(l)
            l_row, l_col = self.columnize(self.m_ix, 4)
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1
        #
        self.m_max_controller = 0
        for l_controller_obj in p_house_obj.Controllers.itervalues():
            if l_controller_obj.Key > self.m_max_controller:
                self.m_max_controller = l_controller_obj.Key
            l_relief = SUNKEN
            if l_controller_obj.Active:
                l_relief = RAISED
            c = Button(p_gui_obj.ModuleMenuFrame, fg = "red", text = l_controller_obj.Name, bg = BG_CTLR, relief = l_relief,
                       command = lambda w = p_gui_obj, x = l_controller_obj.Key, y = 2, z = p_house_obj: self.edit_controllers(w, x, y, z))
            l_light.append(c)
            l_row, l_col = self.columnize(self.m_ix, 4)
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1
        #
        self.m_max_button = 0
        for l_button_obj in p_house_obj.Buttons.itervalues():
            if l_button_obj.Key > self.m_max_button:
                self.m_max_button = l_button_obj.Key
            l_relief = SUNKEN
            if l_button_obj.Active:
                l_relief = RAISED
            b = Button(p_gui_obj.ModuleMenuFrame, fg = "blue", text = l_button_obj.Name, bg = BG_BUTTN, relief = l_relief,
                       command = lambda w = p_gui_obj, x = l_button_obj.Key, y = 3, z = p_house_obj: self.edit_buttons(w, x, y, z))
            l_light.append(b)
            l_row, l_col = self.columnize(self.m_ix, 4)
            l_light[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1
        self.m_ix += 2

    def edit_lights(self, p_gui_obj, p_arg, p_kind, p_house_obj):
        if g_debug > 0:
            print "Edit lights", p_arg, p_kind
        LightingDialog(p_gui_obj, p_arg, p_kind, p_house_obj, "Editing Light")

    def edit_controllers(self, p_gui_obj, p_arg, p_kind, p_house_obj):
        if g_debug > 0:
            print "Edit Controllers", p_arg, p_kind
        LightingDialog(p_gui_obj, p_arg, p_kind, p_house_obj, "Editing Controller")

    def edit_buttons(self, p_gui_obj, p_arg, p_kind, p_house_obj):
        if g_debug > 0:
            print "Edit Buttons", p_arg, p_kind
        LightingDialog(p_gui_obj, p_arg, p_kind, p_house_obj, "Editing Button")

    def add_light(self, p_gui_obj, p_house_obj):
        if g_debug > 0:
            print "gui_lighting.add_light() ", p_house_obj
        LightingDialog(p_gui_obj, self.m_max_light + 1, 4, p_house_obj, "Adding Light")

    def add_controller(self, p_gui_obj, p_house_obj):
        if g_debug > 0:
            print "Adding controller"
        LightingDialog(p_gui_obj, self.m_max_controller + 1, 5, p_house_obj, "Adding Controller")

    def add_button(self, p_gui_obj, p_house_obj):
        if g_debug > 0:
            print "Adding button"
        LightingDialog(p_gui_obj, self.m_max_button + 1, 6, p_house_obj, "Adding Button")

    def save_lighting_and_exit(self, p_gui_obj):
        """
        """
        if g_debug > 1:
            print "gui_schedule.save_schedules_and_exit() "
        self.frame_delete(p_gui_obj.ModuleMenuFrame)
        self.show_main_menu(p_gui_obj.MainMenuFrame)


class LightingDialog(LightingWindow):
    """
    """

    def __init__(self, p_gui_obj, p_device_key, p_kind, p_house_obj, p_title):
        """
        @param p_parent_window: is the TkInter ID of the parent window (.12345678)
        @param p_device_key: is the schedule id we are about to edit.
        @param p_kind: is 1, 2 or 3 for the kind of device (light, controller, button)
        @param p_house_obj: is the house object that we are editing.
        @param p_title is the title to put at the top of the window:
        """
        if g_debug > 1:
            print "LightingDialog.__init__() - LightKey:{0:}".format(p_device_key), p_kind, p_title, p_house_obj
        p_gui_obj.DialogWindow = Toplevel(p_gui_obj.RootWindow)
        p_gui_obj.DialogWindow.title(p_title)
        self.l_result = None
        self.create_device_vars()
        l_type, l_family, l_interface = self.load_device_vars(p_device_key, p_kind, p_house_obj)
        p_gui_obj.ModuleDialogFrame = Frame(p_gui_obj.DialogWindow)
        p_gui_obj.ModuleDialogFrame.grid_columnconfigure(0, minsize = 130)
        p_gui_obj.ModuleDialogFrame.grid_columnconfigure(1, minsize = 300)
        p_gui_obj.ModuleDialogFrame.grid(padx = 5, pady = 5)
        # Common Part - Light
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 1, 'Key', self.Key, state = DISABLED)
        self.get_entry_bol(p_gui_obj.ModuleDialogFrame, 2, 'Active', self.Active)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 3, 'Type', self.Type, state = DISABLED)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 4, 'Name', self.Name, width = 50)
        self.get_entry_pdb(p_gui_obj.ModuleDialogFrame, 5, 'Family', self.Family, VAL_FAM, self.Family, self.get_family)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 6, 'Comment', self.Comment, width = 50)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 7, 'Coords', self.Coords)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 8, 'House Name', self.HouseName, state = DISABLED)
        self.get_entry_pdb(p_gui_obj.ModuleDialogFrame, 9, 'Room Name', self.RoomName, self.build_names(p_house_obj.Rooms), self.RoomName, self.get_roomname)
        self.get_entry_bol(p_gui_obj.ModuleDialogFrame, 10, 'Dimmable', self.Dimmable)
        # nothing extra for buttons yet.
        if l_type == 'Button':
            pass
        # controllers have a lot more.
        elif l_type == 'Controller':
            self.get_entry_pdb(p_gui_obj.ModuleDialogFrame, 31, 'Interface', self.Interface, VAL_INTER, self.Interface, self.get_interface)
            self.get_entry_str(p_gui_obj.ModuleDialogFrame, 32, 'Port', self.Port, width = 50)
            self.get_entry_hex(p_gui_obj.ModuleDialogFrame, 33, 'Vendor', self.Vendor)
            self.get_entry_hex(p_gui_obj.ModuleDialogFrame, 34, 'Product', self.Product)
            if l_interface == 'Serial':
                self.get_entry_str(p_gui_obj.ModuleDialogFrame, 41, 'Baud Rate', self.BaudRate)
                self.get_entry_str(p_gui_obj.ModuleDialogFrame, 42, 'Byte Size', self.ByteSize)
                self.get_entry_str(p_gui_obj.ModuleDialogFrame, 43, 'Parity', self.Parity)
                self.get_entry_str(p_gui_obj.ModuleDialogFrame, 44, 'Stop Bits', self.StopBits)
                self.get_entry_str(p_gui_obj.ModuleDialogFrame, 45, 'Timeout', self.Timeout)
            elif l_interface == 'USB':
                pass
            elif l_interface == 'Ethernet':
                pass
        # Now for interfaces add the following:
        if l_family == 'Insteon':
            self.get_entry_str(p_gui_obj.ModuleDialogFrame, 61, 'Address', self.Address)
            self.get_entry_bol(p_gui_obj.ModuleDialogFrame, 62, 'Controller', self.Controller)
            self.get_entry_str(p_gui_obj.ModuleDialogFrame, 63, 'DevCat', self.DevCat)
            self.get_entry_str(p_gui_obj.ModuleDialogFrame, 64, 'Group Number', self.GroupNumber)
            self.get_entry_str(p_gui_obj.ModuleDialogFrame, 65, 'Group List', self.GroupList)
            self.get_entry_str(p_gui_obj.ModuleDialogFrame, 66, 'Master', self.Master)
            self.get_entry_str(p_gui_obj.ModuleDialogFrame, 67, 'Product Key', self.ProductKey)
            self.get_entry_bol(p_gui_obj.ModuleDialogFrame, 68, 'Responder', self.Responder)
        elif l_family == 'UPB':
            self.get_entry_str(p_gui_obj.ModuleDialogFrame, 61, 'Unit ID', self.UnitID)
            self.get_entry_str(p_gui_obj.ModuleDialogFrame, 62, 'Network ID', self.NetworkID)
            self.get_entry_str(p_gui_obj.ModuleDialogFrame, 63, 'Password', self.Password)
        elif l_family == 'X10':
            pass
        l_text = "Add"
        if p_title.startswith("Edit"):
            l_text = "Save"
            self.get_entry_btn(p_gui_obj.ModuleDialogFrame, 91, 1, 'Delete', lambda x = p_gui_obj, y = p_house_obj: self.delete_entry(x, y), bg = gui_tools.BG_BOTTOM)
        self.get_entry_btn(p_gui_obj.ModuleDialogFrame, 91, 0, l_text, lambda x = p_gui_obj, y = p_house_obj: self.save_device_vars(x, y), fg = "blue", bg = gui_tools.BG_BOTTOM)
        self.get_entry_btn(p_gui_obj.ModuleDialogFrame, 91, 3, "Cancel", lambda x = p_gui_obj, y = p_house_obj: self.quit_dialog(x, y), fg = "blue", bg = gui_tools.BG_BOTTOM)

    def delete_entry(self, p_gui_obj, p_house_obj):
        if g_debug > 1:
            print "gui_lighting.delete_entry() ", p_house_obj
        l_type = self.Type.get()
        l_key = self.Key.get()
        if l_type == 'Light':
            del p_house_obj.Lights[l_key]
        elif l_type == 'Controller':
            del p_house_obj.Controllers[l_key]
        else:
            del p_house_obj.Buttons[l_key]
        config_xml.WriteConfig().write_file()
        self.quit_dialog(p_gui_obj, p_house_obj)

    def create_device_vars(self):
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
        self.RoomName = StringVar()
        self.HouseName = StringVar()
        self.Type = StringVar()
        # Controllers
        self.Interface = StringVar()
        self.Port = StringVar()
        self.Vendor = StringVar()
        self.Product = StringVar()
        # Interface USB
        # Interface Serial
        self.BaudRate = IntVar()
        self.ByteSize = IntVar()
        self.Parity = StringVar()
        self.StopBits = DoubleVar()
        self.Timeout = DoubleVar()
        # Family - UPB
        self.NetworkID = IntVar()
        self.Password = StringVar()
        self.UnitID = IntVar()
        # Family - Insteon
        self.Address = StringVar()
        self.Controller = IntVar()
        self.DevCat = StringVar()
        self.GroupList = StringVar()
        self.GroupNumber = StringVar()
        self.Master = IntVar()
        self.ProductKey = StringVar()
        self.Responder = IntVar()

    def load_device_vars(self, p_key, p_kind, p_house_obj):
        """put the values in the boxes
        """
        # print "LoadVars key, Kind = {0:} - {1:}".format(p_key, p_kind)
        l_interface = None
        l_housename = p_house_obj.Name
        try:
            if p_kind == 1 or p_kind == 4:
                l_type = "Light"
                try:
                    l_obj = p_house_obj.Lights[p_key]
                except KeyError:
                    l_obj = lighting.LightData()
                    l_obj.Key = p_key
                    l_obj.Family = 'Insteon'
                    l_obj.Address = ''
            elif p_kind == 2 or p_kind == 5:
                l_type = "Controller"
                try:
                    l_obj = p_house_obj.Controllers[p_key]
                except KeyError:
                    l_obj = lighting.ControllerData()
                    l_obj.Family = 'Insteon'
                l_interface = l_obj.Interface
            else:
                l_type = "Button"
                try:
                    l_obj = p_house_obj.Buttons[p_key]
                except KeyError:
                    l_obj = lighting.ButtonData()
                    l_obj.Family = 'Insteon'
        except Exception, e:  # KeyError
            print "Load vars exception", sys.exc_info()[0], e
            l_obj = lighting.LightData()
            l_obj.Key = p_key
            l_obj.Family = 'Insteon'
        l_family = l_obj.Family
        self.Active.set(self.get_bool(l_obj.Active))
        self.Comment.set(l_obj.Comment)
        self.Coords.set(l_obj.Coords)
        self.Dimmable.set(self.get_bool(l_obj.Dimmable))
        self.Family.set(l_family)
        self.Key.set(l_obj.Key)
        self.Name.set(l_obj.Name)
        self.RoomName.set(l_obj.RoomName)
        self.HouseName.set(l_housename)
        self.Type.set(l_type)
        if l_type == 'Controller':
            if g_debug > 0:
                print "gui_lighting() - Interface =", l_obj.Interface
            self.Interface.set(l_obj.Interface)
            self.Port.set(l_obj.Port)
            self.Vendor.set(self.put_hex(int(str(l_obj.Vendor), 0)))  # Displays hex
            self.Product.set(self.put_hex(int(str(l_obj.Product), 0)))  # Displays hex
            if l_obj.Interface == 'USB':
                self.Vendor.set(l_obj.Vendor)
                self.Product.set(l_obj.Product)
            if l_obj.Interface == 'Serial':
                self.BaudRate.set(l_obj.BaudRate)
                self.ByteSize.set(l_obj.ByteSize)
                self.Parity.set(l_obj.Parity)
                self.StopBits.set(l_obj.StopBits)
                self.Timeout.set(l_obj.Timeout)
        # TODO: Change to access family modules to fill in these things.
        if l_family == 'Insteon':
            try:
                self.Address.set(l_obj.Address)
                self.Controller.set(self.get_bool(l_obj.Controller))
                self.DevCat.set(self.put_hex(int(str(l_obj.DevCat), 0)))  # Displays hex
                self.GroupList.set(l_obj.GroupList)
                self.GroupNumber.set(l_obj.GroupNumber)
                self.Master.set(self.get_bool(l_obj.Master))
                self.ProductKey.set(l_obj.ProductKey)
                self.Responder.set(self.get_bool(l_obj.Responder))
            except AttributeError:
                self.Address.set('11.22.33')
                self.Controller.set(False)
                self.DevCat.set(0)
                self.GroupList.set('')
                self.GroupNumber.set(0)
                self.Master.set(False)
                self.ProductKey.set('00.00.00')
                self.Responder.set(False)
        elif l_family == 'UPB':
            try:
                self.NetworkID.set(l_obj.NetworkID)
                self.Password.set(self.put_hex(int(str(l_obj.Password), 0)))
                self.UnitID.set(l_obj.UnitID)
            except AttributeError:
                self.NetworkID.set(0)
                self.Password.set(self.put_hex(0))
                self.UnitID.set(0)
        return l_type, l_family, l_interface

    def save_device_vars(self, p_gui_obj, p_house_obj):
        l_type = self.Type.get()
        l_key = self.Key.get()
        l_family = self.Family.get()
        l_interface = self.Interface.get()
        l_obj = lighting.LightData()
        l_obj.Active = int(self.Active.get())
        l_obj.Comment = self.Comment.get()
        l_obj.Coords = self.Coords.get()
        l_obj.Dimmable = self.Dimmable.get()
        l_obj.Family = l_family
        l_obj.Key = l_key
        l_obj.Name = self.Name.get()
        l_obj.RoomName = self.RoomName.get()
        l_obj.HouseName = self.HouseName.get()
        l_obj.Type = l_type
        if l_family == 'Insteon':
            l_obj.Address = self.Address.get()
            l_obj.Controller = int(self.Controller.get())
            l_obj.DevCat = self.DevCat.get()
            l_obj.GroupList = self.GroupList.get()
            l_obj.GroupNumber = self.GroupNumber.get()
            l_obj.Master = int(self.Master.get())
            l_obj.ProductKey = self.ProductKey.get()
            l_obj.Responder = int(self.Responder.get())
        elif l_family == 'UPB':
            l_obj.NetworkID = int(self.NetworkID.get())
            l_obj.Password = self.Password.get()
            l_obj.UnitID = int(self.UnitID.get())
        #
        if l_interface == 'USB':
            l_obj.Vendor = self.Vendor.get()
            l_obj.Product = self.Product.get()
        elif l_interface == 'Serial':
            l_obj.BaudRate = int(self.BaudRate.get())
            l_obj.ByteSize = self.ByteSize.get()
            l_obj.Parity = self.Parity.get()
            l_obj.StopBits = self.StopBits.get()
            l_obj.Timeout = self.Timeout.get()
            pass
        else:
            pass
        if l_type == 'Light':
            p_house_obj.Lights[l_key] = l_obj
        elif l_type == 'Controller':
            l_obj.Interface = self.Interface.get()
            l_obj.Port = self.Port.get()
            p_house_obj.Controllers[l_key] = l_obj
        else:
            p_house_obj.Buttons[l_key] = l_obj
        if g_debug > 1:
            print "gui_schedule.save_device_vars() Saving lighting data ", l_obj
        self.quit_dialog(p_gui_obj, p_house_obj)

    def quit_dialog(self, p_gui_obj, p_house_obj):
        if g_debug > 0:
            print "gui_lighting.quit_dialog()", p_house_obj
        p_gui_obj.DialogWindow.destroy()
        p_gui_obj.ModuleDialogFrame.destroy()
        self.show_buttons_for_one_house(p_gui_obj, p_house_obj)

    def get_family(self, p_val):
        self.Family.set(p_val)
        if g_debug > 0:
            print "get family - ", p_val

    def get_housename(self, p_val):
        self.HouseName.set(p_val)
        if g_debug > 0:
            print "get house name - ", p_val

    def get_interface(self, p_val):
        self.Interface.set(p_val)
        if g_debug > 0: print "get interface - ", p_val

    def get_roomname(self, p_val):
        self.RoomName.set(p_val)
        if g_debug > 0:
            print "get room name - ", p_val

# ## END
