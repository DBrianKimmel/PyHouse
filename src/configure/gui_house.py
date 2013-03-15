#!/usr/bin/env python

"""If a house is added, the entire PyHouse must be restarted to activate the house !
"""

from operator import attrgetter
from Tkinter import Frame, Toplevel, Button, IntVar, StringVar, DoubleVar, W, DISABLED, SUNKEN, RAISED

from configure.gui_tools import GuiTools, BG_BOTTOM, BG_TOP, BG_INACTIVE, FG_INACTIVE, FG_ACTIVE
from housing import house
from housing import houses

g_debug = 6

HousesData = houses.HousesData
HouseData = house.HouseData

FG = 'red'

class HouseWindow(GuiTools):
    """Displays all defined houses and handles house add/change.
    """

    m_ix = 0
    m_adding_flag = False
    m_houses_dict = None

    def __init__(self, p_gui_obj, p_houses_dict):
        # p_gui_obj.ModuleMenuFrame = Frame(p_gui_obj.RootWindow)
        self.m_houses_dict = p_houses_dict
        if g_debug >= 1:
            print "gui_house.HouseWindow() - Show select house window", self.m_houses_dict
        self.show_all_houses(p_gui_obj)

    def show_all_houses(self, p_gui_obj):
        """Show the menu window to allow editing houses or adding a new house.
        """
        if g_debug >= 2:
            print "gui_house.show_all_houses()", self.m_houses_dict
        self.m_ix = 0
        p_gui_obj.ModuleMenuFrame = Frame(p_gui_obj.RootWindow)
        p_gui_obj.ModuleMenuFrame.grid()
        l_max = self.show_house_buttons(p_gui_obj, self.m_houses_dict)
        Button(p_gui_obj.ModuleMenuFrame, text = "ADD New House", fg = FG, bg = BG_BOTTOM,
               command = lambda x = p_gui_obj, y = self.m_houses_dict, z = l_max + 1: self.add_house(x, y, z)
               ).grid(row = self.m_ix, column = 0)
        Button(p_gui_obj.ModuleMenuFrame, text = "Back", fg = FG, bg = BG_BOTTOM,
               command = lambda x = p_gui_obj: self.save_houses_and_exit(x)
               ).grid(row = self.m_ix, column = 1)

    def show_house_buttons(self, p_gui_obj, p_houses_dict):
        """Place the house buttons in the menu.
        """
        if g_debug >= 2:
            print "gui_house.show_house_buttons()", self.m_houses_dict
        l_house = []
        l_max_house_ix = -1
        for l_houses_obj in sorted(self.m_houses_dict.itervalues(), key = attrgetter('Name')):
            l_house_obj = l_houses_obj.Object
            if l_house_obj.Key > l_max_house_ix:
                l_max_house_ix = l_house_obj.Key
            l_relief = SUNKEN
            l_bg = BG_INACTIVE
            l_fg = FG_INACTIVE
            if l_house_obj.Active:
                l_relief = RAISED
                l_bg = BG_TOP
                l_fg = FG_ACTIVE
            if g_debug > 0:
                print l_house_obj.Name, l_house_obj.Key
            h = Button(p_gui_obj.ModuleMenuFrame, text = l_house_obj.Name, bg = l_bg, fg = l_fg, relief = l_relief,
                       command = lambda x = p_gui_obj, y = l_house_obj, z = l_houses_obj.Key: self.edit_house(x, y, z))
            l_house.append(h)
            l_house[self.m_ix].grid(row = self.m_ix, sticky = W)
            self.m_ix += 1
        return l_max_house_ix

    def add_house(self, p_gui_obj, p_houses_dict, p_ix):
        """Add a new house to the houses obj.
        pass the real work into the house dialog.
        """
        self.m_adding_flag = True
        l_name = ''
        l_house_obj = HouseData()
        l_house_obj.Name = l_name
        l_house_obj.Key = p_ix
        #
        l_houses_obj = HousesData()
        l_houses_obj.Key = p_ix
        l_houses_obj.Object = l_house_obj
        l_houses_obj.Name = l_name
        l_houses_obj.HouseAPI = None
        if g_debug > 2:
            print "gui_house.add_house() - Key:{0:}".format(self.m_ix)
        HouseDialog(p_gui_obj, l_house_obj, p_ix, "Adding House")

    def edit_house(self, p_gui_obj, p_house_obj, p_key):
        self.m_adding_flag = False
        if g_debug > 2:
            print "gui_house.edit_house() - Name:{0:}, Key:{1:} ".format(p_house_obj.Name, p_key)
        HouseDialog(p_gui_obj, p_house_obj, p_key, "Editing House")

    def save_houses_and_exit(self, p_gui_obj):
        if g_debug > 1:
            print "gui_house.save_houses_and_exit() "
        self.frame_delete(p_gui_obj.ModuleMenuFrame)
        self.show_main_menu(p_gui_obj.MainMenuFrame)


