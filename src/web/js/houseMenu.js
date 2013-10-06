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

	/**
	 * @param self is <"Instance" of undefined.houseMenu.HouseMenuWidget> 
	 * @param p_node is node <button> of the button clicked
	 */
	function doHandleOnClick(self, p_node) {
		//console.log("houseMenu.doHandleOnClick - self %O", self);
		//console.log("houseMenu.doHandleOnClick - node %O", p_node);
		var l_key = p_node.name;
		//Divmod.debug('---', 'houseMenu.doHandleOnClick(1) was called. ' + l_key);
		switch (l_key) {
		case 'Location':
			//Divmod.debug('---', 'houseMenu.doHandleOnClick(Location) was called.');
			var l_node = findWidgetByClass('Location');
			l_node.showWidget(self);
			self.hideWidget(self);
			break;
		case 'Rooms':
			//Divmod.debug('---', 'houseMenu.doHandleOnClick(Rooms) was called.');
			var l_node = findWidgetByClass('Rooms');
			l_node.showWidget(self);
			self.hideWidget(self);
			break;
		case 'Lights':
			//Divmod.debug('---', 'houseMenu.doHandleOnClick(Lights) was called.');
			var l_node = findWidgetByClass('Lights');
			l_node.showWidget(self);
			self.hideWidget(self);
			break;
		case 'Buttons':
			//Divmod.debug('---', 'houseMenu.doHandleOnClick(Buttons) was called.');
			var l_node = findWidgetByClass('Buttons');
			l_node.showWidget(self);
			self.hideWidget(self);
			break;
		case 'Controllers':
			//Divmod.debug('---', 'houseMenu.doHandleOnClick(Controllers) was called.');
			var l_node = findWidgetByClass('Controllers');
			l_node.showWidget(self);
			self.hideWidget(self);
			break;
		case 'Schedules':
			//Divmod.debug('---', 'houseMenu.doHandleOnClick(Schedules) was called.');
			var l_node = findWidgetByClass('Schedules');
			l_node.showWidget(self);
			self.hideWidget(self);
			break;
		case 'Levels':
			//Divmod.debug('---', 'houseMenu.doHandleOnClick(Levels) was called.');
			var l_node = findWidgetByClass('ControlLights');
			l_node.showWidget(self);
			self.hideWidget(self);
			break;
		case 'Internet':
			//Divmod.debug('---', 'houseMenu.doHandleOnClick(Internet) was called.');
			var l_node = findWidgetByClass('Internet');
			l_node.showWidget(self);
			self.hideWidget(self);
			break;
		default:
			//Divmod.debug('---', 'houseMenu.doHandleOnClick(Default) was called.');
			break;
		}
	}
);

// END DBK