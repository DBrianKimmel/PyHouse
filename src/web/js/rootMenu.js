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
		//Divmod.debug('---', 'rootMenu.__init__() was called. - self=' + self + "  node=" + node);
        rootMenu.RootMenuWidget.upcall(self, "__init__", node);
    },

	// ============================================================================
    /**
     * Place the widget in the workspace.
     * 
     * Override the ready function in C{ helpers.Widget.ready() }
     */
	function ready(self) {
		function cb_widgetready(res) {
			//Divmod.debug('---', 'rootMenu.cb_widgetready() was called. - res=' + res);
			self.hideWidget();
		}
		//Divmod.debug('---', 'rootMenu.ready() was called. ');
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},

	// ============================================================================
	/**
	 * Event handler for the root menu buttons.
	 * 
	 * @param self is    <"Instance" of undefined.rootMenu.RootMenuWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function doHandleOnClick(self, p_node) {  // from html handler onSubmit
		var l_key = p_node.name;
		//Divmod.debug('---', 'rootMenu.doHandleOnClick was called. ' + l_key);
		//console.log("rmb p_node", p_node);
		switch (l_key) {
		case 'Select':
			Divmod.debug('---', 'rootMenu.doHandleOnClick(Select) was called.');
			self.hideWidget();
			var l_node = findWidgetByClass('HouseSelect');
			l_node.startWidget();
			break;
		case 'House':
			//Divmod.debug('---', 'rootMenu.doHandleOnClick was called for House.');
			var l_node = findWidgetByClass('House');
			l_node.showWidget();
			self.hideWidget();
			break;
		case 'Web':
			//Divmod.debug('---', 'rootMenu.doHandleOnClick was called for Web.');
			var l_node = findWidgetByClass('Web');
			l_node.showWidget();
			self.hideWidget();
			break;
		case 'Logs':
			//Divmod.debug('---', 'rootMenu.doHandleOnClick was called for Logs.');
			var l_node = findWidgetByClass('Logs');
			l_node.showWidget();
			self.hideWidget();
			break;
		case 'Quit':
			// Quit the browser by logging out
			//Divmod.debug('---', 'rootMenu.doHandleOnClick was called for Quit.');
			self.doRootQuit(p_node);
			break;
		case 'Reload':
			// Force a save and reload of all XML data
			//Divmod.debug('---', 'rootMenu.doHandleOnClick was called for Reload.');
			self.callRemote("doRootMenuReload", '');
			break;
		default:
			// We should never get here
			Divmod.debug('---', 'rootMenu.doHandleOnClick was called for default.');
			break;
		}
	},
	
	function doRootQuit(self, p_node) {
		Divmod.debug('---', 'rootMenu.doRootQuit was called. ');
		//console.log("rm_rq Node %O", p_node);
		self.callRemote("doRootMenuQuit", '');
		globals.User.Fullname = 'Nobody';
		globals.User.ID = null;
		globals.User.LoggedIn = false;
		globals.User.Password = null;
		self.hideWidget();
		var l_node = findWidgetByClass('Login');
		l_node.showWidget();
		l_node.showLoggingInDiv();
	}
);
//### END DBK
