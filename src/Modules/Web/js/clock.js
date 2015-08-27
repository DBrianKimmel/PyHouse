/**
 * @name:      PyHouse/src/Modules/Web/js/clock.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2012-2015 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created about 2012
 * @summary:   Displays the server time, polling from the client via nevow's RPC
 *
 */
// import Nevow.Athena
// import globals
// import helpers



helpers.Widget.subclass(clock, 'ClockWidget').methods(
		
	function __init__(self, node) {
		clock.ClockWidget.upcall(self, '__init__', node);
	},


	/**
	 * This kicks off the time showing when ready.
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
	 * when the callback returns the time, it displays the time and schedules itself in CLOCK_DISPLAY_INTERVAL seconds.
	 *
	 * @param self
	 */
	function getAndShowTime(self) {
		function cb_showTime(p_time) {
			var CLOCK_DISPLAY_INTERVAL = 5.0;

			self.node.innerHTML = p_time;
			self.callLater(CLOCK_DISPLAY_INTERVAL, function() {
				self.getAndShowTime();
				}
			);
		}
		var l_defer = self.callRemote('getTimeOfDay');
		l_defer.addCallback(cb_showTime);
	}
);
