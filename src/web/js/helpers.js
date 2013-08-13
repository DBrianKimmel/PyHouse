// helpers.js

// import Nevow.Athena

/*
 * This basic widget can attach subwidgets and provides some other basic functionality.
 * Special attention should be paid to the function ready which should be overridden in almost every case,
 *  working with the widgetready function in a closure.
 * widgetready could of call another method func in the class but practice shows, that the point of being informed that
 *  we're setup properly for action is way to important to delegate it into superclass.
 * Think of ready as a stub, which is more like a template to start work on your own widgets implementation.
 */

Nevow.Athena.Widget.subclass(helpers, 'Widget').methods(
		
	function __init__(self, node) {
		helpers.Widget.upcall(self, '__init__', node);
	},

	function ready(self) {

		function widgetready(res) {
		  //do whatever init needs here
		}

		//pre action tasks needing time, getting things from the server like texts
		//should be done here. There is nothing worse as a widget which has stuff
		//percolating in at random.
		    var uris = collectIMG_src(self.node, null);
		    var d = loadImages(uris);
		    d.addCallback(widgetready);
		    return d;
		  },

	  function loaded(self) { //this func called by the athena setup
	    self.isloaded = true;
	  },

  function show(self) {
    self.node.style.visibility = 'visible';
  },

  function hide(self) {
    self.node.style.visibility = 'hidden';
  },

  function genericErrback(self, res) {
	    alert('widget injection failed - ' + res);
	  },
	  
	  function attachWidget(self, name, params, readyfunc) {
	    var d1 = self.callRemote(name, params);
	    d1.addCallback(function liveElementReceived(le) {
	      var d2 = self.addChildWidgetFromWidgetInfo(le);
	      d2.addCallback(function childAdded(widget) {
	        self.node.appendChild(widget.node);
	        var d3 = widget.ready();
	        function isready() {
	          widget.show();
	        }
	        if (!readyfunc)
	          readyfunc = isready;
	        d3.addCallback(readyfunc);
	        d3.addErrback(function(res) {
	          self.genericErrback(res);
	        });
	      });
	      d2.addErrback(function(res) {
	        self.genericErrback(res);
	      });
	    });
	    d1.addErrback(function(res) {
	      self.genericErrback(res);
	    });
	  },
	  
	  function detached(self) {
	    Divmod.debug('---', self.node.className + ' object was detached cleanly');
	    self.node.parentNode.removeChild(self.node);
	    common.helpers.Widget.upcall(self, 'detached');
	  }
	);


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
		    alert('this is a fourOfour Message');
		  }
		);

// END DBK
