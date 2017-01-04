/**
 * @name: PyHouse/src/Modules/Computer/Web/js/handle_rooms.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @copyright: (c) 2016-2017 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Nov 15, 2014
 * @summary: Handle the rooms
 * 
 * This MUST be imported in workspace.js
 * 
 * This module is for things that reference a room.
 * As such, it will use a room name and a room UUID (to select the right room).
 */

// ============================================================================

function buildRoomList() {
	// Divmod.debug('---', 'handle_rooms.buildRoomList() was called.');
	var l_rooms = globals.House.Rooms;
	var l_list = [];
	for (var l_ix = 0; l_ix < Object.keys(l_rooms).length; l_ix++) {
		l_list[l_ix] = l_rooms[l_ix].Name;
	}
	// console.log("handle_rooms.buildRoomList List = %O", l_list);
	return l_list;
}

/**
 * 
 * @param p_event
 * @returns
 */
function handleRoomChange(self, p_event) {
	Divmod.debug('---', 'handle_rooms.handleRoomChange() was called. ' + p_event);
	var l_obj = globals.House.ScheduleObj;
	var l_self = globals.Self;
	l_obj.RoomName = fetchSelectWidget(l_self, 'HrRoomName');
	l_self.buildDataEntryScreen(l_obj, 'handleDataEntryOnClick');
}

/**
 * Build room Special - has onchange
 *
 * @param p_id is the name of the field ('RoomName').
 * @param p_caption is the Description to be used ???
 * @param p_obj is the device object that contains some room information.
 * @param p_change is the literal name of the onchange function to be called when a new room is selected.
 */
function buildRoomSelectWidget(self, p_obj, p_handleChange) {
	// Divmod.debug('---', 'handle_rooms.buildRoomSelectWidget() was called.');
	// console.log("handle_rooms.buildRoomSelectWidget Room %O", p_obj);
	var l_list = buildRoomList();
	var l_html = buildSelectWidget(self, 'HrRoomName', 'Room Name', l_list, p_obj.RoomName, p_handleChange);
	return l_html;
}

function createRoomEntry(self, p_obj) {
	Divmod.debug('---', 'handle_rooms.createRoomEntry() was called. ');
	p_obj.RoomName = 'XXX Room';
	p_obj.RoomUUID = '';
	p_obj.RoomCoords = createCoordinateEntry(self);
	return p_obj;
}

//============================================================================

function buildRoomSelectEntry(self, p_obj, p_handleChange) {
	// Divmod.debug('---', 'handle_rooms.buildRoomSelectEntry() was called. ');
	var l_html = '';
	l_html += buildRoomSelectWidget(self, p_obj, p_handleChange);
	l_html += buildTextWidget(self, 'RoomUUID', 'Room UUID', p_obj.RoomUUID, 'disable');
	l_html += buildCoordinatesWidget(self, 'RoomCoords', 'Room Coords', p_obj.RoomCoords, 'disable');
	return l_html;
}

function fetchRoomSelectEntry(self, p_obj) {
	var l_ix = fetchTextWidget(self, 'HrRoomName');
	// Divmod.debug('---', 'handle_rooms.fetchRoomSelectEntry() was called, ix= ' + l_ix);
	p_obj.RoomName = globals.House.Rooms[l_ix].Name;
	p_obj.RoomUUID = globals.House.Rooms[l_ix].UUID;
	fetchCoordinateEntry(self, p_obj)
	// console.log("handle_rooms.fetchRoomSelectEntry Obj %O", p_obj);
}

function createRoomSelectEntry(self, p_obj) {
	// Divmod.debug('---', 'handle_rooms.createRoomSelectEntry() was called. ');
	p_obj.RoomName = 'XXX Room';
	p_obj.RoomUUID = '';
	p_obj.RoomCoords = createCoordinateEntry(self);
}

// Divmod.debug('---', 'handle_rooms.handleDataEntryOnClick(Back) was called. ');
// console.log("handle_rooms.fetchDataFromServer.cb_fetchDataFromServer p1 %O", p_json);

// ### END DBK
