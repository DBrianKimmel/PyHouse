/* clock.js
 * 
 * Displays the server time, polling from the client via nevow's RPC
 */

// import Nevow.Athena
// import globals
// import helpers


helpers.Widget.subclass(clock, 'ClockWidget').methods(

	function __init__(self, node) {
		clock.ClockWidget.upcall(self, '__init__', node);
	},

	/**
	 * 
	 * @param self is    <"Instance" of undefined.clock.ClockWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		
		function cb_widgetready(res) {
			// do whatever initialization needs here, show for the widget is handled in superclass
			//Divmod.debug('---', 'clock.cb_widgready() was called. res = ' + res);
			self.getAndShowTime();
		}
	
		//Divmod.debug('---', 'clock.ready() was called. ' + self);
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
	function getAndShowTime(self) {

		function cb_showTime(p_time) {
			self.node.innerHTML = p_time;
			self.callLater(1.0, function() {
				self.getAndShowTime();
			});
		}
	
		//Divmod.debug('---', 'clock.getAndShowTime() was called.');
		var d = self.callRemote('getTimeOfDay');
		d.addCallback(cb_showTime);
	}
);
