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
    },

	// ============================================================================
    /**
     * Place the widget in the workspace.
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
	function hideSelectButtons(self) {
		self.nodeById('HouseSelectButtonsDiv').style.display = 'none';	
	},
	function showSelectButtons(self) {
		self.nodeById('HouseSelectButtonsDiv').style.display = 'block';	
	},
	function hideSelectedHouse(self) {
		self.nodeById('HouseSelectedDiv').style.display = 'none';	
	},
	function showSelectedHouse(self) {
		self.nodeById('HouseSelectedDiv').style.display = 'block';	
	},
	
	// ============================================================================
	/**
	 * Called from the root menu screen when the house select button was clicked.
	 * 
	 * Show the house select screen and ask the server for a JSON list of houses to show.
	 * Use a callback to get the information to display.
	 */
	function startWidget(self) {
		function cb_getHousesInfo(p_json) {
			Divmod.debug('---', 'houseSelect.startWidget.cb_getHousesInfo() was called.');
			//console.log("houseSelect.startWidget.cb   JSON = %O", p_json);
			var l_obj = JSON.parse(p_json);
			var l_tab = buildTable(l_obj, 'handleMenuOnClick');
			self.showSelectButtons();
			self.hideSelectedHouse();
			self.nodeById('HouseSelectTableDiv').innerHTML = l_tab;
		}
		function eb_getHousesInfo(res) {
			Divmod.debug('---', 'houseSelect.eb_getHousesInfo() was called. ERROR = ' + res);
		}
		//Divmod.debug('---', 'houseSelect.startWidget() was called.');
		self.showWidget()
        var l_defer = self.callRemote("getHousesToSelect", '');  // call server @ web_houseSelect.py
		l_defer.addCallback(cb_getHousesInfo);
		l_defer.addErrback(eb_getHousesInfo);
        return false;
	},

	/**
	 * A house was selected.
	 * Show the house and then load the information for the selected house.
	 */
	function getSelectedHouseData(self) {
		function cb_getSelectedHouseData(p_json) {
			//Divmod.debug('---', 'houseSelect.getSelectedHouseData.cb_getSelectedHouseData() was called.');
			//console.log("ss.cb   p1 %O", p_json);
			var l_obj = JSON.parse(p_json);
			globals.House.HouseObj = l_obj;
		}
		function eb_getSelectedHouseData(res) {
			Divmod.debug('---', 'houseSelect.eb_getSelectedHouseData() was called. ERROR = ' + res);			
		}
		//Divmod.debug('---', 'houseSelect.getSelectedHouseData() was called. ');
		self.hideSelectButtons();		
		self.showSelectedHouse();		
		self.nodeById('HouseSelectedDiv').innerHTML = 'Working on house: ' + globals.House.HouseName;		
        var l_defer = self.callRemote("getSelectedHouseData", globals.House.HouseIx);  // call server @ web_houseSelect.py
		l_defer.addCallback(cb_getSelectedHouseData);
		l_defer.addErrback(eb_getSelectedHouseData);
        return false;
	},

	/**
	 * Handle the user clicking on some button of the house select menu.
	 * 
	 * @param self is the house select widget
	 * @param p_node is the node of the house button.
	 */
	function handleMenuOnClick(self, p_node) {
		//Divmod.debug('---', 'houseSelect.handleMenuOnClick() was called.  Node: ' + p_node.value);
		//console.log("houseSelect.handleMenuOnClick() - node %O", p_node);
		var l_ix = p_node.name;
		var l_name = p_node.value;
		if (l_ix <= 1000) {
			globals.House.HouseIx = l_ix;
			globals.House.HouseName = l_name;
			//Divmod.debug('---', 'houseSelect.handleMenuOnClick("house" Button) was called.  Ix: ' + l_ix + '  Name: ' + l_name);
			self.getSelectedHouseData(l_ix)
			self.hideSelectButtons();
			self.showSelectedHouse();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget();
		} else if (l_ix == 10001) {
			// The "Add" button
			//Divmod.debug('---', 'houseSelect.handleMenuOnClick(Add Button) was called.  Ix: ' + l_ix);
			globals.House.HouseIx = -1;
			self.hideSelectButtons();
			var l_node = findWidgetByClass('House');
			l_node.showWidget();
		} else if (l_ix == 10002) {
			// The "Back" button
			//Divmod.debug('---', 'houseSelect.handleMenuOnClick(Back Button) was called.  Ix: ' + l_ix);
			self.hideWidget();
			var l_node = findWidgetByClass('RootMenu');
			l_node.showWidget();
		}
	}
);
//### END DBK
