/**
 * @name: PyHouse/src/Modules/Web/js/rooms.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Mar 11, 2014
 * @summary: Displays the rooms
 */
// import Nevow.Athena
// import globals
// import helpers

helpers.Widget.subclass(rooms, 'RoomsWidget').methods(

	function __init__(self, node) {
		rooms.RoomsWidget.upcall(self, '__init__', node);
	},



// ============================================================================
	/**
     * Place the widget in the workspace.
	 * 
	 * @param self is    <"Instance" of undefined.rooms.RoomsWidget>
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
	/**
	 * Show the self.node widget - rooms.RoomsWidget -
	 */
	function startWidget(self) {
		self.node.style.display = 'block';
		self.showSelectionButtons();
		self.hideDataEntry();
		self.fetchDataFromServer();
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



// ============================================================================
	/**
	 * This triggers getting the data from the server.
	 */
	function fetchDataFromServer(self) {
		function cb_fetchDataFromServer(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
			self.buildLcarSelectScreen();
		}
		function eb_fetchDataFromServer(p_result) {
			Divmod.debug('---', 'rooms.eb_fetchDataFromServer() was called. ERROR = ' + p_result);
		}
        var l_defer = self.callRemote("getServerData");  // @ web_rooms.py
		l_defer.addCallback(cb_fetchDataFromServer);
		l_defer.addErrback(eb_fetchDataFromServer);
        return false;
	},
	/**
	 * Build a screen full of buttons - One for each room and some actions.
	 */
	function buildLcarSelectScreen(self){
		var l_button_html = buildLcarSelectionButtonsTable(globals.House.HouseObj.Rooms, 'handleMenuOnClick');
		var l_html = build_lcars_top('Rooms', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(15, l_button_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
	/**
	 * Event handler for room selection buttons.
	 * 
	 * The user can click on a room button, the "Add" button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.schedules.SchedulesWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function handleMenuOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.House.RoomIx = l_ix;
		globals.House.RoomName = l_name;
		if (l_ix <= 1000) {  // One of the rooms buttons.
			var l_obj = globals.House.HouseObj.Rooms[l_ix];
			globals.House.RoomObj = l_obj;
			self.showDataEntry();
			self.hideSelectionButtons();
			self.buildLcarRoomDataEntryScreen(l_obj, 'handleDataEntryOnClick');
		} else if (l_ix == 10001) {  // The "Add" button
			self.showDataEntry();
			self.hideSelectionButtons();
			var l_entry = self.createEntry();
			self.buildLcarRoomDataEntryScreen(l_entry, 'handleDataEntryOnClick');
		} else if (l_ix == 10002) {  // The "Back" button
			self.showWidget2('HouseMenu');
		}
	},


// ============================================================================
	/**
	 * Build a screen full of data entry fields.
	 */
	function buildLcarRoomDataEntryScreen(self, p_entry, p_handler){
		// console.log("rooms.buildLcarRoomDataEntryScreen() - self = %O", self);
		var l_room = arguments[1];
		var l_entry_html = "";
		l_entry_html += buildLcarTextWidget(self, 'Name', 'Room Name', l_room.Name);
		l_entry_html += buildLcarTextWidget(self, 'Key', 'Room Index', l_room.Key);
		l_entry_html += buildLcarTrueFalseWidget(self, 'RoomActive', 'Active ?', l_room.Active);
		l_entry_html += buildLcarTextWidget(self, 'Comment', 'Comment', l_room.Comment);
		l_entry_html += buildLcarTextWidget(self, 'Corner', 'Corner', l_room.Corner);
		l_entry_html += buildLcarTextWidget(self, 'Size', 'Size', l_room.Size);
		l_entry_html += buildLcarEntryButtons(p_handler);
		var l_html = build_lcars_top('Enter Room Data', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(15, l_entry_html);
		l_html += build_lcars_bottom();
		self.nodeById('DataEntryDiv').innerHTML = l_html;
	},
	function createEntry(self) {
    	//Divmod.debug('---', 'rooms.createEntry() was called. ');
        var l_data = {
			Name : 'Change Me',
			Key : Object.keys(globals.House.HouseObj.Rooms).length,
			Active : false,
			Comment : '',
			Corner : '',
			Size : '',
			Delete : false
		};
		return l_data;
	},
	function fetchEntry(self) {
    	// Divmod.debug('---', 'rooms.fetchEntry() was called. ' + self);
        var l_data = {
			Name : fetchTextWidget(self, 'Name'),
			Key : fetchTextWidget(self, 'Key'),
			Active : fetchTrueFalseWidget(self, 'RoomActive'),
			Comment : fetchTextWidget(self, 'Comment'),
			Corner : fetchTextWidget(self, 'Corner'),
			Type : 'Room',
			Size : fetchTextWidget(self, 'Size'),
			Delete : false
		};
		return l_data;
	},


// ============================================================================
	/**
	 * Event handler for rooms buttons at bottom of entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 * 
	 * @param self is   <"Instance" of undefined.rooms.RoomsWidget>
	 * @param p_node is the button node that was clicked on
	 */
	function handleDataEntryOnClick(self, p_node) {
		function cb_handleDataEntryOnClick(p_json) {
			self.startWidget();
		}
		function eb_handleDataEntryOnClick(res){
			Divmod.debug('---', 'rooms.eb_handleDataEntryOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		var l_defer;
		var l_json;
		switch(l_ix) {
		case '10003':  // Change Button
	    	l_json = JSON.stringify(self.fetchEntry());
	        l_defer = self.callRemote("saveRoomData", l_json);  // @ web_schedule
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
	        l_defer = self.callRemote("saveRoomData", l_json);  // @ web_rooms
			l_defer.addCallback(cb_handleDataEntryOnClick);
			l_defer.addErrback(eb_handleDataEntryOnClick);
			break;
		default:
			Divmod.debug('---', 'rooms.handleDataEntryOnClick(Default) was called. l_ix:' + l_ix);
			break;
		}
		// return false stops the resetting of the server.
        return false;
	}
);
//Divmod.debug('---', 'rooms.handleMenuOnClick(1) was called. ' + l_ix + ' ' + l_name);
//console.log("rooms.handleMenuOnClick() - l_obj = %O", l_obj);
// ### END DBK
