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
		Divmod.debug('---', 'rootMenu.startWidget() was called. ');
		self.showWidget();
	},
	function showWidget(self) {
		// Divmod.debug('---', 'rootMenu.showWidget() was called.');
		self.node.style.display = 'block';
		self.showSelectionButtons();
		self.fetchHouseData();  // Continue with next phase
	},
	function hideSelectionButtons(self) {
		self.nodeById('SelectionButtonsDiv').style.display = 'none';
	},
	function showSelectionButtons(self) {
		self.nodeById('SelectionButtonsDiv').style.display = 'block';
	},



// ============================================================================
	function buildLcarScreen(self) {
		// Divmod.debug('---', 'rootMenu.buildLcarScreen was called.');
		var l_menu_html = "";
		var l_obj = {'Name' : 'SelectHouse', 'Key' : 'Select'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-orange-bg')
		l_obj = {'Name' : 'House', 'Key' : 'House'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-orange-bg')
		l_obj = {'Name' : 'Web', 'Key' : 'Web'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-putple-bg')

		l_menu_html += "<div class='lcars-row spaced'>\n";
		l_obj = {'Name' : 'Quit', 'Key' : 'Quit'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-salmon-bg')
		l_obj = {'Name' : 'Reload', 'Key' : 'Reload'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-salmon-bg')
		l_menu_html += "</div>\n";
		var l_html = build_lcars_top('Menu', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(10, l_menu_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
	/**
	 * This triggers getting the data from the server.
	 */
	function fetchHouseData(self) {
		function cb_fetchHouseData(p_json) {
			globals.House.HouseObj = JSON.parse(p_json);
			self.buildLcarSelectScreen()
		}
		function eb_fetchHouseData(p_reason) {
			Divmod.debug('---', 'lights.eb_fetchHouseData() was called. ERROR: ' + p_reason);
		}
		self.buildLcarScreen()
        //var l_defer = self.callRemote("getHouseData");
		//l_defer.addCallback(cb_fetchHouseData);
		//l_defer.addErrback(eb_fetchHouseData);
        return false;
	},
	/**
	 * Event handler for the root menu buttons.
	 * 
	 * @param self is    <"Instance" of undefined.rootMenu.RootMenuWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function doHandleOnClick(self, p_node) {  // from html handler onSubmit
		var l_key = p_node.name;
		// Divmod.debug('---', 'rootMenu.doHandleOnClick() was called with ' + l_key);
		// console.log("rmb p_node", p_node);
		switch (l_key) {
		case 'Select':  // House Select
			// Divmod.debug('---', 'rootMenu.doHandleOnClick(Select) was called.');
			self.hideWidget();
			var l_node = findWidgetByClass('HouseSelect');
			l_node.getHousesInfo();
			break;
		case 'House':
			//Divmod.debug('---', 'rootMenu.doHandleOnClick was called for House.');
			self.hideWidget();
			var l_node = findWidgetByClass('House');
			l_node.startWidget();
			break;
		case 'Web':
			self.hideWidget();
			var l_node = findWidgetByClass('Webs');
			l_node.startWidget();
			break;
		case 'Logs':
			self.hideWidget();
			var l_node = findWidgetByClass('Logs');
			l_node.startWidget();
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
		self.hideWidget();
		var l_node = findWidgetByClass('Login');
		l_node.showWidget();
		l_node.showLoggingInDiv();
	}
);
//Divmod.debug('---', 'rootMenu.doHandleOnClick was called for Web.');
//console.log("rm_rq Node %O", p_node);
//### END DBK
