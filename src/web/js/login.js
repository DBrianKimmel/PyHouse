/* login.js
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
 *  
 *  After successful login, the rootMenu is displayed.
 */
helpers.Widget.subclass(login, 'LoginWidget').methods(

    function __init__(self, node) {
        login.LoginWidget.upcall(self, "__init__", node);
    },

    
    /**
     * Place the widget in the workspace.
     * 
     * Override the ready function in C{ helpers.Widget.ready() }
     */
	function ready(self) {
		function cb_widgetready(res) {
			// do whatever init needs here, 'show' for the widget is handled in superclass
			self.showLoginSection();
		}
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
			//Divmod.debug('---', 'login.cb_doLogin(2) was called.');
		}
		function eb_doLogin(res){
			//Divmod.debug('---', 'login.eb_doLogin(2) was called. res=' + res);
		}
        var l_logData = {
        	Username : self.nodeById('LoginName').value,
        	Password : self.nodeById('LoginPassword').value
        };
    	var l_json = JSON.stringify(l_logData);
		//Divmod.debug('---', 'login.doLogin(1) was called. json:' + l_json);
        var l_defer = self.callRemote("doLogin", l_json);  // @ web_login
		l_defer.addCallback(cb_doLogin);
		l_defer.addErrback(eb_doLogin);
		// return false stops the resetting of the server.
        return false;
	},

	function showLoginSection(self) {
		self.node.style.display = 'block';
		var l_full = self.nodeById('LoggedInDiv');
		l_full.style.display = 'none';
	},

	function hideLoggingInDiv(self) {
		self.nodeById('LoggingInDiv').style.display = "none";
	},

	function showLoggedInDiv(self) {
		var loggedInDiv = self.nodeById('LoggedInDiv');
		loggedInDiv.style.display = "block";		
	},

	
	/**
	 * Pushed from the server
	 * 
	 * @param self   is <"Instance" of undefined.login.LoginWidget>
	 * @param p_json is 
	 */
	function displayFullname(self, p_json) {
		
		function cb_showRootMenu(res) {
			//Divmod.debug('---', 'login.cb_showRootMenu() was called. ');
			var l_node = findWidget(self, 'RootMenu');
			l_node.showWidget(self);
		}
		Divmod.debug('---', 'login.displayFullname() was called. ' + self + ' ' + p_json);
		var l_obj = JSON.parse(p_json);
		globals.User.ID = l_obj.Username;
		globals.User.Password = l_obj.Password;
		globals.User.Fullname = l_obj.Fullname;
		globals.User.LoggedIn = true;
		this.hideLoggingInDiv(self);
		this.showLoggedInDiv(self);
		self.nodeById('LoggedInDiv').innerHTML = 'Logged in: ' + l_obj.Fullname;
		var l_defer = serverState(22);
		l_defer.addCallback(cb_showRootMenu);
	}
);

//### END DBK
