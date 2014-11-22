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
		self.showSelectionButtons();
		self.getHousesInfo();
	},
	function hideSelectionButtons(self) {
		// Divmod.debug('---', 'houseSelect.hideSelectionButtons() was called.');
		self.nodeById('SelectionButtonsDiv').style.display = 'none';
	},
	function showSelectionButtons(self) {
		self.nodeById('SelectionButtonsDiv').style.display = 'block';
	},



// ============================================================================
	/**
	 * Build a screen full of buttons (only one now) - One for each house and some actions.
	 */
	function buildLcarSelectScreen(self){
		var l_button_html = buildLcarSelectionButtonsTable(globals.List, 'handleMenuOnClick', 'NoAdd');
		var l_html = build_lcars_top('Select House', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(10, l_button_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
	/**
	 * Called from the root menu screen when the house select button was clicked.
	 */
	function getHousesInfo(self) {
		function cb_getHousesInfo(p_json) {
			globals.List = JSON.parse(p_json);
			self.buildLcarSelectScreen();
		}
		function eb_getHousesInfo(p_result) {
			Divmod.debug('---', 'houseSelect.eb_getHousesInfo() was called. ERROR = ' + p_result);
		}
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
		function eb_getSelectedHouseData(p_reason) {
			Divmod.debug('---', 'ERROR houseSelect.eb_getSelectedHouseData() - ' + p_reason);
		}
		// Divmod.debug('---', 'houseSelect.getSelectedHouseData() was called. ');
		self.hideSelectionButtons();
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
		var l_node = 0;
		if (l_ix <= 1000) {
			globals.House.HouseIx = l_ix;
			globals.House.HouseName = l_name;
			self.getSelectedHouseData(l_ix);
			self.hideSelectionButtons();
			self.showWidget2('HouseMenu');
		} else if (l_ix == 10001) {  // The "Add" button
			globals.House.HouseIx = -1;
			self.hideSelectionButtons();
			self.showWidget2('House');
		} else if (l_ix == 10002) {  // The "Back" button
			self.showWidget2('RootMenu');
		}
	}
);
// Divmod.debug('---', 'houseSelect.cb_getSelectedHouseData.cb_getSelectedHouseData() was called.');
// console.log("houseSelect.getSelectedHouseData.cb_getSelectedHouseData   p1 %O", p_json);
//### END DBK
