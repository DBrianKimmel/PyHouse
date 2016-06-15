/**
 * @name:      PyHouse/src/Modules/Web/js/clock.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2012-2016 by D. Brian Kimmel
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
		globals.Login.FullName = 'Nobody';
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
			self.fetchServerInfo();
		}

		//Divmod.debug('---', 'clock.ready() was called. ' + self);
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	function fetchServerInfo(self) {
		function cb_serverInfo(p_json) {
			var l_obj = JSON.parse(p_json);
			// Divmod.debug('---', 'clock.cb_serverInfo() was called.');
			// console.log("clock.cb_serverInfo() - Server = %O", l_obj);
			globals.Server = l_obj['ServerName'];
			self.getAndShowTime();
		}
		var l_defer = self.callRemote('getServerInfo');
		l_defer.addCallback(cb_serverInfo)
	},


	/**
	 * This sends a message to the server to get the servers time.
	 * when the callback returns the time, it displays the time and schedules itself in CLOCK_DISPLAY_INTERVAL seconds.
	 *
	 * @param self
	 */
	function getAndShowTime(self) {
		function cb_showTime(p_time) {
			var CLOCK_DISPLAY_INTERVAL = 1.0;
			self.node.innerHTML = globals.Server.Name + ' ' + p_time + ' "' + globals.Login.FullName + '"';
			self.callLater(CLOCK_DISPLAY_INTERVAL, function() {
				self.getAndShowTime();
				}
			);
		}
		var l_defer = self.callRemote('getTimeOfDay');
		l_defer.addCallback(cb_showTime);
	}
);

//Divmod.debug('---', 'clock.handleMenuOnClick(1) was called.');
//console.log("clock.handleMenuOnClick() - l_obj = %O", l_obj);
//### END DBK
