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
     * Startup - Place the widget in the workspace and hide it.
     * 
     * Override the ready function in C{ helpers.Widget.ready() }
     * 
     * This is the initial widget shown in the browser.
     * Do things a little differently in login.js
     */
	function ready(self) {
		function cb_widgetReady() {
			self.showLoggingInDiv();
			self.fetchValidLists();  // Continue with next phase
		}
		function eb_widgetReady(p_reason) {
			Divmod.debug('---', 'ERROR - login.eb_widgetReady() - .' + p_reason);
		}
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetReady);
		l_defer.addErrback(eb_widgetReady);
		return l_defer;
	},
	function hideLoggingInDiv(self) {
		self.nodeById('SelectionButtonsDiv').style.display = "none";  // No space taken
	},
	function showLoggingInDiv(self) {
		self.nodeById('SelectionButtonsDiv').style.display = 'block';
	},



// ============================================================================
	/**
	 * Fetch various valid things from server.
	 * These never change till new software is added to PyHouse.
	 * These are used to build selection widgets used by all later screens.
	 */
	function fetchValidLists(self) {
		function cb_fetchValidLists(p_json) {
    		globals.Valid = JSON.parse(p_json);
    		self.buildLcarLoginScreen('doLoginSubmit');
		}
		function eb_fetchValidLists(p_reason) {
			Divmod.debug('---', 'ERROR - login.eb_fetchValidLists() - .' + p_reason);
		}
		// Divmod.debug('---', 'login.fetchValidLists() was called.');
        var l_defer = self.callRemote("getValidLists");  // @ web_login
		l_defer.addCallback(cb_fetchValidLists);
		l_defer.addErrback(eb_fetchValidLists);
	},
	/**
	 * Build a screen for logging in.
	 */
	function buildLcarLoginScreen(self, p_handler){
		var l_login_html = "";
		l_login_html += buildLcarTextWidget(self, 'LoginName', 'Name', '');
		l_login_html += buildLcarPasswordWidget(self, 'LoginPassword', 'Password', 'size=20');
		l_login_html += buildLcarButton({'Name' : 'Login', 'Key' : 12345}, p_handler, 'lcars-salmon-bg');
		var l_html = build_lcars_top('Login', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(10, l_login_html);
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
	function doLoginSubmit(self) {
		function cb_doLoginSubmit(p_json) {
			var l_obj = JSON.parse(p_json);
			self.showNextScreen(l_obj);
		}
		function eb_doLoginSubmit(res){
			Divmod.debug('---', 'login.eb_doLoginSubmit() was called.  ERROR = ' + res);
		}
        var l_loginData = {
    		LoginName : fetchTextWidget(self, 'LoginName'),
    		Password : fetchTextWidget(self, 'LoginPassword'),
        };
    	var l_json = JSON.stringify(l_loginData);
		// Divmod.debug('---', 'login.doLoginSubmit() was called. JSON: ' + l_json);
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
		function cb_showNextScreen() {
			var l_node = findWidgetByClass('RootMenu');
			self.hideWidget();
			l_node.showWidget(self);
			}
		function eb_showNextScreen(p_reason) {
			Divmod.debug('---', 'ERROR = login.showNextScreen() - ' + p_reason);
		}
		// Divmod.debug('---', 'login.showNextScreen() was called.');
		if (p_obj.IsLoggedIn === true) {
			globals.User.ID = p_obj.Username;
			globals.User.Password = p_obj.Password;
			globals.User.Fullname = p_obj.Fullname;
			globals.User.LoggedIn = true;
			self.hideLoggingInDiv(self);
			var l_defer = serverState(22);
			l_defer.addCallback(cb_showNextScreen);
			l_defer.addErrback(eb_showNextScreen);
		} else {
			Divmod.debug('---', 'login.showNextScreen() was called.');
			self.showLoggingInDiv(self);
        	self.nodeById('LoginPassword').value = '';
		}
	}
);
//Divmod.debug('---', 'login.handleMenuOnClick(1) was called. ' + l_ix + ' ' + l_name);
//console.log("login.handleMenuOnClick() - l_obj = %O", l_obj);
//### END DBK
