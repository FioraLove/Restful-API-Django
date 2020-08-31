window = this;
h = "substring";
i = "split";
j = "replace";
k = "substr";
getHex = function (a) {
    return {
        str: a[h](4),
        hex: a[h](0, 4)[i]("").reverse().join("")
    }
};
getDec = function (a) {
    var b = parseInt(a, 16).toString();
    return {
        pre: b[h](0, 2)[i](""),
        tail: b[h](2)[i]("")
    }
};
substr = function (a, b) {
    var c = a[h](0, b[0]),
        d = a[k](b[0], b[1]);
    return c + a[h](b[0])[j](d, "")
};
getPos = function (a, b) {
    return b[0] = a.length - b[0] - b[1], b
};

var d = "undefined" != typeof b ? b : window,
    e = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
    f = function () {
        try {
            document.createElement("$")
        } catch (a) {
            return a
        }
    }();
d.btoa || (d.btoa = function (a) {
    for (var b, c, d = 0, g = e, h = ""; a.charAt(0 | d) || (g = "=", d % 1); h += g.charAt(63 & b >> 8 - d % 1 * 8)) {
        if (c = a.charCodeAt(d += .75), c > 255) throw f;
        b = b << 8 | c
    }
    return h
}),
    d.base64encode = d.btoa,
d.atob || (d.atob = function (a) {
    if (a = a.replace(/=+$/, ""), a.length % 4 == 1) throw f;
    for (var b, c, d = 0,
             g = 0,
             h = ""; c = a.charAt(g++); ~c && (b = d % 4 ? 64 * b + c : c, d++ % 4) ? h += String.fromCharCode(255 & b >> (-2 * d & 6)) : 0) c = e.indexOf(c);
    return h
}),
    d.base64decode = d.atob;

function getmp4(a) {
    var b = this.getHex(a), c = this.getDec(b.hex), d = this[k](b.str, c.pre);
    return atob(this[k](d, this.getPos(d, c.tail)))
}