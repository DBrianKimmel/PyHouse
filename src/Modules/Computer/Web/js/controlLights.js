/* controlLights.js
 *
 * Displays the control light screens
 */

helpers.Widget.subclass(controlLights, 'ControlLightsWidget').methods(

function __init__(self, node) {
	controlLights.ControlLightsWidget.upcall(self, '__init__', node);
},

// ============================================================================
/**
 * Place the widget in the workspace.
 * 
 * @param self
 *            is <"Instance" of undefined.controlLights.ControlLightsWidget>
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
	self.fetchDataFromServer();
},

// ============================================================================
/**
 * This triggers getting the house data from the server.
 */
function fetchDataFromServer(self) {
	function cb_fetchDataFromServer(p_json) {
		globals.House = JSON.parse(p_json);
		self.buildLcarSelectScreen();
	}
	function eb_fetchDataFromServer(res) {
		Divmod.debug('---', 'controlLights.eb_fetchDataFromServer() was called.  ERROR ' + res);
	}
	var l_defer = self.callRemote("getHouseData"); // call server @ web_controlLights.py
	l_defer.addCallback(cb_fetchDataFromServer);
	l_defer.addErrback(eb_fetchDataFromServer);
	return false;
},

/**
 * Build a screen full of buttons - One for each light and some actions.
 */
function buildLcarSelectScreen(self) {
	var l_button_html = buildLcarSelectionButtonsTable(globals.House.Lighting.Lights, 'handleMenuOnClick');
	var l_html = build_lcars_top('Control Lights', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(15, l_button_html);
	l_html += build_lcars_bottom();
	self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
},

/**
 * Event handler for light selection buttons.
 * 
 * The user can click on a light button or the "Back" button.
 * 
 * @param self
 *            is <"Instance" of undefined.controlLights.ControlLightsWidget>
 * @param p_node
 *            is the node of the button that was clicked.
 */
function handleMenuOnClick(self, p_node) {
	var l_ix = p_node.name;
	var l_name = p_node.value;
	globals.LightIx = l_ix;
	globals.LightName = l_name;
	if (l_ix <= 1000) { // One of the controlLights buttons.
		var l_obj = globals.House.Lighting.Lights[l_ix];
		globals.LightObj = l_obj;
		globals.House.Self = self;
		showDataEntryScreen(self);
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
	Divmod.debug('---', 'controlLights.buildDataEntryScreen() was called.');
	var l_obj = arguments[1];
	var l_html = build_lcars_top('Control Light', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(10, self.buildEntry(l_obj, p_handler));
	l_html += build_lcars_bottom();
	self.nodeById('DataEntryDiv').innerHTML = l_html;
},

function buildEntry(self, p_obj, p_handler) {
	Divmod.debug('---', 'controlLights.buildEntry() was called.');
	var l_html = "";
	l_html = buildBaseEntry(self, p_obj, l_html);
	l_html = self.buildControlEntry(p_obj, l_html);
	l_html = buildLcarEntryButtons(p_handler, l_html, 'NoDelete');
	return l_html;
},

function buildControlEntry(self, p_obj, p_html) {
	Divmod.debug('---', 'controlLights.buildControlEntry() was called.');
	p_html += buildTextWidget(self, 'RoomName', 'Room Name', p_obj.RoomName, 'disabled');
	p_html += buildLcarLevelSliderWidget(self, 'Level', 'Level', p_obj.CurLevel, 'handleSliderChange');
	return p_html;
},

function handleSliderChange(p_event) {
	var l_self = globals.House.Self;
	var l_level = fetchSliderWidget(l_self, 'CtlLightLevel');
	updateSliderBoxValue(l_self, 'CtlLightLevel', l_level);
},

function fetchEntry(self) {
	var l_data = {
		Name : fetchTextWidget(self, 'Name'),
		Key : fetchTextWidget(self, 'Key'),
		UUID : fetchTextWidget(self, 'UUID'),
		Level : fetchSliderWidget(self, 'Level'),
	};
	return l_data;
},

// ============================================================================
/**
 * Event handler for submit buttons at bottom of entry portion of this widget. Get the possibly changed data and send it to the server.
 */
function handleDataEntryOnClick(self, p_node) {
	function cb_handleDataOnClick() {
		self.startWidget();
	}
	function eb_handleDataOnClick(res) {
		Divmod.debug('---', 'controlLights.eb_handleDataOnClick() was called. ERROR=' + res);
	}
	var l_json = JSON.stringify(self.fetchEntry(self));
	var l_defer = self.callRemote("saveControlLightData", l_json); // @ web_controlLights
	l_defer.addCallback(cb_handleDataOnClick);
	l_defer.addErrback(eb_handleDataOnClick);
	return false; // return false stops the resetting of the server.
}

);
// Divmod.debug('---', 'controlLights.fetchDataFromServer.cb_fetchDataFromServer() was called.');
// console.log("controlLights.fetchDataFromServer.cb_fetchDataFromServer p1 %O", p_json);

// ### END DBK

