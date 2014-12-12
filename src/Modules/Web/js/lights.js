/**
 * @name: PyHouse/src/Modules/Web/js/lights.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Mar 11, 2014
 * @summary: Displays the lights
 */
// import Nevow.Athena
// import globals
// import helpers

helpers.Widget.subclass(lights, 'LightsWidget').methods(

    function __init__(self, node) {
        lights.LightsWidget.upcall(self, "__init__", node);
    },



// ============================================================================
	/**
     * Startup - Place the widget in the workspace and hide it.
	 * 
	 * @param self is    <"Instance" of undefined.lights.LightsWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		function cb_widgetready(res) {
			self.hideWidget();
		}
		// Divmod.debug('---', 'lights.ready() was called.');
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	function startWidget(self) {
		self.node.style.display = 'block';
		showSelectionButtons(self);
		self.fetchDataFromServer();  // Continue with next phase
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
			globals.House.HouseObj = JSON.parse(p_json);
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
	/**
	 * Build a screen full of buttons - One for each light and some actions.
	 */
	function buildLcarSelectScreen(self){
		var l_button_html = buildLcarSelectionButtonsTable(globals.House.HouseObj.Lights, 'handleMenuOnClick');
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
	 * @param self is    <"Instance" of undefined.lights.LightsWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function handleMenuOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.House.LightIx = l_ix;
		globals.House.LightName = l_name;
		if (l_ix <= 1000) {  // we clicked on one of the buttons, show the details for the light.
			var l_obj = globals.House.HouseObj.Lights[l_ix];
			globals.House.LightObj = l_obj;
			globals.House.Self = self;
			showDataEntryFields(self);
			self.buildLcarDataEntryScreen(l_obj, 'handleDataEntryOnClick');
		} else if (l_ix == 10001) {  // The "Add" button
			showDataEntryFields(self);
			var l_ent = self.createEntry();
			self.buildLcarDataEntryScreen(l_ent, 'handleDataEntryOnClick');
		} else if (l_ix == 10002) {  // The "Back" button
			self.showWidget('HouseMenu');
		}
	},



// ============================================================================
	/**
	 * Build a screen full of data entry fields.
	 */
	function buildLcarDataEntryScreen(self, p_entry, p_handler){
		var l_obj = arguments[1];
		var l_html = build_lcars_top('Enter Light Data', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(40, self.buildEntry(l_obj, p_handler));
		l_html += build_lcars_bottom();
		self.nodeById('DataEntryDiv').innerHTML = l_html;
	},
	function buildEntry(self, p_obj, p_handler, p_onchange) {
		var p_html = buildBaseEntry(self, p_obj);
		p_html = buildLightingCoreEntry(self, p_obj, p_html, p_onchange);
		p_html = self.buildLightEntry(p_obj, p_html);
		if (p_obj.ControllerFamily === 'Insteon')
			p_html = buildInsteonPart(self, p_obj, p_html);
		else if (p_obj.ControllerFamily === 'UPB')
        	p_html = buildUpbPart(self, p_obj, p_html);
		else
			Divmod.debug('---', 'ERROR - lights.buildAllParts() Family = ' + p_obj.ControllerFamily);
		p_html += buildLcarEntryButtons(p_handler);
		return p_html;
	},
	function buildLightEntry(self, p_obj, p_html, p_onchange) {
		return p_html;
	},
	function familyChanged() {
		var l_obj = globals.House.LightObj;
		var l_self = globals.House.Self;
		var l_family = fetchSelectWidget(l_self, 'Family');
		l_obj.ControllerFamily = l_family;
		l_self.buildLcarDataEntryScreen(l_obj, 'handleDataEntryOnClick');
	},
 	/**
	 * Fetch the data we put out and the user updated.
	 */
	function fetchEntry(self) {
		var l_data = fetchBaseEntry(self, l_data);
		l_data = fetchLightingCoreEntry(self, l_data);
		l_data = self.fetchLightEntry(l_data);
        if (l_data.ControllerFamily === 'Insteon')
        	l_data = fetchInsteonEntry(self, l_data);
        if (l_data.ControllerFamily === 'UPB')
        	l_data = fetchUpbEntry(self, l_data);
		return l_data;
	},
    function fetchLightEntry(self, p_data) {
    	return p_data;
    },
	function createEntry(self) {
		// Divmod.debug('---', 'lights.createEntry() was called.');
		var l_data = createBaseEntry(self, l_data);
		l_data = createLightingCoreEntry(self, l_data);
		l_data = self.createLightEntry(l_data);
        if (l_data.ControllerFamily === 'Insteon')
        	l_data = createInsteonEntry(self, l_data);
        if (l_data.ControllerFamily === 'UPB')
        	l_data = createUpbEntry(self, l_data);
        return l_data;
	},
    function createLightEntry(self, p_data) {
    	return p_data;
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
		function eb_handleDataEntryOnClick(res){
			Divmod.debug('---', 'lights.eb_handleDataEntryOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry());
	        var l_defer = self.callRemote("saveLightData", l_json);
			l_defer.addCallback(cb_handleDataEntryOnClick);
			l_defer.addErrback(eb_handleDataEntryOnClick);
			break;
		case '10002':  // Back button
			showSelectionButtons(self);
			break;
		case '10004':  // Delete button
			var l_obj = self.fetchEntry();
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
        return false;  // false stops the chain.
	}
);
//Divmod.debug('---', 'lights.handleDataEntryOnClick(Change) was called.');
//console.log("lights.handleDataEntryOnClick()  json  %O", l_json);
//### END DBK
