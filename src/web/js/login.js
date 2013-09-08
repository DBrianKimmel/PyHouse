/* login.js
 * 
 * Browser side code.
 * 
 * Displays the login 
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
 */
helpers.Widget.subclass(login, 'LoginWidget').methods(

    function __init__(self, node) {
        login.LoginWidget.upcall(self, "__init__", node);
    },

    /**
     * Override the ready function in C{ helpers.Widget.ready() }
     * 
     * @param self =<"Instance" of undefined.login.LoginWidget> 
     * @returns
     */
	function ready(self) {  // override helpers.Widget.ready()

		function cb_widgetready(res) {
			// do whatever init needs here, 'show' for the widget is handled in superclass
			Divmod.debug('---', 'login.cb_widgready() was called. ' + res);
			self.showLoginSection();
		}
	
		Divmod.debug('---', 'login.ready() was called.  self =' + self);
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	
	function showLoginSection(self) {
		Divmod.debug('---', 'login.showLoginSection() was called.');
		self.node.style.display = 'block';
		var l_full = self.nodeById('LoggedInDiv');
		l_full.style.display = 'none';
	},

	function getAndShowLogin(self) {

		function cb_showLogin(p_user) {
			Divmod.debug('---', 'login.js - cb_showLogin was called. user = ' + p_user);
			self.node.innerHTML = 'Show Login';
		}
	
        var l_logData = {
        		name : 'silly',
        		passwd : '123'
        };
    	var l_json = JSON.stringify(l_logData);
		Divmod.debug('---', 'login.js getAndShowLogin() was called.');
    	var l_defer = self.callRemote("login", l_json);  // @ web_mainpage
		l_defer.addCallback(cb_showLogin);
        return false;
	},
	
	/**
	 * 
	 * @param self
	 * @returns {Boolean}
	 */
	function doLogin(self) {  // from html handler onSubmit
		
		function cb_doLogin(p_json) {
			Divmod.debug('---', 'login.cb_doLogin(2) was called.');
		}
		function eb_doLogin(res){
			Divmod.debug('---', 'login.eb_doLogin(2) was called. res=' + res);
		}

		var loginNameField = self.nodeById('LoginName');
		var loginPasswordField = self.nodeById('LoginPassword');
    	var l_name = loginNameField.value;
    	var l_pass = loginPasswordField.value;
        var l_logData = {
        		Username : l_name,
        		Password : l_pass
        };
    	var l_json = JSON.stringify(l_logData);
		Divmod.debug('---', 'login.doLogin(1) was called. json:' + l_json);
        var l_defer = self.callRemote("doLogin", l_json);  // @ web_login
		l_defer.addCallback(cb_doLogin);
		l_defer.addErrback(eb_doLogin);
		// return false stops the resetting of the server.
        return false;
	},
	
	function loggedInStatus(self, p_json) {
		//var node = self.nodeById('rootMenuDiv');
		Divmod.debug('---', ' login.js loggedInStatus was called. json:' + p_json + ' ' + node);
	},
	
	function displayLoggedIn(self) {
		Divmod.debug('---', ' login.js displayLoggedIn was called.');
		Divmod.debug('---', ' login.js displayLoggedIn was called. json:' + p_json + ' ' + node);
		var formNode = self.nodeById('LoginForm');
		var loggedInDiv = self.nodeById('LoggedInDiv');
		formNode.style.display = "none";
		loggedInDiv.style.display = "visible";
	}
);

//### END DBK
