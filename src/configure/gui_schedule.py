#!/usr/bin/env python

from operator import attrgetter
from Tkinter import Frame, Toplevel, Button, IntVar, StringVar, W, DISABLED, SUNKEN, RAISED

from configure.gui_tools import GuiTools, BG_BOTTOM, BG_INACTIVE, FG_INACTIVE
from scheduling import schedule
from housing import house
from utils import tools

g_debug = 0

House_Data = house.House_Data

VAL_TYPES = schedule.VALID_TYPES


class ScheduleWindow(GuiTools):

    m_gui_obj = None
    m_ix = 0

    def __init__(self, p_gui_obj, p_houses_obj):
        """Initialize then bring up the 'select house' menu.

        @param p_root_window: is the parent TkInter Frame.
        @param p_main_frame: is ?
        """
        if g_debug > 0:
            print "gui_schedule - Show select house window"
        self.m_gui_obj = p_gui_obj
        self.show_house_select_window(p_gui_obj, p_houses_obj)

    def show_buttons_for_one_house(self, p_gui_obj, p_house_obj):
        """Display the schedule menu with the schedule buttons for the selected house.

        This is a callback from gui_tools house select window

        @param p_house_obj: is the house object of the selected house.
        """
        self.m_gui_obj = p_gui_obj
        if g_debug > 1:
            print "gui_schedule.show_buttons_for_one_house() - House:{0:}".format(p_house_obj.Name)
        self.frame_delete(p_gui_obj.HouseSelectFrame)
        self.frame_delete(p_gui_obj.ModuleMenuFrame)
        p_gui_obj.ModuleMenuFrame = Frame(self.m_gui_obj.RootWindow)
        p_gui_obj.ModuleMenuFrame.grid(padx = 5, pady = 5)
        p_gui_obj.RootWindow.title('Add / Edit Schedule')
        self.m_ix = 0
        l_max = self.show_schedule_buttons(p_gui_obj, p_house_obj)
        Button(p_gui_obj.ModuleMenuFrame, text = "ADD Schedule", bg = BG_BOTTOM,
               command = lambda x = p_gui_obj, y = p_house_obj, z = l_max + 1: self.add_schedule(x, y, z)).grid(row = self.m_ix, column = 0)
        Button(p_gui_obj.ModuleMenuFrame, text = "Back", fg = "red", bg = BG_BOTTOM,
               command = lambda x = p_gui_obj: self.save_schedules_and_exit(x)).grid(row = self.m_ix, column = 1)

    def show_schedule_buttons(self, p_gui_obj, p_house_obj):
        """Display one button for each schedule of the selected house.
        Buttons are sorted by 3 variables

        @param p_house_obj: is one House_Data object (see house.py).
        """
        if g_debug > 0:
            print "gui_schedule.show_schedule_buttons() - Show select schedule window buttons"
            print "   Sched = ", p_house_obj.Schedule
        self.m_house_obj = p_house_obj
        l_sched = []
        l_lights = sorted(p_house_obj.Schedule.values(), key = attrgetter('LightName'))  # last sort
        l_rooms = sorted(l_lights, key = attrgetter('RoomName'))  # moddle sort
        l_scheds = sorted(l_rooms, key = attrgetter('Name'))  # first sort
        l_max = 0
        for l_sched_obj in l_scheds:
            if l_sched_obj.Key > l_max:
                l_max = l_sched_obj.Key
            l_relief = SUNKEN
            l_bg = BG_INACTIVE
            l_fg = FG_INACTIVE
            if l_sched_obj.Active:
                l_relief = RAISED
                l_bg, l_fg = self.color_button(int(l_sched_obj.Level))
            l_row, l_col = self.columnize(self.m_ix, 4)
            l_caption = str(l_sched_obj.Name) + ' ' + str(l_sched_obj.RoomName) + ' ' + str(l_sched_obj.LightName)
            l = Button(p_gui_obj.ModuleMenuFrame, text = l_caption, bg = l_bg, fg = l_fg, relief = l_relief,
                       command = lambda x = p_gui_obj, y = p_house_obj, z = l_sched_obj.Key: self.edit_schedule(x, y, z))
            l_sched.append(l)
            l_sched[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1
        return l_max

    def edit_schedule(self, p_gui_obj, p_house_obj, p_schedule_key):
        """
        Callback from clicking on a schedule button.
        @param p_house_obj: is the house object that we are editing.
        @param p_schedule_key: is the schedule id we are about to edit.
        """
        if g_debug > 1:
            print "gui_schedule.edit_schedule()  House:{0:}, SchedKey:{1:}".format(p_house_obj.Name, p_schedule_key)
        ScheduleDialog(p_gui_obj, p_house_obj, int(p_schedule_key), "Editing Schedule")

    def add_schedule(self, p_gui_obj, p_house_obj, p_ix):
        """
        """
        if g_debug > 1:
            print "gui_schedule.add_schedule() ", p_house_obj
        ScheduleDialog(p_gui_obj, p_house_obj, p_ix, "Adding Schedule")

    def save_schedules_and_exit(self, p_gui_obj):
        """callback to 'Back' button
        """
        if g_debug > 1:
            print "gui_schedule.save_schedules_and_exit() "
        self.frame_delete(p_gui_obj.ModuleMenuFrame)
        self.show_main_menu(p_gui_obj)


class ScheduleDialog(ScheduleWindow):
    """Display a schedule dialog window.

    Allow add of new schedule or change or delete of existing schedule.
    """

    def __init__(self, p_gui_obj, p_house_obj, p_schedule_key, p_title):
        """
        @param p_root_window: is ?
        @param p_parent_window: is the frame holding the schedule buttons
        @param p_schedule_key: is the schedule id we are about to edit.
        @param p_house_obj: is the house object that we are editing.
        """
        p_gui_obj.DialogWindow = Toplevel(p_gui_obj.RootWindow)
        if g_debug > 0:
            print "gui_schedule.ScheduleDialog.__init__() - Show add/edit schedule window  House{0:}, SchedKey:{1:}".format(p_house_obj.Name, p_schedule_key)
        p_gui_obj.DialogWindow.title(p_title)
        self.l_result = None
        self.create_schedule_vars()
        self.load_schedule_vars(p_schedule_key, p_house_obj)
        #
        p_gui_obj.ModuleDialogFrame = Frame(p_gui_obj.DialogWindow)
        p_gui_obj.ModuleDialogFrame.grid_columnconfigure(0, minsize = 120)
        p_gui_obj.ModuleDialogFrame.grid_columnconfigure(1, minsize = 300)
        p_gui_obj.ModuleDialogFrame.grid(padx = 5, pady = 5)
        #
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 1, 'Key', self.Key, state = DISABLED)
        self.get_entry_bol(p_gui_obj.ModuleDialogFrame, 2, 'Active', self.Active)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 3, 'Name', self.Name)
        #self.get_entry_str(p_gui_obj.ModuleDialogFrame, 4, 'House Name', self.HouseName, state = DISABLED)
        self.get_entry_pdb(p_gui_obj.ModuleDialogFrame, 5, 'Room Name', self.RoomName, self.build_names(p_house_obj.Rooms), self.RoomName, self.get_roomname)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 6, 'Time', self.Time)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 7, 'Level', self.Level)
        self.get_entry_str(p_gui_obj.ModuleDialogFrame, 8, 'Rate', self.Rate)
        self.get_entry_pdb(p_gui_obj.ModuleDialogFrame, 9, 'Type', self.Type, VAL_TYPES, self.Type, self.get_type)
        self.get_entry_pdb(p_gui_obj.ModuleDialogFrame, 10, 'Light Name', self.LightName, self.build_names(p_house_obj.Lights), self.LightName, self.get_lightname)
        l_text = "Add"
        if p_title.startswith("Edit"):
            l_text = "Save"
            Button(p_gui_obj.ModuleDialogFrame, text = 'Delete', bg = BG_BOTTOM,
                   command = lambda x = p_gui_obj, y = p_house_obj, z = p_schedule_key: self.delete_schedule(x, y, z)).grid(row = 91, column = 1)
        l_as = Button(p_gui_obj.ModuleDialogFrame, text = l_text, fg = "blue", bg = BG_BOTTOM,
                      command = lambda x = p_gui_obj, y = p_house_obj: self.save_schedule_vars(x, y))
        l_as.grid(row = 91, column = 0)
        l_as.focus_set()
        Button(p_gui_obj.ModuleDialogFrame, text = "Cancel", fg = "red", bg = BG_BOTTOM,
               command = lambda x = p_gui_obj, y = p_house_obj: self.quit_dialog(x, y)).grid(row = 91, column = 2)

    def create_schedule_vars(self):
        """Create all the TkInter variables for a single schedule.
        """
        self.Active = IntVar()
        self.HouseName = StringVar()
        self.Key = IntVar()
        self.Level = IntVar()
        self.LightName = StringVar()
        self.Name = StringVar()
        self.Rate = IntVar()
        self.RoomName = StringVar()
        self.Time = StringVar()
        self.Type = StringVar()

    def load_schedule_vars(self, p_schedule_key, p_house_obj):
        """Get the data to show in the Add/Edit dialog box

        @param p_schedule_key: is the schedule id we are about to edit.
        @param p_house_obj: is the house object that we are editing.
        """
        if g_debug > 1:
            print "gui_schedule.load_schedule_vars() - Key:{0:}".format(p_schedule_key)
        l_obj = p_house_obj.Schedule[int(p_schedule_key)]
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

    def save_schedule_vars(self, p_gui_obj, p_house_obj):
        """Called on either Add or Save.

        @param p_house_obj: is the house object that we are editing.
        """
        if g_debug > 1:
            print "gui_schedule.save_schedule_vars() "
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
            print "gui_schedule.save_schedule_vars() Saving schedule data ", l_obj
        self.quit_dialog(p_gui_obj, p_house_obj)

    def delete_schedule(self, p_gui_obj, p_house_obj, p_schedule_key):
        """
        """
        del p_house_obj.Schedules[p_schedule_key]
        self.quit_dialog(p_gui_obj, p_house_obj)

    def quit_dialog(self, p_gui_obj, p_house_obj):
        """Remove the dialog box and return to the schedule window.
        """
        if g_debug > 0:
            print "gui_schedule.quit_dialog()", p_gui_obj
        p_gui_obj.DialogWindow.destroy()
        p_gui_obj.ModuleDialogFrame.destroy()
        self.show_buttons_for_one_house(p_gui_obj, p_house_obj)

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
