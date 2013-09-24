/* lights.js
 * 
 * Browser side code.
 */

// import Nevow.Athena
// import globals
// import helpers

/**
 * 	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  Name: <input type="text" name="Name" value="test_light2" />\n';
	ret = ret + '    <br />\n';
	ret = ret + '  Address: <input type="text" name="Address" value="CC:11:22" /><br />\n';
	ret = ret + '  Family: <input type="text" name="Family" value="Insteon" /><br />\n';
	ret = ret + '  Type: <input type="text" name="Type" value="WSLD" /><br />\n';
	ret = ret + '  <input type="hidden" name="Controller" value="False" />\n';
	ret = ret + '  <input type="hidden" name="Dimmable" value="False" />\n';
	ret = ret + '  <input type="hidden" name="Coords" value="0,0" />\n';
	ret = ret + '  <input type="hidden" name="Master" value="False" />\n';
	ret = ret + '  <input type="hidden" name="CurLevel" value="0" />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="AddLight" />\n';
	ret = ret + '</form>\n';

 */


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
