/* rooms.js
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

	/**
	 * 
	 * @param self is    <"Instance" of undefined.rooms.RoomsWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		
		function cb_widgetready(res) {
			// do whatever initialization needs here, 'show' for the widget is handled in superclass
			//Divmod.debug('---', 'rooms.cb_widgready() was called. self = ' + self);
			self.hideRooms();
		}
	
		//Divmod.debug('---', 'rooms.ready() was called. ' + self);
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},

	/**
	 * This sends a message to the server to get the servers time.
	 * when the callback returns the time, it displays the time and schedules itself in 1 second. 
	 * 
	 * @param self
	 */
	function hideRooms(self) {

		function cb_hideRooms(p_json) {
			//Divmod.debug('---', 'rooms.cb_hideRooms() was called.');
			self.node.style.display = 'none';
		}
	
		//Divmod.debug('---', 'rooms.hideRooms() was called.');
		var d = self.callRemote('getRooms');
		d.addCallback(cb_hideRooms);
	}
);
