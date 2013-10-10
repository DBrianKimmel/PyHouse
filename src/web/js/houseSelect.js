/* houseSelect.js
 * 
 * Displays the house selection element
 */

// import Nevow.Athena
// import globals
// import helpers

/**
 * The house selection widget.
 * 
 * This displays a house select DIV at first and when more than one house exists.
 * If only one house exists, this is skipped and the following happens.
 * When a house is selected, the widget hides the selection DIV and then shows a DIV of the selected house.
 */
helpers.Widget.subclass(houseSelect, 'HouseSelectWidget').methods(

    function __init__(self, node) {
        houseSelect.HouseSelectWidget.upcall(self, "__init__", node);
		globals.House.Selected = {};
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

	/**
	 * Called from the root menu screen when the house select button was clicked.
	 * 
	 * Show the house select screen and ask the server for a JSON list of houses to show.
	 * Use a callback to get the information to display.
	 * 
	 * @param self is the house select widget
	 * @param p1 is the parent widget (rootmenuWidget)
	 */
	function showSelect(self, p1) {
		function cb_getHousesInfo(p_json) {
			//Divmod.debug('---', 'houseSelect.showSelect.cb_getHousesInfo() was called.');
			//console.log("ss.cb   p1 %O", p_json);
			var l_obj = JSON.parse(p_json);
			var l_tab = buildTable(l_obj, 'handleMenuOnClick');
			self.nodeById('HouseSelectTableDiv').innerHTML = l_tab;
		}
		function eb_getHousesInfo(res) {
			Divmod.debug('---', 'houseSelect.eb_getHousesInfo() was called. ERROR = ' + res);
		}
		Divmod.debug('---', 'houseSelect.showSelect() was called.');
		//console.log("showSelect self %O", self);
		//console.log("showSelect   p1 %O", p1);
		self.node.style.display = 'block'; 
        var l_defer = self.callRemote("getHousesToSelect", '');  // call server @ web_houseSelect.py
		l_defer.addCallback(cb_getHousesInfo);
		l_defer.addErrback(eb_getHousesInfo);
        return false;
	},

	/**
	 * A house was selected.
	 * Show the house and then load the information for the selected house.
	 */
	function showSelected(self) {
		function cb_getSelectedHouseData(p_json) {
			//ivmod.debug('---', 'houseSelect.showSelected.cb_getSelectedHouseData() was called.');
			//console.log("ss.cb   p1 %O", p_json);
			var l_obj = JSON.parse(p_json);
			globals.House.Selected.HouseObj = l_obj;
		}
		//Divmod.debug('---', 'houseSelect.showSelected() was called. ');
		self.nodeById('HouseSelectButtonsDiv').style.display = 'none';		
		self.nodeById('HouseSelectedDiv').style.display = 'block';		
		self.nodeById('HouseSelectedDiv').innerHTML = 'Working on house: ' + globals.SelectedHouse.Name;		
        var l_defer = self.callRemote("getSelectedHouseData", globals.SelectedHouse.Ix);  // call server @ web_houseSelect.py
		l_defer.addCallback(cb_getSelectedHouseData);
        return false;
	},

	/**
	 * Handle the user clicking on some button of the house select menu.
	 * 
	 * @param self is the house select widget
	 * @param p_node is the node of the house button.
	 */
	function handleMenuOnClick(self, p_node) {
		//console.log("houseSelect.handleMenuOnClick - self %O", self);
		//console.log("houseSelect.handleMenuOnClick() - node %O", p_node);
		var l_ix = p_node.name;
		var l_name = p_node.value;
		if (l_ix <= 1000) {
			globals.SelectedHouse.Ix = l_ix;
			globals.SelectedHouse.Name = l_name;
			//Divmod.debug('---', 'houseSelect.handleMenuOnClick(1) was called. ' + l_key + ' ' + l_name);
			self.showSelected(self);
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget(self);
		} else if (l_ix == 10001) {
			// The "Add" button
			self.showEntry(self);
			self.hideButtons(self);
		} else if (l_ix == 10002) {
			// The "Back" button
			self.hideWidget();
			var l_node = findWidgetByClass('RootMenu');
			l_node.showWidget(self);
		}
	}
);
//### END DBK
