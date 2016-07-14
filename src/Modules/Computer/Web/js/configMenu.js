/**
 * @name:      PyHouse/src/Modules/Web/js/config.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2015-2015 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created on Aug 23, 2015
 * @summary:   Displays the Config Menu
 * 
 */


/**
 * The Config menu widget.
 * 
 *  This displays house select and other buttons to edit non house related features.
 */

helpers.Widget.subclass(configMenu, 'ConfigMenuWidget').methods(

    function __init__(self, node) {
        configMenu.ConfigMenuWidget.upcall(self, "__init__", node);
    },



// ============================================================================
    /**
     * Startup - Place the widget in the workspace and hide it.
     *
     * Override the ready function in C{ helpers.Widget.ready() }
     */
	function ready(self) {
		function cb_widgetready() {
			self.hideWidget();
		}
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	function startWidget(self) {
		showSelectionButtons(self);
		self.buildLcarSelectScreen();
		// self.fetchDataFromServer();
	},


// ============================================================================
	function menuItems(self){
		var l_list = [
		    // Key,           Caption,               Widget Name
			['Users',        'Users',               'Users'               ]
			];
		return l_list;
	},
	function buildLcarSelectScreen(self){
		var l_menu_html = "<div class='lcars-row spaced'>\n";
		l_menu_html += buildLcarMenuButtons(self.menuItems(), 'doHandleOnClick');
		l_menu_html += "</div>\n";
		l_menu_html += "<div class='lcars-row spaced'>\n";
		l_obj = {'Name' : 'Back', 'Key' : 'Back'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-salmon-bg');
		l_menu_html += "</div>\n";

		var l_html = build_lcars_top('Config Menu', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(10, l_menu_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},


// ============================================================================
	/**
	 * Event handler for the config menu buttons.
	 * 
	 * @param self is    <"Instance" of undefined.configMenu.RootMenuWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function doHandleOnClick(self, p_node) {
		var l_key = p_node.name;
		var l_node;
		switch (l_key) {
		case 'Users':
			self.showWidget('Users');
			break
		case 'Back':
			self.showWidget('RootMenu');
			break;
		default:  // We should never get here
			Divmod.debug('---', 'configMenu.doHandleOnClick was called for default.');
			break;
		}
	}
);
// Divmod.debug('---', 'configMenu.doHandleOnClick was called for Web.');
// console.log("configMenu  Node %O", p_node);
//### END DBK
