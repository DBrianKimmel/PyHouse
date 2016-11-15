/**
 * @name:      PyHouse/src/Modules/Web/js/garageDoor.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2016-2016 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created on Sep 17, 2016
 * @summary:   Displays the Garage Door element
 */

/**
 * The GarageDoors widget.
 */
helpers.Widget.subclass(garageDoors, 'GarageDoorsWidget').methods(

function __init__(self, node) {
	garageDoors.GarageDoorsWidget.upcall(self, '__init__', node);
},

// ============================================================================
/**
 * Place the widget in the workspace.
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

function startWidget(self) {
	showSelectionButtons(self);
	self.fetchDataFromServer();
},

/**
 * Build a screen full of buttons - One for each controller and some actions.
 */
function buildLcarSelectScreen(self) {
	// Divmod.debug('---', 'garageDoors.buildLcarSelectScreen() called
	// ');
	var l_button_html = buildLcarSelectionButtonsTable(globals.House.Security.GarageDoors, 'handleMenuOnClick');
	var l_html = build_lcars_top('Garage Doors', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(10, l_button_html);
	l_html += build_lcars_bottom();
	self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
},

/**
 * This triggers getting the data from the server.
 */
function fetchDataFromServer(self) {
	function cb_fetchDataFromServer(p_json) {
		globals.House = JSON.parse(p_json);
		self.buildLcarSelectScreen();
	}
	function eb_fetchDataFromServer(p_reason) {
		Divmod.debug('---', 'ERROR garageDoors.eb_fetchDataFromServer() - ' + p_reason);
	}
	var l_defer = self.callRemote("getHouseData"); // call server @
	// web_controllers.py
	l_defer.addCallback(cb_fetchDataFromServer);
	l_defer.addErrback(eb_fetchDataFromServer);
	return false;
},

// ============================================================================
/**
 * Event handler for controller selection buttons.
 */
function handleMenuOnClick(self, p_node) {
	// Divmod.debug('---', 'garageDoors.handleMenuOnClick() called ');
	var l_ix = p_node.name;
	var l_name = p_node.value;
	var l_obj;
	globals.GarageDoorIx = l_ix;
	globals.GarageDoorName = l_name;
	globals.Self = self;
	globals.Add = false;
	showDataEntryScreen(self);
	if (l_ix <= 1000) { // One of the controller buttons
		l_obj = globals.House.Security.GarageDoors[l_ix];
		globals.GarageDoorObj = l_obj;
		self.buildDataEntryScreen(l_obj, 'handleDataOnClick');
	} else if (l_ix == 10001) { // The 'Add' button
		l_obj = self.createEntry()
		globals.GarageDoorObj = l_obj;
		globals.Add = true;
		self.buildDataEntryScreen(l_obj, 'handleDataOnClick');
	} else if (l_ix == 10002) { // The 'Back' button
		self.showWidget('HouseMenu');
	}
},

// ============================================================================
/**
 * Build a screen full of data entry fields.
 */
function buildDataEntryScreen(self, p_entry, p_handler) {
	// Divmod.debug('---', 'garageDoors.buildDataEntryScreen() called ');
	var l_obj = arguments[1];
	var l_html = build_lcars_top('Garage Door Data', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(40, self.buildEntry(l_obj, p_handler));
	l_html += build_lcars_bottom();
	self.nodeById('DataEntryDiv').innerHTML = l_html;
},

function buildEntry(self, p_obj, p_handler, p_onchange) {
	Divmod.debug('---', 'garageDoors.buildEntry() called ');
	var l_html = '';
	l_html = buildBaseEntry(self, p_obj, l_html);
	l_html = buildDeviceEntry(self, p_obj, l_html, p_onchange);
	l_html = self.buildDoorEntry(p_obj, l_html);
	l_html = buildFamilyPart(self, p_obj, l_html, 'familyChanged');
	l_html = buildLcarEntryButtons(p_handler, l_html);
	return l_html;
},

function buildDoorEntry(self, p_obj, p_html) {
	p_html += buildLcarTextWidget(self, 'Status', 'Status', p_obj.Status, 'disabled');
	return p_html;
},

function familyChanged() {
	// Divmod.debug('---', 'garageDoors.familyChanged() was called.');
	var l_obj = globals.GarageDoorObj;
	var l_self = globals.Self;
	l_obj.DeviceFamily = fetchSelectWidget(l_self, 'DeviceFamily');
	l_self.buildDataEntryScreen(l_obj, 'handleDataOnClick');
},

function fetchEntry(self) {
	var l_data = fetchBaseEntry(self);
	l_data = fetchDeviceEntry(self, l_data);
	l_data = self.fetchDoorEntry(l_data);
	l_data = fetchFamilyPart(self, l_data);
	// console.log("garageDoors.fetchEntry() - Data = %O", l_data);
	return l_data;
},

function fetchDoorEntry(self, p_data) {
	p_data.Status = fetchTextWidget(self, 'Status');
	return p_data;
},

function createEntry(self) {
	var l_data = createBaseEntry(self, Object.keys(globals.House.Security.GarageDoors).length);
	l_data = createDeviceEntry(self, l_data);
	l_data = self.createDoorEntry(l_data);
	l_data.DeviceFamily = 'Insteon';
	l_data = createFamilyPart(self, l_data);
	return l_data;
},

function createDoorEntry(self, p_data) {
	p_data.Status = 'Unknown';
	return p_data;
},

// ============================================================================
/**
 * Event handler for submit buttons at bottom of entry portion of this widget.
 * Get the possibly changed data and send it to the server.
 */
function handleDataOnClick(self, p_node) {
	function cb_handleDataOnClick(p_json) {
		self.startWidget();
	}
	function eb_handleDataOnClick(p_reason) {
		Divmod.debug('---', 'ERROR garageDoors.eb_handleDataOnClick() - ' + p_reason);
	}
	var l_ix = p_node.name;
	var l_obj = self.fetchEntry();
	var l_json = '';
	var l_defer = '';
	l_obj.Add = globals.Add;
	switch (l_ix) {
	case '10003': // The 'Change' Button
		l_json = JSON.stringify(l_obj);
		l_defer = self.callRemote("saveGarageDoorData", l_json); // @
		// web_controller
		l_defer.addCallback(cb_handleDataOnClick);
		l_defer.addErrback(eb_handleDataOnClick);
		break;
	case '10002': // The 'Back' button
		showSelectionButtons(self);
		break;
	case '10004': // The 'Delete' button
		l_obj.Delete = true;
		l_json = JSON.stringify(l_obj);
		l_defer = self.callRemote("saveGarageDoorData", l_json); // @
		// web_rooms
		l_defer.addCallback(cb_handleDataOnClick);
		l_defer.addErrback(eb_handleDataOnClick);
		break;
	default:
		Divmod.debug('---', 'garageDoors.handleDataOnClick(Default) was called. l_ix:' + l_ix);
		break;
	}
	return false; // false stops the chain.
}

);

// Divmod.debug('---', 'garageDoors.handleMenuOnClick() was called.');
// console.log("garageDoors.handleMenuOnClick() - l_obj = %O", l_obj);

// ### END DBK
