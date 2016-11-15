/**
 * @name: PyHouse/src/Modules/Web/js/users.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2015 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Mar 11, 2014
 * @summary: Displays the users
 */
// import Nevow.Athena
// import globals
// import helpers
helpers.Widget.subclass(users, 'UsersWidget').methods(

function __init__(self, node) {
	users.UsersWidget.upcall(self, '__init__', node);
},

// ============================================================================
/**
 * Place the widget in the workspace.
 * 
 * @param self
 *            is <"Instance" of undefined.users.UsersWidget>
 * @returns a deferred
 */
function ready(self) {
	function cb_widgetready(res) {
		self.hideWidget();
	}
	function eb_widgetready(p_result) {
		Divmod.debug('---', 'users.eb_widgetready() was called. ERROR = ' + p_result);
	}
	var uris = collectIMG_src(self.node, null);
	var l_defer = loadImages(uris);
	l_defer.addCallback(cb_widgetready);
	l_defer.addErrback(eb_widgetready);
	return l_defer;
},
/**
 * Show the self.node widget - users.UsersWidget -
 */
function startWidget(self) {
	// Divmod.debug('---', 'users.startWidget() was called.');
	self.node.style.display = 'block';
	showSelectionButtons(self);
	self.fetchDataFromServer();
},

// ============================================================================
/**
 * This triggers getting the data from the server.
 */
function fetchDataFromServer(self) {
	function cb_fetchDataFromServer(p_json) {
		globals.Computer.Logins = JSON.parse(p_json);
		// console.log("users.fetchDataFromServer() - Data = %O",
		// globals.Computer);
		self.buildLcarSelectScreen();
	}
	function eb_fetchDataFromServer(p_result) {
		Divmod.debug('---', 'users.eb_fetchDataFromServer() was called. ERROR = ' + p_result);
	}
	var l_defer = self.callRemote("getUsersData"); // @ web_users.py
	l_defer.addCallback(cb_fetchDataFromServer);
	l_defer.addErrback(eb_fetchDataFromServer);
	return false;
},
/**
 * Build a screen full of buttons - One for each room and some actions.
 */
function buildLcarSelectScreen(self) {
	var l_button_html = buildLcarSelectionButtonsTable(globals.Computer.Logins, 'handleMenuOnClick');
	var l_html = build_lcars_top('Users', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(15, l_button_html);
	l_html += build_lcars_bottom();
	self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
},
/**
 * Event handler for room selection buttons.
 * 
 * The user can click on a room button, the "Add" button or the "Back" button.
 * 
 * @param self
 *            is <"Instance" of undefined.schedules.SchedulesWidget>
 * @param p_node
 *            is the node of the button that was clicked.
 */
function handleMenuOnClick(self, p_node) {
	var l_ix = p_node.name;
	var l_name = p_node.value;
	globals.Computer.LoginIx = l_ix;
	globals.Computer.LoginName = l_name;
	if (l_ix <= 1000) { // One of the users buttons.
		var l_obj = globals.Computer.Logins[l_ix];
		globals.Computer.Logins = l_obj;
		showDataEntryScreen(self);
		self.buildDataEntryScreen(l_obj, 'handleDataEntryOnClick');
	} else if (l_ix == 10001) { // The "Add" button
		showDataEntryScreen(self);
		var l_entry = self.createEntry();
		self.buildDataEntryScreen(l_entry, 'handleDataEntryOnClick');
	} else if (l_ix == 10002) { // The "Back" button
		self.showWidget('HouseMenu');
	}
},

// ============================================================================
/**
 * Build a screen full of data entry fields.
 */
function buildDataEntryScreen(self, p_entry, p_handler) {
	var l_obj = arguments[1];
	var l_html = build_lcars_top('Login', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(10, self.buildEntry(l_obj, p_handler));
	l_html += build_lcars_bottom();
	self.nodeById('DataEntryDiv').innerHTML = l_html;
},

function buildEntry(self, p_obj, p_add_change, p_handler, p_onchange) {
	var l_html = '';
	l_html = self.buildLoginEntry(p_obj, l_html, p_handler);
	l_html = buildLcarEntryButtons(p_handler, l_html);
	return l_html;
},

function buildLoginEntry(self, p_obj, p_html, p_handler) {
	p_html += buildLcarTextWidget(self, 'Name', 'Name', p_obj.Name);
	p_html += buildLcarTextWidget(self, 'Key', 'User Index', p_obj.Key, 'disabled');
	p_html += buildTrueFalseWidget(self, 'IsActive', 'Active ?', p_obj.Active);
	p_html += buildLcarTextWidget(self, 'FullName', 'Full Name', p_obj.LoginFullName);
	p_html += buildLcarPasswordWidget(self, 'Password_1', 'Password', p_obj.LoginPasswordCurrent);
	p_html += buildLcarPasswordWidget(self, 'Password_2', 'Password Verify', p_obj.LoginPasswordCurrent);
	p_html += buildLcarUserRoleSelectWidget(self, 'Role', 'Role', p_obj.LoginRole);
	return p_html;
},

function createEntry(self) {
	var l_data = {
		Name : 'Change Me',
		Key : Object.keys(globals.Computer.Logins).length,
		Active : true,
		FullName : '',
		Password : '',
		Role : '',
		Delete : false
	};
	return l_data;
},

function fetchEntry(self) {
	Divmod.debug('---', 'users.fetchEntry() was called. ');
	var l_data = {
		Name : fetchTextWidget(self, 'Name'),
		Key : fetchTextWidget(self, 'Key'),
		Active : fetchTrueFalseWidget(self, 'IsActive'),
		FullName : fetchTextWidget(self, 'FullName'),
		Password_1 : fetchTextWidget(self, 'Password_1'),
		Password_2 : fetchTextWidget(self, 'Password_2'),
		Role : fetchSelectWidget(self, 'Role'),
		Delete : false,
		IsValid : false
	};
	if ((l_data['Password_1'] == l_data['Password_2']) && (l_data['Password_1'].length > 7))
		l_data.IsValid = true;
	console.log("users.fetchEntry() - l_data = %O", l_data);
	return l_data;
},

// ============================================================================
/**
 * Event handler for users buttons at bottom of entry portion of this widget.
 * Get the possibly changed data and send it to the server.
 * 
 * @param self
 *            is <"Instance" of undefined.users.UsersWidget>
 * @param p_node
 *            is the button node that was clicked on
 */
function handleDataEntryOnClick(self, p_node) {
	function cb_handleDataEntryOnClick(p_json) {
		self.startWidget();
	}
	function eb_handleDataEntryOnClick(res) {
		Divmod.debug('---', 'users.eb_handleDataEntryOnClick() was called. ERROR =' + res);
	}
	var l_ix = p_node.name;
	var l_defer;
	var l_json;
	switch (l_ix) {
	case '10003': // Change Button
		l_json = JSON.stringify(self.fetchEntry());
		l_defer = self.callRemote("putUsersData", l_json); // @ web_schedule
		l_defer.addCallback(cb_handleDataEntryOnClick);
		l_defer.addErrback(eb_handleDataEntryOnClick);
		break;
	case '10002': // Back button
		showSelectionButtons(self);
		break;
	case '10004': // Delete button
		var l_obj = self.fetchEntry();
		l_obj.Delete = true;
		l_json = JSON.stringify(l_obj);
		l_defer = self.callRemote("putUsersData", l_json); // @ web_users
		l_defer.addCallback(cb_handleDataEntryOnClick);
		l_defer.addErrback(eb_handleDataEntryOnClick);
		break;
	default:
		Divmod.debug('---', 'users.handleDataEntryOnClick(Default) was called. l_ix:' + l_ix);
		break;
	}
	// return false stops the resetting of the server.
	return false;
});
// Divmod.debug('---', 'users.handleMenuOnClick(1) was called. ' + l_ix + ' ' +
// l_name);
// console.log("users.handleMenuOnClick() - l_obj = %O", l_obj);
// ### END DBK
