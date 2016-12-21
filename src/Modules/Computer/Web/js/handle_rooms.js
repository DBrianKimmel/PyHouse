/**
 * @name: PyHouse/src/Modules/Computer/Web/js/handle_rooms.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @copyright: (c) 2016-2016 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Nov 15, 2014
 * @summary: Handle the rooms
 * 
 * This MUST be imported in workspace.js
 */

/**
 * Build room Special - has onchange
 * 
 * @param p_id
 *            is the name of the field.
 */
function buildRoomSelectWidget(self, p_id, p_caption, p_obj, p_change) {
	// Divmod.debug('---', 'handle_rooms.buildRoomSelectWidget() was called.');
	var l_ret = buildSelectWidget(self, p_id, p_caption, globals.House.Rooms, p_obj.DeviceFamily, p_change);
	return l_ret;
}

function buildRooms(self, p_obj, p_html) {
	p_html += buildRoomSelectWidget(self, 'RoomName', 'Room Name', p_obj.RoomName);
	p_html += buildTextWidget(self, 'RoomUUID', 'Room UUID', p_obj.RoomUUID, 'disable');
}

function handleRoomChange(p_event) {
	Divmod.debug('---', 'handle_rooms.handleRoomChange() was called. ' + p_event);
	var l_obj = globals.House.ScheduleObj;
	var l_self = globals.Self;
	l_obj.RoomName = fetchSelectWidget(l_self, 'RoomName');
	l_self.buildDataEntryScreen(l_obj, 'handleDataEntryOnClick');
}

// Divmod.debug('---', 'handle_rooms.handleDataEntryOnClick(Back) was called. ');
// console.log("handle_rooms.fetchDataFromServer.cb_fetchDataFromServer p1 %O", p_json);

// ### END DBK
