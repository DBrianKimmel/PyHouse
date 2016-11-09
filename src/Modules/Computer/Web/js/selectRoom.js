/**
 * @name: PyHouse/src/Modules/Computer/Web/js/selectRoom.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @copyright: (c) 2016-2016 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Nov 07, 2016
 * @summary: Displays and selects a room
 */

// ============================================================================
/**
 * Build room Special - has onchange
 */
function buildRoomSelectWidget(self, p_id, p_caption, p_obj, p_change) {
	// Divmod.debug('---', 'selectRoom.buildRoomSelectWidget() was called.');
	return buildLcarSelectWidget(self, p_id, p_caption, globals.Valid.Families, p_obj.DeviceFamily, p_change);
}


//Divmod.debug('---', 'selectRoom.buildSerialPart() called.');
//console.log("selectRoom.handleMenuOnClick() - l_obj = %O", l_obj);

//### END DBK
