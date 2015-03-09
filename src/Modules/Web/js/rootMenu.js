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



// ============================================================================
    /**
     * Startup - Place the widget in the workspace and hide it.
     *
     * Override the ready function in C{ helpers.Widget.ready() }
     */
	function ready(self) {
		function cb_widgetready() {
			// Divmod.debug('---', 'rootMenu.cb_widgetready() was called.');
			self.hideWidget();
		}
		// Divmod.debug('---', 'rootMenu.ready() was called. ');
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	function startWidget(self) {
		showSelectionButtons(self);
		self.fetchDataFromServer();
	},



// ============================================================================
	function menuItems(self){
		var l_list = [
		    // Key,           Caption,               Widget Name
			['Select' ,      'Select House',        'Select'          ],
			['House',        'House',               'House'           ],
			['Web',          'Web',                 'Web'             ]
			];
		return l_list;
	},
	function buildLcarScreen(self) {
		// Divmod.debug('---', 'rootMenu.buildLcarScreen was called.');
		var l_menu_html = "<div class='lcars-row spaced'>\n";
		l_menu_html += buildLcarMenuButtons(self.menuItems(), 'doHandleOnClick');
		l_menu_html += "</div>\n";

		l_menu_html += "<div class='lcars-row spaced'>\n";
		l_obj = {'Name' : 'Quit', 'Key' : 'Quit'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-salmon-bg');
		l_obj = {'Name' : 'Reload', 'Key' : 'Reload'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-salmon-bg');
		l_menu_html += "</div>\n";
		var l_html = build_lcars_top('Menu', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(10, l_menu_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
	/**
	 * This triggers getting the data from the server.
	 */
	function fetchDataFromServer(self) {
		function cb_fetchDataFromServer(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
			self.buildLcarSelectScreen();
		}
		function eb_fetchDataFromServer(p_reason) {
			Divmod.debug('---', 'lights.eb_fetchDataFromServer() was called. ERROR: ' + p_reason);
		}
		self.buildLcarScreen();
        return false;
	},
	/**
	 * Event handler for the root menu buttons.
	 * 
	 * @param self is    <"Instance" of undefined.rootMenu.RootMenuWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function doHandleOnClick(self, p_node) {
		var l_key = p_node.name;
		var l_node;
		switch (l_key) {
		case 'Select':  // House Select
			self.showWidget('HouseSelect');
			break;
		case 'House':
			self.showWidget('House');
			break;
		case 'Web':
			self.showWidget('Webs');
			break;
		case 'Quit':  // Quit the browser by logging out
			self.doRootQuit(p_node);
			break;
		case 'Reload':  // Force a save and reload of all XML data
			self.callRemote("doRootMenuReload", '');
			break;
		default:  // We should never get here
			Divmod.debug('---', 'rootMenu.doHandleOnClick was called for default.');
			break;
		}
	},

	function doRootQuit(self, p_node) {
		self.callRemote("doRootMenuQuit", '');
		globals.User.Fullname = 'Nobody';
		globals.User.ID = null;
		globals.User.LoggedIn = false;
		globals.User.Password = null;
		self.showWidget('Login');
		l_node.showLoggingInDiv();
	}
);
//Divmod.debug('---', 'rootMenu.doHandleOnClick was called for Web.');
//console.log("rm_rq Node %O", p_node);
//### END DBK
