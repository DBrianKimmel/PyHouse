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
// import lcars

helpers.Widget.subclass(lights, 'LightsWidget').methods(

    function __init__(self, node) {
        lights.LightsWidget.upcall(self, "__init__", node);
    },



// ============================================================================
	/**
     * Place the widget in the workspace.
	 * 
	 * @param self is    <"Instance" of undefined.lights.LightsWidget>
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
		self.showButtons();
		self.hideEntry();
		self.fetchHouseData();
	},
	function hideButtons(self) {
		self.nodeById('SelectionButtonsDiv').style.display = 'none';
	},
	function showButtons(self) {
		self.nodeById('SelectionButtonsDiv').style.display = 'block';
	},
	function hideEntry(self) {
		self.nodeById('DataEntryDiv').style.display = 'none';
	},
	function showEntry(self) {
		self.nodeById('DataEntryDiv').style.display = 'block';
	},
	function buildButtonName(self, p_obj) {
		var l_html = p_obj.Name + '<br>' + p_obj.RoomName;
		return l_html;
	},


	// ============================================================================

	/**
	 * Build a screen full of buttons - One for each light and some actions.
	 */
	function buildLcarSelectScreen(self){
		var l_button_html = buildLcarSelectionButtonsTable(globals.House.HouseObj.Lights, 'handleMenuOnClick');
		var l_html = build_lcars_top('Lights', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(2, l_button_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
	/**
	 * This triggers getting the lights data from the server.
	 */
	function fetchHouseData(self) {
		function cb_fetchHouseData(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
			self.buildLcarSelectScreen()
		}
		function eb_fetchHouseData(res) {
			Divmod.debug('---', 'lights.eb_fetchHouseData() was called. ERROR: ' + res);
		}
        var l_defer = self.callRemote("getHouseData");
		l_defer.addCallback(cb_fetchHouseData);
		l_defer.addErrback(eb_fetchHouseData);
        return false;
	},


	// ============================================================================
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
			self.showEntry();
			self.hideButtons();
			self.fillEntry(l_obj);
		} else if (l_ix == 10001) {  // The "Add" button
			self.showEntry();
			self.hideButtons();
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
		Divmod.debug('---', 'rooms.buildLcarDataEntryScreen() was called.');
		console.log("lights.buildLcarDataEntryScreen() - self = %O", self);
		var l_room = arguments[1];
		var l_entry_html = "";
		l_entry_html += buildLcarTextWidget(self, 'Name', 'Room Name', l_room.Name);
		l_entry_html += buildLcarTextWidget(self, 'Key', 'Room Index', l_room.Key, 'size=10');
		l_entry_html += buildLcarTrueFalseWidget(self, 'RoomActive', 'Active ?', l_room.Active);
		l_entry_html += buildLcarTextWidget(self, 'Comment', 'Comment', l_room.Comment);
		l_entry_html += buildLcarTextWidget(self, 'Coords', 'Coords', l_room.Coords);
		l_entry_html += buildLcarTrueFalseWidget(self, 'LightDimmable', 'Light Dimmable ?', l_room.IsDimmable);
		l_entry_html += buildLcarFamilySelectWidget(self, 'LightFamily', 'Family', l_room.ControllerFamily);
		l_entry_html += buildLcarRoomSelectWidget(self, 'LightRoomName', 'Room', l_room.RoomName);
		l_entry_html += buildLcarLightTypeSelectWidget(self, 'LightType', 'Type', l_room.LightingType, 'disabled');
		l_entry_html += buildLcarTextWidget(self, 'LightUUID', 'UUID', l_room.UUID, 'disabled');

		if (l_room.ControllerFamily == 'Insteon') {
			l_entry_html += buildLcarTextWidget(self, 'LightAddressI', 'Insteon Address', l_room.InsteonAddress);
			l_entry_html += buildLcarTextWidget(self, 'LightDevCat', 'Drv Cat', l_room.DevCat);
			l_entry_html += buildLcarTextWidget(self, 'LightGroupNumber', 'Group Number', l_room.GroupNumber);
			l_entry_html += buildLcarTextWidget(self, 'LightGroupList', 'Group List', l_room.GroupList);
			l_entry_html += buildLcarTrueFalseWidget(self, 'LightMaster', 'Light Master ?', l_room.IsMaster);
			l_entry_html += buildLcarTrueFalseWidget(self, 'LightController', 'Light Controller ?', l_room.IsController);
			l_entry_html += buildLcarTrueFalseWidget(self, 'LightResponder', 'Light Responder ?', l_room.IsResponder);
			l_entry_html += buildLcarTextWidget(self, 'LightProductKey', 'Product Key', l_room.ProductKey);
		}
        if (l_room.ControllerFamily == 'UPB') {
			l_entry_html += buildLcarTextWidget(self, 'LightAddressU', 'UPB Address', l_room.UPBAddress);
			l_entry_html += buildLcarTextWidget(self, 'LightPassword', 'UPB Password', l_room.UPBPassword);
			l_entry_html += buildLcarTextWidget(self, 'LightNetworkID', 'UPB Network', l_room.UPBNetworkID);
        }
		l_entry_html += buildLcarEntryButtons(p_handler);
		var l_html = "";
		l_html += build_lcars_top('Enter Room Data', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(26, l_entry_html);
		l_html += build_lcars_bottom();
		self.nodeById('DataEntryDiv').innerHTML = l_html;
	},

	function fillEntry(self, p_obj) {
		Divmod.debug('---', 'rooms.fillEntry was called.');
		self.buildLcarDataEntryScreen(p_obj, 'handleDataOnClick')
	},
	function fillInsteonEntry(self, p_style) {
		self.nodeById('Row_i01').style.display = p_style;
		self.nodeById('Row_i02').style.display = p_style;
		self.nodeById('Row_i03').style.display = p_style;
		self.nodeById('Row_i04').style.display = p_style;
		self.nodeById('Row_i05').style.display = p_style;
		self.nodeById('Row_i06').style.display = p_style;
		self.nodeById('Row_i07').style.display = p_style;
		self.nodeById('Row_i08').style.display = p_style;
	},
	function fillUpbEntry(self, p_style) {
		self.nodeById('Row_u01').style.display = p_style;
		self.nodeById('Row_u02').style.display = p_style;
		self.nodeById('Row_u03').style.display = p_style;
	},
	function fetchEntry(self) {
		// Divmod.debug('---', 'lights.fetchEntry() was called.');
        var l_data = {
            Name        	: fetchTextWidget('LightName'),
            Key         	: fetchTextWidget('LightKey'),
			Active      	: fetchTrueFalseWidget('LightActive'),
			Comment     	: fetchTextWidget('LightComment'),
			Coords      	: fetchTextWidget('LightCoords'),
			IsDimmable    	: fetchTrueFalseWidget('LightDimmable'),
			ControllerFamily: fetchSelectWidget('LightFamily'),
			RoomName    	: fetchSelectWidget('LightRoomName'),
			LightingType	: fetchSelectWidget('LightType'),
			UUID        	: fetchTextWidget('LightUUID'),
			Delete      	: false
            }
        if (l_data['ControllerFamily'] === 'Insteon') {
        	l_data = self.fetchInsteonEntry(l_data);
        }
        if (l_data['ControllerFamily'] === 'UPB') {
        	l_data = self.fetchUpbEntry(l_data);
        }
		// Divmod.debug('---', 'lights.fetchEntry() finished.');
		return l_data;
	},
	function fetchInsteonEntry(self, p_data) {
		// Divmod.debug('---', 'lights.fetchInsteonEntry() was called.');
        p_data.InsteonAddress = fetchTextWidget('LightAddressI');
        p_data.DevCat = fetchTextWidget('LightDevCat');
        p_data.GroupNumber = fetchTextWidget('LightGroupNumber');
        p_data.GroupList = fetchTextWidget('LightGroupList');
        p_data.IsMaster = fetchTrueFalseWidget('LightMaster');
        p_data.IsResponder = fetchTrueFalseWidget('LightResponder');
        p_data.ProductKey = fetchTextWidget('LightProductKey');
		// Divmod.debug('---', 'lights.fetchInsteonEntry() finished.');
		return p_data;
	},
	function fetchUpbEntry(self, p_data) {
		// Divmod.debug('---', 'lights.fetchUpbEntry() was called.');
        p_data.UPBAddress = fetchTextWidget('LightAddressU');
        p_data.UPBPassword = fetchTextWidget('LightPassword');
        p_data.UPBNetworkID = fetchTextWidget('LightNetworkID');
		// Divmod.debug('---', 'lights.fetchUpbEntry() finished.');
		return p_data;
	},
	function createEntry(self) {
		// Divmod.debug('---', 'lights.createEntry() was called.');
        var l_Data = {
    			Name     : 'Change Me',
    			Key      : Object.keys(globals.House.HouseObj.Lights).length,
    			Active   : false,
    			Comment  : '',
    			Coords   : '',
    			IsDimmable : false,
    			ControllerFamily   : 'Insteon',
    			RoomName : '',
    			Type     : 'Light',
    			UUID     : '',
    			InsteonAddress  : '',
    			Delete   : false
                };
		return l_Data;
	},


	// ============================================================================
	/**
	 * Event handler for buttons at bottom of the data entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataOnClick(self, p_node) {
		function cb_handleDataOnClick(p_json) {
			self.showWidget();
		}
		function eb_handleDataOnClick(res){
			Divmod.debug('---', 'lights.eb_handleDataOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry());
	        var l_defer = self.callRemote("saveLightData", l_json);
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			self.hideEntry();
			self.showButtons();
			break;
		case '10004':  // Delete button
			var l_obj = self.fetchEntry();
			l_obj.Delete = true;
	    	l_json = JSON.stringify(l_obj);
	        l_defer = self.callRemote("saveLightData", l_json);
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		default:
			Divmod.debug('---', 'lights.handleDataOnClick(Default) was called. l_ix:' + l_ix);
			break;
		}
        return false;  // false stops the chain.
	}
);
//console.log("lights.handleDataOnClick()  json  %O", l_json)
//Divmod.debug('---', 'lights.handleDataOnClick(Change) was called. JSON:' + l_json);
//### END DBK
