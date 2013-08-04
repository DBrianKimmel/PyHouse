// mainpage.js

// import Divmod
// import Nevow.Athena
// import globals
// import helpers

Nevow.Athena.PageWidget
		.subclass(mainPage, 'Mainpage')
		.methods(
				function showDisconnectDialog(self) {
					Divmod
							.msg("Connection lost, dialog or status display implementation pending");
				});

// playground.js - let's users play whatever games, contains the whole startup
// logic for the site. This is the client side part of the basis
// of this whole website. If you plan for yet another sequencing of
// events on startup then please change the code here. The actual
// implementation starts, waits for all images to be loaded (assuming
// that all images are loaded before user interaction is allowed.
// That's why there is a waitroller shown during image loading and after
// all is said and done a READY message is displayed.
//
// author : Werner Thie, wth
// last edit: wth, 20.01.2011
// modhistory:
// 20.01.2011 - wth, pruned for minimal

// import Nevow.Athena
// import globals
// import helpers

// this is just another basic widget derived from common.helpers.Widget with a
// twist
// insofar, as the insertion happens through the basic insertion method within
// the
// deliverred pages html, namely <nevow:invisible nevow:render="playground" />
// which
// pumps up a standard lifepage with exactly one fragment inserted. After
// initialisation
// Divmod.Runtime.theRuntime. issues a call via the preset vector which contains
// globals.playground.appStartup you'll find below. This call then starts the
// pulling in
// of whatever is needed, please see additional comments below

Nevow.Athena.Widget.subclass(mainPage, 'Playground').methods(
		function __init__(self, node) {
			mainPage.Playground.upcall(self, '__init__', node);
			globals.playground = self; // this is the crucial ref for the
										// startup sequence.
			// If problems during startup are observed then please
			// have a look at this code
		},

		function showWaitRoller(self) {
			var waitroller = self.nodeById('waitroller');
			waitroller.style.visibility = 'visible';
		},

		function hideWaitRoller(self) {
			var waitroller = self.nodeById('waitroller');
			waitroller.style.visibility = 'hidden';
		},

		// do whatever needs to be started up, checking for images loading
		// and other gory stuff. This function is called by the Divmod.Runtime
		// code as startup event, see globals.js
		//
		// ---- initialization sequence to be followed
		// mainpage.py/.js - the LivePage with the task of keeping up the
		// nevow/athena RPC system
		// playground.py/.js - the mother of all widgets which gets the startup
		// call in the beginning
		// then attaching whatever you please to attach to it.
		//
		// A perfectly working version with qooxdoo is available as well as some
		// trials with processing for mobile webapps. This would also be the place
		// to decide on platform specific issues, like delivering qooxdoo to the
		// desktop vs processing to the mobile client using HTML5 to its full
		// extent

		function appStartup(self) {
			function ready() { // we're now ready for action
				var d1 = self.callRemote('guiready');

				d1.addCallback(function(res) {
					alert("mainPage.addCallback res = " + res)
					globals.__init__();
					globals.reqType = res[0];
					globals.user = res[1];
					self.hideWaitRoller(); // seems we're done, hide the visual
											// amusements for now
					self.attachWidget('clock', 'dummy'); // dummy params
															// passed down to
															// the server
				});

				d1.addErrback(function(res) {
					alert("mainPage.addErrback res = " + res)
					self.node.appendChild(document.createTextNode('Error: '
							+ res.error.message));
				});  // addErrback
			} // ready

			var d = Divmod.Defer.succeed();
			d.addCallback(ready);
		} // appStartup
);

// from globals

Divmod.Runtime.theRuntime.addLoadEvent(function appStartup() {
	globals.playground.appStartup();
});

// ### END
