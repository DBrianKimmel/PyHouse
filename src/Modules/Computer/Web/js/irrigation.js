/**
 * @name:      PyHouse/src/Modules/Computer/Web/js/irrigation.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2016 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created on Mar 11, 2014
 * @summary:   Displays the irrigation widget.
 *
 */

helpers.Widget.subclass(irrigation, 'IrrigationWidget').methods(

	function __init__(self, node) {
		irrigation.IrrigationWidget.upcall(self, '__init__', node);
	},


// ============================================================================
	/**
	 * Place the widget in the workspace.
	 * 
	 * @param self is    <"Instance" of undefined.irrigation.IrrigationWidget>
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
	// Build up the test to be shown within the irrigation selection button.
	function buildButtonName(self, p_obj) {
		var l_html = p_obj.Name;
		// l_html += '<br>' + p_obj.Level + '% ';
		return l_html;
	},

// ============================================================================
	// Build a screen full of buttons - One for each irrigation plus some actions.
	function buildLcarSelectScreen(self){
		// Divmod.debug('---', 'irrigation.buildLcarSelectScreen() was called.');
		var l_button_html = buildLcarSelectionButtonsTable(globals.House.irrigation, 'handleMenuOnClick', self.buildButtonName);
		var l_html = build_lcars_top('irrigation', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(15, l_button_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
	// This triggers getting the irrigation data from the server.
	function fetchDataFromServer(self) {
		function cb_fetchDataFromServer(p_json) {
			globals.House = JSON.parse(p_json);
			self.buildLcarSelectScreen();
		}
		function eb_fetchDataFromServer(res) {
			Divmod.debug('---', 'irrigation.eb_fetchDataFromServer() was called.  ERROR: ' + res);
		}
		var l_defer = self.callRemote("getHouseData");  // call server @ web_irrigation.py
		l_defer.addCallback(cb_fetchDataFromServer);
		l_defer.addErrback(eb_fetchDataFromServer);
		return false;
	},

// ============================================================================
	/**
	 * Event handler for irrigation selection buttons.
	 * 
	 * The user can click on a irrigation button, the "Add" button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.irrigation.IrrigationWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function handleMenuOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
	    var l_obj;
		globals.House.IrrigationIx = l_ix;
		globals.House.IrrigationName = l_name;
		globals.Add = false;
		if (l_ix <= 1000) {  // One of the irrigation buttons.
			showDataEntryScreen(self);
			l_obj = globals.House.Irrigation[l_ix];
			globals.House.IrrigationObj = l_obj;
			globals.House.Self = self;
			self.buildDataEntryScreen(l_obj, 'handleDataEntryOnClick');
		} else if (l_ix == 10001) {  // The "Add" button
			showDataEntryScreen(self);
			l_obj = self.createEntry();
			globals.House.IrrigationObj = l_obj;
			globals.House.Self = self;
			globals.Add = true;
			self.buildDataEntryScreen(l_obj, 'handleDataEntryOnClick');
		} else if (l_ix == 10002) {  // The "Back" button
			self.showWidget('HouseMenu');
		}
	},


// ============================================================================
	/**
	 * Build a screen full of data entry fields.
	 */
	function buildDataEntryScreen(self, p_entry, p_handler){
		Divmod.debug('---', 'irrigation.buildDataEntryScreen() was called.');
		var l_obj = arguments[1];
		var l_html = build_lcars_top('Light Data', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(20, self.buildEntry(l_obj, p_handler));
		l_html += build_lcars_bottom();
		self.nodeById('DataEntryDiv').innerHTML = l_html;
	},
	function buildEntry(self, p_obj, p_handler) {
		Divmod.debug('---', 'irrigation.buildEntry() was called.');
		var l_html = '';
		l_html = buildBaseEntry(self, p_obj, l_html); 
		l_html = self.buildIrrigationEntry(p_obj, l_html);
		l_html = buildLcarEntryButtons(p_handler, l_html);
		return l_html;
	},
	function buildIrrigationEntry(self, p_obj, p_html) {
		Divmod.debug('---', 'irrigation.buildIrrigationEntry() was called.');
		console.log("irrigation.buildIrrigationEntry   Object %O", p_obj);
		return p_html;
	},


// ============================================================================
	/**
	 * Fill in the irrigation entry screen with all of the data for this irrigation.
	 */
	function fillEntry(self, p_entry) {
		self.buildDataEntryScreen(p_entry, 'handleDataEntryOnClick');
	},
	function fetchEntry(self) {
		var l_data = fetchBaseEntry(self);
		l_data = self.fetchIrrigationEntry(l_data);
		return l_data;
	},
	function fetchIrrigationEntry(self, p_data) {
		return p_data
	},
	function createEntry(self) {
		// Divmod.debug('---', 'irrigation.createEntry() was called.);
		var l_data = {
			Name : 'System xxx',
			Key : Object.keys(globals.House.Irrigation).length,
			Active : true,
			Delete : false
		};
		return l_data;
	},


// ============================================================================
	/**
	 * Event handler for submit buttons at bottom of entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataEntryOnClick(self, p_node) {
		function cb_handleDataEntryOnClick(p_json) {
			self.startWidget();
		}
		function eb_handleDataEntryOnClick(res){
			Divmod.debug('---', 'irrigation.eb_handleDataEntryOnClick() was called. ERROR =' + res);
		}
		Divmod.debug('---', 'irrigation.handleDataEntryOnClick() was called.');
		var l_json;
		var l_defer;
		var l_ix = p_node.name;
		var l_obj = self.fetchEntry();
		l_obj.Add = globals.Add;
		l_obj.Delete = false;
		console.log("irrigation.handleDataEntryOnClick   Object %O", l_obj);
		switch(l_ix) {
		case '10003':  // Add/Change Button
			l_json = JSON.stringify(l_obj);
			l_defer = self.callRemote("saveIrrigationData", l_json);  // @ web_irrigation
			l_defer.addCallback(cb_handleDataEntryOnClick);
			l_defer.addErrback(eb_handleDataEntryOnClick);
			break;
		case '10002':  // Back button
			showSelectionButtons(self);
			break;
		case '10004':  // Delete button
			l_obj.Delete = true;
			l_json = JSON.stringify(l_obj);
			l_defer = self.callRemote("saveIrrigationData", l_json);  // @ web_rooms
			l_defer.addCallback(cb_handleDataEntryOnClick);
			l_defer.addErrback(eb_handleDataEntryOnClick);
			break;
		default:
			Divmod.debug('---', 'irrigation.handleDataEntryOnClick(Default) was called. l_ix:' + l_ix);
			break;
		}
		return false;  // return false stops the resetting of the server.
	}
);
// Divmod.debug('---', 'irrigation.handleDataEntryOnClick(Back) was called.  ');
// console.log("irrigation.fetchDataFromServer.cb_fetchDataFromServer   p1 %O", p_json);
// ### END DBK
