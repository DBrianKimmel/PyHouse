/* controlLights.js
 * 
 * Displays the control light screens
 */

// import Nevow.Athena
// import globals
// import helpers

helpers.Widget.subclass(controlLights, 'ControlLightsWidget').methods(

	function __init__(self, node) {
		controlLights.ControlLightsWidget.upcall(self, '__init__', node);
	},

	// ============================================================================
	/**
     * Place the widget in the workspace.
	 *
	 * @param self is    <"Instance" of undefined.controlLights.ControlLightsWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		function cb_widgetready(res) {
			//Divmod.debug('---', 'controlLights.cb_widgready() was called. res = ' + res);
			self.hideWidget();
		}
		//Divmod.debug('---', 'controlLights.ready() was called. ' + self);
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	function showWidget(self) {
		//Divmod.debug('---', 'controlLights.showWidget() was called.');
		self.node.style.display = 'block';
		self.showButtons(self);
		self.hideEntry(self);
		self.fetchHouseData();
	},
	function hideButtons(self) {
		//Divmod.debug('---', 'controlLights.hideButtons() was called. ');
		self.nodeById('ControlLightButtonsDiv').style.display = 'none';
	},
	function showButtons(self) {
		//Divmod.debug('---', 'controlLights.showButtons() was called. ');
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
	 * This triggers getting the house data from the server.
	 */
	function fetchHouseData(self) {
		function cb_fetchHouseData(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
			var l_tab = buildTable(globals.House.HouseObj.Lights, 'handleMenuOnClick');
			self.nodeById('ControlLightTableDiv').innerHTML = l_tab;
		}
		function eb_fetchHouseData(res) {
			Divmod.debug('---', 'controlLights.eb_fetchHouseData() was called.  ERROR ' + res);
		}
        var l_defer = self.callRemote("getHouseData", globals.House.HouseIx);  // call server @ web_controlLights.py
		l_defer.addCallback(cb_fetchHouseData);
		l_defer.addErrback(eb_fetchHouseData);
        return false;
	},

	// ============================================================================
	/**
	 * Event handler for light selection buttons.
	 * 
	 * The user can click on a light button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.controlLights.ControlLightsWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function handleMenuOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.House.LightIx = l_ix;
		globals.House.LightName = l_name;
		if (l_ix <= 1000) {
			// One of the controlLights buttons.
			var l_obj = globals.House.HouseObj.Lights[l_ix];
			globals.House.LightObj = l_obj;
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
	function fillEntry(self, p_obj) {
		//Divmod.debug('---', 'controlLights.fillEntry() was called. ');
		//console.log("controlLights.fillEntry() - Obj %O", p_obj);
        self.nodeById('NameDiv').innerHTML = buildTextWidget('CtlLightName', p_obj.Name, 'disabled');
        self.nodeById('KeyDiv').innerHTML = buildTextWidget('CtlLightKey', p_obj.Key, 'disabled');
		self.nodeById('UUIDDiv').innerHTML = buildTextWidget('CtlLightUUID', p_obj.UUID, 'disabled');
		self.nodeById('RoomNameDiv').innerHTML = buildRoomSelectWidget('CtlLightRoomName', p_obj.RoomName, 'disabled');
		self.nodeById('LevelDiv').innerHTML = buildLevelSliderWidget('CtlLightLevel', p_obj.CurLevel);
		self.nodeById('ControlLightEntryButtonsDiv').innerHTML = buildEntryButtons('handleDataOnClick', 'NoDelete');
	},
	function fetchEntry(self) {
        var l_data = {
            Name : fetchTextWidget('CtlLightName'),
            Key : fetchTextWidget('CtlLightKey'),
			UUID : fetchTextWidget('CtlLightUUID'),
			//RoomName : fetchSelectWidget('CtlLightRoomName'),
			Level : fetchLevelWidget('CtlLightLevel'),
			HouseIx : globals.House.HouseIx,
            }
		return l_data;
	},

	// ============================================================================
	/**
	 * Event handler for submit buttons at bottom of entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataOnClick(self, p_node) {
		function cb_handleDataOnClick(p_json) {
			//Divmod.debug('---', 'controlLights.cb_handleDataOnClick() was called.');
			self.showWidget(self);
		}
		function eb_handleDataOnClick(res){
			Divmod.debug('---', 'controlLights.eb_handleDataOnClick() was called. res=' + res);
		}
    	var l_json = JSON.stringify(self.fetchEntry(self));
		//Divmod.debug('---', 'controlLights.handleDataOnClick() was called. json:' + l_json);
        var l_defer = self.callRemote("saveControlLightData", l_json);  // @ web_controlLights
		l_defer.addCallback(cb_handleDataOnClick);
		l_defer.addErrback(eb_handleDataOnClick);
		// return false stops the resetting of the server.
        return false;
	}
);
//### END DBK

