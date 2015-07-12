/**
 * @name:      PyHouse/src/Modules/Web/js/house.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2012-2015 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created about 2012
 * @summary:   Displays the Internet element
 *
 */


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
		function cb_widgetready() {
			self.hideWidget();
		}
		function eb_widgetready(p_reason) {
			Divmod.debug('---', 'ERROR - house.eb_widgetready() - ' + p_reason);
		}
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	function startWidget(self) {
		showDataEntryFields(self);
		self.fetchDataFromServer();
	},



// ============================================================================
	/**
	 * This triggers getting the house data from the server.
	 */
	function fetchDataFromServer(self) {
		function cb_fetchDataFromServer(p_json) {
			globals.House.HouseObj.House = JSON.parse(p_json);
			var l_obj = globals.House.HouseObj;
			console.log("house.buildLcarRoomDataEntryScreen() - Fetched Data = %O", l_obj);
			self.buildLcarDataEntryScreen(l_obj, 'handleDataEntryOnClick');
		}
		function eb_fetchDataFromServer(p_reason) {
			Divmod.debug('---', 'ERROR - house.eb_fetchDataFromServer() - ' + p_reason);
		}
        var l_defer = self.callRemote("getHouseData");  // call server @ web_house.py
		l_defer.addCallback(cb_fetchDataFromServer);
		l_defer.addErrback(eb_fetchDataFromServer);
        return false;
	},
	function buildLcarDataEntryScreen(self, p_entry, p_handler){
		var l_house = arguments[1];
		var l_location = l_house.Location;
		var l_entry_html = "";
		l_entry_html += buildLcarTextWidget(self, 'Name', 'House Name', l_house.Name);
		l_entry_html += buildLcarTextWidget(self, 'Key', 'House Index', l_house.Key, 'disabled');
		l_entry_html += buildLcarTrueFalseWidget(self, 'Active', 'Active ?', l_house.Active);
		l_entry_html += buildLcarTextWidget(self, 'UUID', 'UUID', l_house.UUID);
		l_entry_html += buildLcarTextWidget(self, 'Street', 'Street', l_location.Street);
		l_entry_html += buildLcarTextWidget(self, 'City', 'City', l_location.City);
		l_entry_html += buildLcarTextWidget(self, 'State', 'State', l_location.State);
		l_entry_html += buildLcarTextWidget(self, 'ZipCode', 'Zip Code', l_location.ZipCode);
		l_entry_html += buildLcarTextWidget(self, 'Phone', 'Phone', l_location.Phone);
		l_entry_html += buildLcarTextWidget(self, 'Latitude', 'Latitude', l_location.Latitude);
		l_entry_html += buildLcarTextWidget(self, 'Longitude', 'Longitude', l_location.Longitude);
		l_entry_html += buildLcarTextWidget(self, 'TimeZoneName', 'TimeZone Name', l_location.TimeZoneName);
		l_entry_html += buildLcarEntryButtons(p_handler, 'NoDelete');
		var l_html = build_lcars_top('Enter House Data', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(20, l_entry_html);
		l_html += build_lcars_bottom();
		self.nodeById('DataEntryDiv').innerHTML = l_html;
	},

	function createEntry() {
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
				DaylightSavingsTime : ''
    		};
        var l_data = {
    			Name	: 'Change Me',
    			Key		: 0,
    			Active	: false,
    			UUID	: '',
    			Location : l_loc,
    			Delete	: false
    		};
        //console.log("create House %O", l_data);
        return l_data;
	},
	function fetchEntry(self) {
		//Divmod.debug('---', 'house.fetchEntry() was called. ');
        var l_data = {
            Name			: fetchTextWidget(self, 'Name'),
            Key				: fetchTextWidget(self, 'Key'),
			Active			: fetchTrueFalseWidget(self, 'Active'),
			UUID			: fetchTextWidget(self, 'UUID'),
			Delete			: false
        };
		var l_location = {
			Street			: fetchTextWidget(self, 'Street'),
			City			: fetchTextWidget(self, 'City'),
			State			: fetchTextWidget(self, 'State'),
			ZipCode			: fetchTextWidget(self, 'ZipCode'),
			Phone			: fetchTextWidget(self, 'Phone'),
			Latitude		: fetchTextWidget(self, 'Latitude'),
			Longitude		: fetchTextWidget(self, 'Longitude'),
			TimeZoneName	: fetchTextWidget(self, 'TimeZoneName'),
        };
        l_data.Location = l_location;
		return l_data;
	},



// ============================================================================
	/**
	 * Event handler for buttons at bottom of the data entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataEntryOnClick(self, p_node) {
		function cb_handleDataEntryOnClick() {
			self.showWidget('HouseMenu');
		}
		function eb_handleDataEntryOnClick(p_reason){
			Divmod.debug('---', 'ERROR house.eb_handleDataEntryOnClick() - ' + p_reason);
		}
		var l_ix = p_node.name;
		switch(l_ix) {
		case '10003':  // Change Button
			Divmod.debug('---', 'house.handleDataEntryOnClick() was called.');
	    	var l_entry = self.fetchEntry();
			globals.House.HouseObj.House = l_entry;
	    	var l_json = JSON.stringify(l_entry);
	        var l_defer = self.callRemote("saveHouseData", l_json);  // @ web_house
			l_defer.addCallback(cb_handleDataEntryOnClick);
			l_defer.addErrback(eb_handleDataEntryOnClick);
			break;
		case '10002':  // Back button
			self.showWidget('HouseMenu');
			break;
		default:
			Divmod.debug('---', 'house.handleDataEntryOnClick(Default) was called. l_ix:' + l_ix);
			break;
		}
        return false;  // false stops the chain.
	}
);
// Divmod.debug('---', 'house.cb_fetchDataFromServer() was called. ' + p_json);
// console.log("house.buildLcarRoomDataEntryScreen() - self = %O", self);
//### END DBK
