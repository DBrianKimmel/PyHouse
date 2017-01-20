/**
 * @name: PyHouse/src/Modules/Web/js/thermostats.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2017 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Sep 03, 2014
 * @summary: Displays the thermostat element
 * 
 */

helpers.Widget.subclass(thermostats, 'ThermostatsWidget').methods(

function __init__(self, node) {
	thermostats.ThermostatsWidget.upcall(self, "__init__", node);
},

// ============================================================================
/**
 * Place the widget in the workspace.
 * 
 * @param self
 *            is <"Instance" of undefined.thermostats.ThermostatsWidget>
 * @returns a deferred
 */
function ready(self) {
	function cb_widgetready(res) {
		self.hideWidget();
	}
	function eb_widgetready(p_reason) {
		Divmod.debug('---', 'ERROR thermostats.eb_widgetready() - ' + p_reason);
	}
	var uris = collectIMG_src(self.node, null);
	var l_defer = loadImages(uris);
	l_defer.addCallback(cb_widgetready);
	l_defer.addErrback(eb_widgetready);
	return l_defer;
},
/**
 * routines for showing and hiding parts of the screen.
 */
function startWidget(self) {
	showSelectionButtons(self);
	self.fetchDataFromServer();
},

// ============================================================================
/**
 * Build a screen full of buttons - One for each thermostat and some actions.
 */
function buildLcarSelectScreen(self) {
	var l_thermostat_html = buildLcarSelectionButtonsTable(globals.House.Hvac.Thermostats, 'handleMenuOnClick');
	var l_html = build_lcars_top('Thermostats', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(10, l_thermostat_html);
	l_html += build_lcars_bottom();
	self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
},
/**
 * This triggers getting the Thermostat data from the server. The server calls
 * displayThermostatButtons with the Thermostat info.
 */
function fetchDataFromServer(self) {
	function cb_fetchDataFromServer(p_json) {
		globals.House = JSON.parse(p_json);
		self.buildLcarSelectScreen();
	}
	function eb_fetchDataFromServer(res) {
		Divmod.debug('---', 'thermostats.eb_fetchDataFromServer() was called. ERROR: ' + res);
	}
	var l_defer = self.callRemote("getHouseData"); // call server @web_thermostat.py
	l_defer.addCallback(cb_fetchDataFromServer);
	l_defer.addErrback(eb_fetchDataFromServer);
	return false;
},
/**
 * Event handler for Thermostat selection buttons.
 * 
 * The user can click on a thermostat button, the "Add" button or the "Back"
 * button.
 * 
 * @param self
 *            is <"Instance" of undefined.thermostats.ThermostatsWidget>
 * @param p_node
 *            is the node of the button that was clicked.
 */
function handleMenuOnClick(self, p_node) {
	// Divmod.debug('---', 'thermostats.handleMenuOnClick() was called. Ix = ' + l_ix);
	var l_ix = p_node.name;
	var l_name = p_node.value;
	var l_obj;
	globals.ThermostatIx = l_ix;
	globals.ThermostatName = l_name;
	globals.Add = false;
	globals.Self = self;
	showDataEntryScreen(self);
	if (l_ix <= 1000) { // One of the Thermostat buttons.
		l_obj = globals.House.Hvac.Thermostats[l_ix];
		globals.ThermostatObj = l_obj;
		self.buildDataEntryScreen(l_obj, 'handleDataOnClick');
	} else if (l_ix == 10001) { // The "Add" button
		globals.Add = true;
		l_obj = self.createEntry();
		globals.Self = self;
		self.buildDataEntryScreen(l_obj, 'handleDataOnClick');
	} else if (l_ix == 10002) { // The "Back" button
		self.showWidget('HouseMenu');
	}
},

// ============================================================================
/**
 * Build a screen full of data entry fields.
 */
function buildDataEntryScreen(self, p_entry, p_handler) {
	// Divmod.debug('---', 'thermostats.buildDataEntryScreen() was called.';
	var l_obj = arguments[1];
	var l_html = build_lcars_top('Thermostat Data', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(35, self.buildEntry(l_obj, p_handler));
	l_html += build_lcars_bottom();
	self.nodeById('DataEntryDiv').innerHTML = l_html;
},

function buildEntry(self, p_obj, p_handler, p_onchange) {
	//Divmod.debug('---', 'thermostats.buildEntry() was called.');
	var l_html = '';
	l_html = buildBaseEntry(self, p_obj, l_html);
	l_html += buildDeviceEntry(self, p_obj, p_onchange);
	l_html = buildFamilyPart(self, p_obj, l_html, 'familyChanged');
	l_html = self.buildThermostatEntry(p_obj, l_html);
	l_html = buildLcarEntryButtons(p_handler, l_html);
	return l_html;
},

function buildThermostatEntry(self, p_obj, p_html, p_onchange) {
	//Divmod.debug('---', 'thermostats.buildThermostatEntry() was called.');
	p_html += buildLcarHvacSliderWidget(self, 'CoolSetting', 'Cool', p_obj.CoolSetPoint, 'handleSliderChangeCool');
	p_html += buildLcarHvacSliderWidget(self, 'HeatSetting', 'Heat', p_obj.HeatSetPoint, 'handleSliderChangeHeat');
	return p_html;
},

function handleSliderChangeCool(p_event) {
	// Divmod.debug('---', 'thermostats.handleSliderChangeCool() was called.');
	var l_obj = globals.House.ThermostatObj;
	var l_self = globals.Self;
	var l_level = fetchSliderWidget(l_self, 'CoolSetting');
	updateSliderBoxValue(l_self, 'CoolSetting', l_level);
},

function handleSliderChangeHeat(p_event) {
	// Divmod.debug('---', 'thermostats.handleSliderChangeHeat() was called.');
	var l_obj = globals.House.ThermostatObj;
	var l_self = globals.Self;
	var l_level = fetchSliderWidget(l_self, 'HeatSetting');
	updateSliderBoxValue(l_self, 'HeatSetting', l_level);
},

function familyChanged() {
	// Divmod.debug('---', 'thermostats.familyChanged() was called.');
	var l_obj = globals.House.ThermostatObj;
	var l_self = globals.Self;
	l_obj.DeviceFamily = fetchSelectWidget(l_self, 'Family');
	l_self.buildDataEntryScreen(l_obj, 'handleDataOnClick');
},

function fetchEntry(self) {
	// Divmod.debug('---', 'thermostats.fetchEntry() was called.');
	var l_data = fetchBaseEntry(self);
	fetchDeviceEntry(self, l_data);
	fetchFamilyPart(self, l_data);
	self.fetchThermostatEntry(l_data);
	return l_data;
},

function fetchThermostatEntry(self, p_data) {
	// Divmod.debug('---', 'thermostats.fetchThermostatEntry() was called.');
	p_data.CoolSetPoint = fetchSliderWidget(self, 'CoolSetting');
	return p_data;
},

function createEntry(self) {
	// Divmod.debug('---', 'thermostats.createEntry() was called.');
	var l_data = createBaseEntry(self, Object.keys(globals.House.Hvac.Thermostats).length);
	createDeviceEntry(self, l_data);
	self.createThermostatEntry(l_data);
	createFamilyPart(self, l_data);
	// console.log("thermostats.createEntry() - Obj = %O", p_data);
	return l_data;
},

function createThermostatEntry(self, p_data) {
	// Divmod.debug('---', 'thermostats.createThermostatEntry() was called.');
	p_data.CoolSetPoint = 78;
	p_data.HeatSetPoint = 70;
},

// ============================================================================
/**
 * Event handler for buttons at bottom of the data entry portion of this widget.
 * Get the possibly changed data and send it to the server.
 */
function handleDataOnClick(self, p_node) {
	function cb_handleDataOnClick(p_json) {
		self.startWidget();
	}
	function eb_handleDataOnClick(res) {
		Divmod.debug('---', 'thermostats.eb_handleDataOnClick() was called. ERROR =' + res);
	}
	var l_ix = p_node.name;
	var l_defer;
	var l_json;
	// Divmod.debug('---', 'thermostats.handleDataOnClick() was called. Node:' + l_ix);
	switch (l_ix) {
	case '10003':  // Add/Change Button
		l_json = JSON.stringify(self.fetchEntry());
		l_defer = self.callRemote("saveThermostatsData", l_json); // @ web_thermostat
		l_defer.addCallback(cb_handleDataOnClick);
		l_defer.addErrback(eb_handleDataOnClick);
		break;
	case '10002':  // Back button
		showSelectionButtons(self);
		break;
	case '10004':  // Delete button
		var l_obj = self.fetchEntry();
		l_obj.Delete = true;
		l_json = JSON.stringify(l_obj);
		l_defer = self.callRemote("saveThermostatsData", l_json); // @web_thermostat
		l_defer.addCallback(cb_handleDataOnClick);
		l_defer.addErrback(eb_handleDataOnClick);
		break;
	default:
		break;
	}
	return false; // false stops the chain.
}

);

// Divmod.debug('---', 'thermostats.startWidget() was called.');
// console.log("thermostats.handleSelectButtonOnClick() - l_obj = %O", l_obj);

// ### END DBK
