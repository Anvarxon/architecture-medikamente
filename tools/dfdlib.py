import zlib

CW, CH = 380, 210
NW, NH = 260, 110
X0, Y0 = 40, 150

STYLES = {
    "entity":   "rounded=0;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=11;verticalAlign=middle;",
    "process":  "rounded=1;arcSize=30;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;",
    "store":    "shape=partialRectangle;top=1;bottom=1;left=0;right=0;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;align=center;",
    "extsys":   "rounded=0;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=11;",
    "control":  "rounded=1;arcSize=30;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=11;dashed=1;",
    "note":     "shape=note;size=16;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=11;align=left;verticalAlign=top;spacing=8;",
    "risk":     "shape=note;size=16;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;fontSize=11;align=left;verticalAlign=top;spacing=8;",
    "good":     "shape=note;size=16;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;align=left;verticalAlign=top;spacing=8;",
    "legend":   "shape=note;size=16;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontSize=11;align=left;verticalAlign=top;spacing=8;",
    "title":    "text;html=1;fontSize=20;fontStyle=1;align=left;verticalAlign=middle;",
    "sub":      "text;html=1;fontSize=12;align=left;verticalAlign=middle;fontColor=#555555;",
    "person":   "rounded=1;arcSize=20;whiteSpace=wrap;html=1;fillColor=#08427B;strokeColor=#073B6F;fontColor=#ffffff;fontSize=11;",
    "personext":"rounded=1;arcSize=20;whiteSpace=wrap;html=1;fillColor=#686868;strokeColor=#4D4D4D;fontColor=#ffffff;fontSize=11;",
    "system":   "rounded=0;whiteSpace=wrap;html=1;fillColor=#1168BD;strokeColor=#0B4884;fontColor=#ffffff;fontSize=11;",
    "sysfocus": "rounded=0;whiteSpace=wrap;html=1;fillColor=#0B4884;strokeColor=#062F55;fontColor=#ffffff;fontSize=12;",
    "syssec":   "rounded=0;whiteSpace=wrap;html=1;fillColor=#7B1FA2;strokeColor=#4A148C;fontColor=#ffffff;fontSize=11;",
    "sysdata":  "rounded=0;whiteSpace=wrap;html=1;fillColor=#2E7D32;strokeColor=#1B5E20;fontColor=#ffffff;fontSize=11;",
    "sysext":   "rounded=0;whiteSpace=wrap;html=1;fillColor=#8C8C8C;strokeColor=#5F5F5F;fontColor=#ffffff;fontSize=11;",
    "container":"rounded=0;whiteSpace=wrap;html=1;fillColor=#438DD5;strokeColor=#2E6295;fontColor=#ffffff;fontSize=11;",
    "cnt_sec":  "rounded=0;whiteSpace=wrap;html=1;fillColor=#9C27B0;strokeColor=#6A1B9A;fontColor=#ffffff;fontSize=11;",
    "cnt_data": "rounded=0;whiteSpace=wrap;html=1;fillColor=#43A047;strokeColor=#2E7D32;fontColor=#ffffff;fontSize=11;",
    "db":       "shape=cylinder3;boundedLbl=1;backgroundOutline=1;size=12;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontSize=11;",
    "queue":    "shape=parallelogram;perimeter=parallelogramPerimeter;fixedSize=1;size=20;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=11;",
}

BOUNDARY = ("rounded=1;dashed=1;dashPattern=8 4;fillColor=none;strokeColor={c};fontColor={c};"
            "verticalAlign=top;align=left;spacing=12;fontSize=13;fontStyle=1;html=1;")

EDGE = ("edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;jumpStyle=arc;fontSize=10;"
        "labelBackgroundColor=#FFFFFF;strokeColor={c};endArrow=blockThin;endFill=1;")


