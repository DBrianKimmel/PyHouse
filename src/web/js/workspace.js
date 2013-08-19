/**
 *  workspace.js
 * 
 * This is the client side part of the basis of this PyHouse controller.
 * 
 * If you plan for yet another sequencing of events on startup then please change the code here.
 * 
 * The actual implementation starts and then waits for all images to be loaded (assuming that all images are loaded before user interaction is allowed).
 * That's why there is a waitroller shown during image loading and after all is said and done a READY message is displayed.
 */

// import Nevow.Athena
// import globals
// import helpers

/**
 * This is just another basic widget derived from C{common.helpers.Widget} with a twist.
 * 
 * Insofar, as the insertion happens through the basic insertion method within the delivered pages HTML,
 * namely C{<nevow:invisible nevow:render="workspace" />} which pumps up a standard livePage with exactly one fragment inserted.
 * 
 * After initialization C{Divmod.Runtime.theRuntime.} issues a call via the preset vector which contains C{globals.workspace.appStartup} you'll find below.
 * 
 * This call then starts the pulling in of whatever is needed.
 * Please see additional comments below. 
 */

helpers.Widget.subclass(workspace, 'Workspace').methods(

	function __init__(self, node) {
		workspace.Workspace.upcall(self, '__init__', node);
		globals.workspace = self; // this is the crucial reference for the startup sequence.
		// If problems during startup are observed then please have a look at this code
	},

	function showWaitRoller(self) {
		var waitroller = self.nodeById('waitroller');
		waitroller.style.visibility = 'visible';
	},

	function hideWaitRoller(self) {
		var waitroller = self.nodeById('waitroller');
		waitroller.style.visibility = 'hidden';
	},
	
	// Hide all our elements - show just what we want as the user selects things.
	function hideAll(self) {
		Divmod.debug('---', 'workspace.hideAll() - Login' + self );
		//var loginWidget = self.nodeById('LoginDiv');
		//loginWidget.style.visibility = 'hidden';
		Divmod.debug('---', 'workspace.hideAll() - Clock' + self );
		//var clockWidget = self.nodeById('ClockDiv');
		//clockWidget.style.visibility = 'visible';
	},

	/**
	 * Do whatever needs to be started up, checking for images loading and other stuff.
	 * This function is called by the C{Divmod.Runtime} code as startup event, see C{globals.js}
	 * 
	 * ---- initialization sequence to be followed:
	 * mainpage.py/.js   - the LivePage with the task of keeping up the nevow/athena RPC system
	 * workspace.py/.js - the mother of all widgets which gets the startup call in the beginning then attaching
	 *  whatever you please to attach to it.
	 * 
	 * A perfectly working version with qooxdoo is available as well as some trials with processing for mobile webapps.
	 * 
	 * This would also be the place to decide on platform specific issues, like delivering qooxdoo to the
	 *  desktop vs processing to the mobile client using HTML5 to its full extent
	 */
	
	function appStartup(self) {

		function ready() { // we're now ready for action
			var d1 = self.callRemote('guiready');

			d1.addCallback(function(res) {
				globals.__init__();
				globals.reqType = res[0];
				globals.user = res[1];
				// seems we're done, hide the visual amusements for now
				self.hideWaitRoller();
				self.attachWidget('clock', 'dummy'); // dummy params - passed down to the server
				self.attachWidget('login', 'dummy');
				//self.attachWidget('rootMenu', 'dummy');
				//self.attachWidget('houseSelect', 'dummy');
				//self.hideAll();
			});  // addCallback

			d1.addErrback(function(res) {
				Divmod.debug('---', 'ERROR - workspace.guiready.errback() - ' + res );
				self.node.appendChild(document.createTextNode('Error: ' + res.error.message));
			});  // addErrback
		} // ready

		var d = Divmod.Defer.succeed();
		d.addCallback(ready);
	} // appStartup
);

// ### END DBK
