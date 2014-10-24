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
		self.nodeById('SelectionButtonsDiv').style.display = 'none';
	},
	function showSelectButtons(self) {
		self.nodeById('SelectionButtonsDiv').style.display = 'block';
	},
	function hideSelectedHouse(self) {
		self.nodeById('HouseDataEntryDiv').style.display = 'none';
	},
	function showSelectedHouse(self) {
		self.nodeById('HouseDataEntryDiv').style.display = 'block';
	},
	
	// ============================================================================
	/**
	 * Build a screen full of buttons (only one now) - One for each house and some actions.
	 */
	function buildLcarSelectScreen(self){
		// Divmod.debug('---', 'houseSelect.buildLcarSelectScreen was called.');
		// console.log("houseSelect.buildLcarSelectScreen  Globals - %O", globals.House);
		var l_button_html = buildLcarTable(globals.List, 'handleMenuOnClick', 'NoAdd');
		var l_html = build_lcars_top('Select House', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(2, l_button_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
	/**
	 * Called from the root menu screen when the house select button was clicked.
	 */
	function startWidget(self) {
		function cb_getHousesInfo(p_json) {
			// Divmod.debug('---', 'houseSelect.cb_getHousesInfo was called.');
			globals.List = JSON.parse(p_json);
			self.buildLcarSelectScreen()
		}
		function eb_getHousesInfo(p_result) {
			Divmod.debug('---', 'houseSelect.eb_getHousesInfo() was called. ERROR = ' + p_result);
		}
		// Divmod.debug('---', 'houseSelect.startWidget was called.');
		self.showWidget()
        var l_defer = self.callRemote("getHousesToSelect", '');  // @ web_houseSelect.py
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
			// Divmod.debug('---', 'houseSelect.cb_getSelectedHouseData() was called.');
			var l_obj = JSON.parse(p_json);
			globals.House.HouseObj = l_obj;
		}
		function eb_getSelectedHouseData(res) {
			Divmod.debug('---', 'houseSelect.eb_getSelectedHouseData() was called. ERROR = ' + res);
		}
		// Divmod.debug('---', 'houseSelect.getSelectedHouseData() was called. ');
		self.hideSelectButtons();
		self.showSelectedHouse();
		// self.nodeById('HouseSelectedDiv').innerHTML = 'Working on house: ' + globals.House.HouseName;
        var l_defer = self.callRemote("getSelectedHouseData");  // call server @ web_houseSelect.py
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
		var l_ix = p_node.name;
		var l_name = p_node.value;
		// Divmod.debug('---', 'houseSelect.handleMenuOnClick(1) was called. ' + l_ix + '  ' + l_name);
		if (l_ix <= 1000) {
			globals.House.HouseIx = l_ix;
			globals.House.HouseName = l_name;
			self.getSelectedHouseData(l_ix)
			self.hideSelectButtons();
			// Divmod.debug('---', 'houseSelect.handleMenuOnClick(2) was called. ' + l_ix + '  ' + l_name);
			self.showSelectedHouse();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget();
		} else if (l_ix == 10001) {  // The "Add" button
			globals.House.HouseIx = -1;
			self.hideSelectButtons();
			var l_node = findWidgetByClass('House');
			l_node.showWidget();
		} else if (l_ix == 10002) {  // The "Back" button
			self.hideWidget();
			var l_node = findWidgetByClass('RootMenu');
			l_node.showWidget();
		}
	}
);
// Divmod.debug('---', 'houseSelect.cb_getSelectedHouseData.cb_getSelectedHouseData() was called.');
// console.log("houseSelect.getSelectedHouseData.cb_getSelectedHouseData   p1 %O", p_json);
//### END DBK
