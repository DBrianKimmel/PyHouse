/** rootMenu.js
 * 
 * Displays the Root Menu section
 */

// import Nevow.Athena
// import globals
// import helpers

/**
 * The root menu widget.
 * 
 *  This displays house select and other buttons to edit non house related features.
 */

helpers.Widget.subclass(rootMenu, 'RootMenuWidget').methods(

    function __init__(self, node) {
        rootMenu.RootMenuWidget.upcall(self, "__init__", node);
    },

    
    /**
     * Place the widget in the workspace.
     * 
     * Override the ready function in C{ helpers.Widget.ready() }
     */
	function ready(self) {
		function cb_widgetready(res) {
			// do whatever init needs here, show for the widget is handled in superclass
			self.hideWidget();
		}
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},

	function doHandleOnClick(self, p_node) {  // from html handler onSubmit
		//console.log("rmb    %O", self);
		//console.log("rmb p_node", p_node);
		var l_key = p_node.name;
		//Divmod.debug('---', 'rootMenu.doHandleOnClick was called. ' + l_key);
		switch (l_key) {
		case 'Select':
			//Divmod.debug('---', 'rootMenu.doHandleOnClick was called for HouseSelect.');
			var l_node = findWidget(self, 'HouseSelect');
			l_node.showSelect(self);
			self.hideWidget(self);
			break;
		case 'House':
			//Divmod.debug('---', 'rootMenu.doHandleOnClick was called for House.');
			var l_node = findWidget(self, 'House');
			break;
		case 'Web':
			var l_node = findWidget(self, 'Webt');
			break;
		case 'Logs':
			var l_node = findWidget(self, 'Logs');
			break;
		case 'Quit':
			break;
		case 'Reload':
			break;
		default:
			break;
		}
		//this.hideRootMenu(self);
	},
	
	function doRootMenuSubmit(self, p1, p2) {  // from html handler onSubmit
		console.log("rms%O", self);
		console.log("rms p1 %O", p1);
		console.log("rms p2 %O", p2);
		this.hideRootMenu(self);
		var l_node = findWidget(self, 'HouseSelect');
		l_node.showSelect(self);
	},
	
	function doRootQuit(self, p1, p2) {
		console.log("rm_rq %O", self);
		console.log("rm_rq p1 %O", p1);
		console.log("rm_rq p2 %O", p2);
	},

	function doRootReload(self, p1, p2) {
		console.log("rm_rr %O", self);
		console.log("rm_rr p1 %O", p1);
		console.log("rm_rr p2 %O", p2);
	}
);

//### END DBK
