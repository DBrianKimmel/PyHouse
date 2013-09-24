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
		//console.log("ss self %O", self);
		//console.log("ss   p1 %O", p1);
		self.node.style.display = 'block'; 
        var l_defer = self.callRemote("getHousesToSelect", '');  // call server @ web_houseSelect.py
		l_defer.addCallback(cb_getHousesInfo);
		l_defer.addErrback(eb_getHousesInfo);
        return false;
	},
	
	function showSelected(self) {
		Divmod.debug('---', 'houseSelect.showSelected() was called. ');
		self.nodeById('HouseSelectingDiv').style.display = 'none';		
		self.nodeById('HouseSelectedDiv').style.display = 'block';		
		self.nodeById('HouseSelectedDiv').innerHTML = 'Working on house: ' + globals.selectedHouseName;		
	},
	
	function doHandleOnClick(self, p_node) {
		//console.log("houseSelect.doHandleOnClick - self %O", self);
		console.log("houseSelect.doHandleOnClick() - node %O", p_node);
		var l_key = p_node.name;
		var l_name = p_node.value;
		globals.selectedHouse = l_key;
		globals.selectedHouseName = l_name;
		Divmod.debug('---', 'houseSelect.doHandleOnClick(1) was called. ' + l_key + ' ' + l_name);
		this.showSelected(self);
		var l_node = findWidget(self, 'HouseMenu');
		l_node.showWidget(self);
	},

	/**
	 * Build an 'onclick' handler phrase to insert.
	 * 
	 * @param p_funct is a string that is the name if the function to be called.
	 */
	function buildHandlOnClick(self) {
		Divmod.debug('---', 'houseSelect.buildHandlOnClick() was called.');
		var l_html = '';
		//l_html += "<athena:handler event='onclick' handler='" + doHandleOnClick + "' />";
		return l_html;
	},

	/**
	 * Pushed from the server
	 */
	function displayHousesToSelect(self, p_json) {
		Divmod.debug('---', 'houseSelect.displayHousesToSelect(1) was called. ');
		var l_obj = JSON.parse(p_json);
		l_tab = buildTable(self, l_obj);
		self.nodeById('HSTableDiv').innerHTML = l_tab;
	}
);

//### END DBK
