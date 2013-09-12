/** server.js
 *
 */

// import Divmod.Runtime
// import helpers

Divmod.debug('---', 'server.js imported.');

/**
 * Create a server state class that returns a deferred.
 * 
 * The deferred id triggered whenever the server state changes.
 * 
 * The main purpose is to control the display of the various sections of the PyHouse web page.
 */

function serverState(p_state) {
	Divmod.debug('---', 'server.serverState was called. state:' + p_state);
	var state = p_state;
	
	var stateDeferred = Divmod.Defer.Deferred();
	
	return stateDeferred;
}

//### EBD DBK
