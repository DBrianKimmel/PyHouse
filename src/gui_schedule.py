#!/usr/bin/env python

from Tkinter import *
import Pmw

import gui
import gui_tools
import lighting
import schedule
import config_xml

Schedule_Data = schedule.Schedule_Data
Light_Data = lighting.Light_Data

class ScheduleWindow(gui_tools.GuiTools):
    """Display a schedule selection window.
    """

    def __init__(self, p_root, p_main_frame = None):
        self.m_root = p_root
        self.m_main_frame = p_main_frame
        self.m_sched_frame = Frame(p_root, bg = '#006000')
        self.m_sched_frame.grid(padx = 5, pady = 5)
        
        self.m_ix = 0
        print "ScheduleWindow.__init__", p_root, self.m_sched_frame
        self.show_all_schedules()
        Button(self.m_sched_frame, text = "ADD Schedule", command = self.add_schedule).grid(row = self.m_ix, column = 0)
        Button(self.m_sched_frame, text = "Back", fg = "red", command = self.main_screen).grid(row = self.m_ix, column = 1)

    def show_all_schedules(self):
        l_sched = []
        for l_obj in Schedule_Data.itervalues():
            l_bg, l_fg = self.color_button(int(l_obj.Level))
            l_row, l_col = self.get_grid(self.m_ix)
            l = Button(self.m_sched_frame, text = l_obj.Name + ' ' + l_obj.LightName + ' ' + l_obj.Level,
                       bg = l_bg, fg = l_fg,
                       command = lambda x = l_obj.Key: self.edit_schedule(x))
            l_sched.append(l)
            l_sched[self.m_ix].grid(row = l_row, column = l_col, padx = 5, sticky = W)
            self.m_ix += 1

    def edit_schedule(self, p_key):
        print "edit schedule", self.m_sched_frame, self.m_ix 
        d = ScheduleDialog(self.m_root, self.m_sched_frame, p_key, "Editing Schedule")
        self.save_schedule()

    def add_schedule(self):
        print "add schedule", self.m_sched_frame, self.m_ix 
        d = ScheduleDialog(self.m_root, self.m_sched_frame, self.m_ix + 1, "Adding Schedule")
        self.save_schedule()

    def save_schedule(self):
        print "Save_Schedule"
        config_xml.WriteConfig().write_schedules()
        self.main_screen()
        
    def main_screen(self):
        """Exit the schedule screen.
        """
        print "MainScreen"
        self.frame_delete(self.m_sched_frame)
        self.m_main_frame.grid()

    def color_button(self, p_level):
        l_bg = '#FFFFD0' # Very Light yellow - full on
        l_fg = 'black'
        if p_level < 10: # Dark
            l_bg = '#505010'
            l_fg = 'white'
        elif p_level <= 40: # Dark Yellow
            l_bg = '#707030'
            l_fg = 'white'
        elif p_level <= 60: # Dark Yellow
            l_bg = '#909050'
            l_fg = 'white'
        elif p_level <= 80: # Dark Yellow
            l_bg = '#B0B070'
        elif p_level < 90: # Medium Yellow
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
        print "ScheduleDialog.__init__", p_root, p_parent, p_key, p_title
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
        self.m_frame.grid_columnconfigure(0, minsize=120)
        self.m_frame.grid_columnconfigure(1, minsize=300)
        self.m_frame.grid(padx = 5, pady = 5)
        Label(self.m_frame, text = "Key").grid(row = 1, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Key, state = DISABLED).grid(row = 1, column = 1, sticky = W)
        Label(self.m_frame, text = "Active").grid(row = 2, column = 0, sticky = E)
        self.yes_no_radio(self.m_frame, self.Active).grid(row = 2, column = 1, sticky = W)
        Label(self.m_frame, text = "Name").grid(row = 3, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Name).grid(row = 3, column = 1, sticky = W)
        Label(self.m_frame, text = "Time").grid(row = 5, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Time).grid(row = 5, column = 1, sticky = W)
        Label(self.m_frame, text = "Level").grid(row = 9, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Level).grid(row = 9, column = 1, sticky = W)
        Label(self.m_frame, text = "Rate").grid(row = 11, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Rate).grid(row = 11, column = 1, sticky = W)
        Label(self.m_frame, text = "Type").grid(row = 15, column = 0, sticky = E)
        Entry(self.m_frame, textvar = self.Type).grid(row = 15, column = 1, sticky = W)
        Label(self.m_frame, text = "LightName").grid(row = 31, column = 0, sticky = E)
        self.light_box(self.m_frame).grid(row = 31, column = 1, sticky = W)
        l_text = "Add"
        if p_title.startswith("Edit"):
            l_text = "Save"
            Button(self.m_frame, text = 'Delete', command = self.delete_schedule).grid(row = 91, column = 1)
        Button(self.m_frame, text = l_text, fg = "blue", command = self.get_vars).grid(row = 91, column = 0)
        Button(self.m_frame, text = "Cancel", fg = "red", command = self.quit_dialog).grid(row = 91, column = 2)

    def create_vars(self):
        self.Active = IntVar()
        self.Key = IntVar()
        self.Level = IntVar()
        self.Name = StringVar()
        self.Rate = IntVar()
        self.LightName = StringVar()
        self.Time = StringVar()
        self.Type = StringVar()

    def load_vars(self, p_key):
        try:
            l_obj = Schedule_Data[p_key]
        except:
            l_obj = schedule.ScheduleData()
            l_obj.Key = p_key
        print "Load vars - got schedule #{0:} {1:}".format(p_key, l_obj.Name)
        self.Active.set(self.get_bool(l_obj.Active))
        self.Key.set(l_obj.Key)
        self.Level.set(l_obj.Level)
        self.Name.set(l_obj.Name)
        self.LightName.set(l_obj.LightName)
        self.Rate.set(l_obj.Rate)
        self.Time.set(l_obj.Time)
        self.Type.set(l_obj.Type)

    def get_vars(self):
        """Called on either Add or Save.
        """
        l_obj = schedule.ScheduleData()
        l_obj.Active = self.Active.get()
        l_obj.Key = self.Key.get()
        l_obj.Level = self.Level.get()
        l_obj.Name = self.Name.get()
        l_obj.Rate = self.Rate.get()
        l_obj.LightName = self.LightName.get()
        l_obj.Time = self.Time.get()
        l_obj.Type = self.Type.get()
        Schedule_Data[l_obj.Key] = l_obj
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
    
    def light_box(self, p_parent, p_light = None):
        # Create and pack the dropdown ComboBox.
        items = self.build_names(Light_Data)
        dropdown = Pmw.ComboBox(p_parent,
                scrolledlist_items = items,
        )
        l_name = self.LightName.get()
        try:
            l_sel = items.index(l_name)
        except ValueError:
            l_sel = items[0]
        dropdown.selectitem(l_sel)
        return dropdown

### END
