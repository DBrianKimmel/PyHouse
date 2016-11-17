/**
 * @name:      PyHouse/src/Modules/Web/js/helpers.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2012-2016 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created about 2012
 * @summary:   Displays the elements
 * 
 * This script is the live element functionality.
 * 
 * This MUST be imported in workspace.js
 */
// import Nevow.Athena



/**
 * This basic widget can attach subwidgets and provides some other basic functionality.
 */
Nevow.Athena.Widget.subclass(helpers, 'Widget').methods(

	function __init__(self, node) {
		helpers.Widget.upcall(self, '__init__', node);
	},


	/**
	 *  Special attention should be paid to the function C{ready} which should be overridden in almost every case,
	 *  working with the C{widgetready} function in a closure.
	 *
	 * C{widgetready} could of call another method C{func} in the class but practice shows, that the point of being informed that
	 *  we're setup properly for action is way too important to delegate it into superclass.
	 *
	 * Think of C{ready} as a stub, which is more like a template to start work on your own widgets implementation.
	 *
	 * @param self =
	 * @returns a deferred that completes async
	 */
	function ready(self) {

		function cb_widgetready(res) {
			//do whatever init needs here
		}

		/**
		 * Pre action tasks needing time, getting things from the server like text should be done here.
		 * There is nothing worse than a widget which has stuff percolating in at random.
		 */
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},  // ready


	function loaded(self) {
		// This function is called by the Athena setup.
		self.isloaded = true;
	},


	function show(self) {
		self.node.style.visibility = 'visible';
	},


	function hide(self) {
		self.node.style.visibility = 'hidden';
	},


	/** Generic ErrorBack 
	 *
	 * @param self is an instance of workspace.Workspace
	 * @param p_ewason(string) is an error message.
	 */
	function eb_genericErrback(self, p_reason) {
		var l_node = self.node;
		var l_nodeName = l_node.nodeName;
		var l_obj = l_node.attributes;
		Divmod.debug('---', 'helpers.js eb_genericErrback - ERROR - attachWidget failed\n\tReason = ' + p_reason);
		console.log("    GenericErrBck - Node: %O", l_node);
	},


	/**
	 * Do the things that a widget requests when it becomes ready.
	 * <This was originally embedded in attachWidget>
	 *
	 * @param p_widget is the widget being added/started.
	 * @param p_readyfunc is the optional function to be called when the widget is done loading (and initializing?)
	 */
	function widget_ready(self, p_widget, p_readyfunc) {
		// Default readyfunc that shows the widget.
		function isready() {
			p_widget.show();
		}
		// If we did not call with a readyfunc, add a dummy function that is ready
		if (!p_readyfunc)
			p_readyfunc = isready;
		function eb_widget_ready(p_reason) {  // widget.ready failed
			Divmod.debug('---', 'helpers.eb_widget_ready - ERROR - Reason = ' + p_reason);
			self.eb_genericErrback('widget.ready failed for: ' + p_widget.node.className + ' - ' + p_reason);
		}
		// console.log("helpers.widget_ready()  p_widget  %O", p_widget);
		var l_defer = p_widget.ready();
		l_defer.addCallback(p_readyfunc);
		l_defer.addErrback(eb_widget_ready);
	},

	function liveElementReceived(self, p_liveElement, p_readyfunc) {
		function cb_childAdded(widget) {
			self.node.appendChild(widget.node);
			self.widget_ready(widget, p_readyfunc);
		}
		function eb_add_child(p_reason) {  // addChildWidgetFromWidgetInfo failed
			Divmod.debug('---', 'helpers.eb_add_child - ERROR - Reason = ' + p_reason);
			console.log("helpers.eb_add_child()  p_reason:  %O", p_reason);
			console.log("helpers.eb_add_child()  p_readyfunc:  %O", p_readyfunc);
			console.log("helpers.eb_add_child()  p_live_element:  %O", p_liveElement);
			self.eb_genericErrback('Error: ' + p_reason + ' in addChildWidgetFromWidgetInfo failed ----');
		}
		var l_defer_2 = self.addChildWidgetFromWidgetInfo(p_liveElement);
		l_defer_2.addCallback(cb_childAdded);
		l_defer_2.addErrback(eb_add_child);
	},

	function attachWidget(self, p_name, p_params, p_readyfunc) {
		// Divmod.debug('---', 'helpers.attachWidget() - "' + p_name + '" is being attached to:' + self.node.className + ', with params:'+ p_params);
		function cb_call_remote(p_liveElement) {
			self.liveElementReceived(p_liveElement, p_readyfunc);
		}
		function eb_call_remote(p_reason) {
			Divmod.debug('---', 'helpers.eb_call_remote - ERROR - Reason = ' + p_reason);
			self.eb_genericErrback('Error: ' + p_reason + ' in callRemote failed for Name: ' + p_name);
		}
		var l_defer_1 = self.callRemote(p_name, p_params);
		l_defer_1.addCallback(cb_call_remote);
		l_defer_1.addErrback(eb_call_remote);
	},

	function detached(self) {
		Divmod.debug('---', self.node.className + ' object was detached cleanly.');
		self.node.parentNode.removeChild(self.node);
		helpers.Widget.upcall(self, 'detached');
	},


	// DBK Added all widget functions below this line ----------------

	function showWidget(self, p_className) {
		self.node.style.display = 'none';
		var l_widget = findWidgetByClass(p_className);
		l_widget.node.style.display = 'block';
		showSelectionButtons(l_widget);
		l_widget.startWidget();
	},
	function hideWidget(self) {
		self.node.style.display = 'none';
	},
	function startWidget(self) {
		self.node.style.display = 'block';
		showSelectionButtons(self);
		self.fetchDataFromServer();
	}
);


/**
 * Page not found widget
 */

helpers.Widget.subclass(helpers, 'FourOfour').methods(

	function ready(self) {
		function widgetready(res) {
			//do whatever init needs here
		}
		var uris = collectIMG_src(self.node, null);
		var d = loadImages(uris);
		d.addCallback(widgetready);
		return d;
	},

	function show(self) {
		//alert('this is a fourOfour Message');
	}
);
// console.log("helpers.handleDataOnClick()  json  %O", l_json);
// Divmod.debug('---', 'helpers.handleDataOnClick(Change) was called. JSON:' + l_json);
// END DBK
