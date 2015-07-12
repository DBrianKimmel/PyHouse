/**
 * @name:      PyHouse/src/Modules/Web/js/computerMenu.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2015-2015 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created on June 20, 2015
 * @summary:   Displays the computer menu element
 *
 */
// import Nevow.Athena
// import globals
// import helpers

/**
 * The computer menu widget.
 *
 */
helpers.Widget.subclass(computerMenu, 'ComputerMenuWidget').methods(

    function __init__(self, node) {
        computerMenu.ComputerMenuWidget.upcall(self, "__init__", node);
    },


	// ============================================================================
    /**
     * Startup - Place the widget in the workspace and hide it.
     * 
     * Override the ready function in C{ helpers.Widget.ready() }
     */
	function ready(self) {
		function cb_widgetready(res) {
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
	},



// ============================================================================
		/**
		 * Build a screen full of buttons - One for each menu item and some actions.
		 */
	function menuItems(self){
		var l_list = [
		    // Key,           Caption,               Widget Name
			['Internet',     'Network Addressing',  'Internet'        ],
			['Nodes',        'Nodes',               'Nodes'           ],
			['Mqtt',		 'Mqtt Broker',			'Mqtt'			  ],
			['Update',       'Update PyHouse',      'Update'          ],
			['Weather',      'Weather',             'Weather'         ],
			['Web',          'Web',                 'Web'             ]
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

		var l_html = build_lcars_top('Computer Menu', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(10, l_menu_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},


// ============================================================================
	/**
	 * @param self is <"Instance" of undefined.computerMenu.ComputereMenuWidget> 
	 * @param p_node is node <button> of the button clicked
	 */
	function doHandleOnClick(self, p_node) {
		var l_key = p_node.name;
		var l_node;
		switch (l_key) {
		case 'Internet':
			self.showWidget('Internet');
			break;
		case 'Nodes':
			self.showWidget('Nodes');
			break;
		case 'Mqtt':
			self.showWidget('Mqtt');
			break;
		case 'Update':
			self.showWidget('Update');
			break;
		case 'Weather':
			self.showWidget('Weather');
			break;
		case 'Web':
			self.showWidget('Web');
			break;
		case 'Back':
			self.showWidget('RootMenu');
			break;
		default:
			Divmod.debug('---', 'computerMenu.doHandleOnClick(Default) was called.');
			break;
		}
	}
);
// Divmod.debug('---', 'computerMenu.***Function() was called.');
// console.log("computerMenu.***function()  json  %O", l_json);
// END DBK