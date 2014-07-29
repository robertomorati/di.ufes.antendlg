// KineticScrolling
// http://code.google.com/p/kineticscrolling/
// Copyright (c) 2010 Tatsuhiro Tsujikawa
// Released under the MIT License
var g = null;
function i() {
	this.a = g;
	this.b = [];
	this.i = this.h = this.j = this.l = this.f = this.c = g;
	this.d = new KineticScrollingOverlay_;
	this.g = 5.0E-5;
	this.m = 25
}
function l(a, b) {
	return Math.sqrt(b[0] * b[0] + b[1] * b[1])
}
function p(a, b, e, c, f, d, q, r) {
	function o(h) {
		var m = (new Date).getTime();
		if (!(m - h > 150)) {
			h = m - r;
			var j = h * h;
			h = b - c * j;
			j = f - q * j;
			var k = a.d.getProjection(), n = k.fromLatLngToDivPixel(a.a
					.getCenter());
			n.x += h * e;
			n.y += j * d;
			k = k.fromDivPixelToLatLng(n);
			if (h > 1 || j > 1) {
				a.a.setCenter(k);
				a.c = window.setTimeout(function() {
					o(m)
				}, a.m)
			}
		}
	}
	return o
}
function s(a) {
	return function() {
		a.c && window.clearTimeout(a.c);
		a.b = []
	}
}
function t(a) {
	return function() {
		if (!(a.b.length < 2)) {
			for ( var b = a.b[0].k, e = a.b[0].e, c = g, f = g, d = 1; d < a.b.length; ++d) {
				if (e - a.b[d].e > 200)
					break;
				c = a.b[d].k;
				f = a.b[d].e
			}
			if (c)
				if (e != f) {
					b = [ b.x - c.x, b.y - c.y ];
					d = l(a, b);
					if (d != 0) {
						c = [ 1, 0 ];
						c = Math.acos((b[0] * c[0] + b[1] * c[1])
								/ (l(a, b) * l(a, c)));
						e = Math.min(40, d / (e - f) * 30);
						f = Math.cos(c);
						c = Math.sin(c);
						d = (new Date).getTime();
						p(a, Math.abs(f) * e, b[0] >= 0 ? 1 : -1,
								Math.abs(f * a.g), Math.abs(c) * e,
								b[1] >= 0 ? 1 : -1, Math.abs(c * a.g), d)(d)
					}
				}
		}
	}
}
function u(a) {
	return function() {
		a.b.unshift({
			k : a.d.getProjection().fromLatLngToDivPixel(a.a.getCenter()),
			e : (new Date).getTime()
		});
		a.b.length > 100 && a.b.pop()
	}
}
i.prototype.setMap = function(a) {
	if (this.a != a) {
		var b = this, e = function() {
			b.c && window.clearTimeout(b.c)
		};
		if (this.a) {
			google.maps.event.removeListener(this.f);
			google.maps.event.removeListener(this.l);
			google.maps.event.removeListener(this.j);
			google.maps.event.removeListener(this.h);
			google.maps.event.removeListener(this.i);
			this.d.setMap(g);
			e()
		}
		if (this.a = a) {
			this.d.setMap(this.a);
			this.f = google.maps.event.addListener(this.a, "click", e);
			this.l = google.maps.event.addListener(this.a, "zoom_changed", e);
			this.j = google.maps.event
					.addListener(this.a, "dragstart", s(this));
			this.h = google.maps.event.addListener(this.a, "dragend", t(this));
			this.i = google.maps.event.addListener(this.a, "drag", u(this))
		}
	}
};
i.prototype.getMap = function() {
	return this.a
};
function KineticScrollingOverlay_() {
}
KineticScrollingOverlay_.prototype = new google.maps.OverlayView;
KineticScrollingOverlay_.prototype.onAdd = function() {
};
KineticScrollingOverlay_.prototype.draw = function() {
};
KineticScrollingOverlay_.prototype.onRemove = function() {
};
window.KineticScrolling = i;
i.prototype.getMap = i.prototype.getMap;
i.prototype.setMap = i.prototype.setMap;
window.KineticScrollingOverlay_ = KineticScrollingOverlay_;
KineticScrollingOverlay_.onAdd = KineticScrollingOverlay_.prototype.onAdd;
KineticScrollingOverlay_.draw = KineticScrollingOverlay_.prototype.draw;
KineticScrollingOverlay_.onRemove = KineticScrollingOverlay_.prototype.onRemove;