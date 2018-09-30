/**
 * @name: PyHouse/src/Modules/Computer/Web/js/schedules.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2017 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Mar 11, 2014
 * @summary: Displays the Schedule widget.
 * 
 */

helpers.Widget.subclass(schedules, 'SchedulesWidget').methods(

function __init__(self, node) {
	schedules.SchedulesWidget.upcall(self, '__init__', node);
},

// ============================================================================
/**
 * Place the widget in the workspace.
 * 
 * @param self
 *            is <"Instance" of undefined.schedules.SchedulesWidget>
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

// Routines for showing and hiding parts of the screen.
function startWidget(self) {
	self.node.style.display = 'block';
	showSelectionButtons(self);
	self.fetchDataFromServer();
},

// Build up the test to be shown within the schedule selection button.
function buildButtonName(self, p_obj) {
	var l_html = p_obj.Name;
	l_html += '<br>' + p_obj.ScheduleType;
	if (p_obj.ScheduleType == 'Lighting') {
		l_html += '<br>' + p_obj.RoomName;
		l_html += '<br>' + p_obj.LightName;
	} else if (p_obj.ScheduleType == 'Irrigation') {
		l_html += '<br>';
	}
	// l_html += '<br>' + p_obj.Level + '% ';
	return l_html;
},

// ============================================================================
// Build a screen full of buttons - One for each schedule plus some actions.
function buildLcarSelectScreen(self) {
	// Divmod.debug('---', 'schedules.buildLcarSelectScreen() was called.');
	var l_button_html = buildLcarSelectionButtonsTable(globals.House.Schedules, 'handleMenuOnClick', self.buildButtonName);
	var l_html = build_lcars_top('Schedules', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(15, l_button_html);
	l_html += build_lcars_bottom();
	self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
},

// This triggers getting the schedule data from the server.
function fetchDataFromServer(self) {
	function cb_fetchDataFromServer(p_json) {
		globals.House = JSON.parse(p_json);
		self.buildLcarSelectScreen();
	}
	function eb_fetchDataFromServer(res) {
		Divmod.debug('---', 'schedules.eb_fetchDataFromServer() was called.  ERROR: ' + res);
	}
	var l_defer = self.callRemote("getHouseData"); // call server @ web_schedules.py
	l_defer.addCallback(cb_fetchDataFromServer);
	l_defer.addErrback(eb_fetchDataFromServer);
	return false;
},

// ============================================================================
/**
 * Event handler for schedule selection buttons.
 * 
 * The user can click on a schedule button, the "Add" button or the "Back" button.
 * 
 * @param self
 *            is <"Instance" of undefined.schedules.SchedulesWidget>
 * @param p_node
 *            is the node of the button that was clicked.
 */
function handleMenuOnClick(self, p_node) {
	var l_ix = p_node.name;
	var l_name = p_node.value;
	var l_obj;
	globals.House.ScheduleIx = l_ix;
	globals.House.ScheduleName = l_name;
	globals.Add = false;
	if (l_ix <= 1000) { // One of the schedule buttons.
		showDataEntryScreen(self);
		l_obj = globals.House.Schedules[l_ix];
		globals.House.ScheduleObj = l_obj;
		globals.Self = self;
		self.buildDataEntryScreen(l_obj, 'handleDataEntryOnClick');
	} else if (l_ix == 10001) { // The "Add" button
		showDataEntryScreen(self);
		l_obj = self.createEntry();
		globals.House.ScheduleObj = l_obj;
		globals.Self = self;
		globals.Add = true;
		self.buildDataEntryScreen(l_obj, 'handleDataEntryOnClick');
	} else if (l_ix == 10002) { // The "Back" button
		self.showWidget('HouseMenu');
	}
},

// ============================================================================
/**
 * Build a screen full of data entry fields.
 */
function buildDataEntryScreen(self, p_entry, p_handler) {
	// Divmod.debug('---', 'schedules.buildDataEntryScreen() was called.');
	var l_obj = arguments[1];
	var l_html = build_lcars_top('Schedule Data', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(20, self.buildEntry(l_obj, p_handler));
	l_html += build_lcars_bottom();
	self.nodeById('DataEntryDiv').innerHTML = l_html;
},

function buildEntry(self, p_obj, p_handler) {
	Divmod.debug('---', 'schedules.buildEntry() was called.');
	var l_html = '';
	l_html = buildBaseEntry(self, p_obj, l_html, 'nouuid');
	l_html = self.buildScheduleEntry(p_obj, l_html);
	l_html = buildLcarEntryButtons(p_handler, l_html);
	return l_html;
},

function buildScheduleEntry(self, p_obj, p_html) {
	Divmod.debug('---', 'schedules.buildScheduleEntry() was called.');
	console.log("schedules.buildScheduleEntry   Object %O", p_obj);
	p_html += buildLcarScheduleTypeSelectWidget(self, 'ScheduleType', 'Type', p_obj.ScheduleType, 'handleScheduleTypeChange');
	p_html += buildTextWidget(self, 'ScheduleTime', 'Time', p_obj.Time);
	p_html += buildLcarDowWidget(self, 'ScheduleDOW', 'Day of Week', p_obj.DOW);
	p_html += buildLcarScheduleModeSelectWidget(self, 'ScheduleMode', 'ScheduleMode', p_obj.ScheduleMode);
	if (p_obj.ScheduleType === 'Lighting')
		p_html = self.buildLightingEntry(p_obj, p_html)
	else if (p_obj.ScheduleType === 'Irrigation')
		p_html = self.buildIrrigationEntry(p_obj, p_html)
	return p_html;
},

function buildIrrigationEntry(self, p_obj, p_html) {
	Divmod.debug('---', 'schedules.buildIrigationEntry() was called.');
	p_html += buildTextWidget(self, 'Duration', 'Duration', p_obj.Duration);
	return p_html;
},

function buildLightingEntry(self, p_obj, p_html) {
	Divmod.debug('---', 'schedules.buildLightingEntry() was called.');
	p_html += buildTextWidget(self, 'RoomName', 'Room Name', p_obj.RoomName, 'disabled');
	p_html += buildLightNameSelectWidget(self, 'ScheduleLightName', 'Light Name', p_obj.LightName);
	p_html += buildLcarLevelSliderWidget(self, 'ScheduleLevel', 'Level', p_obj.Level, 'handleSliderChange');
	p_html += buildTextWidget(self, 'ScheduleRate', 'Rate', p_obj.Rate);
	return p_html;
},

function handleSliderChange(p_event) {
	Divmod.debug('---', 'schedules.handleSliderChange() was called.  ');
	var l_obj = globals.House.ScheduleObj;
	var l_self = globals.Self;
	var l_level = fetchSliderWidget(l_self, 'ScheduleLevel');
	updateSliderBoxValue(l_self, 'ScheduleLevel', l_level);
},

function handleScheduleTypeChange(p_event) {
	// change form when schedule type changes
	Divmod.debug('---', 'schedules.handleScheduleTypeChange() was called.  ');
	var l_obj = globals.House.ScheduleObj;
	var l_self = globals.Self;
	l_obj.ScheduleType = fetchSelectWidget(l_self, 'ScheduleType');
	l_self.buildDataEntryScreen(l_obj, 'handleDataEntryOnClick');
},

function fetchEntry(self) {
	var l_data = fetchBaseEntry(self);
	l_data = self.fetchScheduleEntry(l_data);
	return l_data;
},

function fetchScheduleEntry(self, p_data) {
	p_data.ScheduleType = fetchSelectWidget(self, 'ScheduleType');
	p_data.Time = fetchTextWidget(self, 'ScheduleTime');
	p_data.DOW = fetchDowWidget(self, 'ScheduleDOW');
	p_data.ScheduleMode = fetchSelectWidget(self, 'ScheduleMode');
	p_data.Level = fetchSliderWidget(self, 'ScheduleLevel');
	p_data.Rate = fetchTextWidget(self, 'ScheduleRate');
	p_data.RoomName = fetchSelectWidget(self, 'ScheduleRoomName');
	p_data.LightName = fetchSelectWidget(self, 'ScheduleLightName');
	return p_data
},

function createEntry(self) {
	// Divmod.debug('---', 'schedules.createEntry() was called.);
	var l_data = {
		Name : 'Change Me',
		Key : Object.keys(globals.House.Schedules).length,
		Active : true,
		ScheduleType : 'Lighting',
		Time : '',
		DOW : 127,
		ScheduleMode : 0,
		Level : 0,
		Rate : 0,
		RoomName : '',
		LightName : '',
		Delete : false
	};
	return l_data;
},

// ============================================================================
/**
 * Event handler for submit buttons at bottom of entry portion of this widget. Get the possibly changed data and send it to the server.
 */
function handleDataEntryOnClick(self, p_node) {
	function cb_handleDataEntryOnClick(p_json) {
		self.startWidget();
	}
	function eb_handleDataEntryOnClick(res) {
		Divmod.debug('---', 'schedules.eb_handleDataEntryOnClick() was called. ERROR =' + res);
	}
	var l_json;
	var l_defer;
	var l_ix = p_node.name;
	var l_obj = self.fetchEntry();
	l_obj.Add = globals.Add;
	l_obj.Delete = false;
	switch (l_ix) {
	case '10003': // Change Button
		l_json = JSON.stringify(l_obj);
		l_defer = self.callRemote("saveScheduleData", l_json); // @ web_schedule
		l_defer.addCallback(cb_handleDataEntryOnClick);
		l_defer.addErrback(eb_handleDataEntryOnClick);
		break;
	case '10002': // Back button
		showSelectionButtons(self);
		break;
	case '10004': // Delete button
		l_obj.Delete = true;
		l_json = JSON.stringify(l_obj);
		l_defer = self.callRemote("saveScheduleData", l_json); // @ web_rooms
		l_defer.addCallback(cb_handleDataEntryOnClick);
		l_defer.addErrback(eb_handleDataEntryOnClick);
		break;
	default:
		Divmod.debug('---', 'schedules.handleDataEntryOnClick(Default) was called. l_ix:' + l_ix);
		break;
	}
	return false; // return false stops the resetting of the server.
}

);

// Divmod.debug('---', 'schedules.handleDataEntryOnClick(Back) was called. ');
// console.log("schedules.fetchDataFromServer.cb_fetchDataFromServer p1 %O", p_json);
// ### END DBK
