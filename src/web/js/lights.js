/* lights.js
 * 
 * Browser side code.
 */

// import Nevow.Athena
// import globals
// import helpers

helpers.Widget.subclass(lights, 'LightsWidget').methods(

    function __init__(self, node) {
        lights.LightsWidget.upcall(self, "__init__", node);
    },

	function ready(self) {

		function cb_widgetready(res) {
			//Divmod.debug('---', 'lights.js - cb_widgready was called.');
			self.hideLights();
		}

		var uris = collectIMG_src(self.node, null);
		var d = loadImages(uris);
		d.addCallback(cb_widgetready);
		return d;
	},

	function hideLights(self) {
		//Divmod.debug('---', 'lights.hideLights() was called.');
		self.node.style.display = 'none';
	}
);

//### END DBK
