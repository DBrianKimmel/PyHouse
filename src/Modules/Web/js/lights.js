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
		Divmod.debug('---', 'lights.startWidget() was called.');
		self.node.style.display = 'block';
		self.showSelectionButtons();
		self.hideDataEntry();
		self.fetchHouseData();  // Continue with next phase
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
		l_html += build_lcars_middle_menu(10, l_button_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
	/**
	 * This triggers getting the lights data from the server.
	 */
	function fetchHouseData(self) {
		function cb_fetchHouseData(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
			self.buildLcarSelectScreen();
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
			globals.House.Self = self;
			self.showDataEntry();
			self.hideSelectionButtons();
			self.fillEntry(l_obj);
		} else if (l_ix == 10001) {  // The "Add" button
			self.showDataEntry();
			self.hideSelectionButtons();
			var l_ent = self.createEntry();
			self.fillEntry(l_ent);
		} else if (l_ix == 10002) {  // The "Back" button
			self.showWidget2('HouseMenu');
		}
	},

	// ============================================================================

	/**
	 * Build a screen full of data entry fields.
	 */
	function buildBasicPart(self, p_light, p_html, p_onchange) {
		p_html += buildLcarTextWidget(self, 'Name', 'Light Name', p_light.Name);
		p_html += buildLcarTextWidget(self, 'Key', 'Light Index', p_light.Key, 'size=10');
		p_html += buildLcarTrueFalseWidget(self, 'Active', 'Active ?', p_light.Active);
		p_html += buildLcarTextWidget(self, 'Comment', 'Comment', p_light.Comment);
		p_html += buildLcarTextWidget(self, 'LightCoords', 'Coords', p_light.Coords);
		p_html += buildLcarTrueFalseWidget(self, 'LightDimmable', 'Light Dimmable ?', p_light.IsDimmable);
		p_html += buildLcarFamilySelectWidget(self, 'LightFamily', 'Family', p_light.ControllerFamily, p_onchange);
		p_html += buildLcarRoomSelectWidget(self, 'LightRoomName', 'Room', p_light.RoomName);
		p_html += buildLcarLightTypeSelectWidget(self, 'LightType', 'Type', p_light.LightingType, 'disabled');
		p_html += buildLcarTextWidget(self, 'LightUUID', 'UUID', p_light.UUID, 'disabled');
		return p_html;
	},
	function buildInsteonPart(self, p_light, p_html) {
		p_html += buildLcarTextWidget(self, 'LightAddressI', 'Insteon Address', p_light.InsteonAddress);
		p_html += buildLcarTextWidget(self, 'LightDevCat', 'Dev Cat', p_light.DevCat);
		p_html += buildLcarTextWidget(self, 'LightGroupNumber', 'Group Number', p_light.GroupNumber);
		p_html += buildLcarTextWidget(self, 'LightGroupList', 'Group List', p_light.GroupList);
		p_html += buildLcarTrueFalseWidget(self, 'LightMaster', 'Light Master ?', p_light.IsMaster);
		p_html += buildLcarTrueFalseWidget(self, 'LightController', 'Light Controller ?', p_light.IsController);
		p_html += buildLcarTrueFalseWidget(self, 'LightResponder', 'Light Responder ?', p_light.IsResponder);
		p_html += buildLcarTextWidget(self, 'LightProductKey', 'Product Key', p_light.ProductKey);
		return p_html;
	},
	function buildUpbPart(self, p_light, p_html) {
		p_html += buildLcarTextWidget(self, 'LightAddressU', 'UPB Address', p_light.UPBAddress);
		p_html += buildLcarTextWidget(self, 'LightPassword', 'UPB Password', p_light.UPBPassword);
		p_html += buildLcarTextWidget(self, 'LightNetworkID', 'UPB Network', p_light.UPBNetworkID);
		return p_html;
	},
	function buildAllParts(self, p_light, p_html, p_handler, p_onchange) {
		p_html = self.buildBasicPart(p_light, p_html, p_onchange);
		if (p_light.ControllerFamily == 'Insteon') {
			p_html = self.buildInsteonPart(p_light, p_html);
		}
        if (p_light.ControllerFamily == 'UPB') {
        	p_html = self.buildUpbPart(p_light, p_html);
        }
		p_html += buildLcarEntryButtons(p_handler);
		return p_html;
	},
	function buildLcarDataEntryScreen(self, p_entry, p_handler){
		// Divmod.debug('---', 'rooms.buildLcarDataEntryScreen() was called.');
		// console.log("lights.buildLcarDataEntryScreen() - self = %O", self);
		var l_light = arguments[1];
		var l_html = self.buildAllParts(l_light, l_html, p_handler, 'familyChanged');
		var l_html_2 = "";
		l_html_2 += build_lcars_top('Enter Light Data', 'lcars-salmon-color');
		l_html_2 += build_lcars_middle_menu(40, l_html);
		l_html_2 += build_lcars_bottom();
		self.nodeById('DataEntryDiv').innerHTML = l_html_2;
	},
	function familyChanged() {
		var l_obj = globals.House.LightObj;
		var l_self = globals.House.Self;
		// Divmod.debug('---', 'lights.familyChanged was called !!!');
		// console.log("lights.buildLcarDataEntryScreen() - light %O", l_obj);
		// console.log("lights.buildLcarDataEntryScreen() - l_self %O", l_self);
		var l_family = fetchSelectWidget(l_self, 'LightFamily');
		l_obj.ControllerFamily = l_family;
		l_self.fillEntry(l_obj);
	},

	function fillEntry(self, p_obj) {
		// Divmod.debug('---', 'lights.fillEntry was called.');
		self.buildLcarDataEntryScreen(p_obj, 'handleDataOnClick');
	},
	function fetchEntry(self) {
		// Divmod.debug('---', 'lights.fetchEntry(1) was called.');
        var l_data = {
			Name			: fetchTextWidget(self, 'Name'),
			Key				: fetchTextWidget(self, 'Key'),
			Active			: fetchTrueFalseWidget(self, 'Active'),
			Comment			: fetchTextWidget(self, 'Comment'),
			Coords      	: fetchTextWidget(self, 'LightCoords'),
			IsDimmable    	: fetchTrueFalseWidget(self, 'LightDimmable'),
			ControllerFamily: fetchSelectWidget(self, 'LightFamily'),
			RoomName    	: fetchSelectWidget(self, 'LightRoomName'),
			LightingType	: fetchSelectWidget(self, 'LightType'),	
			UUID        	: fetchTextWidget(self, 'LightUUID'),
			Delete      	: false
            };
        if (l_data.ControllerFamily === 'Insteon') {
        	l_data = self.fetchInsteonEntry(l_data);
        }
        if (l_data.ControllerFamily === 'UPB') {
        	l_data = self.fetchUpbEntry(l_data);
        }
      	// console.log("lights.fetchEntry()  l_data  %O", l_data)
		return l_data;
	},
	function fetchInsteonEntry(self, p_data) {
		// Divmod.debug('---', 'lights.fetchInsteonEntry() was called.');
        p_data.InsteonAddress = fetchTextWidget(self, 'LightAddressI');
        p_data.DevCat = fetchTextWidget(self, 'LightDevCat');
        p_data.GroupNumber = fetchTextWidget(self, 'LightGroupNumber');
        p_data.GroupList = fetchTextWidget(self, 'LightGroupList');
        p_data.IsMaster = fetchTrueFalseWidget(self, 'LightMaster');
        p_data.IsResponder = fetchTrueFalseWidget(self, 'LightResponder');
        p_data.IsController = fetchTrueFalseWidget(self, 'LightController');
        p_data.ProductKey = fetchTextWidget(self, 'LightProductKey');
		// Divmod.debug('---', 'lights.fetchInsteonEntry() finished.');
      	// console.log("lights.fetchInsteonEntry()  p_data  %O", p_data)
		return p_data;
	},
	function fetchUpbEntry(self, p_data) {
		Divmod.debug('---', 'lights.fetchUpbEntry() was called.');
        p_data.UPBAddress = fetchTextWidget(self, 'LightAddressU');
        p_data.UPBPassword = fetchTextWidget(self, 'LightPassword');
        p_data.UPBNetworkID = fetchTextWidget(self, 'LightNetworkID');
		// Divmod.debug('---', 'lights.fetchUpbEntry() finished.');
      	// console.log("lights.fetchUpbEntry()  p_data  %O", p_data)
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
    			DevCat			: 0,
    			GroupNumber		: 0,
    			GroupList		: '',
    			IsMaster		: false,
    			IsResponder		: false,
    			ProductKey		: 0,
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
			// self.showWidget();
		}
		function eb_handleDataOnClick(res){
			Divmod.debug('---', 'lights.eb_handleDataOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		// Divmod.debug('---', 'lights.handleDataOnClick was called. IX:' + l_ix);
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry());
	        var l_defer = self.callRemote("saveLightData", l_json);
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			self.hideDataEntry();
			self.showSelectionButtons();
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
//Divmod.debug('---', 'lights.handleDataOnClick(Change) was called.');
//console.log("lights.handleDataOnClick()  json  %O", l_json);
//### END DBK
