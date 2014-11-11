/**
 * @name: PyHouse/src/Modules/Web/js/houseMenu.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2012-2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created about 2012
 * @summary: Displays the house menu element
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
			// do whatever init needs here, show for the widget is handled in superclass
			self.hideWidget();
		}
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	function showWidget(self) {
		self.node.style.display = 'block';
	},
	function hideSelectionButtons(self) {
		self.nodeById('SelectionButtonsDiv').style.display = 'none';
	},
	function showSelectionButtons(self) {
		self.nodeById('SelectionButtonsDiv').style.display = 'block';
	},



// ============================================================================
		/**
		 * Build a screen full of buttons - One for each menu item and some actions.
		 */
	function buildLcarSelectScreen(self){
		var l_menu_html = "";
		var l_obj = {'Name' : 'House Location', 'Key' : 'Location'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-orange-bg');
		l_obj = {'Name' : 'Rooms', 'Key' : 'Rooms'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-orange-bg');
		l_obj = {'Name' : 'Lights', 'Key' : 'Lights'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-orange-bg');
		l_obj = {'Name' : 'Buttons', 'Key' : 'Buttons'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-orange-bg');
		l_obj = {'Name' : 'Controllers', 'Key' : 'Controllers'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-orange-bg');
		l_obj = {'Name' : 'Schedules', 'Key' : 'Schedules'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-orange-bg');

		l_menu_html += "<div class='lcars-row spaced'>\n";
		l_obj = {'Name' : 'Control Lights', 'Key' : 'Levels'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-orange-bg');
		l_obj = {'Name' : 'Internet', 'Key' : 'Internet'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-orange-bg');
		l_obj = {'Name' : 'Thermostats', 'Key' : 'Thermo'};
		l_menu_html += buildLcarButton(l_obj, 'doHandleOnClick', 'lcars-orange-bg');
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
	function showWidget(self) {
		// Divmod.debug('---', 'houseMenu.showWidget() was called.');
		// console.log("houseMenu.showWidget()  self  %O", self);
		self.node.style.display = 'block';
		self.showSelectionButtons();
		self.buildLcarSelectScreen();
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
			self.hideWidget();
			l_node = findWidgetByClass('House');
			l_node.showWidget();
			break;
		case 'Rooms':
			self.hideWidget();
			l_node = findWidgetByClass('Rooms');
			l_node.showWidget();
			break;
		case 'Lights':
			self.hideWidget();
			l_node = findWidgetByClass('Lights');
			l_node.showWidget();
			break;
		case 'Buttons':
			self.hideWidget();
			l_node = findWidgetByClass('Buttons');
			l_node.showWidget();
			break;
		case 'Controllers':
			self.hideWidget();
			l_node = findWidgetByClass('Controllers');
			l_node.showWidget();
			break;
		case 'Schedules':
			self.hideWidget();
			l_node = findWidgetByClass('Schedules');
			l_node.showWidget();
			break;
		case 'Levels':
			self.hideWidget();
			l_node = findWidgetByClass('ControlLights');
			l_node.showWidget();
			break;
		case 'Internet':
			self.hideWidget();
			l_node = findWidgetByClass('Internet');
			l_node.showWidget();
			break;
		case 'Thermo':
			self.hideWidget();
			l_node = findWidgetByClass('Thermostat');
			l_node.showWidget();
			break;
		case 'Back':
			self.hideWidget();
			l_node = findWidgetByClass('RootMenu');
			l_node.showWidget();
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