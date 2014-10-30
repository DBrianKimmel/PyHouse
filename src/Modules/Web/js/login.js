/**
 * @name: PyHouse/src/Modules/Web/js/login.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created on Mar 11, 2014
 * @summary: Displays the login element
 */
// import Nevow.Athena
// import globals
// import helpers


/**
 * The login widget.
 * 
 * This displays a login DIV at first and when C{LoggedIn} is false.
 * When properly authenticated, C{Fullname} becomes defined and C{LoggedIn} is set to true,
 *  the widget hides the login screen and shows a DIV that shows who is logged in.
 *  
 *  After successful login, the rootMenu is displayed.
 */
helpers.Widget.subclass(login, 'LoginWidget').methods(

    function __init__(self, node) {
        login.LoginWidget.upcall(self, "__init__", node);
    },

    // ============================================================================
    /**
     * Place the widget in the workspace.
     * 
     * Override the ready function in C{ helpers.Widget.ready() }
     */
	function ready(self) {
		function cb_widgetready(res) {
			self.showLoggingInDiv();
			self.fetchValidLists();
		}
		//Divmod.debug('---', 'login.ready() was called. ');
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	function hideLoggingInDiv(self) {
		self.nodeById('LoggingInDiv').style.display = "none";
	},
	function showLoggingInDiv(self) {
		//Divmod.debug('---', 'login.showLoggingInDiv() was called. ');
		self.nodeById('LoggingInDiv').style.display = 'block';
		// self.nodeById('LoggedInDiv').style.display = 'none';
	},
	function hideLoggedInDiv(self) {
		//self.nodeById('LoggedInDiv').style.display = "none";
	},
	function showLoggedInDiv(self) {
		//self.nodeById('LoggedInDiv').style.display = "block";
	},

    // ============================================================================
	/**
	 * Fetch various valid things from server.
	 */
	function fetchValidLists(self) {
		function cb_fetchValidLists(p_json) {
    		globals.Valid = JSON.parse(p_json);
			//Divmod.debug('---', 'login.cb_fetchValidLists() was called.');
		}
		//Divmod.debug('---', 'login.fetchValidLists() was called. ');
        var l_defer = self.callRemote("getValidLists");  // @ web_login
		l_defer.addCallback(cb_fetchValidLists);
	},
	function buildLcarLoginScreen(self, p_handler){
		Divmod.debug('---', 'login.buildLcarLoginScreen() was called.');
		var l_login_html = "";
		l_login_html += buildLcarTextWidget(self, 'LoginName', 'Name', '');
		l_login_html += buildLcarTextWidget(self, 'LoginPassword', 'Password', '');
		l_login_html += xxxx;
		var l_html = build_lcars_top('Control Lights', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(2, l_login_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},

	// ============================================================================
	/**
	 * This is an event handler from the LogIn key in the login form.
	 * 
	 * @param self
	 * @returns {Boolean} False to stop the processing cycle.
	 */
	function doLoginSubmit(self) {  // from html handler onSubmit
		function cb_doLoginSubmit(p_json) {
			//Divmod.debug('---', 'login.cb_doLoginSubmit() was called.  JSON: ' + p_json);
			var l_obj = JSON.parse(p_json);
			self.showNextScreen(l_obj);
		}
		function eb_doLoginSubmit(res){
			Divmod.debug('---', 'login.eb_doLoginSubmit() was called.  ERROR = ' + res);
		}
        var l_logData = {
        	Username : self.nodeById('LoginName').value,
        	Password : self.nodeById('LoginPassword').value
        };
    	var l_json = JSON.stringify(l_logData);
		//Divmod.debug('---', 'login.doLoginSubmit() was called. JSON: ' + l_json);
        var l_defer = self.callRemote("doLogin", l_json);  // @ web_login
		l_defer.addCallback(cb_doLoginSubmit);
		l_defer.addErrback(eb_doLoginSubmit);
        return false;  // Stops the resetting of the server.
	},
	
	// ============================================================================
	/**
	 * Based on the login success - show the next screen.
	 */
	function showNextScreen(self, p_obj) {
		function cb_showNextScreen(res) {
			var l_node = findWidgetByClass('RootMenu');
			l_node.showWidget(self);
		}
		if (p_obj.LoggedIn === true) {
			globals.User.ID = p_obj.Username;
			globals.User.Password = p_obj.Password;
			globals.User.Fullname = p_obj.Fullname;
			globals.User.LoggedIn = true;
			self.hideLoggingInDiv(self);
			// self.showLoggedInDiv(self);
			var l_defer = serverState(22);
			l_defer.addCallback(cb_showNextScreen);
		} else {
			self.showLoggingInDiv(self);
			// self.hideLoggedInDiv(self);
        	self.nodeById('LoginPassword').value = '';
		}
	}
);
//### END DBK
