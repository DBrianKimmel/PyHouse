/**
 * Houses.js
 * 
 * version 1.00
 * 
 * D. Brian Kimmel
 * 
 * 	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  Name: <input type="text" name="Name" value="Name Required !!" /><br />\n';
	ret = ret + '  Active: <input type="text" name="Active" value="True" /><br />\n';
	ret = ret + '  Street: <input type="text" name="Street" value="" /><br />\n';
	ret = ret + '  City: <input type="text" name="Street" value="" /><br />\n';
	ret = ret + '  State: <input type="text" name="State" value="" /><br />\n';
	ret = ret + '  ZipCode: <input type="text" name="ZipCode" value="" /><br />\n';
	ret = ret + '  Latitude: <input type="text" name="Latitude" value="" /><br />\n';
	ret = ret + '  Longitude: <input type="text" name="Longitude" value="" /><br />\n';
	ret = ret + '  TimeZone: <input type="text" name="TimeZone" value="-5.0" /><br />\n';
	ret = ret + '  DST: <input type="text" name="Type" value="True" /><br />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="add" />\n';
	ret = ret + '</form>\n';
 */

helpers.Widget.subclass(houses, 'HousesWidget').methods(

    function __init__(self, node) {
		Divmod.debug('---', 'houses.__init__() was called. - self=' + self + "  node=" + node);
        housess.HousesWidget.upcall(self, "__init__", node);
		globals.Houses.Selected = {};
    },

	function ready(self) {

		function cb_widgetready(res) {
			Divmod.debug('---', 'houses.js - cb_widgready was called.');
			self.hideWidget();
		}

		Divmod.debug('---', 'houses.ready() was called.');
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	}
);

//### END