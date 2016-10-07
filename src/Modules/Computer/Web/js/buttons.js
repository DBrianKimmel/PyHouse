/*
 * @name:      PyHouse/src/Modules/Web/js/buttons.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2016 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created on Mar 11, 2014
 * @summary:   Displays the buttons element
 *
 */

helpers.Widget.subclass(buttons, 'ButtonsWidget').methods(

function __init__(self, node) {
	buttons.ButtonsWidget.upcall(self, '__init__', node);
},

// ============================================================================
/**
 * 
 * @param self
 *            is <"Instance" of undefined.buttons.ButtonsWidget>
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
function startWidget(self) {
	self.node.style.display = 'block';
	showSelectionButtons(self);
	self.fetchDataFromServer();
},

// ============================================================================
/**
 * This triggers getting the button data from the server. The server calls displayButtonButtons with the buttons info.
 */
function fetchDataFromServer(self) {
	function cb_fetchDataFromServer(p_json) {
		globals.House = JSON.parse(p_json);
		self.buildLcarSelectScreen();
	}
	function eb_fetchDataFromServer(p_reason) {
		Divmod.debug('---', 'buttons.eb_fetchDataFromServer() was called.  ERROR - ' + p_reason);
	}

	var l_defer = self.callRemote("getHouseData"); // call server @
	// web_buttons.py
	l_defer.addCallback(cb_fetchDataFromServer);
	l_defer.addErrback(eb_fetchDataFromServer);
	return false;
},

// ============================================================================
/**
 * Build a screen full of buttons - One for each Button and some actions.
 */
function buildLcarSelectScreen(self) {
	var l_button_html = buildLcarSelectionButtonsTable(globals.House.Lighting.Buttons, 'handleMenuOnClick');
	var l_html = build_lcars_top('Buttons', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(10, l_button_html);
	l_html += build_lcars_bottom();
	self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
},

/**
 * Event handler for button selection buttons.
 * 
 * The user can click on a button button, the "Add" button or the "Back" button.
 * 
 * @param self
 *            is <"Instance" of undefined.buttons.ButtonsWidget>
 * @param p_node
 *            is the node of the button that was clicked.
 */
function handleMenuOnClick(self, p_node) {
	var l_ix = p_node.name;
	var l_name = p_node.value;
	var l_obj;
	globals.ButtonIx = l_ix;
	globals.ButtonName = l_name;
	globals.Add = false;
	globals.Self = self;
	showDataEntryScreen(self);
	if (l_ix <= 1000) { // One of the "Button" buttons.
		l_obj = globals.House.Lighting.Buttons[l_ix];
		globals.ButtonObj = l_obj;
		self.buildDataEntryScreen(l_obj, 'handleDataEntryOnClick');
	} else if (l_ix == 10001) { // The "Add" button
		globals.Add = true;
		l_obj = self.createEntry();
		globals.ButtonObj = l_obj;
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
	var l_obj = arguments[1];
	var l_html = build_lcars_top('Button Data', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(25, self.buildEntry(l_obj, p_handler));
	l_html += build_lcars_bottom();
	self.nodeById('DataEntryDiv').innerHTML = l_html;
},

function buildEntry(self, p_obj, p_handler, p_onchange) {
	var l_html = '';
	l_html = buildBaseEntry(self, p_obj, l_html);
	l_html = buildDeviceEntry(self, p_obj, l_html, p_onchange);
	l_html = buildFamilyPart(self, p_obj, l_html, 'familyChanged');
	l_html = buildLcarEntryButtons(p_handler, l_html);
	return l_html;
},

function familyChanged() {
	Divmod.debug('---', 'buttons.familyChanged() was called.');
	var l_obj = globals.ButtonObj;
	var l_self = globals.Self;
	l_obj.DeviceFamily = fetchSelectWidget(l_self, 'DeviceFamily');
	l_self.buildDataEntryScreen(l_obj, 'handleDataEntryOnClick');
},

function fetchEntry(self) {
	Divmod.debug('---', 'buttons.fetchEntry() was called.');
	var l_data = fetchBaseEntry(self);
	l_data = fetchDeviceEntry(self, l_data);
	l_data = fetchFamilyPart(self, l_data);
	console.log("buttons.fetchEntry() - Data = %O", l_data);
	return l_data;
},

function createEntry(self) {
	Divmod.debug('---', 'buttons.createEntry() was called.');
	var l_key = Object.keys(globals.House.Lighting.Buttons).length;
	var l_data = createBaseEntry(self, l_key);
	l_data = self.createButtonEntry(l_data);
	l_data = createFamilyPart(self, l_data);
	l_data.LightingType = 'Button';
	return l_data;
},

// ============================================================================
/**
 * Event handler for submit buttons at bottom of entry portion of this widget.
 * 
 * Get the possibly changed data and send it to the server.
 */
function handleDataEntryOnClick(self, p_node) {
	function cb_handleDataOnClick(p_json) {
		self.startWidget();
	}
	function eb_handleDataOnClick(res) {
	}
	var l_defer;
	var l_ix = p_node.name;
	var l_json;
	var l_obj = self.fetchEntry();
	l_obj.Add = globals.Add;
	switch (l_ix) {
	case '10003': // "Change" Button
		l_json = JSON.stringify(self.fetchEntry(self));
		l_defer = self.callRemote("saveButtonData", l_json); // @ web_button
		l_defer.addCallback(cb_handleDataOnClick);
		l_defer.addErrback(eb_handleDataOnClick);
		break;
	case '10002': // "Back" button
		showSelectionButtons(self);
		break;
	case '10004': // "Delete" button
		l_obj.Delete = true;
		l_json = JSON.stringify(l_obj);
		l_defer = self.callRemote("saveButtonData", l_json); // @ web_button
		l_defer.addCallback(cb_handleDataOnClick);
		l_defer.addErrback(eb_handleDataOnClick);
		break;
	default:
		Divmod.debug('---', 'buttons.handleDataOnClick(Default) was called. l_ix:' + l_ix);
		break;
	}
	return false; // false stops the chain.
}

);

// Divmod.debug('---', 'buttons.handleMenuOnClick(1) was called. ' + l_ix + ' ' + l_name);
// console.log("buttons.handleMenuOnClick() - l_obj = %O", l_obj);

// ### END DBK