class HouseDialog(HouseWindow):
    """We are working on a single house in this section.
    Display a house dialog with room buttons.

    Add / edit / delete dialog window for a house.

    @param p_parent: is the parent frame for the new dialog frame.
    @param p_key: is the house key value.
    @param p_title: is the title to display on the dialog frame.
    """

    m_house_obj = None

    def __init__(self, p_gui_obj, p_house_obj, p_house_key, p_title = None):
        if g_debug > 0:
            print "gui_house.HouseDialog.__init__() - Show add/edit house dialog", p_house_obj
        p_gui_obj.DialogWindow = Toplevel(p_gui_obj.RootWindow)
        self.m_house_obj = p_house_obj
        self.m_title = p_title
        if p_title:
            p_gui_obj.DialogWindow.title(p_title)
        _l_adding = "normal"
        if p_title.startswith("Edit"):
            _l_adding = 'disabled'
        self.show_house_dialog(p_gui_obj, p_house_obj)

    def show_house_dialog(self, p_gui_obj, p_house_obj):
        p_gui_obj.ModuleDialogFrame = Frame(p_gui_obj.DialogWindow)
        p_gui_obj.ModuleDialogFrame.grid(padx = 5, pady = 5)
        self.create_house_vars()
        self.load_house_vars(p_house_obj)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 1, 'Key', self.Key, state = DISABLED)
        self.get_entry_bol(p_gui_obj.ModuleDialogFrame, 2, 'Active', self.Active)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 3, 'Name', self.Name, width = 50)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 4, 'Street', self.Street, width = 50)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 5, 'City', self.City)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 6, 'State', self.State)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 7, 'Zip Code', self.Zip)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 8, 'Time Zone', self.Timezone)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 9, 'Savings Time', self.SavingTime)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 10, 'Phone', self.Phone)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 11, 'Latitude', self.Latitude)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 12, 'Longitude', self.Longitude)
        l_max = self.show_all_rooms(p_gui_obj, p_house_obj)
        if self.m_title.startswith("Edit"):
            Button(p_gui_obj.ModuleDialogFrame, text = 'Delete House', bg = BG_BOTTOM,
                   command = lambda x = p_gui_obj, y = p_house_obj: self.delete_house(x, y)).grid(row = 91, column = 1)
            Button(p_gui_obj.ModuleDialogFrame, text = 'Update House', fg = "blue", bg = BG_BOTTOM,
                   command = lambda x = p_gui_obj, y = self.m_houses_obj, z = p_house_obj: self.save_house(x, y, z)).grid(row = 91, column = 0)
            Button(p_gui_obj.ModuleDialogFrame, text = 'Add Room', bg = BG_BOTTOM,
                   command = lambda x = p_gui_obj, y = p_house_obj, z = l_max + 1: self.add_room(x, y, z)).grid(row = 91, column = 2)
        else:
            Button(p_gui_obj.ModuleDialogFrame, text = 'Add this House', fg = "blue", bg = BG_BOTTOM,
                   command = lambda x = p_gui_obj, y = self.m_houses_obj, z = p_house_obj: self.add_house_d(x, y, z)).grid(row = 91, column = 0)
        Button(p_gui_obj.ModuleDialogFrame, text = "Cancel", fg = "red", bg = BG_BOTTOM,
               command = lambda x = p_gui_obj: self.quit_house_dialog(x)).grid(row = 91, column = 3)
        pass

    def XXget_house_object(self, p_houses_obj, p_house_key):
        """In case of add - defines the internal house object.
        """
        if g_debug > 3:
            print "gui_house.get_house_object() - Key:{0:}".format(p_house_key)
        try:
            l_obj = p_houses_obj.Object
        except:
            l_obj = HouseData()
            l_obj.Key = p_house_key
            if g_debug >= 1:
                print "gui_house.get_house_object() - Created object ", l_obj
        return l_obj

    def show_all_rooms(self, p_gui_obj, p_house_obj):
        """Display all the rooms in a house on the dialog so they may be edited.

        @param p_house_obj: is the house object with rooms lights schedules ...
        """
        if g_debug >= 9:
            print "gui_house.show_all_rooms() - {0:}".format(p_house_obj.Name)
        l_name = self.Name.get()
        l_frame = Frame(p_gui_obj.ModuleDialogFrame)
        l_ix = 0
        l_max_room_ix = -1
        for l_room_obj in sorted(p_house_obj.Rooms.itervalues(), key = attrgetter('Name')):
            if g_debug >= 5:
                print "gui_house.show_all_rooms() - {0:}".format(l_room_obj.Name)
            if l_room_obj.Key > l_max_room_ix:
                l_max_room_ix = l_room_obj.Key
            if l_room_obj.HouseName != l_name:
                continue
            l_row, l_col = self.columnize(l_ix, 5)
            Button(l_frame, text = l_room_obj.Name, bg = BG_TOP,
                   command = lambda x = p_gui_obj, y = p_house_obj, z = l_room_obj.Key: self.edit_room(x, y, z)).grid(row = l_row, column = l_col)
            l_ix += 1
        l_frame.grid(row = 31, column = 0, columnspan = 3)
        return l_max_room_ix

    def add_house_d(self, p_gui_obj, p_houses_obj, p_house_obj):
        """Merge the location(in vars) into the house
        Create new entry in houses and restart PyHouse
        TODO: add a house
        """
        if g_debug >= 3:
            print "gui_house.add_house_d() - Adding new house with Key:{0:} into {1:}".format(p_house_obj.Key, p_houses_obj)

        l_house_obj = self.save_house_vars(p_house_obj)
        p_houses_obj[p_house_obj.Key] = HousesData()
        p_houses_obj[p_house_obj.Key].Name = p_house_obj.Name
        p_houses_obj[p_house_obj.Key].Key = p_house_obj.Key
        p_houses_obj[p_house_obj.Key].Object = l_house_obj
        p_houses_obj[p_house_obj.Key].HouseAPI = None
        self.m_houses_dict = p_houses_obj
        if g_debug >= 3:
            print "gui_house.add_house_d() - Name:{0:}, Key:{1:}".format(l_house_obj.Name, l_house_obj.Key), p_houses_obj
        self.quit_house_dialog(p_gui_obj)

    def delete_house(self, p_gui_obj, p_house_obj):
        l_key = p_house_obj.Key
        if g_debug > 2:
            print "gui_house.delete_house() #", l_key
        del self.m_houses_dict[l_key]
        self.quit_house_dialog(p_gui_obj)

    def save_house(self, p_gui_obj, p_houses_obj, p_house_obj):
        """Merge the location(in vars) into the house
        """
        l_house_obj = self.save_house_vars(p_house_obj)
        p_houses_obj[l_house_obj.Key].Object = l_house_obj
        if g_debug >= 2:
            print "gui_house.save_house() - Name:{0:}, Key:{1:}".format(l_house_obj.Name, l_house_obj.Key)
        self.quit_house_dialog(p_gui_obj)

    def add_room(self, p_gui_obj, p_house_obj, p_room_key):
        if g_debug >= 2:
            print "gui_house.add_room() #", p_room_key, p_house_obj
        RoomDialog(p_gui_obj, p_house_obj, p_room_key, "Adding Room")

    def edit_room(self, p_gui_obj, p_house_obj, p_room_key):
        if g_debug >= 2:
            print "gui_house.edit_room() # ", p_room_key
        RoomDialog(p_gui_obj, p_house_obj, p_room_key, "Editing Room")

    def quit_house_dialog(self, p_gui_obj):
        if g_debug >= 2:
            print "gui_house.quit_house_dialog() # ", self.m_houses_dict
        p_gui_obj.DialogWindow.destroy()
        p_gui_obj.ModuleMenuFrame.destroy()
        self.show_all_houses(p_gui_obj)

    def create_house_vars(self):
        self.Active = IntVar()
        self.Key = IntVar()
        self.Name = StringVar()
        #
        self.Street = StringVar()
        self.City = StringVar()
        self.State = StringVar()
        self.Zip = StringVar()
        self.Timezone = StringVar()
        self.SavingTime = StringVar()
        self.Phone = StringVar()
        self.Latitude = DoubleVar()
        self.Longitude = DoubleVar()

    def load_house_vars(self, p_house_obj):
        """Load the variables for a given house.

        @param p_house_obj: is the house object in House_Data.
        """
        self.Active.set(self.get_bool(p_house_obj.Active))
        self.Key.set(p_house_obj.Key)
        self.HouseName = p_house_obj.Name
        self.Name.set(p_house_obj.Name)
        #
        l_location_obj = p_house_obj.Location
        if g_debug >= 3:
            print "gui_house.load_house_vars() ", l_location_obj
        self.Street.set(l_location_obj.Street)
        self.City.set(l_location_obj.City)
        self.State.set(l_location_obj.State)
        self.Zip.set(l_location_obj.ZipCode)
        self.Timezone.set(l_location_obj.TimeZone)
        self.SavingTime.set(l_location_obj.SavingTime)
        self.Phone.set(l_location_obj.Phone)
        self.Latitude.set(l_location_obj.Latitude)
        self.Longitude.set(l_location_obj.Longitude)

    def save_house_vars(self, p_house_obj):
        """Get the on screen vars and save them in the original house object.
        This will preserve the rest of the information.
        """
        p_house_obj.Active = self.Active.get()
        p_house_obj.Key = self.Key.get()
        p_house_obj.Name = self.Name.get()
        p_house_obj.Location = house.LocationData()
        p_house_obj.Location.Street = self.Street.get()
        p_house_obj.Location.City = self.City.get()
        p_house_obj.Location.State = self.State.get()
        p_house_obj.Location.ZipCode = self.Zip.get()
        p_house_obj.Location.TimeZone = self.Timezone.get()
        p_house_obj.Location.SavingTime = self.SavingTime.get()
        p_house_obj.Location.Phone = self.Phone.get()
        p_house_obj.Location.Latitude = self.Latitude.get()
        p_house_obj.Location.Longitude = self.Longitude.get()
        return p_house_obj

