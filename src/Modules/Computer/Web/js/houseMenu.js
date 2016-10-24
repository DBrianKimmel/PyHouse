/**
 * @name:      PyHouse/src/Modules/Web/js/houseMenu.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2012-2016 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created about 2012
 * @summary:   Displays the house menu element
 *
 */
// import Nevow.Athena
// import globals
// import helpers

/**
 * The house menu widget.
 *
 */
helpers.Widget.subclass(houseMenu, 'HouseMenuWidget').methods(

    function __init__(self, node) {
        houseMenu.HouseMenuWidget.upcall(self, "__init__", node);
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
		    // Key,        		   Caption,               Widget Name
			['Location',     	'House Information',   'House'           ],
			['Rooms',        	'Rooms',               'Rooms'           ],
			['Lights',       	'Lights',              'Lights'          ],
			['Buttons',      	'Buttons',             'Buttons'         ],
			['Controllers',  	'Controllers',         'Controllers'     ],
			['GarageDoors',  	'Garage Doors',        'GarageDoors'     ],
			['MotionSensors',	'Motion Sensors',      'MotionSensors'   ],
			['Schedules',    	'Scheduling',          'Schedules'       ],
			['Levels',       	'Lighting Control',    'ControlLighting' ],
			['Thermo',       	'Thermostat',          'Thermostat'      ],
			['Irrigation',   	'Irrigation   ',       'Irrigation'      ],
			['Entertain',    	'Entertainment',       'Entertain'       ]
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

		var l_html = build_lcars_top('House Menu', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(10, l_menu_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},


// ============================================================================
	/**
	 * @param self is <"Instance" of undefined.houseMenu.HouseMenuWidget> 
	 * @param p_node is node <button> of the button clicked
	 */
	function doHandleOnClick(self, p_node) {
		var l_key = p_node.name;
		var l_node;
		switch (l_key) {
		case 'Location':
			self.showWidget('House');
			break;
		case 'Levels':
			self.showWidget('ControlLights');
			break;
		case 'Lights':
			self.showWidget('Lights');
			break;
		case 'Buttons':
			self.showWidget('Buttons');
			break;
		case 'Controllers':
			self.showWidget('Controllers');
			break;
		case 'GarageDoors':
			self.showWidget('GarageDoors');
			break;
		case 'MotionSensors':
			self.showWidget('MotionSensors');
			break;
		case 'Schedules':
			self.showWidget('Schedules');
			break;
		case 'Rooms':
			self.showWidget('Rooms');
			break;
		case 'Thermo':
			self.showWidget('Thermostat');
			break;
		case 'Irrigation':
			self.showWidget('Irrigation');
			break;
		case 'Entertain':
			self.showWidget('EntertainmentMenu');
			break;
		case 'Back':
			self.showWidget('RootMenu');
			break;
		default:
			Divmod.debug('---', 'houseMenu.doHandleOnClick(Default) was called.');
			break;
		}
	}
);

// Divmod.debug('---', 'houseMenu.doHandleOnClick(Default) was called.');
// console.log("houseMenu.handleDataOnClick()  json  %O", l_json);

// END DBK