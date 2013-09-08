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
	
	function showSelect(self) {
		//Divmod.debug('---', 'houseSelect.showSelect() was called. self = ' + self);
		self.node.style.display = 'block';
	}
);

//### END DBK
