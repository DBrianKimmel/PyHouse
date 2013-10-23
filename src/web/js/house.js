/**
 * house.js
 * 
 * The house widget.
 */

// import Nevow.Athena
// import globals
// import helpers

/**
 * The house widget.
 */
helpers.Widget.subclass(house, 'HouseWidget').methods(

    function __init__(self, node) {
        house.HouseWidget.upcall(self, "__init__", node);
    },

	// ============================================================================
	/**
     * Place the widget in the workspace.
	 * 
	 * @param self is    <"Instance" of undefined.house.HouseWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		function cb_widgetready(res) {
			//Divmod.debug('---', 'house.js - cb_widgready was called.');
			self.hideWidget();
		}
		//Divmod.debug('---', 'house.ready() was called.');
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	function showWidget(self) {
		self.node.style.display = 'block';
		self.showEntry();
		self.fetchHouseData();
	},
	function hideEntry(self) {
		self.nodeById('HouseEntryDiv').style.display = 'none';		
	},
	function showEntry(self) {
		self.nodeById('HouseEntryDiv').style.display = 'block';		
	},

	// ============================================================================
	/**
	 * This triggers getting the house data from the server.
	 * The server calls displayHouseButtons with the house info.
	 */
	function fetchHouseData(self) {
		function cb_fetchHouseData(p_json) {
			Divmod.debug('---', 'house.cb_fetchHouseData() was called. ' + p_json);
			globals.House.HouseObj.House = JSON.parse(p_json);
			var l_obj = globals.House.HouseObj;
			self.fillEntry(l_obj);
		}
		function eb_fetchHouseData(res) {
			Divmod.debug('---', 'house.eb_fetchHouseData() was called. ERROR: ' + res);
		}
		Divmod.debug('---', 'house.fetchHouseData() was called. ');
		if (globals.House.HouseIx == -1) {
			globals.House.HouseObj = {};
			globals.House.HouseObj.House = self.createEntry(0);
			var l_obj = globals.House.HouseObj.House;
			self.fillEntry(l_obj);
			return false;
		}
        var l_defer = self.callRemote("getHouseData", globals.House.HouseIx);  // call server @ web_house.py
		l_defer.addCallback(cb_fetchHouseData);
		l_defer.addErrback(eb_fetchHouseData);
        return false;
	},

	/**
	 * Fill in the schedule entry screen with all of the data for this schedule.
	 * 
	 */
	function fillEntry(self, p_obj) {
		Divmod.debug('---', 'house.fillEntry(1) was called. ');
		console.log("house.fillEntry() - Obj = %O", p_obj);
        self.nodeById('NameDiv').innerHTML = buildTextWidget('HouseName', p_obj.Name);
        self.nodeById('KeyDiv').innerHTML = buildTextWidget('HouseKey', p_obj.Key, 'disabled');
		self.nodeById('ActiveDiv').innerHTML = buildTrueFalseWidget('HouseActive', p_obj.Active);
		self.nodeById('StreetDiv').innerHTML = buildTextWidget('HouseStreet', p_obj.Location.Street);
		self.nodeById('CityDiv').innerHTML = buildTextWidget('HouseCity', p_obj.Location.City);
		self.nodeById('StateDiv').innerHTML = buildTextWidget('HouseState', p_obj.Location.State);
		self.nodeById('ZipCodeDiv').innerHTML = buildTextWidget('HouseZipCode', p_obj.Location.ZipCode);
		self.nodeById('PhoneDiv').innerHTML = buildTextWidget('HousePhone', p_obj.Location.Phone);
		self.nodeById('LatitudeDiv').innerHTML = buildTextWidget('HouseLatitude', p_obj.Location.Latitude);
		self.nodeById('LongitudeDiv').innerHTML = buildTextWidget('HouseLongitude', p_obj.Location.Longitude);
		self.nodeById('TimeZoneDiv').innerHTML = buildTextWidget('HouseTimeZone', p_obj.Location.TimeZone);
		self.nodeById('SavingsTimeDiv').innerHTML = buildTextWidget('HouseSavingsTime', p_obj.Location.SavingsTime);
		self.nodeById('UUIDDiv').innerHTML = buildTextWidget('HouseUUID', p_obj.UUID, 'disabled');
		self.nodeById('HouseEntryButtonsDiv').innerHTML = buildEntryButtons('handleDataOnClick', 'NoDelete');
	},
	function createEntry(self, p_ix) {
    	Divmod.debug('---', 'house.createEntry() was called. ' + p_ix);
        var l_loc = {
				Street : '',
				City : '',
				State : '',
				ZipCode : '',
				Phone : '',
				Latitude : '',
				Longitude : '',
				TimeZone : '',
				SavingsTime : ''
    		}
        var l_data = {
    			Name : 'Change Me',
    			Key : 0,
    			Active : false,
    			Location : l_loc,
    			HouseIx : p_ix,
    			Delete : false
    		}
        //console.log("create House %O", l_data);
        return l_data;
	},
	function fetchEntry(self) {
		Divmod.debug('---', 'house.fetchEntry() was called. ');
        var l_data = {
            Name : fetchTextWidget('HouseName'),
            Key : fetchTextWidget('HouseKey'),
			Active : fetchTrueFalseWidget('HouseActive'),
			Street : fetchTextWidget('HouseStreet'),
			City : fetchTextWidget('HouseCity'),
			State : fetchTextWidget('HouseState'),
			ZipCode : fetchTextWidget('HouseZipCode'),
			Phone : fetchTextWidget('HousePhone'),
			Latitude : fetchTextWidget('HouseLatitude'),
			Longitude : fetchTextWidget('HouseLongitude'),
			TimeZone : fetchTextWidget('HouseTimeZone'),
			SavingsTime : fetchTextWidget('HouseSavingsTime'),
			UUID : fetchTextWidget('HouseUUID'),
			HouseIx : globals.House.HouseIx,
			Delete : false
            }
		return l_data;
	},

	// ============================================================================
	/**
	 * Event handler for house selection buttons.
	 * 
	 * The user can click on a house button, the "Add" button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.house.HouseWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function handleMenuOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.House.HouseIx = l_ix;
		globals.House.HouseName = l_name;
		if (l_ix <= 1000) {
			// One of the House buttons.
			var l_obj = globals.House.HouseObj.House[l_ix];
			globals.House.HouseObj = l_obj;
			//Divmod.debug('---', 'house.handleMenuOnClick("House" Button) was called. ' + l_ix + ' ' + l_name);
			//console.log("house.handleMenuOnClick() - l_obj = %O", l_obj);
			self.showEntry();
			self.fillEntry(l_obj);
		} else if (l_ix == 10001) {
			// The "Add" button
			//Divmod.debug('---', 'house.handleMenuOnClick(Add Button) was called. ' + l_ix + ' ' + l_name);
			self.showEntry();
			var l_ent = self.createEntry(globals.House.HouseIx);
			self.fillEntry(l_ent);
		} else if (l_ix == 10002) {
			// The "Back" button
			//Divmod.debug('---', 'house.handleMenuOnClick(Back Button) was called. ' + l_ix + ' ' + l_name);
			self.hideWidget();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget();
		}
	},
	
	// ============================================================================
	/**
	 * Event handler for buttons at bottom of the data entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataOnClick(self, p_node) {
		function cb_handleDataOnClick(p_json) {
			//Divmod.debug('---', 'house.cb_handleDataOnClick() was called.');
			self.showWidget();
		}
		function eb_handleDataOnClick(res){
			Divmod.debug('---', 'house.eb_handleDataOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		//Divmod.debug('---', 'house.handleDataOnClick() was called. Node:' + l_ix);
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry());
			Divmod.debug('---', 'house.handleDataOnClick(Change) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveHouseData", l_json);  // @ web_house
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			self.hideEntry();
			break;
		default:
			Divmod.debug('---', 'house.handleDataOnClick(Default) was called. l_ix:' + l_ix);
			break;			
		}
        return false;  // false stops the chain.
	}
);
//### END DBK
