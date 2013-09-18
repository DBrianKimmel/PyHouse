/* houseSelect.js
 * 
 * Displays the house selection element
 */

// import Nevow.Athena
// import globals
// import helpers
// import w_server

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

    
    /**
     * Place the widget in the workspace.
     * 
     * Override the ready function in C{ helpers.Widget.ready() }
     */
	function ready(self) {
		function cb_widgetready(res) {
			// do whatever init needs here, show for the widget is handled in superclass
			self.hideSelect();
		}
		var uris = collectIMG_src(self.node, null);
		var d = loadImages(uris);
		d.addCallback(cb_widgetready);
		return d;
	},


	function hideSelect(self) {
		//Divmod.debug('---', 'houseSelect.hideSelect() was called. self = ' + self);
		self.node.style.display = 'none';
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
		function cb_getHousesInfo(self, p1, p2) {
			Divmod.debug('---', 'houseSelect.showSelect.cb_getHousesInfo() was called.');
			//console.log("ss.cb self %O", self);
			//console.log("ss.cb   p1 %O", p1);
			//console.log("ss.cb   p2 %O", p2);
		}
		function eb_getHousesInfo(self, p1, p2) {
			Divmod.debug('---', 'houseSelect.eb_getHousesInfo() was called. self = ' + self);
		}
		Divmod.debug('---', 'houseSelect.showSelect() was called.');
		console.log("ss self %O", self);
		console.log("ss   p1 %O", p1);
		self.node.style.display = 'block';
        var l_defer = self.callRemote("getHousesToSelect", '');  // call server @ web_houseSelect.py
		l_defer.addCallback(cb_getHousesInfo);
		l_defer.addErrback(eb_getHousesInfo);
        return false;
	},
	
	//var doSelectHouse1 = function () {
	//	Divmod.debug('---', 'houseSelect.doSelectHouse1() was called.');
	//}

	function doSelectHouse2() {
		Divmod.debug('---', 'houseSelect.doSelectHouse2() was called.');
	},


	/**
	 * Pushed from the server
	 */
	function displayHousesToSelect(self, p_json) {
		//Divmod.debug('---', 'houseSelect.displayHousesToSelect(1) was called.');
		var l_obj = JSON.parse(p_json);
		l_tab = buildTable(self, l_obj, doSelectHouse2);
		self.nodeById('HSTableDiv').innerHTML = l_tab;
	}
);

//### END DBK
