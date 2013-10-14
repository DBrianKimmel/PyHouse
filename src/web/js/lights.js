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
    },

	/**
     * Place the widget in the workspace.
	 * 
	 * @param self is    <"Instance" of undefined.lights.LightsWidget>
	 * @returns a deferred
	 */
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

	/**
	 * routines for showing and hiding parts of the screen.
	 */
	function showWidget(self) {
		//Divmod.debug('---', 'lights.showWidget() was called.');
		self.node.style.display = 'block';
		self.showButtons();
		self.hideEntry();
		self.fetchLightData(self, globals.House.HouseIx);
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
	 */
	function fetchLightData(self) {
		function cb_fetchLightData(p_json) {
			//Divmod.debug('---', 'lights.cb_fetchLightData() was called. ' + p_json);
			globals.House.HouseObj.Lights = JSON.parse(p_json);
			var l_tab = buildTable(globals.House.HouseObj.Lights, 'handleMenuOnClick');
			self.nodeById('LightTableDiv').innerHTML = l_tab;
		}
		function eb_fetchLightData(res) {
			Divmod.debug('---', 'lights.eb_fetchLightData() was called. ERROR: ' + res);
		}
		//Divmod.debug('---', 'lights.fetchLightData() was called. ');
        var l_defer = self.callRemote("getLightData", globals.House.HouseIx);  // call server @ web_lights.py
		l_defer.addCallback(cb_fetchLightData);
		l_defer.addErrback(eb_fetchLightData);
        return false;
	},

	/**
	 * Fill in the schedule entry screen with all of the data for this schedule.
	 * 
	 */
	function fillEntry(self, p_obj) {
		Divmod.debug('---', 'lights.fillEntry(1) was called.  Self:' + self);
		console.log("lights.fillEntry() - Obj = %O", p_obj);
		var light = arguments[1];
		self.nodeById('Name').value = light.Name;
		self.nodeById('Key').value = light.Key;
		self.nodeById('ActiveDiv').innerHTML = buildTrueFalseWidget('LightsActive', light.Active);
		self.nodeById('Comment').value = light.Comment;
		self.nodeById('Coords').value = light.Coords;
		self.nodeById('Dimmable').innerHTML = buildTrueFalseWidget('LightDimmable', light.Dimmable);
		self.nodeById('Family').value = light.Family;
		self.nodeById('RoomNameDiv').innerHTML = buildRoomSelectWidget('LightRoomName', light.RoomName);
		self.nodeById('Type').value = light.Type;
		self.nodeById('UUID').value = light.UUID;
		self.nodeById('LightEntryButtonsDiv').innerHTML = buildEntryButtons('handleDataOnClick');
	},
	function fetchEntry(self) {
		Divmod.debug('---', 'lights.fetchEntry() was called. ');
        var l_scheduleData = {
			Name : self.nodeById('Name').value,
			Key : self.nodeById('Key').value,
			Active : fetchTrueFalse('SchedActive'),
			Comment : self.nodeById('Comment'),
			Coords : self.nodeById('Coords'),
			Dimmable : fetchTrueFalse('LightDimmable'),
			Family : self.nodeById('Family'),
			RoomName : fetchSelectWidget('LightRoomName'),
			Type : self.nodeById('Type').value,
			UUID : self.nodeById('UUID').value,
			HouseIx : globals.House.HouseIx,
			Delete : false
            }
		return l_scheduleData;
	},
	function createEntry(self, p_ix) {
		Divmod.debug('---', 'lights.createEntry() was called.  Ix: ' + p_ix);
        var l_Data = {
    			Name : 'Change Me',
    			Key : Object.keys(globals.House.HouseObj.Lights).length,
    			Active : false,
    			Comment : '',
    			Coords : '',
    			Dimmable : false,
    			Family : '',
    			RoomName : '',
    			Type : 'Light',
    			UUID : '',
    			HouseIx : p_ix,
    			Delete : false
                }
		return l_Data;
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
		if (l_ix <= 1000) {
			// One of the Light buttons.
			var l_obj = globals.House.HouseObj.Lights[l_ix];
			globals.House.LightObj = l_obj;
			Divmod.debug('---', 'lights.handleMenuOnClick("Light" Button) was called. ' + l_ix + ' ' + l_name);
			//console.log("lights.handleMenuOnClick() - l_obj = %O", l_obj);
			self.showEntry();
			self.hideButtons();
			self.fillEntry(l_obj);
		} else if (l_ix == 10001) {
			// The "Add" button
			Divmod.debug('---', 'lights.handleMenuOnClick(Add Button) was called. ' + l_ix + ' ' + l_name);
			self.showEntry();
			self.hideButtons();
			var l_ent = self.createEntry(globals.House.HouseIx);
			self.fillEntry(l_ent);
		} else if (l_ix == 10002) {
			// The "Back" button
			Divmod.debug('---', 'lights.handleMenuOnClick(Back Button) was called. ' + l_ix + ' ' + l_name);
			self.hideWidget();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget();
		}
	},
	
	/**
	 * Event handler for submit buttons at bottom of entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataOnClick(self, p_node) {
		function cb_doHandleSubmit(p_json) {
			//Divmod.debug('---', 'lights.cb_handleDataOnClick() was called.');
			self.showWidget();
		}
		function eb_doHandleSubmit(res){
			Divmod.debug('---', 'lights.eb_handleDataOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		Divmod.debug('---', 'lights.handleDataOnClick() was called. Node:' + l_ix);
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry());
			Divmod.debug('---', 'lights.handleDataOnClick(Change) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveLightData", l_json);  // @ web_lights
			l_defer.addCallback(cb_doHandleSubmit);
			l_defer.addErrback(eb_doHandleSubmit);
			break;
		case '10002':  // Back button
			Divmod.debug('---', 'lights.handleDataOnClick(Back) was called.  ');
			self.hideEntry();
			self.showButtons();
			break;
		case '10004':  // Delete button
			var l_obj = self.fetchEntry();
			l_obj['Delete'] = true;
	    	var l_json = JSON.stringify(l_obj);
			Divmod.debug('---', 'lights.handleDataOnClick(Delete) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveLightData", l_json);  // @ web_rooms
			l_defer.addCallback(cb_doHandleSubmit);
			l_defer.addErrback(eb_doHandleSubmit);
			break;
		default:
			Divmod.debug('---', 'lights.handleDataOnClick(Default) was called. l_ix:' + l_ix);
			break;			
		}
		// return false stops the resetting of the server.
        return false;
	}
);
//### END DBK
