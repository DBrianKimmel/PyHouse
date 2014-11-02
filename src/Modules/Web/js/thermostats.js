/**
 * @name: PyHouse/src/Modules/Web/js/thermostats.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Mar 11, 2014
 * @summary: Displays the thermostat element
 *
 */
// import Nevow.Athena
// import globals
// import helpers



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
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	/**
	 * routines for showing and hiding parts of the screen.
	 */
	function showWidget(self) {
		self.node.style.display = 'block';
		self.showSelectionButtons();
		self.hideDataEntry();
		self.fetchHouseData();
	},
	function hideSelectionButtons(self) {
		self.nodeById('SelectionButtonsDiv').style.display = 'none';
	},
	function showSelectionButtons(self) {
		self.nodeById('SelectionButtonsDiv').style.display = 'block';
	},
	function hideDataEntry(self) {
		self.nodeById('DataEntryDiv').style.display = 'none';
	},
	function showDataEntry(self) {
		self.nodeById('DataEntryDiv').style.display = 'block';
	},


// ============================================================================
	/**
	 * Build a screen full of buttons - One for each room and some actions.
	 */
	function buildLcarSelectScreen(self){
		var l_thermostat_html = buildLcarSelectionButtonsTable(globals.House.HouseObj.Thermostats, 'handleMenuOnClick');
		var l_html = build_lcars_top('Thermostats', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(2, l_thermostat_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
	/**
	 * This triggers getting the Thermostat data from the server.
	 * The server calls displayThermostatButtons with the Thermostat info.
	 */
	function fetchHouseData(self) {
		function cb_fetchHouseData(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
			self.buildLcarSelectScreen()
		}
		function eb_fetchHouseData(res) {
			Divmod.debug('---', 'thermostats.eb_fetchHouseData() was called. ERROR: ' + res);
		}
        var l_defer = self.callRemote("getHouseData");  // call server @ web_thermostat.py
		l_defer.addCallback(cb_fetchHouseData);
		l_defer.addErrback(eb_fetchHouseData);
        return false;
	},
	/**
	 * Event handler for Thermostat selection buttons.
	 * 
	 * The user can click on a room button, the "Add" button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.schedules.SchedulesWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function handleMenuOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.House.RoomIx = l_ix;
		globals.House.RoomName = l_name;
		if (l_ix <= 1000) {  // One of the Thermostat buttons.
			var l_obj = globals.House.HouseObj.Thermostats[l_ix];
			globals.House.ThermostatObj = l_obj;
			self.showDataEntry();
			self.hideSelectionButtons();
			self.fillEntry(l_obj);
		} else if (l_ix == 10001) {  // The "Add" button
			self.showDataEntry();
			self.hideSelectionButtons();
			var l_ent = self.createEntry();
			self.fillEntry(l_ent);
		} else if (l_ix == 10002) {  // The "Back" button
			self.hideWidget();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget();
		}
	},


	// ============================================================================
	/**
	 * Build a screen full of data entry fields.
	 */
	function buildLcarDataEntryScreen(self, p_entry, p_handler){
		// console.log("rooms.buildLcarDataEntryScreen() - self = %O", self);
		var l_thermostat = arguments[1];
		var l_entry_html = "";
		l_entry_html += buildLcarTextWidget(self, 'Name', 'Thermostat Name', l_thermostat.Name);
		l_entry_html += buildLcarTextWidget(self, 'Key', 'Index', l_thermostat.Key, 'disable');
		l_entry_html += buildLcarTrueFalseWidget(self, 'ThermostatActive', 'Active ?', l_thermostat.Active);
		l_entry_html += buildLcarTextWidget(self, 'UUID', 'UUID', l_thermostat.UUID, 'disable');
		l_entry_html += buildLcarFamilySelectWidget(self, 'ControllerFamily', 'Family', l_thermostat.ControllerFamily);
		l_entry_html += buildLcarHvacSliderWidget(self, 'CoolSetting', 'Cool', l_thermostat.CoolSetPoint, 'handleSliderChangeCold');
		l_entry_html += buildLcarHvacSliderWidget(self, 'HeatSetting', 'Heat', l_thermostat.HeatSetPoint, 'handleSliderChangeHot');
		l_entry_html += buildLcarEntryButtons(p_handler);
		var l_html = build_lcars_top('Enter Thermostat Data', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(15, l_entry_html);
		l_html += build_lcars_bottom();
		self.nodeById('DataEntryDiv').innerHTML = l_html;
	},
	function handleSliderChangeCold(p_event){
		var l_obj = globals.House.ThermostatObj;
		var l_self = globals.House.Self;
		var l_level = fetchSliderWidget(l_self, 'HeatSetting');
		updateSliderBoxValue(l_self, 'HeatSetting', l_level)
	},
	function handleSliderChangeHot(p_event){
		var l_obj = globals.House.ThermostatObj;
		var l_self = globals.House.Self;
		var l_level = fetchSliderWidget(l_self, 'HeatSetting');
		updateSliderBoxValue(l_self, 'HeatSetting', l_level)
	},
	/**
	 * Fill in the dynamic dns part of the compound entry screen with all of the data for this schedule.
	 * 
	 */
	function fillEntry(self, p_entry, p_ix) {
		Divmod.debug('---', 'thermostats.fillEntry() was called.  Ix:' + p_ix);
		self.buildLcarDataEntryScreen(p_entry, 'handleDataOnClick')
	},
	function fetchEntry(self) {
		Divmod.debug('---', 'thermostats.fetchEntry() was called. ');
        var l_data = {
            Name      : fetchTextWidget(self, 'Name'),
            Key       : fetchTextWidget(self, 'Key'),
			Active    : fetchTrueFalseWidget(self, 'ThermostatActive'),
			UUID      : fetchTextWidget(self, 'UUID'),
			ControllerFamily : fetchSelectWidget(self, 'ControllerFamily'),
			CoolSetPoint : fetchSliderWidget(self, 'CoolSetting'),
			HeatSetPoint : fetchSliderWidget(self, 'HeatSetting'),
			Delete : false
            };
		return l_data;
	},
	function createEntry(self, p_ix) {
		Divmod.debug('---', 'thermostats.createEntry() was called.  Ix: ' + p_ix);
		var l_key = 0;
		if (globals.House.HouseObj.Thermostats !== 'undefined')
			l_key = Object.keys(globals.House.HouseObj.Thermostats).length
        var l_Data = {
    			Name : 'Change Me',
    			Key : l_key,
    			Active : false,
    			ControllerFamily : 'Insteon',
    			CoolSetPoint : 75,
    			HeatSetPoint : 65,
    			Delete : false
                };
		return l_Data;
	},


	// ============================================================================
	/**
	 * Event handler for thermostat selection buttons.
	 * 
	 * The user can click on a thermostat button, the "Add" button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.thermostats.ThermostatWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function handleMenuOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.House.ThermostatIx = l_ix;
		globals.House.ThermostatName = l_name;
		if (l_ix <= 1000) {
			// One of the Thermostat buttons.
			var l_obj = globals.House.HouseObj.Thermostat;
			Divmod.debug('---', 'thermostats.handleMenuOnClick("Thermostat" Button) was called. ' + l_ix + ' ' + l_name);
			//console.log("thermostats.handleMenuOnClick() - l_obj = %O", l_obj);
			self.showDataEntry();
			//self.hideSelectionButtons();
			self.fillEntry(l_obj, l_ix);
		} else if (l_ix == 10001) {
			// The "Add" button
			Divmod.debug('---', 'thermostats.handleMenuOnClick(Add Button) was called. ' + l_ix + ' ' + l_name);
			self.showDataEntry();
			self.hideSelectionButtons();
			var l_ent = self.createEntry(globals.House.ThermostatIx);
			self.fillEntry(l_ent);
		} else if (l_ix == 10002) {
			// The "Back" button
			Divmod.debug('---', 'thermostats.handleMenuOnClick(Back Button) was called. ' + l_ix + ' ' + l_name);
			self.hideWidget();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget();
		}
	},


	// ============================================================================
	/**
	 * Event handler for buttons at bottom of the data entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataOnClick(self, p_node) {
		function cb_handleDataOnClick(p_json) {
			//Divmod.debug('---', 'thermostats.cb_handleDataOnClick() was called.');
			self.showWidget();
		}
		function eb_handleDataOnClick(res){
			Divmod.debug('---', 'thermostats.eb_handleDataOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		//Divmod.debug('---', 'thermostats.handleDataOnClick() was called. Node:' + l_ix);
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry());
	        var l_defer = self.callRemote("saveThermostatsData", l_json);  // @ web_thermostat
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			self.hideDataEntry();
			self.showSelectionButtons();
			break;
		case '10004':  // Delete button
			var l_obj = self.fetchEntry();
			l_obj['Delete'] = true;
	    	var l_json = JSON.stringify(l_obj);
	        var l_defer = self.callRemote("saveThermostatsData", l_json);  // @ web_rooms
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		default:
			break;
		}
        return false;  // false stops the chain.
	}
);
//Divmod.debug('---', 'thermostats.handleDataOnClick() was called. Node:' + l_ix);
//console.log("thermostats.handleMenuOnClick() - l_obj = %O", l_obj);
//### END DBK
