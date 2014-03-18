/* houseMenu.js
 * 
 * Displays the house menu element
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
     * Place the widget in the workspace.
     * 
     * Override the ready function in C{ helpers.Widget.ready() }
     */
	function ready(self) {
		function cb_widgetready(res) {
			// do whatever init needs here, show for the widget is handled in superclass
			//Divmod.debug('---', 'houseMenu.cb_widgetready() was called.');
			self.hideWidget();
		}
		//Divmod.debug('---', 'houseMenu.ready() was called.');
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	function showWidget(self) {
		self.node.style.display = 'block';
	},

	// ============================================================================
	/**
	 * @param self is <"Instance" of undefined.houseMenu.HouseMenuWidget> 
	 * @param p_node is node <button> of the button clicked
	 */
	function doHandleOnClick(self, p_node) {
		var l_key = p_node.name;
		switch (l_key) {
		case 'Location':
			self.hideWidget();
			var l_node = findWidgetByClass('House');
			l_node.showWidget();
			break;
		case 'Rooms':
			self.hideWidget();
			var l_node = findWidgetByClass('Rooms');
			l_node.showWidget();
			break;
		case 'Lights':
			self.hideWidget();
			var l_node = findWidgetByClass('Lights');
			l_node.showWidget();
			break;
		case 'Buttons':
			self.hideWidget();
			var l_node = findWidgetByClass('Buttons');
			l_node.showWidget();
			break;
		case 'Controllers':
			self.hideWidget();
			var l_node = findWidgetByClass('Controllers');
			l_node.showWidget();
			break;
		case 'Schedules':
			self.hideWidget();
			var l_node = findWidgetByClass('Schedules');
			l_node.showWidget();
			break;
		case 'Levels':
			self.hideWidget();
			var l_node = findWidgetByClass('ControlLights');
			l_node.showWidget();
			break;
		case 'Internet':
			self.hideWidget();
			var l_node = findWidgetByClass('Internet');
			l_node.showWidget();
			break;
		case 'Back':
			self.hideWidget();
			var l_node = findWidgetByClass('RootMenu');
			l_node.showWidget();
			break;
		default:
			Divmod.debug('---', 'houseMenu.doHandleOnClick(Default) was called.');
			break;
		}
	}
);

// END DBK