def esc(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    return t.replace("\n", "&lt;br&gt;")


def cell(col, row):
    return X0 + col * CW, Y0 + row * CH


class Page:
    def __init__(self, name, title=None, subtitle=None, subtitle2=None):
        self.name = name
        self.items = []
        self.geo = {}
        self._n = 0
        if title:
            self.free("t_title", "title", title, X0, 6, 1600, 30)
        if subtitle:
            self.free("t_sub", "sub", subtitle, X0, 36, 1600, 20)
        if subtitle2:
            self.free("t_sub2", "sub", subtitle2, X0, 56, 1600, 20)

    def boundary(self, nid, label, c0, r0, c1, r1, color="#B85450", pad=26):
        x, y = cell(c0, r0)
        x1, y1 = cell(c1, r1)
        w = (x1 + NW) - x + 2 * pad
        h = (y1 + NH) - y + 2 * pad
        self.items.insert(0, '<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
                             '<mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry"/></mxCell>'
                          % (nid, esc(label), BOUNDARY.format(c=color), x - pad, y - pad - 14, w, h + 14))

    def node(self, nid, kind, label, col, row, w=NW, h=NH, dx=0, dy=0):
        x, y = cell(col, row)
        self.free(nid, kind, label, x + dx, y + dy, w, h)

    def free(self, nid, kind, label, x, y, w, h):
        self.geo[nid] = (x, y, w, h)
        self.items.append('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
                          '<mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry"/></mxCell>'
                          % (nid, esc(label), STYLES[kind], x, y, w, h))

    def edge(self, src, dst, label="", color="#1F6FB2", dashed=False,
             so=0.0, to=0.0, lx=0, ly=0, force=None, waypoints=None, an=None):
        assert src in self.geo, "нет узла " + src
        assert dst in self.geo, "нет узла " + dst
        x1, y1, w1, h1 = self.geo[src]
        x2, y2, w2, h2 = self.geo[dst]
        ddx = (x2 + w2 / 2.0) - (x1 + w1 / 2.0)
        ddy = (y2 + h2 / 2.0) - (y1 + h1 / 2.0)
        horiz = abs(ddx) >= abs(ddy) if force is None else (force == "h")
        o1, o2 = 0.5 + so * 0.3, 0.5 + to * 0.3
        if horiz:
            ex, ey, tx, ty = (1, o1, 0, o2) if ddx > 0 else (0, o1, 1, o2)
        else:
            ex, ey, tx, ty = (o1, 1, o2, 0) if ddy > 0 else (o1, 0, o2, 1)
        if an is not None:
            ex, ey, tx, ty = an
        self._n += 1
        st = (EDGE.format(c=color) +
              "exitX=%s;exitY=%s;exitDx=0;exitDy=0;entryX=%s;entryY=%s;entryDx=0;entryDy=0;" % (ex, ey, tx, ty))
        if dashed:
            st += "dashed=1;"
        geo = '<mxGeometry relative="1" as="geometry">'
        if waypoints:
            geo += '<Array as="points">' + "".join(
                '<mxPoint x="%d" y="%d"/>' % (px, py) for px, py in waypoints) + "</Array>"
        if lx or ly:
            geo += '<mxPoint as="offset" x="%d" y="%d"/>' % (lx, ly)
        geo += "</mxGeometry>"
        self.items.append('<mxCell id="e_%s_%d" value="%s" style="%s" edge="1" parent="1" source="%s" target="%s">%s</mxCell>'
                          % (src, self._n, esc(label), st, src, dst, geo))

    def flow(self, src, dst, label="", **kw):
        self.edge(src, dst, label, color="#1F6FB2", **kw)

    def risk_edge(self, src, dst, label="", **kw):
        self.edge(src, dst, label, color="#B85450", **kw)

    def ctl_edge(self, src, dst, label="", **kw):
        self.edge(src, dst, label, color="#7B1FA2", dashed=True, **kw)

    def xml(self):
        return ('  <diagram name="%s" id="d%s">\n'
                '    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
                'arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">\n'
                '      <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n        %s\n'
                '      </root>\n    </mxGraphModel>\n  </diagram>\n'
                % (self.name.replace("&", "&amp;"), zlib.crc32(self.name.encode()),
                   "\n        ".join(self.items)))


def write(path, pages):
    body = "".join(p.xml() for p in pages)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<mxfile host="app.diagrams.net" version="24.0.0" type="device">\n%s</mxfile>\n' % body)
    with open(path, "w", encoding="utf-8") as f:
        f.write(xml)
    print("written", path, len(xml))
