/**
 * @name: PyHouse/src/Modules/Web/js/schedules.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Mar 11, 2014
 * @summary: Displays the Schedule widget.
 *
 */
// import Nevow.Athena
// import globals
// import helpers



helpers.Widget.subclass(schedules, 'SchedulesWidget').methods(

	function __init__(self, node) {
		schedules.SchedulesWidget.upcall(self, '__init__', node);
	},



	/**
     * Place the widget in the workspace.
	 * 
	 * @param self is    <"Instance" of undefined.schedules.SchedulesWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		function cb_widgetready(res) {
			self.hideWidget();
		}
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},

	/**
	 * routines for showing and hiding parts of the screen.
	 */
	function showWidget(self) {
		self.node.style.display = 'block';
		self.showSelectionButtons();
		self.hideDataEntry();
		self.fetchHouseData();
	},
	function hideSelectionButtons(self) {
		self.nodeById('SelectionButtonsDiv').style.display = 'none';
	},
	function showSelectionButtons(self) {
		self.nodeById('SelectionButtonsDiv').style.display = 'block';
	},
	function hideDataEntry(self) {
		self.nodeById('DataEntryDiv').style.display = 'none';
	},
	function showDataEntry(self) {
		self.nodeById('DataEntryDiv').style.display = 'block';
	},
	function buildButtonName(self, p_obj) {
		var l_html = p_obj.Name;
		l_html += '<br>' + p_obj.RoomName;
		l_html += '<br>' + p_obj.LightName;
		l_html += '<br>' + p_obj.Level + '% ';
		return l_html;
	},



// ============================================================================
	/**
	 * Build a screen full of buttons - One for each schedule and some actions.
	 */
	function buildLcarSelectScreen(self){
		// Divmod.debug('---', 'schedules.buildLcarSelectScreen() was called.');
		var l_button_html = buildLcarSelectionButtonsTable(globals.House.HouseObj.Schedules, 'handleMenuOnClick', 'buildButtonName');
		var l_html = build_lcars_top('Schedules', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(4, l_button_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
	/**
	 * This triggers getting the schedule data from the server.
	 */
	function fetchHouseData(self) {
		function cb_fetchHouseData(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
			self.buildLcarSelectScreen();
		}
		function eb_fetchHouseData(res) {
			Divmod.debug('---', 'schedules.eb_fetchHouseData() was called.  ERROR: ' + res);
		}
        var l_defer = self.callRemote("getHouseData");  // call server @ web_schedules.py
		l_defer.addCallback(cb_fetchHouseData);
		l_defer.addErrback(eb_fetchHouseData);
        return false;
	},


// ============================================================================
	/**
	 * Event handler for schedule selection buttons.
	 * 
	 * The user can click on a schedule button, the "Add" button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.schedules.SchedulesWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function handleMenuOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.House.ScheduleIx = l_ix;
		globals.House.ScheduleName = l_name;
		if (l_ix <= 1000) {  // One of the schedule buttons.
			var l_obj = globals.House.HouseObj.Schedules[l_ix];
			globals.House.ScheduleObj = l_obj;
			globals.House.Self = self;
			self.showDataEntry();
			self.hideSelectionButtons();
			self.fillEntry(l_obj);
		} else if (l_ix == 10001) {  // The "Add" button
			self.showDataEntry();
			self.hideSelectionButtons();
			var l_ent = self.createEntry();
			self.fillEntry(l_ent);
		} else if (l_ix == 10002) {  // The "Back" button
			self.hideWidget();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget();
		}
	},


// ============================================================================

	function buildLcarDataEntryScreen(self, p_entry, p_handler){
		var l_schedule = arguments[1];
		var l_entry_html = "";
		l_entry_html += buildLcarTextWidget(self, 'Name', 'Name', l_schedule.Name);
		l_entry_html += buildLcarTextWidget(self, 'Key', 'Key', l_schedule.Key, 'disabled, size=05');
		l_entry_html += buildLcarTrueFalseWidget(self, 'ScheduleActive', 'Active', l_schedule.Active);
		l_entry_html += buildLcarTextWidget(self, 'ScheduleUUID', 'UUID', l_schedule.UUID, 'disabled');
		l_entry_html += buildLcarScheduleTypeSelectWidget(self, 'ScheduleType', 'Type', l_schedule.Type);
		l_entry_html += buildLcarTextWidget(self, 'ScheduleTime', 'Time',  l_schedule.Time);
		l_entry_html += buildLcarRoomSelectWidget(self, 'ScheduleRoomName', 'Room Name', l_schedule.RoomName);
		l_entry_html += buildLcarLightNameSelectWidget(self, 'ScheduleLightName', 'Light Name', l_schedule.LightName);
		l_entry_html += buildLcarLevelSliderWidget(self, 'ScheduleLevel', 'Level', l_schedule.Level, 'handleSliderChange');
		l_entry_html += buildLcarTextWidget(self, 'ScheduleRate', 'Rate', l_schedule.Rate);
		l_entry_html += buildLcarDowWidget(self, 'ScheduleDow', 'Day of Week', l_schedule.DOW);
		l_entry_html += buildLcarScheduleModeSelectWidget(self, 'ScheduleMode', 'Mode', l_schedule.Mode);
		l_entry_html += buildLcarEntryButtons(p_handler);
		var l_html = build_lcars_top('Schedules', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(30, l_entry_html);
		l_html += build_lcars_bottom();
		self.nodeById('DataEntryDiv').innerHTML = l_html;
	},
	function handleSliderChange(p_event){
		var l_obj = globals.House.ScheduleObj;
		var l_self = globals.House.Self;
		var l_level = fetchSliderWidget(l_self, 'ScheduleLevel');
		updateSliderBoxValue(l_self, 'ScheduleLevel', l_level);
	},

	/**
	 * Fill in the schedule entry screen with all of the data for this schedule.
	 */
	function fillEntry(self, p_entry) {
		self.buildLcarDataEntryScreen(p_entry, 'handleDataEntryOnClick');
	},

	function fetchEntry(self) {
        var l_data = {
            Name      : fetchTextWidget(self, 'Name'),
            Key       : fetchTextWidget(self, 'Key'),
			Active    : fetchTrueFalseWidget(self, 'ScheduleActive'),
			UUID      : fetchTextWidget(self, 'ScheduleUUID'),
			ScheduleType : fetchSelectWidget(self, 'ScheduleType'),
			Time      : fetchTextWidget(self, 'ScheduleTime'),  // be sure to strip any leading or trailing white space and lower case text
			DOW       : fetchDowWidget(self, 'ScheduleDow'),
			Mode      : fetchSelectWidget(self, 'ScheduleMode'),

			Level     : fetchSliderWidget(self, 'ScheduleLevel'),
			Rate      : fetchTextWidget(self, 'ScheduleRate'),
			RoomName  : fetchSelectWidget(self, 'ScheduleRoomName'),
			LightName : fetchSelectWidget(self, 'ScheduleLightName'),
			Delete : false
        };
		return l_data;
	},
	function createEntry(self) {
		//Divmod.debug('---', 'schedules.createEntry() was called.);
        var l_data = {
			Name : 'Change Me',
			Key : Object.keys(globals.House.HouseObj.Schedules).length,
			Active : false,
			UUID : '',
			ScheduleType : 'LightingDevice',
			Time : '',
			DOW : 127,
			Mode : 0,
			Level : 0,
			Rate : 0,
			RoomName : '',
			LightName : '',
			Delete : false
        };
		return l_data;
	},


	/**
	 * Event handler for submit buttons at bottom of entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataEntryOnClick(self, p_node) {
		function cb_handleDataEntryOnClick(p_json) {
			self.showWidget();
		}
		function eb_handleDataEntryOnClick(res){
			Divmod.debug('---', 'schedules.eb_handleDataEntryOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry());
	        var l_defer = self.callRemote("saveScheduleData", l_json);  // @ web_schedule
			l_defer.addCallback(cb_handleDataEntryOnClick);
			l_defer.addErrback(eb_handleDataEntryOnClick);
			break;
		case '10002':  // Back button
			self.hideDataEntry();
			self.showSelectionButtons();
			break;
		case '10004':  // Delete button
			var l_obj = self.fetchEntry();
			l_obj.Delete = true;
	    	l_json = JSON.stringify(l_obj);
	        l_defer = self.callRemote("saveScheduleData", l_json);  // @ web_rooms
			l_defer.addCallback(cb_handleDataEntryOnClick);
			l_defer.addErrback(eb_handleDataEntryOnClick);
			break;
		default:
			Divmod.debug('---', 'schedules.handleDataEntryOnClick(Default) was called. l_ix:' + l_ix);
			break;
		}
        return false;  // return false stops the resetting of the server.
	}
);
//Divmod.debug('---', 'schedules.handleDataEntryOnClick(Back) was called.  ');
//console.log("schedules.fetchHouseData.cb_fetchHouseData   p1 %O", p_json);
// ### END DBK
