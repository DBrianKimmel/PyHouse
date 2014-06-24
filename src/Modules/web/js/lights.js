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

	// ============================================================================
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
	function showWidget(self) {
		//Divmod.debug('---', 'lights.showWidget() was called.');
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
			Divmod.debug('---', 'lights.cb_fetchHouseData was called.  Self:' + self);
			globals.House.HouseObj = JSON.parse(p_json);
			var l_tab = buildTable(globals.House.HouseObj.Lights, 'handleMenuOnClick', self.buildButtonName);
			self.nodeById('LightTableDiv').innerHTML = l_tab;
		}
		function eb_fetchHouseData(res) {
			Divmod.debug('---', 'lights.eb_fetchHouseData() was called. ERROR: ' + res);
		}
		Divmod.debug('---', 'lights.fetchHouseData was called.  Self:' + self);
        var l_defer = self.callRemote("getHouseData", globals.House.HouseIx);  // call server @ web_lights.py
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
		if (l_ix <= 1000) {  // One of the Light buttons.
			var l_obj = globals.House.HouseObj.Lights[l_ix];
			globals.House.LightObj = l_obj;
			self.showEntry();
			self.hideButtons();
			self.fillEntry(l_obj);
		} else if (l_ix == 10001) {  // The "Add" button
			self.showEntry();
			self.hideButtons();
			var l_ent = self.createEntry(globals.House.HouseIx);
			self.fillEntry(l_ent);
		} else if (l_ix == 10002) {  // The "Back" button
			self.hideWidget();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget();
		}
	},
	function fillEntry(self, p_obj) {
		//Divmod.debug('---', 'lights.fillEntry(1) was called.  Self:' + self);
		//console.log("lights.fillEntry() - Obj = %O", p_obj);
        self.nodeById('NameDiv').innerHTML     = buildTextWidget('LightName', p_obj.Name);
        self.nodeById('KeyDiv').innerHTML      = buildTextWidget('LightKey', p_obj.Key, 'disabled');
		self.nodeById('ActiveDiv').innerHTML   = buildTrueFalseWidget('LightActive', p_obj.Active);
		self.nodeById('CommentDiv').innerHTML  = buildTextWidget('LightComment', p_obj.Comment);
		self.nodeById('CoordsDiv').innerHTML   = buildTextWidget('LightCoords', p_obj.Coords);
		self.nodeById('DimmableDiv').innerHTML = buildTrueFalseWidget('LightDimmable', p_obj.IsDimmable);
		self.nodeById('FamilyDiv').innerHTML   = buildFamilySelectWidget('LightFamily', 'Families', p_obj.LightingFamily);
		self.nodeById('RoomNameDiv').innerHTML = buildRoomSelectWidget('LightRoomName', p_obj.RoomName);
		self.nodeById('TypeDiv').innerHTML     = buildTextWidget('LightType', p_obj.LightingType, 'disabled');
		self.nodeById('UUIDDiv').innerHTML     = buildTextWidget('LightUUID', p_obj.UUID, 'disabled');
        if (p_obj['LightingFamily'] == 'Insteon') {  // Insteon info
			self.fillInsteonEntry(p_obj);
        }
		self.nodeById('LightEntryButtonsDiv').innerHTML = buildEntryButtons('handleDataOnClick');
	},
	function fillInsteonEntry(self, p_obj) {
		//console.log("lights.fillInsteonEntry() - Obj = %O", p_obj);
		//self.nodeById('Row_i01').style.display = 'inline';	
		//self.nodeById('Row_i02').style.display = 'block';	
		//self.nodeById('Row_i03').style.display = 'inline';	
		//self.nodeById('Row_i04').style.display = 'block';	
		//self.nodeById('Row_i05').style.display = 'block';	
		//self.nodeById('Row_i06').style.display = 'block';	
		//self.nodeById('Row_i07').style.display = 'block';	
		self.nodeById('i01Div').innerHTML  = buildTextWidget('LightAddress', p_obj.InsteonAddress);
		self.nodeById('i02Div').innerHTML  = buildTextWidget('LightDevCat', p_obj.DevCat);
		self.nodeById('i03Div').innerHTML  = buildTextWidget('LightGroupNumber', p_obj.GroupNumber);
		self.nodeById('i04Div').innerHTML  = buildTextWidget('LightGroupList', p_obj.GroupList);
		self.nodeById('i05Div').innerHTML  = buildTrueFalseWidget('LightMaster', p_obj.IsMaster);
		self.nodeById('i06Div').innerHTML  = buildTrueFalseWidget('LightResponder', p_obj.IsResponder);
		self.nodeById('i07Div').innerHTML  = buildTextWidget('LightProductKey', p_obj.ProductKey);
	},
	function fillUpbEntry(self, p_obj) {
		self.nodeById('i01Div').innerHTML  = buildTextWidget('LightAddress', p_obj.Address);
	},
	function fetchEntry(self) {
        var l_data = {
            Name        : fetchTextWidget('LightName'),
            Key         : fetchTextWidget('LightKey'),
			Active      : fetchTrueFalseWidget('LightActive'),
			Comment     : fetchTextWidget('LightComment'),
			Coords      : fetchTextWidget('LightCoords'),
			IsDimmable    : fetchTrueFalseWidget('LightDimmable'),
			LightingFamily : fetchSelectWidget('LightFamily'),
			RoomName    : fetchSelectWidget('LightRoomName'),
			LightingType: fetchTextWidget('LightType'),
			UUID        : fetchTextWidget('LightUUID'),
			HouseIx     : globals.House.HouseIx,
			Delete      : false
            }
        if (l_data['LightingFamily'] == 'Insteon') {
        	l_data = self.fetchInsteonEntry(l_data);
        }
		return l_data;
	},
	function fetchInsteonEntry(self, p_data) {
		//Divmod.debug('---', 'lights.fetchInsteonEntry(1) was called. ' + p_data);
        p_data['InsteonAddress'] = fetchTextWidget('LightAddress');
        p_data['DevCat'] = fetchTextWidget('LightDevCat');
        p_data['GroupNumber'] = fetchTextWidget('LightGroupNumber');
        p_data['GroupList'] = fetchTextWidget('LightGroupList');
        p_data['IsMaster'] = fetchTrueFalseWidget('LightMaster');
        p_data['IsResponder'] = fetchTrueFalseWidget('LightResponder');
        p_data['ProductKey'] = fetchTextWidget('LightProductKey');
		//Divmod.debug('---', 'lights.fetchInsteonEntry(2) was called. ' + p_data);
        //console.log("lights.fetchInsteonEntry(3)  %O", p_data)
		return p_data;
	},
	function createEntry(self, p_ix) {
		//Divmod.debug('---', 'lights.createEntry() was called.  Ix: ' + p_ix);
        var l_Data = {
    			Name     : 'Change Me',
    			Key      : Object.keys(globals.House.HouseObj.Lights).length,
    			Active   : false,
    			Comment  : '',
    			Coords   : '',
    			IsDimmable : false,
    			LightingFamily   : 'Insteon',
    			RoomName : '',
    			Type     : 'Light',
    			UUID     : '',
    			InsteonAddress  : '',
    			HouseIx  : p_ix,
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
			//Divmod.debug('---', 'lights.cb_handleDataOnClick() was called.');
			self.showWidget();
		}
		function eb_handleDataOnClick(res){
			Divmod.debug('---', 'lights.eb_handleDataOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		//Divmod.debug('---', 'lights.handleDataOnClick() was called. Node:' + l_ix);
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry());
	        //console.log("lights.handleDataOnClick()  json  %O", l_json)
			//Divmod.debug('---', 'lights.handleDataOnClick(Change) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveLightData", l_json);  // @ web_lights
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			//Divmod.debug('---', 'lights.handleDataOnClick(Back) was called.  ');
			self.hideEntry();
			self.showButtons();
			break;
		case '10004':  // Delete button
			var l_obj = self.fetchEntry();
			l_obj['Delete'] = true;
	    	var l_json = JSON.stringify(l_obj);
			//Divmod.debug('---', 'lights.handleDataOnClick(Delete) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveLightData", l_json);  // @ web_rooms
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
//### END DBK
