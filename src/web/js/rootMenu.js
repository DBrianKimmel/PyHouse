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
			//self.displayRootMenu();
		}
	
		var uris = collectIMG_src(self.node, null);
		var d = loadImages(uris);
		d.addCallback(cb_widgetready);
		return d;
	},  // ready

	function displayRootMenu(self) {

		function cb_showRootMenu() {
			Divmod.debug('---', 'rootMenu.js - cb_showRootMenu was called. ');
			//self.node.innerHTML = 'Show Root Menu';
		}

		Divmod.debug('---', 'rootMenu.displayRoot() was called.');
		var d = self.callRemote('rootMenu', 'dummy');
		d.addCallback(cb_showRootMenu);
		return false;
	},  //  displayRoot
	
	function showRootMenuStuff(self, text) {
		Divmod.debug('---', 'rootMenu.showRootMenuStuff() was pushed from server. ' + text);
		
	}
);

//### END DBK
