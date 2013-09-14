/* houseSelect.js
 * 
 * Displays the house selection element
 */

// import Nevow.Athena
// import globals
// import helpers

helpers.Widget.subclass(houseSelect, 'HouseSelectWidget').methods(

    function __init__(self, node) {
        houseSelect.HouseSelectWidget.upcall(self, "__init__", node);
    },

	function ready(self) {

		function cb_widgetready(res) {
			// do whatever init needs here, show for the widget is handled in superclass
			//Divmod.debug('---', 'houseSelect.cb_widgready() was called. self = ' + self);
			self.hideSelect();
		}
	
		//Divmod.debug('---', 'houseSelect.ready() was called. self = ' + self);
		var uris = collectIMG_src(self.node, null);
		var d = loadImages(uris);
		d.addCallback(cb_widgetready);
		return d;
	},

	function hideSelect(self) {
		//Divmod.debug('---', 'houseSelect.hideSelect() was called. self = ' + self);
		self.node.style.display = 'none';
	},
	
	function cb_getHousesInfo(self, p1, p2) {
		Divmod.debug('---', 'houseSelect.cb_getHousesInfo() was called. self = ' + self);
		
	},
	
	function eb_getHousesInfo(self, p1, p2) {
		Divmod.debug('---', 'houseSelect.eb_getHousesInfo() was called. self = ' + self);
	},

	/**
	 * Show the house select screen and ask the server for a json list of houses to show.
	 * Use a callback to get the information to display.
	 */
	function showSelect(self) {
		//Divmod.debug('---', 'houseSelect.showSelect() was called. self = ' + self);
		self.node.style.display = 'block';
        var l_defer = self.callRemote("getHousesToSelect", '');  // @ web_login
		l_defer.addCallback(cb_getHousesInfo);
		l_defer.addErrback(eb_getHousesInfo);
		// return false stops the resetting of the server.
        return false;
	}
);

//### END DBK
