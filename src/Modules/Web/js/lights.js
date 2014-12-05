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
		self.fetchDataFromServer();  // Continue with next phase
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
	 * This triggers getting the lights data from the server.
	 */
	function fetchDataFromServer(self) {
		function cb_fetchDataFromServer(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
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
		var l_button_html = buildLcarSelectionButtonsTable(globals.House.HouseObj.Lights, 'handleMenuOnClick');
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
		p_html += buildLcarTextWidget(self, 'Coords', 'Coords', p_light.Coords);
		p_html += buildLcarTrueFalseWidget(self, 'Dimmable', 'Light Dimmable ?', p_light.IsDimmable);
		p_html += buildLcarFamilySelectWidget(self, 'Family', 'Family', p_light.ControllerFamily, p_onchange);
		p_html += buildLcarRoomSelectWidget(self, 'RoomName', 'Room', p_light.RoomName);
		p_html += buildLcarLightTypeSelectWidget(self, 'Type', 'Type', p_light.LightingType, 'disabled');
		p_html += buildLcarTextWidget(self, 'UUID', 'UUID', p_light.UUID, 'disabled');
		return p_html;
	},
	function buildInsteonPart(self, p_light, p_html) {
		p_html += buildLcarTextWidget(self, 'InsteonAddress', 'Insteon Address', p_light.InsteonAddress);
		p_html += buildLcarTextWidget(self, 'DevCat', 'Dev Cat', p_light.DevCat);
		p_html += buildLcarTextWidget(self, 'GroupNumber', 'Group Number', p_light.GroupNumber);
		p_html += buildLcarTextWidget(self, 'GroupList', 'Group List', p_light.GroupList);
		p_html += buildLcarTrueFalseWidget(self, 'Master', 'Light Master ?', p_light.IsMaster);
		p_html += buildLcarTrueFalseWidget(self, 'Controller', 'Light Controller ?', p_light.IsController);
		p_html += buildLcarTrueFalseWidget(self, 'Responder', 'Light Responder ?', p_light.IsResponder);
		p_html += buildLcarTextWidget(self, 'ProductKey', 'Product Key', p_light.ProductKey);
		return p_html;
	},
	function buildUpbPart(self, p_light, p_html) {
		p_html += buildLcarTextWidget(self, 'UpbAddress', 'UPB Address', p_light.UPBAddress);
		p_html += buildLcarTextWidget(self, 'UpbPassword', 'UPB Password', p_light.UPBPassword);
		p_html += buildLcarTextWidget(self, 'UpbNetworkID', 'UPB Network', p_light.UPBNetworkID);
		return p_html;
	},
	function buildAllParts(self, p_light, p_html, p_handler, p_onchange) {
		p_html = self.buildBasicPart(p_light, p_html, p_onchange);
		if (p_light.ControllerFamily === 'Insteon')
			p_html = self.buildInsteonPart(p_light, p_html);
		else if (p_light.ControllerFamily === 'UPB')
        	p_html = self.buildUpbPart(p_light, p_html);
		else
			Divmod.debug('---', 'ERROR - lights.buildAllParts() Family = ' + p_light.ControllerFamily);
		p_html += buildLcarEntryButtons(p_handler);
		return p_html;
	},
	function buildLcarDataEntryScreen(self, p_entry, p_handler){
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
		var l_family = fetchSelectWidget(l_self, 'Family');
		l_obj.ControllerFamily = l_family;
		l_self.fillEntry(l_obj);
	},
	function fillEntry(self, p_obj) {
		self.buildLcarDataEntryScreen(p_obj, 'handleDataEntryOnClick');
	},
	function fetchEntry(self) {
		// Divmod.debug('---', 'lights.fetchEntry(1) was called.');
        var l_data = {
			Name			: fetchTextWidget(self, 'Name'),
			Key				: fetchTextWidget(self, 'Key'),
			Active			: fetchTrueFalseWidget(self, 'Active'),
			Comment			: fetchTextWidget(self, 'Comment'),
			Coords      	: fetchTextWidget(self, 'Coords'),
			IsDimmable    	: fetchTrueFalseWidget(self, 'Dimmable'),
			ControllerFamily: fetchSelectWidget(self, 'Family'),
			RoomName    	: fetchSelectWidget(self, 'RoomName'),
			LightingType	: fetchSelectWidget(self, 'Type'),	
			UUID        	: fetchTextWidget(self, 'UUID'),
			Delete      	: false
            };
        if (l_data.ControllerFamily === 'Insteon')
        	l_data = self.fetchInsteonEntry(l_data);
        if (l_data.ControllerFamily === 'UPB')
        	l_data = self.fetchUpbEntry(l_data);
		return l_data;
	},
	function fetchInsteonEntry(self, p_data) {
		// Divmod.debug('---', 'lights.fetchInsteonEntry() was called.');
        p_data.InsteonAddress = fetchTextWidget(self, 'InsteonAddress');
        p_data.DevCat = fetchTextWidget(self, 'DevCat');
        p_data.GroupNumber = fetchTextWidget(self, 'GroupNumber');
        p_data.GroupList = fetchTextWidget(self, 'GroupList');
        p_data.IsMaster = fetchTrueFalseWidget(self, 'Master');
        p_data.IsResponder = fetchTrueFalseWidget(self, 'Responder');
        p_data.IsController = fetchTrueFalseWidget(self, 'Controller');
        p_data.ProductKey = fetchTextWidget(self, 'ProductKey');
		return p_data;
	},
	function fetchUpbEntry(self, p_data) {
		// Divmod.debug('---', 'lights.fetchUpbEntry() was called.');
        p_data.UPBAddress = fetchTextWidget(self, 'UpbAddress');
        p_data.UPBPassword = fetchTextWidget(self, 'UpbPassword');
        p_data.UPBNetworkID = fetchTextWidget(self, 'UpbNetworkID');
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
    			InsteonAddress  : '11.22.33',
    			DevCat			: 0,
    			GroupNumber		: 0,
    			GroupList		: '',
    			IsMaster		: false,
    			IsResponder		: false,
    			IsController	: false,
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
	function handleDataEntryOnClick(self, p_node) {
		function cb_handleDataEntryOnClick(p_json) {
			self.startWidget();
		}
		function eb_handleDataEntryOnClick(res){
			Divmod.debug('---', 'lights.eb_handleDataEntryOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry());
	        var l_defer = self.callRemote("saveLightData", l_json);
			l_defer.addCallback(cb_handleDataEntryOnClick);
			l_defer.addErrback(eb_handleDataEntryOnClick);
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
//Divmod.debug('---', 'lights.handleDataEntryOnClick(Change) was called.');
//console.log("lights.handleDataEntryOnClick()  json  %O", l_json);
//### END DBK
