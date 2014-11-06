/**
 * @name: PyHouse/src/Modules/Web/js/house.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2012-2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created about 2012
 * @summary: Displays the Internet element
 *
 */
// import Nevow.Athena
// import globals
// import helpers



helpers.Widget.subclass(house, 'HouseWidget').methods(

    function __init__(self, node) {
        house.HouseWidget.upcall(self, "__init__", node);
		//Divmod.debug('---', 'house.__init__() was called.');
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
			self.hideWidget();
		}
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	function showWidget(self) {
		self.node.style.display = 'block';
		self.showDataEntry();
		self.fetchHouseData();
	},
	function hideDataEntry(self) {
		self.nodeById('HouseEntryDiv').style.display = 'none';		
	},
	function showDataEntry(self) {
		self.nodeById('HouseEntryDiv').style.display = 'block';		
	},



// ============================================================================
	function buildLcarDataEntryScreen(self, p_entry, p_handler){
		// Divmod.debug('---', 'house.cb_fetchHouseData() was called. ' + p_json);
		// console.log("house.buildLcarRoomDataEntryScreen() - self = %O", self);
		var l_house = arguments[1];
		var l_entry_html = "";
		l_entry_html += buildLcarTextWidget(self, 'Name', 'House Name', l_house.Name);
		l_entry_html += buildLcarTextWidget(self, 'Key', 'House Index', l_house.Key);
		l_entry_html += buildLcarTrueFalseWidget(self, 'Active', 'Active ?', l_house.Active);
		l_entry_html += buildLcarTextWidget(self, 'Street', 'Street', l_house.Street);
		l_entry_html += buildLcarTextWidget(self, 'City', 'City', l_house.City);
		l_entry_html += buildLcarTextWidget(self, 'State', 'State', l_house.State);
		l_entry_html += buildLcarTextWidget(self, 'ZipCode', 'Zip Code', l_house.ZipCode);
		l_entry_html += buildLcarTextWidget(self, 'Phone', 'Phone', l_house.Phone);
		l_entry_html += buildLcarTextWidget(self, 'Latitude', 'Latitude', l_house.Latitude);
		l_entry_html += buildLcarTextWidget(self, 'Longitude', 'Longitude', l_house.Longitude);
		l_entry_html += buildLcarTextWidget(self, 'TimeZoneName', 'TimeZone Name', l_house.TimeZone);
		l_entry_html += buildLcarTextWidget(self, 'TimeZoneOffset', 'TimeZone Offset', l_house.TimeZone);
		l_entry_html += buildLcarTextWidget(self, 'DST', 'DST', l_house.DaylightSavingsTime);
		l_entry_html += buildLcarTextWidget(self, 'UUID', 'UUID', l_house.UUID);

		l_entry_html += buildLcarEntryButtons(p_handler);
		var l_html = build_lcars_top('Enter House Data', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(20, l_entry_html);
		l_html += build_lcars_bottom();
		self.nodeById('DataEntryDiv').innerHTML = l_html;
	},
	/**
	 * This triggers getting the house data from the server.
	 * The server calls displayHouseButtons with the house info.
	 */
	function fetchHouseData(self) {
		function cb_fetchHouseData(p_json) {
			//Divmod.debug('---', 'house.cb_fetchHouseData() was called. ' + p_json);
			globals.House.HouseObj.House = JSON.parse(p_json);
			var l_obj = globals.House.HouseObj;
			self.fillEntry(l_obj);
		}
		function eb_fetchHouseData(res) {
			Divmod.debug('---', 'house.eb_fetchHouseData() was called. ERROR: ' + res);
		}
		if (globals.House.HouseIx == -1) {
			globals.House.HouseObj = {};
			globals.House.HouseObj.House = self.createEntry(0);
			var l_obj = globals.House.HouseObj.House;
			self.fillEntry(l_obj);
			return false;
		}
        var l_defer = self.callRemote("getHouseData");  // call server @ web_house.py
		l_defer.addCallback(cb_fetchHouseData);
		l_defer.addErrback(eb_fetchHouseData);
        return false;
	},

	/**
	 * Fill in the schedule entry screen with all of the data for this schedule.
	 * 
	 */
	function fillEntry(self, p_entry) {
		buildLcarDataEntryScreen(p_entry, 'handleDataOnClick')
	},
	function createEntry(self, p_ix) {
    	//Divmod.debug('---', 'house.createEntry() was called. ' + p_ix);
        var l_loc = {
				Street : '',
				City : '',
				State : '',
				ZipCode : '',
				Phone : '',
				Latitude : '',
				Longitude : '',
				TimeZoneName : '',
				TimeZoneOffset : '',
				DaylightSavingsTime : ''
    		}
        var l_data = {
    			Name : 'Change Me',
    			Key : 0,
    			Active : false,
    			Location : l_loc,
    			Delete : false
    		}
        //console.log("create House %O", l_data);
        return l_data;
	},
	function fetchEntry(self) {
		//Divmod.debug('---', 'house.fetchEntry() was called. ');
        var l_data = {
            Name			: fetchTextWidget(self, 'Name'),
            Key				: fetchTextWidget(self, 'Key'),
			Active			: fetchTrueFalseWidget(self, 'Active'),
			Street			: fetchTextWidget(self, 'Street'),
			City			: fetchTextWidget(self, 'City'),
			State			: fetchTextWidget(self, 'State'),
			ZipCode			: fetchTextWidget(self, 'ZipCode'),
			Phone			: fetchTextWidget(self, 'Phone'),
			Latitude		: fetchTextWidget(self, 'Latitude'),
			Longitude		: fetchTextWidget(self, 'Longitude'),
			TimeZoneName	: fetchTextWidget(self, 'TimeZoneName'),
			TimeZoneOffset	: fetchTextWidget(self, 'TimeZoneOffset'),
			DaylightSavingsTime : fetchTextWidget(self, 'DaylightSavingsTime'),
			UUID			: fetchTextWidget(self, 'UUID'),
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
		globals.House.HouseName = l_name;
		if (l_ix <= 1000) {
			// One of the House buttons.
			var l_obj = globals.House.HouseObj.House[l_ix];
			globals.House.HouseObj = l_obj;
			//Divmod.debug('---', 'house.handleMenuOnClick("House" Button) was called. ' + l_ix + ' ' + l_name);
			//console.log("house.handleMenuOnClick() - l_obj = %O", l_obj);
			self.showDataEntry();
			self.fillEntry(l_obj);
		} else if (l_ix == 10001) {
			// The "Add" button
			//Divmod.debug('---', 'house.handleMenuOnClick(Add Button) was called. ' + l_ix + ' ' + l_name);
			self.showDataEntry();
			var l_ent = self.createEntry();
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
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_entry = self.fetchEntry();
			globals.House.HouseObj.House = l_entry;
	    	var l_json = JSON.stringify(l_entry);
	        var l_defer = self.callRemote("saveHouseData", l_json);  // @ web_house
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			self.hideDataEntry();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget();
			break;
		case '10004':  // Delete button
			var l_entry = self.fetchEntry();
			l_entry['Delete'] = true;
	    	var l_json = JSON.stringify(l_entry);
			//Divmod.debug('---', 'house.handleDataOnClick(Delete) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveHouseData", l_json);  // @ web_rooms
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		default:
			Divmod.debug('---', 'house.handleDataOnClick(Default) was called. l_ix:' + l_ix);
			break;			
		}
        return false;  // false stops the chain.
	}
);
// Divmod.debug('---', 'house.cb_fetchHouseData() was called. ' + p_json);
// console.log("house.buildLcarRoomDataEntryScreen() - self = %O", self);
//### END DBK
