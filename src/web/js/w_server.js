/** server.js
 *
 */

// import Divmod.Runtime
// import helpers

/**
 * Create a server state class that returns a deferred.
 * 
 * The deferred id triggered whenever the server state changes.
 * 
 * The main purpose is to control the display of the various sections of the PyHouse web page.
 */

w_server.ServerStateError = Divmod.Error.subclass('w_server.ServerStateError');

function serverState(p_state) {
	Divmod.debug('---', 'w_server.serverState was called. state:' + p_state);
	var m_state = p_state;
	
	var steprate = 1; // checks per second
	var maxsteps = steprate * 60 * 60 * 24;
	var stepcount = 0;
	var stateDeferred = Divmod.Defer.Deferred();

	var checkStep = function() {
		if ((stepcount > maxsteps)) {
			self.timer = null;
			stateDeferred.errback(new w_server.ServerStateError('Invalid Server State: ' + m_state));
		} else if ((m_state < 999)) {
			stateDeferred.callback();
		} else {
			stepcount++;
			self.timer = setTimeout(checkStep, 1000 / steprate);
		}
	};

	self.timer = setTimeout(checkStep, 1000 / steprate);
	return stateDeferred;
}

//### END DBK