class RoomDialog(HouseDialog):
    """
    Add / edit / delete dialog window for a room.
    """

    def __init__(self, p_gui_obj, p_house_obj, p_room_key, p_title = None):
        """

        @param p_parent: is the parent frame that this dialog comes from.
        @param p_room_key: is the room key(index)
        @param p_house_name: is the name of the house
        @param p_title: is the title of the dialog to be shown.
        """
        if g_debug >= 2:
            print "gui_house.RoomDialog.__init__()", p_house_obj
        p_gui_obj.SecondDialogWindow = Toplevel(p_gui_obj.RootWindow)
        if p_title:
            p_gui_obj.SecondDialogWindow.title(p_title)
        self.l_result = None
        self.create_room_vars()
        self.load_room_vars(p_house_obj, p_room_key)
        p_gui_obj.SecondDialogFrame = Frame(p_gui_obj.SecondDialogWindow)
        p_gui_obj.SecondDialogFrame.grid(padx = 5, pady = 5)
        self.get_entry_str(p_gui_obj.SecondDialogFrame, 1, 'Key', self.Key, state = DISABLED)
        self.get_entry_bol(p_gui_obj.SecondDialogFrame, 2, 'Active', self.Active)
        self.get_entry_str(p_gui_obj.SecondDialogFrame, 3, 'Name', self.Name, width = 50)
        self.get_entry_str(p_gui_obj.SecondDialogFrame, 4, 'Comment', self.Comment, width = 50)
        self.get_entry_str(p_gui_obj.SecondDialogFrame, 5, 'Size', self.Size)
        self.get_entry_str(p_gui_obj.SecondDialogFrame, 6, 'Corner', self.Corner)
        self.get_entry_str(p_gui_obj.SecondDialogFrame, 7, 'House Name', self.HouseName, state = DISABLED)
        l_text = "Add"
        if p_title.startswith("Edit"):
            l_text = "Save"
            self.get_entry_btn(p_gui_obj.SecondDialogFrame, 91, 1, 'Delete',
                    lambda x = p_gui_obj, y = p_house_obj, z = p_room_key: self.delete_room(x, y, z), bg = BG_BOTTOM)
        self.get_entry_btn(p_gui_obj.SecondDialogFrame, 91, 0, l_text,
                    lambda x = p_gui_obj, y = p_house_obj: self.add_save_room(x, y), fg = "blue", bg = BG_BOTTOM)
        self.get_entry_btn(p_gui_obj.SecondDialogFrame, 91, 2, "Cancel",
                    lambda x = p_gui_obj, y = p_house_obj: self.quit_room_dialog(x, y), fg = "red", bg = BG_BOTTOM)

    def delete_room(self, p_gui_obj, p_house_obj, p_room_key):
        del p_house_obj.Rooms[p_room_key]
        self.quit_room_dialog(p_gui_obj, p_house_obj)

    def add_save_room(self, p_gui_obj, p_house_obj):
        """store the new or edited room.
        """
        if g_debug >= 2:
            print "gui_house.add_save_room()", p_house_obj
        l_obj = self.save_room_vars()
        p_house_obj.Rooms[l_obj.Key] = l_obj
        self.quit_room_dialog(p_gui_obj, p_house_obj)

    def quit_room_dialog(self, p_gui_obj, p_house_obj):
        """Close the room dialog and re-show the updated house dialog.
        """
        if g_debug >= 2:
            print "gui_house.quit_room_dialog()", p_house_obj
        p_gui_obj.SecondDialogWindow.destroy()
        self.show_house_dialog(p_gui_obj, p_house_obj)

    def get_room_obj(self, p_house_obj, p_room_key):
        """Allow new room to be added
        """
        try:
            l_room_obj = p_house_obj.Rooms[p_room_key]
        except KeyError:
            l_room_obj = house.RoomData()
            l_room_obj.Key = p_room_key
            l_room_obj.HouseName = p_house_obj.Name
        return l_room_obj

    def create_room_vars(self):
        self.Active = IntVar()
        self.Comment = StringVar()
        self.Corner = StringVar()
        self.HouseName = StringVar()
        self.Key = IntVar()
        self.Name = StringVar()
        self.Size = StringVar()

    def load_room_vars(self, p_house_obj, p_room_key):
        l_room_obj = self.get_room_obj(p_house_obj, p_room_key)
        self.Active.set(l_room_obj.Active)
        self.Comment.set(l_room_obj.Comment)
        self.Corner.set(l_room_obj.Corner)
        self.HouseName.set(p_house_obj.Name)
        self.Key.set(l_room_obj.Key)
        self.Name.set(l_room_obj.Name)
        self.Size.set(l_room_obj.Size)

    def save_room_vars(self):
        l_obj = house.RoomData()
        l_obj.Active = self.Active.get()
        l_obj.Comment = self.Comment.get()
        l_obj.Corner = self.Corner.get()
        l_obj.HouseName = self.HouseName.get()
        l_obj.Key = self.Key.get()
        l_obj.Name = self.Name.get()
        l_obj.Size = self.Size.get()
        return l_obj

# ## END
