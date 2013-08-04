// helpers.js

// import Nevow.Athena
Nevow.Athena.Widget.subclass(helpers, "Widget").methods(
		function __init__(_1, _2) {
			helpers.Widget.upcall(_1, "__init__", _2);
		},
		function ready(_3) {
			function widgetready(_4) {
			}
			var _5 = collectIMG_src(_3.node, null);
			var d = loadImages(_5);
			d.addCallback(widgetready);
			return d;
		},
		function loaded(_7) {
			_7.isloaded = true;
		},
		function show(_8) {
			_8.node.style.visibility = "visible";
		},
		function hide(_9) {
			_9.node.style.visibility = "hidden";
		},
		function genericErrback(_a, _b) {
			alert("widget injection failed - " + _b);
		},
		function attachWidget(_c, _d, _e, _f) {
			var d1 = _c.callRemote(_d, _e);
			d1.addCallback(function liveElementReceived(le) {
				var d2 = _c.addChildWidgetFromWidgetInfo(le);
				d2.addCallback(function childAdded(_13) {
					_c.node.appendChild(_13.node);
					var d3 = _13.ready();
					function isready() {
						_13.show();
					}
					if (!_f) {
						_f = isready;
					}
					d3.addCallback(_f);
					d3.addErrback(function(res) {
						_c.genericErrback(res);
					});
				});
				d2.addErrback(function(res) {
					_c.genericErrback(res);
				});
			});
			d1.addErrback(function(res) {
				_c.genericErrback(res);
			});
		},
		function detached(_18) {
			Divmod.debug("---", _18.node.className
					+ " object was detached cleanly");
			_18.node.parentNode.removeChild(_18.node);
			common.helpers.Widget.upcall(_18, "detached");
		});
helpers.Widget.subclass(helpers, "FourOfour")
		.methods(function ready(_19) {
			function widgetready(res) {
			}
			var _1b = collectIMG_src(_19.node, null);
			var d = loadImages(_1b);
			d.addCallback(widgetready);
			return d;
		}, function show(_1d) {
			alert("this is a fourOfour Message");
		});

// END DBK
