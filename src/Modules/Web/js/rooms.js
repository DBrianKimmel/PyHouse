/**
 *  rooms.js
 *
 * Displays the rooms
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
	function showWidget(self) {
		self.node.style.display = 'block';
		self.showButtons();
		self.hideEntry();
		self.fetchHouseData();
	},
	function showButtons(self) {
		self.nodeById('RoomButtonsDiv').style.display = 'block';	
	},
	function hideButtons(self) {
		self.nodeById('RoomButtonsDiv').style.display = 'none';		
	},
	function showEntry(self) {
		self.nodeById('RoomEntryDiv').style.display = 'block';
	},
	function hideEntry(self) {
		self.nodeById('RoomEntryDiv').style.display = 'none';
	},

	// ============================================================================
	/**
	 * This triggers getting the room data from the server.
	 */
	function fetchHouseData(self) {
		function cb_fetchHouseData(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
			var l_tab = buildTable(globals.House.HouseObj.Rooms, 'handleMenuOnClick');
			self.nodeById('RoomTableDiv').innerHTML = l_tab;
		}
		function eb_fetchHouseData(res) {
			Divmod.debug('---', 'rooms.eb_fetchHouseData() was called. ERROR = ' + res);
		}
        var l_defer = self.callRemote("getHouseData");  // call server @ web_rooms.py
		l_defer.addCallback(cb_fetchHouseData);
		l_defer.addErrback(eb_fetchHouseData);
        return false;
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
		if (l_ix <= 1000) {
			// One of the rooms buttons.
			var l_obj = globals.House.HouseObj.Rooms[l_ix];
			globals.House.RoomObj = l_obj;
			//Divmod.debug('---', 'rooms.handleMenuOnClick(1) was called. ' + l_ix + ' ' + l_name);
			//console.log("rooms.handleMenuOnClick() - l_obj = %O", l_obj);
			self.showEntry();
			self.hideButtons();
			self.fillEntry(l_obj);
		} else if (l_ix == 10001) {
			// The "Add" button
			self.showEntry();
			self.hideButtons();
			var l_ent = self.createEntry();
			self.fillEntry(l_ent);
		} else if (l_ix == 10002) {
			// The "Back" button
			self.hideWidget();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget();
		}
	},
	
	/**
	 * Fill in the schedule entry screen with all of the data for this room.
	 */
	function fillEntry(self, p_entry) {
		var sched = arguments[1];
		//Divmod.debug('---', 'rooms.fillEntry() was called. ' + sched);
		self.nodeById('Name').value = sched.Name;
		self.nodeById('Key').value = sched.Key;
		self.nodeById('ActiveDiv').innerHTML = buildTrueFalseWidget('RoomActive', sched.Active);
		self.nodeById('Comment').value = sched.Comment;
		self.nodeById('Corner').value = sched.Corner;
		self.nodeById('Size').value = sched.Size;
		self.nodeById('RoomEntryButtonsDiv').innerHTML = buildEntryButtons('handleDataOnClick');
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
		}
		return l_data;
	},
	function fetchEntry(self) {
    	//Divmod.debug('---', 'rooms.fetchEntry() was called. ' + self);
        var l_data = {
			Name : self.nodeById('Name').value,
			Key : self.nodeById('Key').value,
			Active : fetchTrueFalseWidget('RoomActive'),
			Comment : self.nodeById('Comment').value,
			Corner : self.nodeById('Corner').value,
			Type : 'Room',
			Size : self.nodeById('Size').value,
			Delete : false
		}
		return l_data;
	},

	/**
	 * Event handler for rooms buttons at bottom of entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 * 
	 * @param self is   <"Instance" of undefined.rooms.RoomsWidget>
	 * @param p_node is the button node that was clicked on
	 */
	function handleDataOnClick(self, p_node) {
		function cb_handleDataOnClick(p_json) {
			//Divmod.debug('---', 'rooms.cb_handleDataOnClick() was called.');
			self.showWidget();
		}
		function eb_handleDataOnClick(res){
			Divmod.debug('---', 'rooms.eb_handleDataOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry());
			//Divmod.debug('---', 'rooms.handleDataOnClick(Change) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveRoomData", l_json);  // @ web_schedule
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			//Divmod.debug('---', 'rooms.handleDataOnClick(Back) was called.  ');
			self.hideEntry();
			self.showButtons();
			break;
		case '10004':  // Delete button
			var l_obj = self.fetchEntry();
			l_obj['Delete'] = true;
	    	var l_json = JSON.stringify(l_obj);
			//Divmod.debug('---', 'rooms.handleDataOnClick(Delete) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveRoomData", l_json);  // @ web_rooms
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		default:
			Divmod.debug('---', 'rooms.handleDataOnClick(Default) was called. l_ix:' + l_ix);
			break;			
		}
		// return false stops the resetting of the server.
        return false;
	}
);