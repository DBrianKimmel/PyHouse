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
	 * These never change during a run of this PyHouse daemon.
	 * These are used to build selection widgets used by all later screens.
	 */
	function fetchValidLists(self) {
		function cb_fetchValidLists(p_json) {
    		globals.Valid = JSON.parse(p_json);
    		self.buildLcarLoginScreen('handleLoginButtonClick');
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
	 * This is an event handler for the 'LogIn' button in the login screen.
	 *
	 * Sends the login information to the server.
	 * Receives the result of the login attempt back from the server.
	 *
	 * @param self
	 * @returns {Boolean} False to stop the processing cycle.
	 */
	function handleLoginButtonClick(self) {
		function cb_handleLoginButtonClick(p_json) {
			var l_obj = JSON.parse(p_json);
			self.showNextScreen(l_obj);
		}
		function eb_handleLoginButtonClick(res){
			Divmod.debug('---', 'login.eb_handleLoginButtonClick() was called.  ERROR = ' + res);
		}
        var l_loginData = {
    		LoginName : fetchTextWidget(self, 'LoginName'),
    		Password : fetchTextWidget(self, 'LoginPassword'),
        };
    	var l_json = JSON.stringify(l_loginData);
        var l_defer = self.callRemote("doLogin", l_json);  // @ web_login
		l_defer.addCallback(cb_handleLoginButtonClick);
		l_defer.addErrback(eb_handleLoginButtonClick);
        return false;  // Stops the resetting of the server.
	},


// ============================================================================
	/**
	 * Based on the login success - show the next screen.
	 */
	function showNextScreen(self, p_obj) {
		function cb_showNextScreen() {
			// Divmod.debug('---', 'login.cb_showNextScreen(1) was called.');
			self.showWidget('RootMenu');
			}
		function eb_showNextScreen(p_reason) {
			Divmod.debug('---', 'ERROR = login.showNextScreen() - ' + p_reason);
		}
		// Divmod.debug('---', 'login.showNextScreen(2) was called.');
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
			Divmod.debug('---', 'login.showNextScreen(3) was called.');
			globals.User.Fullname = 'Login Attempt failed!';
			self.showLoggingInDiv(self);
        	self.nodeById('LoginPassword').value = '';
		}
	}
);
//Divmod.debug('---', 'login.handleMenuOnClick(1) was called.');
//console.log("login.handleMenuOnClick() - l_obj = %O", l_obj);
//### END DBK
