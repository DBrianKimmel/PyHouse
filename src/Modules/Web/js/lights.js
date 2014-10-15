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
		self.nodeById('LightButtonsDiv').style.display = 'none';
	},
	function showButtons(self) {
		self.nodeById('LightButtonsDiv').style.display = 'block';
	},
	function hideEntry(self) {
		self.nodeById('LightEntryDiv').style.display = 'none';
	},
	function showEntry(self) {
		self.nodeById('LightEntryDiv').style.display = 'block';
	},
	function buildButtonName(self, p_obj) {
		return l_html = p_obj['Name'] + '<br>' + p_obj['RoomName'];
	},


	// ============================================================================
	/**
	 * This triggers getting the lights data from the server.
	 * The server calls displayLightsButtons with the lights info.
	 */
	function fetchHouseData(self) {
		function cb_fetchHouseData(p_json) {
			// We now have all the light data (+ other) so build the button desctiption and show the table of light buttins
			globals.House.HouseObj = JSON.parse(p_json);
			var l_tab = buildTable(globals.House.HouseObj.Lights, 'handleMenuOnClick', self.buildButtonName);
			self.nodeById('LightTableDiv').innerHTML = l_tab;
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
		if (l_ix <= 1000) {
			// we clicked on one of the buttons, show the details for the light.
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
	function fillEntry(self, p_obj) {
        self.nodeById('NameDiv').innerHTML     = buildTextWidget('LightName', p_obj.Name);
        self.nodeById('KeyDiv').innerHTML      = buildTextWidget('LightKey', p_obj.Key, 'disabled');
		self.nodeById('ActiveDiv').innerHTML   = buildTrueFalseWidget('LightActive', p_obj.Active);
		self.nodeById('CommentDiv').innerHTML  = buildTextWidget('LightComment', p_obj.Comment);
		self.nodeById('CoordsDiv').innerHTML   = buildTextWidget('LightCoords', p_obj.Coords);
		self.nodeById('DimmableDiv').innerHTML = buildTrueFalseWidget('LightDimmable', p_obj.IsDimmable);
		self.nodeById('FamilyDiv').innerHTML   = buildFamilySelectWidget('LightFamily', p_obj.ControllerFamily);
		self.nodeById('RoomNameDiv').innerHTML = buildRoomSelectWidget('LightRoomName', p_obj.RoomName);
		self.nodeById('TypeDiv').innerHTML     = buildLightTypeSelectWidget('LightType', p_obj.LightingType, 'disabled');
		self.nodeById('UUIDDiv').innerHTML     = buildTextWidget('LightUUID', p_obj.UUID, 'disabled');

		self.nodeById('i01Div').innerHTML  = buildTextWidget('LightAddressI', p_obj.InsteonAddress);
		self.nodeById('i02Div').innerHTML  = buildTextWidget('LightDevCat', p_obj.DevCat);
		self.nodeById('i03Div').innerHTML  = buildTextWidget('LightGroupNumber', p_obj.GroupNumber);
		self.nodeById('i04Div').innerHTML  = buildTextWidget('LightGroupList', p_obj.GroupList);
		self.nodeById('i05Div').innerHTML  = buildTrueFalseWidget('LightMaster', p_obj.IsMaster);
		self.nodeById('i06Div').innerHTML  = buildTrueFalseWidget('LightController', p_obj.IsController);
		self.nodeById('i07Div').innerHTML  = buildTrueFalseWidget('LightResponder', p_obj.IsResponder);
		self.nodeById('i08Div').innerHTML  = buildTextWidget('LightProductKey', p_obj.ProductKey);

		self.nodeById('u01Div').innerHTML  = buildTextWidget('LightAddressU', p_obj.UPBAddress);
		self.nodeById('u02Div').innerHTML  = buildTextWidget('LightPassword', p_obj.UPBPassword);
		self.nodeById('u03Div').innerHTML  = buildTextWidget('LightNetworkID', p_obj.UPBNetworkID);

		if (p_obj['ControllerFamily'] == 'Insteon') {
			self.fillInsteonEntry('');
			self.fillUpbEntry('None');
        }
        if (p_obj['ControllerFamily'] == 'UPB') {
			self.fillInsteonEntry('none');
			self.fillUpbEntry('');
        }
		self.nodeById('LightEntryButtonsDiv').innerHTML = buildEntryButtons('handleDataOnClick');
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
        p_data['InsteonAddress'] = fetchTextWidget('LightAddressI');
        p_data['DevCat'] = fetchTextWidget('LightDevCat');
        p_data['GroupNumber'] = fetchTextWidget('LightGroupNumber');
        p_data['GroupList'] = fetchTextWidget('LightGroupList');
        p_data['IsMaster'] = fetchTrueFalseWidget('LightMaster');
        p_data['IsResponder'] = fetchTrueFalseWidget('LightResponder');
        p_data['ProductKey'] = fetchTextWidget('LightProductKey');
		// Divmod.debug('---', 'lights.fetchInsteonEntry() finished.');
		return p_data;
	},
	function fetchUpbEntry(self, p_data) {
		// Divmod.debug('---', 'lights.fetchUpbEntry() was called.');
        p_data['UPBAddress'] = fetchTextWidget('LightAddressU');
        p_data['UPBPassword'] = fetchTextWidget('LightPassword');
        p_data['UPBNetworkID'] = fetchTextWidget('LightNetworkID');
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
                }
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
			l_obj['Delete'] = true;
	    	var l_json = JSON.stringify(l_obj);
	        var l_defer = self.callRemote("saveLightData", l_json);
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
