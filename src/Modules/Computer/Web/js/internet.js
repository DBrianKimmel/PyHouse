/**
 * @name: PyHouse/src/Modules/Web/js/internet.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @c:opyright (c) 2012-2015 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created about 2012
 * @summary: Displays the Internet element
 * 
 */

helpers.Widget.subclass(internet, 'InternetWidget').methods(

function __init__(self, node) {
	internet.InternetWidget.upcall(self, "__init__", node);
	// Divmod.debug('---', 'internet.__init__() was called.');
},

// ============================================================================
/**
 * Place the widget in the workspace.
 * 
 * @param self
 *            is <"Instance" of undefined.internet.InternetWidget>
 * @returns a deferred
 */
function ready(self) {
	function cb_widgetready(res) {
		// Divmod.debug('---', 'internet.cb_widgready was called.');
		self.hideWidget();
	}
	// Divmod.debug('---', 'internet.ready() was called.');
	var uris = collectIMG_src(self.node, null);
	var l_defer = loadImages(uris);
	l_defer.addCallback(cb_widgetready);
	return l_defer;
},

function startWidget(self) {
	self.node.style.display = 'block';
	showSelectionButtons(self);
	self.fetchDataFromServer();
},

// ============================================================================
/**
 * This triggers getting the Internet data from the server.
 */
function fetchDataFromServer(self) {
	function cb_fetchDataFromServer(p_json) {
		globals.Computer = JSON.parse(p_json);
		console.log("internet.fetchDataFromServer() - Json = %O", globals.Computer);
		self.buildLcarSelectScreen();
	}
	function eb_fetchDataFromServer(res) {
		Divmod.debug('---', 'internet.eb_fetchDataFromServer() was called. ERROR: ' + res);
	}
	var l_defer = self.callRemote("getInternetData"); // call server @ web_internet.py
	l_defer.addCallback(cb_fetchDataFromServer);
	l_defer.addErrback(eb_fetchDataFromServer);
	return false;
},

/**
 * Build a screen full of buttons - One for each internet and some actions.
 */
function buildLcarSelectScreen(self) {
	// Divmod.debug('---', 'internet.buildLcarSelectScreen() was called.');
	var l_button_html = buildLcarSelectionButtonsTable(globals.Computer.Internet, 'handleMenuOnClick');
	var l_html = build_lcars_top('Internet', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(10, l_button_html);
	l_html += build_lcars_bottom();
	self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
},

// ============================================================================
/**
 * Event handler for internet selection buttons.
 * 
 * The user can click on a internet button, the "Add" button or the "Back" button.
 * 
 * @param self
 *            is <"Instance" of undefined.internet.InternetWidget>
 * @param p_node
 *            is the node of the button that was clicked.
 */
function handleMenuOnClick(self, p_node) {
	// Divmod.debug('---', 'internet.handleMenuOnClick() was called.');
	var l_ix = p_node.name;
	var l_name = p_node.value;
	var l_obj;
	globals.InternetIx = l_ix;
	globals.InternetName = l_name;
	globals.Self = self;
	globals.Add = false;
	showDataEntryScreen(self);
	if (l_ix <= 1000) { // One of the Internet buttons.
		l_obj = globals.Computer.Internet[l_ix];
		globals.InternetObj = l_obj;
		self.buildDataEntryScreen(l_obj, 'handleDataOnClick');
	} else if (l_ix == 10001) { // The "Add" button
		l_obj= self.createEntry();
		globals.Add = true;
		self.buildDataEntryScreen(l_obj, 'handleDataOnClick');
	} else if (l_ix == 10002) { // The "Back" button
		self.showWidget('ComputerMenu');
	}
},

//============================================================================
/**
 * Build a screen full of data entry fields.
 */
function buildDataEntryScreen(self, p_entry, p_handler) {
	var l_obj = arguments[1];
	var l_html = build_lcars_top('InternetData', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(15, self.buildEntry(l_obj, p_handler));
	l_html += build_lcars_bottom();
	self.nodeById('DataEntryDiv').innerHTML = l_html;
},

function buildEntry(self, p_obj, p_handler, p_onchange) {
	// console.log("internet.buildEntry() - p_obj = %O", p_obj);
	var l_html = '';
	// l_html = buildBaseEntry(self, p_obj, l_html);
	l_html = self.buildInternetEntry(p_obj, l_html);
	l_html = buildLcarEntryButtons(p_handler, l_html);
	return l_html;
},

function buildInternetEntry(self, p_obj, p_html) {
	p_html += buildLcarTextWidget(self, 'IPv4', 'IPv4', p_obj.ExternalIPv4, 'disabled');
	p_html += buildLcarTextWidget(self, 'IPv6', 'IPv6', p_obj.ExternalIPv6, 'disabled');
	p_html += buildLcarTextWidget(self, 'Interval', 'Update Interval', p_obj.UpdateInterval, 'size=20');
	p_html += buildLcarTextWidget(self, 'Discovery', 'Discovery Urls', p_obj.LocateUrls, 'size=80');
	p_html += buildLcarTextWidget(self, 'Update', 'Update Urls', p_obj.UpdateUrls, 'size=80');
	return p_html;
},

function fetchEntry(self) {
	// Divmod.debug('---', 'internet.fetchEntry() was called. ');
	var l_data = {};
	l_data.Delete = false;
	// l_data = fetchBaseEntry(self);
	l_data = self.fetchInternetEntry(l_data);
	// console.log("internet.fetchEntry() - Data = %O", l_data);
	return l_data;
},

function fetchInternetEntry(self, p_data) {
	p_data.UpdateInterval = fetchTextWidget(self, 'Interval');

	var l_txt = fetchTextWidget(self, 'Discovery');
	l_txt = l_txt.split(" ")
	p_data.LocateUrls = l_txt;

	var l_txt = fetchTextWidget(self, 'Update');
	l_txt = l_txt.split(" ")
	p_data.UpdateUrls = l_txt;

	// p_data.LocateUrls = fetchTextWidget(self, 'Discovery');
	return p_data;
},

function createEntry(self) {
	// Divmod.debug('---', 'internet.createEntry() was called.');
	var l_data = {};
	// var l_key = 0;
	// var l_data = createBaseEntry(self, l_key);
	self.createInternetEntry(l_data);
	return l_data;
},

function createInternetEntry(self, p_data) {
	p_data.ExternalIPv4 = '0.0.0.0';
	p_data.ExternalIPv6 = '1111:222::3333';
	p_data.UpdateInterval = '86400';
	p_data.LocateUrls = '';
	p_data.UpdateUrls = '';
},

// ============================================================================

/**
 * Event handler for buttons at bottom of the data entry portion of this widget. Get the possibly changed data and send it to the server.
 */
function handleDataOnClick(self, p_node) {
	function cb_handleDataOnClick(p_json) {
		// Divmod.debug('---', 'internet.cb_handleDataOnClick() was called.');
		self.startWidget();
	}
	function eb_handleDataOnClick(res) {
		Divmod.debug('---', 'internet.eb_handleDataOnClick() was called. ERROR =' + res);
	}
	var l_ix = p_node.name;
	var l_defer;
	var l_json;
	// Divmod.debug('---', 'internet.handleDataOnClick() was called. Node:' + l_ix);
	switch (l_ix) {
	case '10003': // Change Button
		l_json = JSON.stringify(self.fetchEntry());
		console.log("internet.handleDataOnClick(Change) - Json = %O", l_json);
		l_defer = self.callRemote("saveInternetData", l_json); // @ web_internet
		l_defer.addCallback(cb_handleDataOnClick);
		l_defer.addErrback(eb_handleDataOnClick);
		break;
	case '10002': // Back button
		showSelectionButtons(self);
		break;
	case '10004': // Delete button
		var l_obj = self.fetchEntry();
		l_obj.Delete = true;
		console.log("internet.handleDataOnClick(Delete) - Json = %O", l_json);
		l_json = JSON.stringify(l_obj);
		l_defer = self.callRemote("saveInternetData", l_json); // @ web_rooms
		l_defer.addCallback(cb_handleDataOnClick);
		l_defer.addErrback(eb_handleDataOnClick);
		break;
	default:
		break;
	}
	return false; // false stops the chain.
}

);

// Divmod.debug('---', 'internet.handleMenuOnClick(1) was called. ' + l_ix + ' ' + l_name);
// console.log("internet.handleMenuOnClick() - l_obj = %O", l_obj);

// ### END DBK
