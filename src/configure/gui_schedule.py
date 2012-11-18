#!/usr/bin/env python

from Tkinter import Frame, Label, Entry, Toplevel, Button, IntVar, StringVar, W, E, DISABLED, SUNKEN, RAISED
import Pmw

# import gui
import gui_tools
import house
import lighting.lighting as lighting
import schedule.schedule as schedule
import config_xml
# from src.schedule.schedule import Schedule_Data, ScheduleData


g_debug = 1
VAL_TYPES = schedule.VALID_TYPES
Schedule_Data = schedule.Schedule_Data
Light_Data = lighting.Light_Data
House_Data = house.House_Data
Location_Data = house.Location_Data
Room_Data = house.Room_Data

class ScheduleWindow(gui_tools.GuiTools):
    """Display a schedule selection window.
    """

    def __init__(self, p_root, p_main_frame = None):
        self.m_root = p_root
        self.m_main_frame = p_main_frame
        self.m_sched_frame = Frame(p_root)
        self.m_sched_frame.grid(padx = 5, pady = 5)
        self.m_ix = 0
        self.show_all_schedules()
        Button(self.m_sched_frame, text = "ADD Schedule", bg = gui_tools.BG_BOTTOM, command = self.add_schedule).grid(row = self.m_ix, column = 0)
        Button(self.m_sched_frame, text = "Back", fg = "red", bg = gui_tools.BG_BOTTOM, command = self.main_screen).grid(row = self.m_ix, column = 1)

    def show_all_schedules(self):
        l_sched = []
        for l_obj in Schedule_Data.itervalues():
            l_relief = SUNKEN
            if l_obj.Active: l_relief = RAISED
            l_bg, l_fg = self.color_button(int(l_obj.Level))
            l_row, l_col = self.get_grid(self.m_ix)
            l = Button(self.m_sched_frame, text = l_obj.Name + ' ' + l_obj.LightName,
                       bg = l_bg, fg = l_fg, relief = l_relief,
                       command = lambda x = l_obj.Key: self.edit_schedule(x))
            l_sched.append(l)
            l_sched[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1

    def edit_schedule(self, p_key):
        ScheduleDialog(self.m_root, self.m_sched_frame, p_key, "Editing Schedule")
        self.save_schedule()

    def add_schedule(self):
        ScheduleDialog(self.m_root, self.m_sched_frame, self.m_ix + 1, "Adding Schedule")
        self.save_schedule()

    def save_schedule(self):
        config_xml.WriteConfig().write_schedules()
        self.main_screen()

    def main_screen(self):
        """Exit the schedule screen.
        """
        self.frame_delete(self.m_sched_frame)
        self.m_main_frame.grid()

    def color_button(self, p_level):
        l_bg = '#FFFFD0'  # Very Light yellow - full on
        l_fg = 'black'
        if p_level < 10:  # Dark
            l_bg = '#505010'
            l_fg = 'white'
        elif p_level <= 40:  # Dark Yellow
            l_bg = '#707030'
            l_fg = 'white'
        elif p_level <= 60:  # Dark Yellow
            l_bg = '#909050'
            l_fg = 'white'
        elif p_level <= 80:  # Dark Yellow
            l_bg = '#B0B070'
        elif p_level < 90:  # Medium Yellow
            l_bg = '#D0D080'
        return l_bg, l_fg

    def get_grid(self, p_count):
            l_row = p_count // 4
            l_col = p_count % 4
            return l_row, l_col


class ScheduleDialog(gui_tools.GuiTools):
    """Display a schedule dialog window.

    Allow add of new schedule or change or delete of existing schedule.
    """

    m_frame = None
    m_top = None

    def __init__(self, p_root, p_parent, p_key, p_title):
        self.m_root = p_root
        self.m_top = Toplevel()
        if p_title:
            self.m_top.title(p_title)
        self.m_parent = p_parent
        self.l_result = None
        self.create_vars()
        self.load_vars(p_key)
        #
        self.m_frame = Frame(self.m_top)
        self.m_frame.grid_columnconfigure(0, minsize = 120)
        self.m_frame.grid_columnconfigure(1, minsize = 300)
        self.m_frame.grid(padx = 5, pady = 5)
        #
        self.get_entry_str(self.m_frame, 1, 'Key', self.Key, state = DISABLED)
        self.get_entry_bol(self.m_frame, 2, 'Active', self.Active)
        self.get_entry_str(self.m_frame, 3, 'Name', self.Name)
        self.get_entry_pdb(self.m_frame, 4, 'House Name', self.HouseName, self.build_names(Location_Data), self.HouseName, self.get_housename)
        self.get_entry_pdb(self.m_frame, 5, 'Room Name', self.RoomName, self.build_names(Room_Data), self.RoomName, self.get_roomname)
        self.get_entry_str(self.m_frame, 6, 'Time', self.Time)
        self.get_entry_str(self.m_frame, 7, 'Level', self.Level)
        self.get_entry_str(self.m_frame, 8, 'Rate', self.Rate)
        self.get_entry_pdb(self.m_frame, 9, 'Type', self.Type, VAL_TYPES, self.Type, self.get_type)
        self.get_entry_pdb(self.m_frame, 10, 'Light Name', self.LightName, self.build_names(Light_Data), self.LightName, self.get_lightname)
        l_text = "Add"
        if p_title.startswith("Edit"):
            l_text = "Save"
            Button(self.m_frame, text = 'Delete', bg = gui_tools.BG_BOTTOM, command = self.delete_schedule).grid(row = 91, column = 1)
        Button(self.m_frame, text = l_text, fg = "blue", bg = gui_tools.BG_BOTTOM, command = self.get_vars).grid(row = 91, column = 0)
        Button(self.m_frame, text = "Cancel", fg = "red", bg = gui_tools.BG_BOTTOM, command = self.quit_dialog).grid(row = 91, column = 2)

    def create_vars(self):
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

    def load_vars(self, p_key):
        try:
            l_obj = Schedule_Data[p_key]
        except:
            l_obj = schedule.ScheduleData()
            l_obj.Key = p_key
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

    def get_vars(self):
        """Called on either Add or Save.
        """
        l_obj = schedule.ScheduleData()
        l_obj.Active = self.Active.get()
        l_obj.HouseName = self.HouseName.get()
        l_obj.Key = self.Key.get()
        l_obj.Level = self.Level.get()
        l_obj.LightName = self.LightName.get()
        l_obj.Name = self.Name.get()
        l_obj.Rate = self.Rate.get()
        l_obj.RoomName = self.RoomName.get()
        l_obj.Time = self.Time.get()
        l_obj.Type = self.Type.get()
        Schedule_Data[l_obj.Key] = l_obj
        print "Saving schedule data ", l_obj
        config_xml.WriteConfig().write_schedules()
        self.quit_dialog()

    def delete_schedule(self):
        pass

    def quit_dialog(self):
        """Remove the dialog box and return to the schedule window.
        """
        self.m_top.destroy()
        self.m_root.grid()

    def build_names(self, p_dict):
        l_ret = []
        for l_obj in p_dict.itervalues():
            l_ret.append(l_obj.Name)
        return l_ret

    def get_housename(self, p_val):
        self.HouseName.set(p_val)
        if g_debug > 0: print "get house name - ", p_val

    def get_lightname(self, p_val):
        self.LightName.set(p_val)
        if g_debug > 0: print "get light name - ", p_val

    def get_roomname(self, p_val):
        self.RoomName.set(p_val)
        if g_debug > 0: print "get room name - ", p_val

    def get_type(self, p_val):
        self.Type.set(p_val)
        if g_debug > 0: print "get type - ", p_val

# ## END
