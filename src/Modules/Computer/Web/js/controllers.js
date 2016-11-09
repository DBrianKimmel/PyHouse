/**
 * @name:      PyHouse/src/Modules/Computer/Web/js/controllers.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2016 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created on Mar 11, 2014
 * @summary:   Displays the controller element
 *
 * Note that a controller contains common light info, controller info, family info and interface info.
 */

/**
 * The controller widget.
 */
helpers.Widget.subclass(controllers, 'ControllersWidget').methods(

function __init__(self, node) {
	controllers.ControllersWidget.upcall(self, '__init__', node);
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

// ============================================================================
/**
 * Get all interface info from the server. This data can never change during a
 * server run.
 */
function fetchInterfaceData(self) {
	function cb_fetchInterfaceData(p_json) {
		globals.Interface.Obj = JSON.parse(p_json);
	}
	function eb_fetchInterfaceData(p_reason) {
		Divmod.debug('---', 'ERROR - controllers.cb_fetchInterfaceData() - ' + p_reason);
	}

	// Divmod.debug('---', 'controllers.fetchInterfaceData() was called.
	// ');
	var l_defer = self.callRemote("getInterfaceData"); // call server @
	// web_controllers.py
	l_defer.addCallback(cb_fetchInterfaceData);
	l_defer.addeRRback(eb_fetchInterfaceData);
	return false;
},

// ============================================================================
/**
 * Build a screen full of buttons - One for each controller and some actions.
 */
function buildLcarSelectScreen(self) {
	// Divmod.debug('---', 'controllers.buildLcarSelectScreen() called
	// ');
	var l_button_html = buildLcarSelectionButtonsTable(globals.House.Lighting.Controllers, 'handleMenuOnClick');
	var l_html = build_lcars_top('Controllers', 'lcars-salmon-color');
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
		Divmod.debug('---', 'ERROR controllers.eb_fetchDataFromServer() - ' + p_reason);
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
	// Divmod.debug('---', 'controllers.handleMenuOnClick() called ');
	var l_ix = p_node.name;
	var l_name = p_node.value;
	var l_obj;
	globals.ControllerIx = l_ix;
	globals.ControllerName = l_name;
	globals.Add = false;
	globals.Self = self;
	showDataEntryScreen(self);
	if (l_ix <= 1000) { // One of the controller buttons
		l_obj = globals.House.Lighting.Controllers[l_ix];
		globals.ControllerObj = l_obj;
		self.buildDataEntryScreen(l_obj, 'handleDataOnClick');
	} else if (l_ix == 10001) { // The 'Add' button
		globals.Add = true;
		l_obj = self.createEntry()
		globals.ControllerObj = l_obj;
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
	// Divmod.debug('---', 'controllers.buildDataEntryScreen() called ');
	var l_obj = arguments[1];
	var l_html = build_lcars_top('Controller Data', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(40, self.buildEntry(l_obj, p_handler));
	l_html += build_lcars_bottom();
	self.nodeById('DataEntryDiv').innerHTML = l_html;
},

function buildEntry(self, p_obj, p_handler, p_onchange) {
	// Divmod.debug('---', 'controllers.buildEntry() called ');
	var l_html = '';
	l_html = buildBaseEntry(self, p_obj, l_html);
	l_html = buildDeviceEntry(self, p_obj, l_html, p_onchange);
	l_html = self.buildControllerEntry(p_obj, l_html);
	l_html = buildFamilyPart(self, p_obj, l_html, 'familyChanged');
	l_html = buildInterfacePart(self, p_obj, l_html, 'interfaceChanged');
	l_html = buildLcarEntryButtons(p_handler, l_html);
	return l_html;
},

function buildControllerEntry(self, p_obj, p_html) {
	p_html += buildLcarTextWidget(self, 'Port', 'Port', p_obj.Port);
	return p_html;
},

function familyChanged() {
	// Divmod.debug('---', 'controllers.familyChanged() was called.');
	var l_obj = globals.ControllerObj;
	var l_self = globals.Self;
	l_obj.DeviceFamily = fetchSelectWidget(l_self, 'DeviceFamily');
	l_self.buildDataEntryScreen(l_obj, 'handleDataOnClick');
},

function interfaceChanged() {
	// Divmod.debug('---', 'controllers.interfaceChanged() was called.');
	var l_obj = globals.ControllerObj;
	var l_self = globals.Self;
	l_obj.InterfaceType = fetchSelectWidget(l_self, 'InterfaceType');
	l_self.buildDataEntryScreen(l_obj, 'handleDataOnClick');
},

function fetchEntry(self) {
	var l_data = fetchBaseEntry(self);
	l_data = fetchDeviceEntry(self, l_data);
	l_data = self.fetchControllerEntry(l_data);
	l_data = fetchFamilyPart(self, l_data);
	if (l_data.InterfaceType === 'Serial')
		l_data = fetchSerialEntry(self, l_data);
	// console.log("controllers.fetchEntry() - Data = %O", l_data);
	return l_data;
},

function fetchControllerEntry(self, p_data) {
	p_data.InterfaceType = fetchSelectWidget(self, 'InterfaceType');
	p_data.Port = fetchTextWidget(self, 'Port');
	return p_data;
},

function createEntry(self) {
	var l_data = createBaseEntry(self, Object.keys(globals.House.Lighting.Controllers).length);
	l_data = createDeviceEntry(self, l_data);  // in lcars.js,
	l_data.DeviceFamily = 'Insteon';
	l_data = self.createControllerEntry(l_data);
	l_data = createFamilyPart(self, l_data)
	l_data = createInterfacePart(self, l_data);
	return l_data;
},

function createControllerEntry(self, p_data) {
	p_data.InterfaceType = 'Serial';
	p_data.Port = '/dev/ttyS0';
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
		Divmod.debug('---', 'ERROR controllers.eb_handleDataOnClick() - ' + p_reason);
	}

	var l_ix = p_node.name;
	var l_obj = self.fetchEntry();
	var l_json = '';
	var l_defer = '';
	l_obj.Add = globals.Add;
	switch (l_ix) {
	case '10003': // The 'Change' Button
		l_json = JSON.stringify(l_obj);
		l_defer = self.callRemote("saveControllerData", l_json); // @
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
		l_defer = self.callRemote("saveControllerData", l_json); // @
		// web_rooms
		l_defer.addCallback(cb_handleDataOnClick);
		l_defer.addErrback(eb_handleDataOnClick);
		break;
	default:
		Divmod.debug('---', 'controllers.handleDataOnClick(Default) was called. l_ix:' + l_ix);
		break;
	}
	return false; // false stops the chain.
});

// Divmod.debug('---', 'controllers.handleMenuOnClick() was called.');
// console.log("controllers.handleMenuOnClick() - l_obj = %O", l_obj);

// ### END DBK
