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
			self.hideWidget();
		}
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	function showWidget(self) {
		self.node.style.display = 'block';
		self.showSelectionButtons(self);
		self.hideDataEntry(self);
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
	 * Build a screen full of buttons - One for each light and some actions.
	 */
	function buildLcarSelectScreen(self){
		// Divmod.debug('---', 'controlLights.buildLcarSelectScreen() was called.');
		var l_button_html = buildLcarSelectionButtonsTable(globals.House.HouseObj.Lights, 'handleMenuOnClick');
		var l_html = build_lcars_top('Control Lights', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(2, l_button_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
	/**
	 * This triggers getting the house data from the server.
	 */
	function fetchHouseData(self) {
		function cb_fetchHouseData(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
			self.buildLcarSelectScreen();
		}
		function eb_fetchHouseData(res) {
			Divmod.debug('---', 'controlLights.eb_fetchHouseData() was called.  ERROR ' + res);
		}
		// Divmod.debug('---', 'controlLights.fetchHouseData() was called.');
       	var l_defer = self.callRemote("getHouseData");  // call server @ web_controlLights.py
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
		//Divmod.debug('---', 'controlLights.handleMenuOnClick() was called.');
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.House.LightIx = l_ix;
		globals.House.LightName = l_name;
		if (l_ix <= 1000) {  // One of the controlLights buttons.
			var l_obj = globals.House.HouseObj.Lights[l_ix];
			globals.House.LightObj = l_obj;
			globals.House.Self = self;
			self.showDataEntry();
			self.hideSelectionButtons();
			//console.log("controlLights.handleMenuOnClick() - l_ix = %O", l_ix);
			//console.log("controlLights.handleMenuOnClick() - l_obj = %O", l_obj);
			self.fillEntry(l_obj);
		} else if (l_ix == 10002) {  // The "Back" button
			self.hideWidget();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget();
		}
	},


// ============================================================================

	function buildLcarDataEntryScreen(self, p_entry, p_handler){
		var l_light = arguments[1];
		var l_entry_html = "";
		l_entry_html += buildLcarTextWidget(self, 'CtlLightName', 'Light Name', l_light.Name, 'disabled');
		l_entry_html += buildLcarTextWidget(self, 'CtlLightKey', 'Light Index', l_light.Key, 'disabled');
		l_entry_html += buildLcarTextWidget(self, 'CtlLightUUID', 'UUID', l_light.UUID, 'disabled');
		l_entry_html += buildLcarRoomSelectWidget(self, 'CtlLightRoomName', 'Room Name', l_light.RoomName, 'disabled');
		l_entry_html += buildLcarLevelSliderWidget(self, 'CtlLightLevel', 'Level', l_light.CurLevel, 'handleSliderChange');
		l_entry_html += buildLcarEntryButtons(p_handler, 'NoAdd');
		var l_html = build_lcars_top('Control Light', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(6, l_entry_html);
		l_html += build_lcars_bottom();
		self.nodeById('DataEntryDiv').innerHTML = l_html;
	},
	function handleSliderChange(p_event){
		// Divmod.debug('---', 'controlLights.handleSliderChange() called. - Event= ' + p_event);
		console.log("controlLights.handleSliderChange   Event:  %O", p_event);
		var l_obj = globals.House.LightObj;
		var l_self = globals.House.Self;
		var l_level = fetchSliderWidget(l_self, 'CtlLightLevel');
		// Divmod.debug('---', 'controlLights.handleSliderChange() called. - Level= ' + l_level);
		updateSliderBoxValue(l_self, 'CtlLightLevel', l_level)
	},
	function fillEntry(self, p_entry) {
		self.buildLcarDataEntryScreen(p_entry, 'handleDataEntryOnClick')
	},
	function fetchEntry(self) {
        var l_data = {
            Name : fetchTextWidget(self, 'CtlLightName'),
            Key : fetchTextWidget(self, 'CtlLightKey'),
			UUID : fetchTextWidget(self, 'CtlLightUUID'),
			Level : fetchSliderWidget(self, 'CtlLightLevel'),
            };
		return l_data;
	},


// ============================================================================
	/**
	 * Event handler for submit buttons at bottom of entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataEntryOnClick(self, p_node) {
		function cb_handleDataOnClick(p_json) {
			self.showWidget(self);
		}
		function eb_handleDataOnClick(res){
			Divmod.debug('---', 'controlLights.eb_handleDataOnClick() was called. ERROR=' + res);
		}
    	var l_json = JSON.stringify(self.fetchEntry(self));
        var l_defer = self.callRemote("saveControlLightData", l_json);  // @ web_controlLights
		l_defer.addCallback(cb_handleDataOnClick);
		l_defer.addErrback(eb_handleDataOnClick);
        return false;  // return false stops the resetting of the server.
	}
);
//Divmod.debug('---', 'controlLights.fetchHouseData.cb_fetchHouseData() was called.');
//console.log("controlLights.fetchHouseData.cb_fetchHouseData   p1 %O", p_json);
//### END DBK

