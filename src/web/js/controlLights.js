/* controlLights.js
 * 
 * Displays the schedules
 */

// import Nevow.Athena
// import globals
// import helpers


helpers.Widget.subclass(controlLights, 'ControlLightsWidget').methods(

	function __init__(self, node) {
		controlLights.ControlLightsWidget.upcall(self, '__init__', node);
	},

	/**
	 * 
	 * @param self is    <"Instance" of undefined.controlLights.ControlLightsWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		
		function cb_widgetready(res) {
			// do whatever initialization needs here, 'show' for the widget is handled in superclass
			//Divmod.debug('---', 'controlLights.cb_widgready() was called. res = ' + res);
			self.hideWidget();
		}
	
		//Divmod.debug('---', 'controlLights.ready() was called. ' + self);
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},

	/**
	 * routines for showing and hiding parts of the screen.
	 */
	function showWidget(self) {
		Divmod.debug('---', 'controlLights.showWidget() was called.');
		self.node.style.display = 'block';
		self.showButtons(self);
		self.hideEntry(self);
		self.fetchLightData(self, globals.House.HouseIx);
	},
	function hideButtons(self) {
		Divmod.debug('---', 'controlLights.hideButtons() was called. ');
		self.nodeById('ControlLightButtonsDiv').style.display = 'none';		
	},
	function showButtons(self) {
		Divmod.debug('---', 'controlLights.showButtons() was called. ');
		self.nodeById('ControlLightButtonsDiv').style.display = 'block';	
	},
	function hideEntry(self) {
		//Divmod.debug('---', 'controlLights.hideEntry() was called. ');
		self.nodeById('ControlLightEntryDiv').style.display = 'none';		
	},
	function showEntry(self) {
		//Divmod.debug('---', 'controlLights.showEntry() was called. ');
		self.nodeById('ControlLightEntryDiv').style.display = 'block';		
	},

	// ============================================================================
	/**
	 * This triggers getting the lights data from the server.
	 * The server calls displayLightsButtons with the lights info.
	 * 
	 * @param p_houseIndex is the house index that was selected
	 */
	function fetchLightData(self, p_houseIndex) {
		function cb_fetchLightData(self, p_json, p2) {
			Divmod.debug('---', 'controlLights.cb_fetchLightData() was called. ' + p_json + ' ' + p2);
		}
		function eb_fetchLightData(self, p1, p2) {
			Divmod.debug('---', 'controlLights.eb_fetchLightData() was called. ' + p1 + ' ' + p2);
		}
        var l_defer = self.callRemote("getControlLightEntries", globals.House.HouseIx);  // call server @ web_controlLights.py
		l_defer.addCallback(cb_fetchLightData);
		l_defer.addErrback(eb_fetchLightData);
        return false;
	},

	/**
	 * Fill in the schedule entry screen with all of the data for this schedule.
	 */
	function fillEntry(self, p_entry) {
		var sched = arguments[1];
		Divmod.debug('---', 'controlLights.fillEntry() was called. ' + sched);
		self.nodeById('Name').value = sched.Name;
		self.nodeById('Key').value = sched.Key;
		self.nodeById('Active').value = sched.Active;
		self.nodeById('Type').value = sched.Type;
		self.nodeById('Time').value = sched.Time;
		self.nodeById('Level').value = sched.Level;
		self.nodeById('Rate').value = sched.Rate;
		self.nodeById('RoomName').value = sched.RoomName;
		self.nodeById('LightName').value = sched.LightName;
	},
	
	function fetchEntry(self) {
        var l_scheduleData = {
			Name : self.nodeById('Name').value,
			Key : self.nodeById('Key').value,
			Active : self.nodeById('Active').value,
			Type : self.nodeById('Type').value,
			Time : self.nodeById('Time').value,
			Level : self.nodeById('Level').value,
			Rate : self.nodeById('Rate').value,
			RoomName : self.nodeById('RoomName').value,
			LightName : self.nodeById('LightName').value,
			HouseIx : globals.House.HouseIx
            }
		return l_scheduleData;
	},

	/**
	 * Event handler for light selection buttons.
	 * 
	 * The user can click on a light button, the "Add" button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.lights.LightsWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function doHandleOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.House.LightIx = l_ix;
		globals.House.LightName = l_name;
		if (l_ix <= 1000) {
			// One of the schedule buttons.
			var l_obj = globals.House.HouseObj.Lights[l_ix];
			globals.House.LightsObj = l_obj;
			Divmod.debug('---', 'controlLights.doHandleOnClick(1) was called. ' + l_ix + ' ' + l_name);
			console.log("controlLights.doHandleOnClick() - l_obj = %O", l_obj);
			self.showEntry();
			self.hideButtons();
			self.fillEntry(l_obj);
		} else if (l_ix == 10002) {
			// The "Back" button
			self.hideWidget();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget();
		}
	},
	
	/**
	 * Event handler for submit buttons at bottom of entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function doHandleSubmit(self, p_node) {
		Divmod.debug('---', 'controlLights.doHandleSubmit() was called. ');
		console.log("controlLights.doHandleSubmit() - self %O", self);
		console.log("controlLights.doHandleSubmit() - node %O", p_node);
		
		function cb_doHandleSubmit(p_json) {
			Divmod.debug('---', 'controlLights.cb_doHandleSubmit() was called.');
			self.showWidget(self);
		}
		function eb_doHandleSubmit(res){
			Divmod.debug('---', 'controlLights.eb_doHandleSubmit() was called. res=' + res);
		}
    	var l_json = JSON.stringify(self.fetchEntry(self));
		Divmod.debug('---', 'controlLights.doHandleSubmit(1) was called. json:' + l_json);
        var l_defer = self.callRemote("doLightsSubmit", l_json);  // @ web_lights
		l_defer.addCallback(cb_doHandleSubmit);
		l_defer.addErrback(eb_doHandleSubmit);
		// return false stops the resetting of the server.
        return false;
	},

	// ============================================================================
	/**
	 * Pushed from the server. fill in the table and wait for an event to happen (doHandleOnClick).
	 */
	function displayControlLightButtons(self, p_json) {
		Divmod.debug('---', 'controlLights.displayControlLightsButtons(1) was called. ');
		globals.House.HouseObj.Lights = JSON.parse(p_json);
		var l_tab = buildTable(self, globals.House.HouseObj.Lights, '');
		self.nodeById('ControlLightsTableDiv').innerHTML = l_tab;
	}
);
//### END DBK

