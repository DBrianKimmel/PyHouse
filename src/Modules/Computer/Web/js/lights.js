/**
 * @name: PyHouse/src/Modules/Computer/Web/js/lights.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2016 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Mar 11, 2014
 * @summary: Displays the lights
 */

helpers.Widget.subclass(lights, 'LightsWidget').methods(

function __init__(self, node) {
	lights.LightsWidget.upcall(self, "__init__", node);
},

// ============================================================================
/**
 * Startup - Place the widget in the workspace and hide it.
 * 
 * @param self
 *            is <"Instance" of undefined.lights.LightsWidget>
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

function startWidget(self) {
	self.node.style.display = 'block';
	showSelectionButtons(self);
	self.fetchDataFromServer(); // Continue with next phase
},

function buildButtonName(self, p_obj) {
	var l_html = p_obj.Name + '<br>' + p_obj.RoomName;
	return l_html;
},

// ============================================================================
/**
 * This triggers getting the lights data from the server.
 */
function fetchDataFromServer(self) {
	function cb_fetchDataFromServer(p_json) {
		globals.House = JSON.parse(p_json);
		self.buildLcarSelectScreen();
	}
	function eb_fetchDataFromServer(res) {
		Divmod.debug('---', 'lights.eb_fetchDataFromServer() was called. ERROR: ' + res);
	}

	var l_defer = self.callRemote("getHouseData");
	l_defer.addCallback(cb_fetchDataFromServer);
	l_defer.addErrback(eb_fetchDataFromServer);
	return false;
},

//============================================================================
/**
 * Build a screen full of buttons - One for each light and some actions.
 */
function buildLcarSelectScreen(self) {
	var l_button_html = buildLcarSelectionButtonsTable(globals.House.Lighting.Lights, 'handleMenuOnClick', self.buildButtonName);
	var l_html = build_lcars_top('Lights', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(10, l_button_html);
	l_html += build_lcars_bottom();
	self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
},

/**
 * Event handler for light selection buttons.
 * 
 * The user can click on a light button, the "Add" button or the "Back" button.
 * 
 * @param self
 *            is <"Instance" of undefined.lights.LightsWidget>
 * @param p_node
 *            is the node of the button that was clicked.
 */
function handleMenuOnClick(self, p_node) {
	var l_ix = p_node.name;
	var l_name = p_node.value;
	var l_obj;
	globals.LightIx = l_ix;
	globals.LightName = l_name;
	globals.Add = false;
	showDataEntryScreen(self);
	globals.Self = self;
	if (l_ix <= 1000) { // one of the buttons, show the details for that light.
		l_obj = globals.House.Lighting.Lights[l_ix];
		globals.LightObj = l_obj;
		try {
			l_obj.RoomName = globals.House.Rooms[l_obj.RoomName].Name;
		} catch (err) {
			l_obj.RoomName = l_obj.RoomName;
		}
		self.buildDataEntryScreen(l_obj, 'change', 'handleDataEntryOnClick');
	} else if (l_ix == 10001) {  // The "Add" button
		l_obj = self.createEntry();
		globals.ControllerObj = l_obj;
		globals.Add = true;
		self.buildDataEntryScreen(l_obj, 'add', 'handleDataEntryOnClick');
	} else if (l_ix == 10002) {  // The "Back" button
		self.showWidget('HouseMenu');
	}
},

// ============================================================================
/**
 * Build a screen full of data entry fields.
 */
function buildDataEntryScreen(self, p_entry, p_add_change, p_handler) {
	var l_obj = arguments[1];
	var l_html = build_lcars_top('Light Data', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(27, self.buildEntry(l_obj, p_handler));
	l_html += build_lcars_bottom();
	self.nodeById('DataEntryDiv').innerHTML = l_html;
},

/**
 * @param self
 * @param p_obj is
 * @param p_handler is text name of handler ('handleMenuHandler').
 * @param p_onchange is
 * @returns is HTML
 */
function buildEntry(self, p_obj, p_handler, p_onchange) {
	// Divmod.debug('---', 'lights.buildEntry() was called ');
	// console.log("lights.buildEntry() Obj %O", p_obj);
	var l_html = '';
	l_html = buildBaseEntry(self, p_obj, l_html);
	// l_html += buildTextWidget(self, 'Comment', 'Comment', p_obj.Comment);
	l_html += buildDeviceEntry(self, p_obj, 'handleRoomChanged');  // in lcars.js
	l_html = buildFamilyPart(self, p_obj, l_html, 'handleFamilyChanged');
	l_html = self.buildLightEntry(p_obj, l_html);
	l_html = buildLcarEntryButtons(p_handler, l_html);
	return l_html;
},

function buildLightEntry(self, p_obj, p_html) {
	p_html += buildTextWidget(self, 'CurLevel', 'Level', p_obj.CurLevel, 'disabled');
	p_html += buildTrueFalseWidget(self, 'IsDimmable', 'Dimmable ?', p_obj.IsDimmable);
	return p_html;
},

function handleFamilyChanged() {
	Divmod.debug('---', 'lights.handleFamilyChanged() was called ');
	var l_obj = globals.LightObj;
	var l_self = globals.Self;
	var l_family = fetchSelectWidget(l_self, 'Family');
	l_obj.DeviceFamily = l_family;
	l_self.buildDataEntryScreen(l_obj, 'handleDataEntryOnClick');
},

function handleRoomChanged() {
	Divmod.debug('---', 'lights.handleRoomChanged() was called ');
	l_self.buildDataEntryScreen(l_obj, 'handleDataEntryOnClick');
},

/**
 * Fetch the data we put out and the user updated.
 */
function fetchEntry(self) {
	var l_obj = fetchBaseEntry(self);
	fetchDeviceEntry(self, l_obj);  // in lcars.js
	fetchFamilyPart(self, l_obj);
	self.fetchLightEntry(l_obj);
	return l_obj;
},

function fetchLightEntry(self, p_data) {
	p_data.CurLevel = fetchTextWidget(self, 'CurLevel');
	p_data.IsDimmable = fetchTrueFalseWidget(self, 'IsDimmable');
	// Get non displayed fields
	p_data.DeviceSubType = 3;
	p_data.DeviceType = 1;
},

function createEntry(self) {
	var l_ix = Object.keys(globals.House.Lighting.Lights).length;
	Divmod.debug('---', 'lights.createEntry() was called Ix=' + l_ix);
	var l_obj = createBaseEntry(self, l_ix);
	createDeviceEntry(self, l_obj);    // in lcars.js
	createFamilyPart(self, l_obj);
	self.createLightEntry(l_obj);
	console.log("lights.createEntry() Obj = %O", l_obj);
	return l_obj;
},

function createLightEntry(self, p_data) {
	p_data.CurLevel = 0;
	p_data.IsDimmable = 'True';
},

// ============================================================================
/**
 * Event handler for buttons at bottom of the data entry portion of this widget.
 * Get the possibly changed data and send it to the server.
 */
function handleDataEntryOnClick(self, p_node) {
	function cb_handleDataEntryOnClick(p_json) {
		self.startWidget();
	}
	function eb_handleDataEntryOnClick(res) {
		Divmod.debug('---', 'lights.eb_handleDataEntryOnClick() was called. ERROR =' + res);
	}
	var l_ix = p_node.name;
	var l_obj = self.fetchEntry();
	// console.log("lights.handleDataEntryOnClick() Obj %O", l_obj);
	var l_json = '';
	var l_defer = '';
	l_obj.Add = globals.Add;
	switch (l_ix) {
	case '10003':  // Add/Change/Save Button
		l_json = JSON.stringify(l_obj);
		l_defer = self.callRemote("saveLightData", l_json);
		l_defer.addCallback(cb_handleDataEntryOnClick);
		l_defer.addErrback(eb_handleDataEntryOnClick);
		break;
	case '10002':  // Back button
		showSelectionButtons(self);
		break;
	case '10004':  // Delete button
		l_obj.Delete = true;
		l_json = JSON.stringify(l_obj);
		l_defer = self.callRemote("saveLightData", l_json);
		l_defer.addCallback(cb_handleDataEntryOnClick);
		l_defer.addErrback(eb_handleDataEntryOnClick);
		break;
	default:
		Divmod.debug('---', 'lights.handleDataEntryOnClick(Default) was called. l_ix:' + l_ix);
		break;
	}
	return false; // false stops the chain.
}

);

// Divmod.debug('---', 'lights.handleDataEntryOnClick(Default) was called. l_ix:' + l_ix);
// console.log("lights.handleDataEntryOnClick() Obj = %O", l_obj);

// ### END DBK
