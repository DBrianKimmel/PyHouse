#!/usr/bin/env python

from operator import attrgetter
from Tkinter import Frame, Toplevel, Button, IntVar, StringVar, W, DISABLED, SUNKEN, RAISED

import gui_tools
from schedule import schedule
from main import houses
from house import house
from main import tools

g_debug = 5

House_Data = house.House_Data
Houses_Data = houses.Houses_Data

VAL_TYPES = schedule.VALID_TYPES


class ScheduleWindow(gui_tools.GuiTools):

    m_house_module = None

    def __init__(self, p_root, p_main_window):
        """Initialize then bring up the 'select house' menu.

        @param p_root: is the parent TkInter Frame.
        @param p_main_frame: is ?
        """
        if g_debug > 0:
            print "gui_schedule - Show select house window"
        self.m_root = p_root
        self.main_window = p_main_window
        self.m_house_select_window = self.show_house_select_window(p_root, p_main_window)

    def show_buttons_for_one_house(self, p_ix, p_house_obj):
        """Display the schedule menu with the schedule buttons for the selected house.

        This is a callback from gui_tools house select window

        @param p_ix: is the index of the house in Houses_Data
        @param p_house_obj: is one House_Data object (see house.py).
        """
        if g_debug > 1:
            print "gui_schedule.show_buttons_for_one_house() - Ix:{0:}".format(p_ix), p_house_obj
        self.m_ix = p_ix
        self.frame_delete(self.m_house_select_window)
        self.m_schedule_select_window = Frame(self.m_root)
        self.m_root.title('Add / Edit Schedule')
        self.m_schedule_select_window.grid(padx = 5, pady = 5)
        self.m_ix = 0
        self.show_schedule_button(p_ix, p_house_obj)
        Button(self.m_schedule_select_window, text = "ADD Schedule", bg = gui_tools.BG_BOTTOM,
               command = lambda x = p_house_obj: self.add_schedule(x)).grid(row = self.m_ix, column = 0)
        Button(self.m_schedule_select_window, text = "Back", fg = "red", bg = gui_tools.BG_BOTTOM,
               command = self.save_schedules_and_exit).grid(row = self.m_ix, column = 1)

    def show_schedule_button(self, p_ix, p_house_obj):
        """Display one button for each schedule of the selected house.

        @param p_ix: is the index of the house in Houses_Data
        @param p_house_obj: is one House_Data object (see house.py).
        """
        if g_debug > 0:
            print "gui_schedule.show_schedule_button() - Show select schedule window  House_ix:{0:}".format(p_ix), p_house_obj
        l_sched = []
        for l_sched_obj in sorted(p_house_obj.Schedule.itervalues(), key = attrgetter('Name')):
            if l_sched_obj.HouseName != p_house_obj.Name:
                continue
            l_relief = SUNKEN
            if l_sched_obj.Active:
                l_relief = RAISED
            l_bg, l_fg = self.color_button(int(l_sched_obj.Level))
            l_row, l_col = self.get_grid(self.m_ix)
            l_caption = str(l_sched_obj.Name) + ' ' + str(l_sched_obj.RoomName) + ' ' + str(l_sched_obj.LightName)
            l = Button(self.m_schedule_select_window, text = l_caption, bg = l_bg, fg = l_fg, relief = l_relief,
                       command = lambda x = l_sched_obj.Key, y = p_house_obj: self.edit_schedule(x, y))
            l_sched.append(l)
            l_sched[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1

    def edit_schedule(self, p_key, p_house_obj):
        """
        Callback from clicking on a schedule button.

        @param p_key: is the schedule id we are about to edit.
        @param p_house_obj: is the house object that we are editing.
        """
        if g_debug > 1:
            print "gui_schedule.edit_schedule()  House:{0:}, SchedKey:{1:}".format(p_house_obj.Name, p_key)
        ScheduleDialog(self.m_root, self.m_schedule_select_window, int(p_key), p_house_obj, "Editing Schedule", p_house_obj.Key)

    def add_schedule(self, p_house_obj):
        """
        TODO: will need a house index for calling back menu
        """
        if g_debug > 1:
            print "gui_schedule.add_schedule() ", p_house_obj
        ScheduleDialog(self.m_root, self.m_schedule_select_window, self.m_ix, p_house_obj, "Adding Schedule", self.m_ix)
        self.show_buttons_for_one_house(p_house_obj)

    def save_schedules_and_exit(self):
        """
        """
        if g_debug > 1:
            print "gui_schedule.save_schedules_and_exit() "
        houses.API().save_all_houses()
        self.frame_delete(self.m_schedule_select_window)
        self.show_main_menu()



class ScheduleDialog(ScheduleWindow):
    """Display a schedule dialog window.

    Allow add of new schedule or change or delete of existing schedule.
    """

    m_sched_window = None
    m_top = None
    m_house_module = None

    def __init__(self, p_root, p_parent_window, p_key, p_house_obj, p_title, p_ix):
        """
        @param p_root: is ?
        @param p_parent_window: is the frame holding the schedule buttons
        @param p_key: is the schedule id we are about to edit.
        @param p_house_obj: is the house object that we are editing.
        """
        if g_debug > 0:
            print "gui_schedule.ScheduleDialog.__init__() - Show add/edit schedule window   House{0:}, SchedKey:{1:}, House_ix:{2:}".format(p_house_obj.Name, p_key, p_ix)
        self.m_house_module = Houses_Data[p_ix].HouseAPI
        self.m_root = p_root
        self.m_top = Toplevel()
        if p_title:
            self.m_top.title(p_title)
        self.m_parent_window = p_parent_window
        # self.m_parent_window.withdraw()
        self.l_result = None
        self.create_vars()
        self.load_vars(p_key, p_house_obj)
        #
        self.m_sched_window = Frame(self.m_top)
        self.m_sched_window.grid_columnconfigure(0, minsize = 120)
        self.m_sched_window.grid_columnconfigure(1, minsize = 300)
        self.m_sched_window.grid(padx = 5, pady = 5)
        #
        self.get_entry_str(self.m_sched_window, 1, 'Key', self.Key, state = DISABLED)
        self.get_entry_bol(self.m_sched_window, 2, 'Active', self.Active)
        self.get_entry_str(self.m_sched_window, 3, 'Name', self.Name)
        self.get_entry_str(self.m_sched_window, 4, 'House Name', self.HouseName, state = DISABLED)
        self.get_entry_pdb(self.m_sched_window, 5, 'Room Name', self.RoomName, self.build_names(p_house_obj.Rooms), self.RoomName, self.get_roomname)
        self.get_entry_str(self.m_sched_window, 6, 'Time', self.Time)
        self.get_entry_str(self.m_sched_window, 7, 'Level', self.Level)
        self.get_entry_str(self.m_sched_window, 8, 'Rate', self.Rate)
        self.get_entry_pdb(self.m_sched_window, 9, 'Type', self.Type, VAL_TYPES, self.Type, self.get_type)
        self.get_entry_pdb(self.m_sched_window, 10, 'Light Name', self.LightName, self.build_names(p_house_obj.Lights), self.LightName, self.get_lightname)
        l_text = "Add"
        if p_title.startswith("Edit"):
            l_text = "Save"
            Button(self.m_sched_window, text = 'Delete', bg = gui_tools.BG_BOTTOM, command = self.delete_schedule).grid(row = 91, column = 1)
        l_as = Button(self.m_sched_window, text = l_text, fg = "blue", bg = gui_tools.BG_BOTTOM, command = lambda x = p_house_obj: self.save_vars(x))
        l_as.grid(row = 91, column = 0)
        l_as.focus_set()
        # self.m_sched_window.bind("<Return>", self.save_vars)
        Button(self.m_sched_window, text = "Cancel", fg = "red", bg = gui_tools.BG_BOTTOM,
               command = self.quit_dialog).grid(row = 91, column = 2)

    def create_vars(self):
        """Create all the TkInter variables for a single schedule.
        """
        self.Active = IntVar()
        self.HouseName = StringVar()
        self.Key = IntVar()
        self.Level = IntVar()
        self.LightName = StringVar()
        # self.LightNumber = IntVar()
        self.Name = StringVar()
        self.Rate = IntVar()
        self.RoomName = StringVar()
        self.Time = StringVar()
        self.Type = StringVar()

    def load_vars(self, p_key, p_house_obj):
        """Get the data to show in the Add/Edit dialog box

        @param p_key: is the schedule id we are about to edit.
        @param p_house_obj: is the house object that we are editing.
        """
        if g_debug > 1:
            print "gui_schedule.load_vars() - Key:{0:}".format(p_key), p_house_obj
        l_obj = p_house_obj.Schedule[int(p_key)]
        self.Active.set(self.get_bool(l_obj.Active))
        self.HouseName.set(l_obj.HouseName)
        self.Key.set(l_obj.Key)
        self.Level.set(l_obj.Level)
        self.LightName.set(l_obj.LightName)
        self.Name.set(l_obj.Name)
        self.Rate.set(l_obj.Rate)
        self.RoomName.set(l_obj.RoomName)
        self.Time.set(l_obj.Time)
        self.Type.set(l_obj.Type)

    def save_vars(self, p_house_obj):
        """Called on either Add or Save.

        @param p_house_obj: is the house object that we are editing.
        """
        if g_debug > 1:
            print "gui_schedule.save_vars() ", p_house_obj  # , self.m_house_module
        l_obj = schedule.ScheduleData()
        l_obj.Active = self.Active.get()
        l_obj.HouseName = self.HouseName.get()
        l_obj.Key = self.Key.get()
        l_obj.Level = self.Level.get()
        l_obj.LightName = self.LightName.get()
        l_obj.LightNumber = tools.get_light_object(p_house_obj, name = l_obj.LightName).Key
        l_obj.Name = self.Name.get()
        l_obj.Object = {}
        l_obj.Rate = self.Rate.get()
        l_obj.RoomName = self.RoomName.get()
        l_obj.Time = self.Time.get()
        l_obj.Type = self.Type.get()
        p_house_obj.Schedule[l_obj.Key] = l_obj  # update schedule entry within a house
        if g_debug > 1:
            print "gui_schedule.save_vars() Saving schedule data ", l_obj
        self.quit_dialog()

    def delete_schedule(self):
        """
        TODO: Implement this
        """
        pass

    def quit_dialog(self):
        """Remove the dialog box and return to the schedule window.
        """
        if g_debug > 0:
            print "gui_schedule.quit_dialog()"
        self.m_top.destroy()
        # self.m_root.grid()

        self.m_parent_window.update()
        # self.m_parent_window.deiconify()

    def get_housename(self, p_val):
        self.HouseName.set(p_val)
        if g_debug > 0:
            print "gui_schedule.get_housename() - ", p_val
            for l_obj in House_Data.itervalues():
                if l_obj.Name == p_val:
                    for l_rm in l_obj.Rooms.itervalues():
                        print l_rm.Name, ' ',
                    print

    def get_lightname(self, p_val):
        if g_debug > 0:
            print "gui_schedule.get_lightname() - ", p_val
        self.LightName.set(p_val)
        self.LightNumber = 1

    def get_roomname(self, p_val):
        if g_debug > 0:
            print "gui_schedule.get_roomname() - ", p_val
        self.RoomName.set(p_val)

    def get_type(self, p_val):
        self.Type.set(p_val)
        if g_debug > 0:
            print "gui_schedule.gettype() - ", p_val

# ## END
