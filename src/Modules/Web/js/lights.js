 /**
 * @name:      PyHouse/src/Modules/Web/js/lights.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2016 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created on Mar 11, 2014
 * @summary:   Displays the lights
 */

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
	/**
	 * Build a screen full of buttons - One for each light and some actions.
	 */
	function buildLcarSelectScreen(self){
		var l_button_html = buildLcarSelectionButtonsTable(globals.House.Lighting.Lights, 'handleMenuOnClick');
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
        var l_obj;
		globals.House.LightIx = l_ix;
		globals.House.LightName = l_name;
		globals.Add = false;
		if (l_ix <= 1000) {  // we clicked on one of the buttons, show the details for the light.
			showDataEntryScreen(self);
			l_obj = globals.House.Lighting.Lights[l_ix];
			// console.log("lights.handleMenuOnClick()  Light  %O", l_obj);
			globals.House.LightObj = l_obj;
			try {
				l_obj.RoomName = globals.House.Rooms[l_obj.RoomName].Name;
			}
			catch(err) {
				l_obj.RoomName = l_obj.RoomName;
			}
			globals.House.Self = self;
			self.buildLcarDataEntryScreen(l_obj, 'change', 'handleDataEntryOnClick');
		} else if (l_ix == 10001) {  // The "Add" button
			showDataEntryScreen(self);
			l_obj = self.createEntry();
			globals.House.ControllerObj = l_obj;
			globals.House.Self = self;
			globals.Add = true;
			self.buildLcarDataEntryScreen(l_obj, 'add', 'handleDataEntryOnClick');
		} else if (l_ix == 10002) {  // The "Back" button
			self.showWidget('HouseMenu');
		}
	},


// ============================================================================
	/**
	 * Build a screen full of data entry fields.
	 */
	function buildLcarDataEntryScreen(self, p_entry, p_add_change, p_handler){
		var l_obj = arguments[1];
		var l_html = build_lcars_top('Light Data', 'lcars-salmon-color');
		// console.log("lights.buildLcarDataEntryScreen()  Light  %O", l_obj);
		l_html += build_lcars_middle_menu(40, self.buildEntry(l_obj, p_add_change, p_handler));
		l_html += build_lcars_bottom();
		self.nodeById('DataEntryDiv').innerHTML = l_html;
	},
	function buildEntry(self, p_obj, p_add_change, p_handler, p_onchange) {
		var l_html = buildBaseEntry(self, p_obj);
		l_html = buildLightingCoreEntry(self, p_obj, l_html, p_onchange);
		l_html = self.buildLightEntry(p_obj, l_html);
		if (p_obj.DeviceFamily === 'Insteon')
			l_html = buildInsteonPart(self, p_obj, l_html);
		else if (p_obj.DeviceFamily === 'UPB')
        	l_html = buildUpbPart(self, p_obj, l_html);
		else
			Divmod.debug('---', 'ERROR - lights.buildEntry() Unknown Family = ' + p_obj.DeviceFamily);
		l_html += buildLcarEntryButtons(p_handler, 1);
		return l_html;
	},
	function buildLightEntry(self, p_obj, p_html, p_onchange) {
		return p_html;
	},
	function familyChanged() {
		var l_obj = globals.House.LightObj;
		var l_self = globals.House.Self;
		var l_family = fetchSelectWidget(l_self, 'Family');
		l_obj.DeviceFamily = l_family;
		l_self.buildLcarDataEntryScreen(l_obj, 'handleDataEntryOnClick');
	},
 	/**
	 * Fetch the data we put out and the user updated.
	 */
	function fetchEntry(self) {
		var l_data = fetchBaseEntry(self);
		l_data = fetchLightingCoreEntry(self, l_data);
		l_data = self.fetchLightEntry(l_data);
        if (l_data.DeviceFamily === 'Insteon')
        	l_data = fetchInsteonEntry(self, l_data);
        if (l_data.DeviceFamily === 'UPB')
        	l_data = fetchUpbEntry(self, l_data);
		return l_data;
	},
    function fetchLightEntry(self, p_data) {
    	return p_data;
    },
	function createEntry(self) {
    	var l_ix = 0;
    	try {
    		l_ix = Object.keys(globals.House.Lighting.Lights).length;
    	}
    	catch(e_err) {
    		Divmod.debug('---', 'ERROR lights.createEntry() ' + e_err);
    		l_ix = 0;
    	}
    	
		var l_data = createBaseEntry(self, l_ix);
		Divmod.debug('---', 'lights.createEntry() was called ' + l_ix);
		l_data = createLightingCoreEntry(self, l_data);
		l_data = self.createLightEntry(l_data);
        if (l_data.DeviceFamily === 'Insteon')
        	l_data = createInsteonEntry(self, l_data);
        if (l_data.DeviceFamily === 'UPB')
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
		var l_obj = self.fetchEntry();
		var l_json = '';
		var l_defer = '';
		l_obj.Add = globals.Add;
		switch(l_ix) {
		case '10003':  // Change/Save Button
	    	var l_json = JSON.stringify(l_obj);
	        var l_defer = self.callRemote("saveLightData", l_json);
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
        return false;  // false stops the chain.
	}
);
// Divmod.debug('---', 'lights.handleDataEntryOnClick(Change) was called.');
// console.log("lights.handleDataEntryOnClick()  json  %O", l_json);
// ### END DBK
