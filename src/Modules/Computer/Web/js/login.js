/**
 * @name:      PyHouse/src/Modules/Web/js/login.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2016 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created on Mar 11, 2014
 * @summary:   Displays the login element
 *
 * This is the first screen to show when a connection is made to the web server.
 *
 * Validate the user/password in python code - then...
 * Bring up the main menu next
 */
// import Nevow.Athena
// import globals
// import helpers
// import lcars


/**
 * The login widget.
 * 
 * This displays a login DIV at first and when C{LoggedIn} is false.
 * When properly authenticated, C{Fullname} becomes defined and C{LoggedIn} is set to true,
 *  the widget hides the login screen and shows a DIV that shows who is logged in.
 *  
 *  After successful login, the rootMenu is displayed.
 */
var m_login_obj = {
	Name : '',
    FullName : '',
    Role : 'Not logged in.',
    PasswordCurrent : '',
    PasswordNew: '',
    PasswordVerify: '',
    ChangeFlag : false,
    IsLoggedIn : false
}

helpers.Widget.subclass(login, 'LoginWidget').methods(

    function __init__(self, node) {
        login.LoginWidget.upcall(self, "__init__", node);
        globals.Login = m_login_obj;
    },


// ============================================================================
    /**
     * Startup - Place the login widget in the workspace and hide it.
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
    		self.buildLcarLoginScreen(globals.Login, 'handleLoginButtonClick');
		}
		function eb_fetchValidLists(p_reason) {
			Divmod.debug('---', 'ERROR - login.eb_fetchValidLists() - .' + p_reason);
		}
		// Divmod.debug('---', 'login.fetchValidLists');
		// console.log("login.fetchValidLists() - Login = %O", globals.Login);
		var l_defer = self.callRemote("getValidLists");  // @ web_login
		l_defer.addCallback(cb_fetchValidLists);
		l_defer.addErrback(eb_fetchValidLists);
	},

// ============================================================================
	/**
	 * Build a screen for logging in.
	 * Set the entry focus to the 'Name' Field
	 * Set the enter key action to the 'Log In' button
	 * 
	 * @param p_obj is m_login_obj that contains all the login info.
	 * @param p_handler is the function to be called when the kogin button is clicked
	 */
	function buildLcarLoginScreen(self, p_obj, p_handler) {
		var l_obj = arguments[1];
		var l_html = build_lcars_top('Login', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(10, self.buildEntry(l_obj, 'change', p_handler));
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
	},
	function buildEntry(self, p_obj, p_add_change, p_handler, p_onchange) {
		var l_html = '';
		l_html = self.buildLoginEntry(p_obj, l_html, p_onchange);
		l_html += buildLcarButton({'Name' : 'Login', 'Key' : 12345}, p_handler, 'lcars-salmon-bg');
		return l_html;
	},
	function buildLoginEntry(self, p_obj, p_html, p_onchange) {
		p_html += buildLcarTextWidget(self, 'LoginName', 'Name', p_obj.Name);
		p_html += buildLcarPasswordWidget(self, 'PasswordCurrent', 'Current Password', 'size=20', p_obj.PasswordCurrent);
		p_html += buildLcarTrueFalseWidget(self, 'ChangeFlag', 'Change Password ?', p_obj.ChangeFlag, 'handlePasswordChangeClick')
		if (p_obj.ChangeFlag === true) {
			p_html += buildLcarPasswordWidget(self, 'PasswordNew', 'New Password', 'size=20', p_obj.PasswordNew);
			p_html += buildLcarPasswordWidget(self, 'PasswordVerify', 'Verify Password', 'size=20', p_obj.PasswordVerify);
		}
		p_html += buildLcarTextWidget(self, 'FullName', 'Full Name', p_obj.FullName, 'disable')
		p_html += buildLcarTextWidget(self, 'Role', 'Role', p_obj.Role, 'disable');
		return p_html;
	},
	function handlePasswordChangeClick(self) {
		// Divmod.debug('---', 'login.handlePasswordChangeClick was called.');
		var l_flag = fetchTrueFalseWidget(self, 'ChangeFlag');
		globals.Login.ChangeFlag = l_flag;
		//if (l_flag === true)
		self.buildLcarLoginScreen(globals.Login, 'handleLoginButtonClick');
		// console.log("login.handlePasswordChangeClick() - self = %O", self);
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
			var LOGIN_DISPLAY_INTERVAL = 2.0;
			var l_obj = JSON.parse(p_json);
			// self.showNextScreen(l_obj);
        	self.nodeById('FullName').value = l_obj.LoginFullName;
        	globals.Login.FullName = l_obj.LoginFullName;
        	self.nodeById('Role').value = l_obj.LoginRole;
			self.callLater(LOGIN_DISPLAY_INTERVAL, function() {
				self.showNextScreen(l_obj);
				}
			);
		}
		function eb_handleLoginButtonClick(res){
			Divmod.debug('---', 'login.eb_handleLoginButtonClick() was called.  ERROR = ' + res);
		}
        globals.Login.Name = fetchTextWidget(self, 'LoginName');
        globals.Login.PasswordCurrent = fetchTextWidget(self, 'PasswordCurrent');
        globals.Login.ChangeFlag = fetchTrueFalseWidget(self, 'ChangeFlag');
        if (globals.Login.ChangeFlag === true)
            globals.Login.PasswordNew = fetchTextWidget(self, 'PasswordNew');
        else
            globals.Login.PasswordNew = '';
       	var l_json = JSON.stringify(globals.Login);
        var l_defer = self.callRemote("doLogin", l_json);  // @ web_login
		l_defer.addCallback(cb_handleLoginButtonClick);
		l_defer.addErrback(eb_handleLoginButtonClick);
        return false;  // Stops the resetting of the server.
	},


// ============================================================================
	/**
	 * Based on the login success - show the next screen >> RootMenu.
	 */
	function showNextScreen(self, p_obj) {
		function cb_showNextScreen() {
			self.showWidget('RootMenu');
			}
		function eb_showNextScreen(p_reason) {
			Divmod.debug('---', 'ERROR = login.eb_showNextScreen() - ' + p_reason);
		}
		if (p_obj.IsLoggedIn === true) {
			globals.User.ID = p_obj.Username;
			globals.User.Password = p_obj.PasswordCurrent;
			globals.User.Fullname = p_obj.Fullname;
			globals.User.LoggedIn = true;
			self.hideLoggingInDiv(self);
			var l_defer = serverState(22);
			l_defer.addCallback(cb_showNextScreen);
			l_defer.addErrback(eb_showNextScreen);
		} else {
			// Divmod.debug('---', 'login.showNextScreen() was called.');
			globals.User.Fullname = 'Login Attempt failed!';
			globals.Login.FullName = 'Login Attempt failed!';
			self.showLoggingInDiv(self);
        	self.nodeById('PasswordCurrent').value = '';
        	self.nodeById('FullName').value = globals.Login.FullName;
		}
	}
);
// Divmod.debug('---', 'login.handleMenuOnClick(1) was called.');
// console.log("login.handleMenuOnClick() - l_obj = %O", l_obj);
//### END DBK
