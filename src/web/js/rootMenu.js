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
	},

	function doRootMenuButton(self, p1, p2) {  // from html handler onSubmit
		console.log("rmb %O", self);
		console.log("rmb p1 %O", p1);
		console.log("rmb p2 %O", p2);
		this.hideRootMenu(self);
		var l_node = findWidget(self, 'HouseSelect');
		l_node.showSelect(self);
	},
	
	function doRootMenuSubmit(self, p1, p2) {  // from html handler onSubmit
		console.log("rms%O", self);
		console.log("rms p1 %O", p1);
		console.log("rms p2 %O", p2);
		this.hideRootMenu(self);
		var l_node = findWidget(self, 'HouseSelect');
		l_node.showSelect(self);
	},
	
	function doSelectHouse(self, p1, p2) {
		console.log("rsh %O", self);
		console.log("rsh p1 %O", p1);
		console.log("rsh p2 %O", p2);
	},

	function doAddHouse(self, p1, p2) {
		console.log("rsa %O", self);
		console.log("rsa p1 %O", p1);
		console.log("rsa p2 %O", p2);
	}
);

//### END DBK
