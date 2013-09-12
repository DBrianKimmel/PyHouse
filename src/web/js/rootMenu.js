/** rootMenu.js
 * 
 * Displays the Root Menu section
 */

// import Nevow.Athena
// import globals
// import helpers

helpers.Widget.subclass(rootMenu, 'RootMenuWidget').methods(

    function __init__(self, node) {
        rootMenu.RootMenuWidget.upcall(self, "__init__", node);
    },

	function ready(self) {
		
		function cb_widgetready(res) {
			// do whatever init needs here, show for the widget is handled in superclass
			//Divmod.debug('---', 'rootMenu.cb_widgready() was called.');
			self.hideRootMenu();
		}
	
		//Divmod.debug('---', 'rootMenu.ready() was called.  self =' + self);
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},

	function hideRootMenu(self) {
		Divmod.debug('---', 'rootMenu.hideRootMenu was called.');
		self.node.style.display = 'none';
	},
	
	function showRootMenu(self) {
		Divmod.debug('---', 'rootMenu.showRootMenu was called.');
		self.node.style.display = 'block';
	}

);

//### END DBK
