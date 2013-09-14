/* login.js
 * 
 * Browser side code.
 * 
 * Displays the login 
 */

// import Nevow.Athena
// import globals
// import helpers
// import w_server


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
	
	/**
	 * This is an event handler from the submit key in the login form.
	 * 
	 * @param self
	 * @returns {Boolean} False to stop the processing cycle.
	 */
	function doLoginSubmit(self) {  // from html handler onSubmit
		
		function cb_doLogin(p_json) {
			Divmod.debug('---', 'login.cb_doLogin(2) was called.');
		}
		function eb_doLogin(res){
			Divmod.debug('---', 'login.eb_doLogin(2) was called. res=' + res);
		}
        var l_logData = {
        	Username : self.nodeById('LoginName').value,
        	Password : self.nodeById('LoginPassword').value
        };
    	var l_json = JSON.stringify(l_logData);
		Divmod.debug('---', 'login.doLogin(1) was called. json:' + l_json);
        var l_defer = self.callRemote("doLogin", l_json);  // @ web_login
		l_defer.addCallback(cb_doLogin);
		l_defer.addErrback(eb_doLogin);
		// return false stops the resetting of the server.
        return false;
	},
	
	function showLoginSection(self) {
		Divmod.debug('---', 'login.showLoginSection() was called.');
		self.node.style.display = 'block';
		var l_full = self.nodeById('LoggedInDiv');
		l_full.style.display = 'none';
	},

	function hideLoggingInDiv(self) {
		//var loggingInDiv = self.nodeById('LoggingInDiv');
		//loggingInDiv.style.display = "none";		
		self.nodeById('LoggingInDiv').style.display = "none";		
		Divmod.debug('---', 'login.hideLoggingInDiv was called.');
	},
	
	function showLoggedInDiv(self) {
		Divmod.debug('---', 'login.showLoggedInDiv was called.');
		var loggedInDiv = self.nodeById('LoggedInDiv');
		loggedInDiv.style.display = "block";		
	},
	
	function displayFullname(self, p_json) {
		
		function cb_showRootMenu(res) {
			Divmod.debug('---', 'login.cb_showRootMenu was called. self:' + self);
			var l_node = findWidget(self, 'RootMenu');
			l_node.showRootMenu(self);
		}
		var l_obj = JSON.parse(p_json);
		Divmod.debug('---', 'login.displayFullname was called. json:' + p_json);
		this.hideLoggingInDiv(self);
		this.showLoggedInDiv(self);
		self.nodeById('LoggedInDiv').innerHTML = 'Logged in: ' + l_obj.Fullname;
		var l_defer = serverState(22);
		l_defer.addCallback(cb_showRootMenu);
	}
);

//### END DBK
