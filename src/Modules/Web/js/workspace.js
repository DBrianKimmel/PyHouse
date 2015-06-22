/**
 * @name:      PyHouse/src/Modules/Web/js/workspace.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @Copyright: (c) 2012-2015 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created about 2012
 * @summary:   Displays the Internet element
 *
 * This script is the live element functionality.
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
// import lcars
// import interface
// import family



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
		// Divmod.debug('---', 'workspace.Workspace.showWaitRoller - ' + self );
		var waitroller = self.nodeById('waitroller');
		// waitroller.style.visibility = 'visible';
		waitroller.style.display = 'block';
	},

	function hideWaitRoller(self) {
		// Divmod.debug('---', 'workspace.Workspace.hideWaitRoller - ' + self );
		var waitroller = self.nodeById('waitroller');
		// waitroller.style.visibility = 'hidden';
		waitroller.style.display = 'none';
	},



	/**
	 * Do whatever needs to be started up, checking for images loading and other stuff.
	 * This function is called by the C{Divmod.Runtime} code as startup event, see C{globals.js}
	 * 
	 * ---- initialization sequence to be followed:
	 * mainpage.py/.js   - the LivePage with the task of keeping up the nevow/athena RPC system
	 * workspace.py/.js - the mother of all widgets which gets the startup call in the beginning then attaching
	 *  whatever you please to attach to it.
	 */
	function appStartup(self) {

		function ready() { // we're now ready for action
			function cb_ready(res) {
				globals.__init__();
				globals.reqType = res[0];
				globals.user = res[1];
				self.attachWidget('clock', 'dummy');
				self.attachWidget('login', 'dummy');
				self.attachWidget('rootMenu', 'dummy');
				//
				self.attachWidget('computerMenu', 'dummy');
				self.attachWidget('internet', 'dummy');
				self.attachWidget('mqtt', 'dummy');
				self.attachWidget('nodes', 'dummy');
				self.attachWidget('update', 'dummy');
				self.attachWidget('webs', 'dummy');
				//
				self.attachWidget('houseMenu', 'dummy');
				self.attachWidget('buttons', 'dummy');
				self.attachWidget('controllers', 'dummy');
				self.attachWidget('controlLights', 'dummy');
				self.attachWidget('house', 'dummy');
				self.attachWidget('lights', 'dummy');
				self.attachWidget('rooms', 'dummy');
				self.attachWidget('schedules', 'dummy');
				self.attachWidget('thermostats', 'dummy');
				self.hideWaitRoller();
			}
			function eb_ready(p_reason) {
				Divmod.debug('---', 'ERROR - workspace.guiready.errback() - ' + p_reason );
				self.node.appendChild(document.createTextNode('Error: ' + p_reason.error.message));
			}
			// Divmod.debug('---', 'workspace.appStartup.ready()');
			var l_defer = self.callRemote('guiready');
			l_defer.addCallback(cb_ready);
			l_defer.addErrback(eb_ready);
		} // ready

		// Divmod.debug('---', 'workspace.appStartup()');
		var d = Divmod.Defer.succeed();
		d.addCallback(ready);
	} // appStartup
);

// ### END DBK
