/**
 * @name:      PyHouse/src/Modules/Web/js/thermostats.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2016 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created on Sep 03, 2014
 * @summary:   Displays the thermostat element
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
	 * @param self is    <"Instance" of undefined.thermostats.ThermostatsWidget>
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
	function buildLcarSelectScreen(self){
		var l_thermostat_html = buildLcarSelectionButtonsTable(globals.House.Hvac.Thermostats, 'handleSelectButtonOnClick');
		var l_html = build_lcars_top('Thermostats', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(10, l_thermostat_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
	/**
	 * This triggers getting the Thermostat data from the server.
	 * The server calls displayThermostatButtons with the Thermostat info.
	 */
	function fetchDataFromServer(self) {
		function cb_fetchDataFromServer(p_json) {
			globals.House = JSON.parse(p_json);
			self.buildLcarSelectScreen();
		}
		function eb_fetchDataFromServer(res) {
			Divmod.debug('---', 'thermostats.eb_fetchDataFromServer() was called. ERROR: ' + res);
		}
        var l_defer = self.callRemote("getHouseData");  // call server @ web_thermostat.py
		l_defer.addCallback(cb_fetchDataFromServer);
		l_defer.addErrback(eb_fetchDataFromServer);
        return false;
	},
	/**
	 * Event handler for Thermostat selection buttons.
	 * 
	 * The user can click on a thermostat button, the "Add" button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.thermostats.ThermostatsWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function handleSelectButtonOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.House.ThermostatIx = l_ix;
		globals.House.ThermostatName = l_name;
		globals.Add = false;
		// Divmod.debug('---', 'thermostats.handleSelectButtonOnClick() was called. Ix = ' + l_ix);
		if (l_ix <= 1000) {  // One of the Thermostat buttons.
			showDataEntryScreen(self);
			var l_obj = globals.House.Hvac.Thermostats[l_ix];
			globals.House.ThermostatObj = l_obj;
			globals.House.Self = self;
			globals.Add = false;
			self.buildLcarDataEntryScreen(l_obj, 'handleDataOnClick');
		} else if (l_ix == 10001) {  // The "Add" button
			showDataEntryScreen(self);
			var l_obj = self.createEntry();
			globals.House.Self = self;
			globals.Add = true;
			// console.log("thermostats.handleSelectButtonOnClick() - l_obj = %O", l_obj);
			self.buildLcarDataEntryScreen(l_obj, 'handleDataOnClick');
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
		var l_html = build_lcars_top('Thermostat Data', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(35, self.buildEntry(l_obj, p_handler));
		l_html += build_lcars_bottom();
		self.nodeById('DataEntryDiv').innerHTML = l_html;
	},
	function buildEntry(self, p_obj, p_handler, p_onchange){
		var l_html = buildBaseEntry(self, p_obj);
		// l_html = buildLightingCoreEntry(self, p_obj, l_html, p_onchange);
		l_html = self.buildThermostatEntry(p_obj, l_html);
		if (p_obj.DeviceFamily === 'Insteon')
			l_html = buildInsteonPart(self, p_obj, l_html);
		else if (p_obj.DeviceFamily === 'UPB')
        	l_html = buildUpbPart(self, p_obj, l_html);
		else
			Divmod.debug('---', 'ERROR - thermostats.buildEntry() Unknown Family = ' + p_obj.DeviceFamily);
		l_html += buildLcarEntryButtons(p_handler);
		return l_html;
	},
	function buildThermostatEntry(self, p_obj, p_html, p_onchange){
		p_html += buildLcarTextWidget(self, 'Comment', 'Comment', p_obj.Comment);
		p_html += buildLcarRoomSelectWidget(self, 'RoomName', 'Room', p_obj.RoomName);
		p_html += buildLcarLightTypeSelectWidget(self, 'Type', 'Type', p_obj.LightingType, 'disabled');
		p_html += buildLcarFamilySelectWidget(self, 'DeviceFamily', 'Family', p_obj.DeviceFamily, 'familyChanged');
		p_html += buildLcarHvacSliderWidget(self, 'CoolSetting', 'Cool', p_obj.CoolSetPoint, 'handleSliderChangeCool');
		p_html += buildLcarHvacSliderWidget(self, 'HeatSetting', 'Heat', p_obj.HeatSetPoint, 'handleSliderChangeHeat');
		return p_html;
	},
	function handleSliderChangeCool(p_event){
		// Divmod.debug('---', 'thermostats.handleSliderChangeCool() was called.');
		var l_obj = globals.House.ThermostatObj;
		var l_self = globals.House.Self;
		var l_level = fetchSliderWidget(l_self, 'CoolSetting');
		updateSliderBoxValue(l_self, 'CoolSetting', l_level);
	},
	function handleSliderChangeHeat(p_event){
		// Divmod.debug('---', 'thermostats.handleSliderChangeHeat() was called.');
		var l_obj = globals.House.ThermostatObj;
		var l_self = globals.House.Self;
		var l_level = fetchSliderWidget(l_self, 'HeatSetting');
		updateSliderBoxValue(l_self, 'HeatSetting', l_level);
	},
	function familyChanged() {
		var l_obj = globals.House.ThermostatObj;
		var l_self = globals.House.Self;
		l_obj.DeviceFamily = fetchSelectWidget(l_self, 'Family');;
		l_self.buildLcarDataEntryScreen(l_obj, 'handleDataOnClick');
	},



// ============================================================================
	function fetchEntry(self) {
		var l_data = fetchBaseEntry(self);
		l_data = self.fetchThermostatEntry(l_data);
        if (l_data.DeviceFamily === 'Insteon')
        	l_data = fetchInsteonEntry(self, l_data);
        if (l_data.DeviceFamily === 'UPB')
        	l_data = fetchUpbEntry(self, l_data);
		return l_data;
	},
	function fetchThermostatEntry(self, p_data) {
	    p_data.Comment = fetchTextWidget(self, 'Comment');
	    p_data.RoomName = fetchTextWidget(self, 'RoomName');
	    p_data.LightingType = 'Thermostat';
	    p_data.DeviceFamily = fetchSelectWidget(self, 'DeviceFamily');
		p_data.CoolSetPoint = fetchSliderWidget(self, 'CoolSetting');
		p_data.HeatSetPoint = fetchSliderWidget(self, 'HeatSetting');
		return p_data;
	},
	function createEntry(self) {
		var l_data = createBaseEntry(self, Object.keys(globals.House.Hvac.Thermostats).length);
		l_data = createLightingCoreEntry(self, l_data);
		l_data.DeviceFamily = "Insteon";
		l_data = self.createThermostatEntry(l_data);
        if (l_data.DeviceFamily === 'Insteon')
        	l_data = createInsteonEntry(self, l_data);
        if (l_data.DeviceFamily === 'UPB')
        	l_data = createUpbEntry(self, l_data);
        return l_data;
	},
	function createThermostatEntry(self, p_data) {
	    p_data.Comment = '';
	    p_data.RoomName = '';
	    p_data.LightingType = 'Thermostat';
		p_data.CoolSetPoint = 78;
		p_data.HeatSetPoint = 70;
		// Divmod.debug('---', 'thermostats.createThermostatEntry() was called.');
		// console.log("thermostats.createThermostatEntry() - p_data = %O", p_data);
		return p_data;
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
		function eb_handleDataOnClick(res){
			Divmod.debug('---', 'thermostats.eb_handleDataOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		var l_defer;
		var l_json;
		//Divmod.debug('---', 'thermostats.handleDataOnClick() was called. Node:' + l_ix);
		switch(l_ix) {
		case '10003':  // Add/Change Button
	    	l_json = JSON.stringify(self.fetchEntry());
	        l_defer = self.callRemote("saveThermostatsData", l_json);  // @ web_thermostat
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
	        l_defer = self.callRemote("saveThermostatsData", l_json);  // @ web_rooms
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		default:
			break;
		}
        return false;  // false stops the chain.
	}
);
// Divmod.debug('---', 'thermostats.startWidget() was called.');
// console.log("thermostats.handleSelectButtonOnClick() - l_obj = %O", l_obj);
//### END DBK
