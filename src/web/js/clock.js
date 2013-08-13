//clock.js - displays the server time, polling from the client via nevows RPC
//

// import Nevow.Athena
// import globals
// import helpers

helpers.Widget.subclass(clock, 'Clock').methods(

	function __init__(self, node) {
		clock.Clock.upcall(self, '__init__', node);
	},

	function ready(self) {
		function widgetready(res) {
			self.getAndShowTime(); // do whatever init needs here, show for the widget is handled in superclass
		}
	
		var uris = collectIMG_src(self.node, null);
		var d = loadImages(uris);
		d.addCallback(widgetready);
		return d;
	},

	function getAndShowTime(self) {

		function showTime(time) {
			self.node.innerHTML = time;
			self.callLater(1.0, function() {
				self.getAndShowTime();
			});
		}
	
		var d = self.callRemote('getTimeOfDay');
		d.addCallback(showTime);
	}
);
