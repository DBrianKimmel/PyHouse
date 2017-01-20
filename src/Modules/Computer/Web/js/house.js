/**
 * @name: PyHouse/src/Modules/Web/js/house.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @copyright: (c) 2012-2017 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created about 2012
 * @summary: Displays the House element
 * 
 */

helpers.Widget.subclass(house, 'HouseWidget').methods(

function __init__(self, node) {
	house.HouseWidget.upcall(self, "__init__", node);
},

// ============================================================================
/**
 * Place the widget in the workspace.
 * 
 * @param self
 *            is <"Instance" of undefined.house.HouseWidget>
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
	// Divmod.debug('---', 'house.ready() was called.');
	l_defer.addCallback(cb_widgetready);
	l_defer.addErrback(eb_widgetready);
	return l_defer;
},

function startWidget(self) {
	showDataEntryScreen(self);
	self.fetchDataFromServer();
},

// ============================================================================
/**
 * This triggers getting the data from the server.
 */
function fetchDataFromServer(self) {
	function cb_fetchDataFromServer(p_json) {
		globals.House = JSON.parse(p_json);
		var l_obj = globals.House;
		// console.log("house.buildLcarRoomDataEntryScreen() - Fetched Data = %O", l_obj);
		self.buildDataEntryScreen(l_obj, 'handleDataEntryOnClick');
	}
	function eb_fetchDataFromServer(p_reason) {
		Divmod.debug('---', 'ERROR - house.eb_fetchDataFromServer() - ' + p_reason);
	}
	var l_defer = self.callRemote("getHouseData"); // call server @ web_house.py
	l_defer.addCallback(cb_fetchDataFromServer);
	l_defer.addErrback(eb_fetchDataFromServer);
	return false;
},

function buildDataEntryScreen(self, p_entry, p_handler) {
	var l_obj = arguments[1];
	// console.log("house.buildDataEntryScreen() - Data = %O", l_obj);
	var l_html = build_lcars_top('Enter House Data', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(25, self.buildEntry(l_obj, p_handler));
	l_html += build_lcars_bottom();
	self.nodeById('DataEntryDiv').innerHTML = l_html;
},

function buildEntry(self, p_obj, p_handler, p_onchange) {
	var l_html = '';
	l_html = buildBaseEntry(self, p_obj, l_html);
	l_html = self.buildLocationEntry(p_obj.Location, l_html);
	l_html = buildLcarEntryButtons(p_handler, l_html);
	return l_html;
},

function buildLocationEntry(self, p_obj, p_html) {
	p_html += buildTextWidget(self, 'Street', 'Street', p_obj.Street);
	p_html += buildTextWidget(self, 'City', 'City', p_obj.City);
	p_html += buildTextWidget(self, 'State', 'State', p_obj.State);
	p_html += buildTextWidget(self, 'ZipCode', 'Zip Code', p_obj.ZipCode);
	p_html += buildTextWidget(self, 'Region', 'Region', p_obj.Region);
	p_html += buildTextWidget(self, 'Phone', 'Phone', p_obj.Phone);
	p_html += buildTextWidget(self, 'Latitude', 'Latitude', p_obj.Latitude);
	p_html += buildTextWidget(self, 'Longitude', 'Longitude', p_obj.Longitude);
	p_html += buildTextWidget(self, 'Elevation', 'Elevation', p_obj.Elevation);
	p_html += buildTextWidget(self, 'TimeZoneName', 'TimeZone Name', p_obj.TimeZoneName);
	p_html += buildTrueFalseWidget(self, 'Master', 'Master', p_obj.Master);
	return p_html;
},

function fetchEntry(self) {
	var l_data = fetchBaseEntry(self);
	var l_loc = self.fetchLocationEntry(l_data);
	l_data.Location = l_loc;
	return l_data;
},

function fetchLocationEntry(self) {
	var l_data = {
		Street : fetchTextWidget(self, 'Street'),
		City : fetchTextWidget(self, 'City'),
		State : fetchTextWidget(self, 'State'),
		ZipCode : fetchTextWidget(self, 'ZipCode'),
		Region : fetchTextWidget(self, 'Region'),
		Phone : fetchTextWidget(self, 'Phone'),
		Latitude : fetchTextWidget(self, 'Latitude'),
		Longitude : fetchTextWidget(self, 'Longitude'),
		Elevation : fetchTextWidget(self, 'Elevation'),
		TimeZoneName : fetchTextWidget(self, 'TimeZoneName'),
		Master : fetchTrueFalseWidget(self, 'Master')
	}
	return l_data;
},

function createEntry(self) {
	var l_data = createBaseEntry(self, 0);
	l_data = self.createLocationEntry(l_data);
	return l_data;
},

function createLocationEntry(self, p_data) {
	p_data.Name = 'Change Me';
	p_data.Key = 0;
	p_data.Active = false;
	// p_data.UUID = ''; Keep the UUID generated in createBaseEntry
	p_data.Location.Street = '';
	p_data.Location.City = '';
	p_data.Location.State = '';
	p_data.Location.ZipCode = '';
	p_data.Location.Region = '';
	p_data.Location.Phone = '';
	p_data.Location.Latitude = '';
	p_data.Location.Longitude = '';
	p_data.Location.Elevation = '';
	p_data.Location.TimeZoneName = '';
	p_data.Master = true;
	p_data.Delete = false;
	return p_data;
},

// ============================================================================
/**
 * Event handler for buttons at bottom of the data entry portion of this widget. Get the possibly changed data and send it to the server.
 */
function handleDataEntryOnClick(self, p_node) {
	function cb_handleDataEntryOnClick() {
		self.showWidget('HouseMenu');
	}
	function eb_handleDataEntryOnClick(p_reason) {
		Divmod.debug('---', 'ERROR house.eb_handleDataEntryOnClick() - ' + p_reason);
	}
	var l_ix = p_node.name;
	switch (l_ix) {
	case '10003': // Change Button
		// Divmod.debug('---', 'house.handleDataEntryOnClick() was called.');
		var l_entry = self.fetchEntry();
		globals.House = l_entry;
		var l_json = JSON.stringify(l_entry);
		var l_defer = self.callRemote("saveHouseData", l_json); // @ web_house
		l_defer.addCallback(cb_handleDataEntryOnClick);
		l_defer.addErrback(eb_handleDataEntryOnClick);
		break;
	case '10002': // Back button
		self.showWidget('HouseMenu');
		break;
	default:
		Divmod.debug('---', 'house.handleDataEntryOnClick(Default) was called. l_ix:' + l_ix);
		break;
	}
	return false; // false stops the chain.
}

);

// Divmod.debug('---', 'house.cb_fetchDataFromServer() was called.');
// console.log("house.buildLcarRoomDataEntryScreen() - self = %O", self);

// ### END DBK
