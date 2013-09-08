/* schedules.js
 * 
 * Displays the schedules
 */

// import Nevow.Athena
// import globals
// import helpers


helpers.Widget.subclass(schedules, 'SchedulesWidget').methods(

	function __init__(self, node) {
		schedules.SchedulesWidget.upcall(self, '__init__', node);
	},

	/**
	 * 
	 * @param self is    <"Instance" of undefined.schedules.SchedulesWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		
		function cb_widgetready(res) {
			// do whatever initialization needs here, 'show' for the widget is handled in superclass
			//Divmod.debug('---', 'schedules.cb_widgready() was called. res = ' + res);
			self.hideSchedules();
		}
	
		//Divmod.debug('---', 'scheduless.ready() was called. ' + self);
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
	function hideSchedules(self) {

		function cb_hideSchedules(p_json) {
			//Divmod.debug('---', 'schedules.cb_hideSchedules() was called.');
			self.node.style.display = 'none';
		}
	
		//Divmod.debug('---', 'schedules.getAndShowSchedules() was called.');
		self.node.style.display = 'none';
		//var l_defer = self.callRemote('getSchedules');
		//l_defer.addCallback(cb_hideSchedules);
	}
);
