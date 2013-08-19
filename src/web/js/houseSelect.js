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
			//self.displaySelect();
		}  // cb_widgetready
	
		var uris = collectIMG_src(self.node, null);
		var d = loadImages(uris);
		d.addCallback(cb_widgetready);
		return d;
	},  // ready

	function displaySelect(self) {

		function cb_showSelect() {
			self.node.innerHTML = 'Show House Select';
		}
	
		Divmod.debug('---', 'houseSelect.displaySelect() was called.');
        var d = self.callRemote("houseSelect", 'dumb');
		d.addCallback(cb_showSelect);
        return false;
	}  // displaySelect
);

//### END DBK
