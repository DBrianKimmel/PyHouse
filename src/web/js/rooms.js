/* rooms.js
 * 
 * Displays the rooms
 */

// import Nevow.Athena
// import globals
// import helpers

/**
 * 	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  <input type="text" name="Key" value="" />\n';
	ret = ret + '    <br />\n';
	ret = ret +	'  Name:';
	ret = ret +	'    <input type = "text"  name = "Name" value = "" /><br />\n';
	ret = ret +	'  Key:';
	ret = ret +	'    <input type = "text" name = "Key" value = "' + p_key + '" /><br />\n';
	ret = ret +	'  Level:';
	ret = ret +	'    <input type = "range" name = "Level" min="0" max="100" value="0" onchange="showLightValue(this.value)" />\n';
	ret = ret +	'    <span name = slid_02  id="range">0</span>\n';
	ret = ret + '    <br />\n';
	ret = ret + '    <br />\n';
	ret = ret +	'  Rate:';
	ret = ret +	'    <input type = "text" name = "Rate" value = "0" /><br />\n';
	ret = ret + '  <input type="hidden" value="' + p_id + '" name="slider_no" />\n';
	ret = ret +			'<br />\n';
	ret = ret + '  <input type="submit" value="AddSlot" name="post_btn" />\n';
	ret = ret + '</form>\n';

 */

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
