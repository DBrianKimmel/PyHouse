/**
 * lights.js
 * 
 * The lights widget.
 */

// import Nevow.Athena
// import globals
// import helpers

/**
 * The lights widget.
 */
helpers.Widget.subclass(lights, 'LightsWidget').methods(

    function __init__(self, node) {
		//Divmod.debug('---', 'lights.__init__() was called. - self=' + self + "  node=" + node);
        lights.LightsWidget.upcall(self, "__init__", node);
		globals.Lights.Selected = {};
    },

	function ready(self) {
		function cb_widgetready(res) {
			//Divmod.debug('---', 'lights.js - cb_widgready was called.');
			self.hideWidget();
		}
		//Divmod.debug('---', 'lights.ready() was called.');
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},

	function hideWidget(self) {
		//Divmod.debug('---', 'lights.hideLights() was called.');
		self.node.style.display = 'none';
	},

	/**
	 * routines for showing and hiding parts of the screen.
	 */
	function showWidget(self) {
		//Divmod.debug('---', 'lights.showWidget() was called.');
		self.node.style.display = 'block';
		self.showButtons(self);
		self.hideEntry(self);
		self.fetchLightData(self, globals.SelectedHouse.Ix);
	},
	function hideButtons(self) {
		//Divmod.debug('---', 'lights.hideButtons() was called. ');
		self.nodeById('LightButtonsDiv').style.display = 'none';		
	},
	function showButtons(self) {
		//Divmod.debug('---', 'lights.showButtons() was called. ');
		self.nodeById('LightButtonsDiv').style.display = 'block';	
	},
	function hideEntry(self) {
		//Divmod.debug('---', 'lights.hideEntry() was called. ');
		self.nodeById('LightEntryDiv').style.display = 'none';		
	},
	function showEntry(self) {
		//Divmod.debug('---', 'lights.showEntry() was called. ');
		self.nodeById('LightEntryDiv').style.display = 'block';		
	},

	// ============================================================================
	/**
	 * This triggers getting the lights data from the server.
	 * The server calls displayLightsButtons with the lights info.
	 * 
	 * @param p_houseIndex is the house index that was selected
	 */
	function fetchLightData(self, p_houseIndex) {
		function cb_fetchLightData(p_json) {
			//Divmod.debug('---', 'lights.cb_fetchLightData() was called. ' + p_json);
			globals.Lights.Obj = JSON.parse(p_json);
			var l_tab = buildTable(self, globals.Lights.Obj, '');
			self.nodeById('LightTableDiv').innerHTML = l_tab;
		}
		function eb_fetchLightData(res) {
			//Divmod.debug('---', 'lights.eb_fetchLightData() was called. ERR = ' + res);
		}
        var l_defer = self.callRemote("getLightData", globals.SelectedHouse.Ix);  // call server @ web_lights.py
		l_defer.addCallback(cb_fetchLightData);
		l_defer.addErrback(eb_fetchLightData);
        return false;
	},

	/**
	 * Fill in the schedule entry screen with all of the data for this schedule.
	 * 
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  Name: <input type="text" name="Name" value="test_light2" />\n';
	ret = ret + '    <br />\n';
	ret = ret + '  Address: <input type="text" name="Address" value="CC:11:22" /><br />\n';
	ret = ret + '  Family: <input type="text" name="Family" value="Insteon" /><br />\n';
	ret = ret + '  Type: <input type="text" name="Type" value="WSLD" /><br />\n';
	ret = ret + '  <input type="hidden" name="Controller" value="False" />\n';
	ret = ret + '  <input type="hidden" name="Dimmable" value="False" />\n';
	ret = ret + '  <input type="hidden" name="Coords" value="0,0" />\n';
	ret = ret + '  <input type="hidden" name="Master" value="False" />\n';
	ret = ret + '  <input type="hidden" name="CurLevel" value="0" />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="AddLight" />\n';
	ret = ret + '</form>\n';
	 *
	 */
	function fillEntry(self, p_entry) {
		var sched = arguments[2];
		//Divmod.debug('---', 'lights.fillEntry() was called. ' + sched);
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
			HouseIx : globals.SelectedHouse.Ix
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
		globals.Lights.Selected.Ix = l_ix;
		globals.Lights.Selected.Name = l_name;
		if (l_ix <= 1000) {
			// One of the schedule buttons.
			var l_obj = globals.Lights.Obj[l_ix];
			globals.Lights.Selected.LightsObj = l_obj;
			//Divmod.debug('---', 'lights.doHandleOnClick(1) was called. ' + l_ix + ' ' + l_name);
			console.log("lights.doHandleOnClick() - l_obj = %O", l_obj);
			self.showEntry(self);
			self.hideButtons(self);
			self.fillEntry(self, l_obj);
		} else if (l_ix == 10001) {
			// The "Add" button
			self.showEntry(self);
			self.hideButtons(self);
		} else if (l_ix == 10002) {
			// The "Back" button
			self.hideWidget();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget(self);
		}
	},
	
	/**
	 * Event handler for submit buttons at bottom of entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function doHandleSubmit(self, p_node) {
		//Divmod.debug('---', 'lights.doHandleSubmit() was called. ');
		//console.log("lights.doHandleSubmit() - self %O", self);
		//console.log("lights.doHandleSubmit() - node %O", p_node);
		
		function cb_doHandleSubmit(p_json) {
			//Divmod.debug('---', 'lights.cb_doHandleSubmit() was called.');
			self.showWidget(self);
		}
		function eb_doHandleSubmit(res){
			//Divmod.debug('---', 'lights.eb_doHandleSubmit() was called. res=' + res);
		}
    	var l_json = JSON.stringify(self.fetchEntry(self));
		//Divmod.debug('---', 'lights.doHandleSubmit(1) was called. json:' + l_json);
        var l_defer = self.callRemote("doLightsSubmit", l_json);  // @ web_lights
		l_defer.addCallback(cb_doHandleSubmit);
		l_defer.addErrback(eb_doHandleSubmit);
		// return false stops the resetting of the server.
        return false;
	}
);
//### END DBK
