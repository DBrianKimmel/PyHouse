/* clock.js
 * 
 * Displays the server time, polling from the client via nevows RPC
 */

// import Nevow.Athena
// import globals
// import helpers

helpers.Widget.subclass(clock, 'Clock').methods(

	function __init__(self, node) {
		clock.Clock.upcall(self, '__init__', node);
	},

	function ready(self) {
		
		function cb_widgetready(res) {
			// do whatever init needs here, show for the widget is handled in superclass
			self.getAndShowTime();
		}
	
		var uris = collectIMG_src(self.node, null);
		var d = loadImages(uris);
		d.addCallback(cb_widgetready);
		return d;
	},

	function getAndShowTime(self) {

		function cb_showTime(p_time) {
			self.node.innerHTML = p_time;
			self.callLater(1.0, function() {
				self.getAndShowTime();
			});
		}
	
		var d = self.callRemote('getTimeOfDay');
		d.addCallback(cb_showTime);
	}
);
