#!/usr/bin/env python
"""Generate TimegrapherPreamp.kicad_pcb — through-hole piezo preamp.

Run with KiCad's bundled python:
  "C:/Program Files/KiCad/9.0/bin/python.exe" gen_pcb.py

Valid KiCad 9 board with the full ratsnest. Placement is a sensible first pass on
a compact 2-layer outline; final placement/routing is finished in the PCB editor
(this mirrors ../carrier/gen_pcb.py). Net assignments mirror gen_sch.py 1:1.
"""
import os
import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
FPDIR = r"C:/Program Files/KiCad/9.0/share/kicad/footprints"
OUT = os.path.join(HERE, "TimegrapherPreamp.kicad_pcb")

MM = pcbnew.FromMM
def V(x, y):
    return pcbnew.VECTOR2I(MM(x), MM(y))

board = pcbnew.CreateEmptyBoard()

# ---- nets -----------------------------------------------------------------
_nets = {}
def net(name):
    if name not in _nets:
        n = pcbnew.NETINFO_ITEM(board, name)
        board.Add(n)
        _nets[name] = n
    return _nets[name]

for n in ["+5V", "+5VF", "GND", "VREF_DIV", "VREF", "PZ", "AUDIO_OUT",
          "FB", "GLEG", "GLEGC"]:
    net(n)

# ---- footprint helper -----------------------------------------------------
def add(lib, fp, ref, val, x, y, rot=0, back=False):
    """Place so the footprint bounding-box CENTER lands at (x, y) mm."""
    f = pcbnew.FootprintLoad(FPDIR + "/" + lib + ".pretty", fp)
    if f is None:
        raise RuntimeError("missing footprint %s:%s" % (lib, fp))
    f.SetReference(ref)
    f.SetValue(val)
    f.SetPosition(V(0, 0))
    if rot:
        f.SetOrientationDegrees(rot)
    board.Add(f)
    bb = f.GetBoundingBox(False, False)
    cx = (bb.GetLeft() + bb.GetRight()) // 2
    cy = (bb.GetTop() + bb.GetBottom()) // 2
    f.Move(pcbnew.VECTOR2I(MM(x) - cx, MM(y) - cy))
    if back:
        f.Flip(f.GetPosition(), False)
    return f

def wire(fp, mapping):
    for pad in fp.Pads():
        num = pad.GetNumber()
        if num in mapping:
            pad.SetNet(net(mapping[num]))

# ---- board outline: 36 x 28 mm --------------------------------------------
W, H = 36.0, 28.0

# ---- U1: MCP602 DIP-8 (centre) --------------------------------------------
u1 = add("Package_DIP", "DIP-8_W7.62mm", "U1", "MCP602-I/P", 18, 12)
wire(u1, {
    "1": "AUDIO_OUT", "2": "FB", "3": "PZ", "4": "GND",
    "5": "VREF_DIV", "6": "VREF", "7": "VREF", "8": "+5VF",
})

# ---- power input + filter -------------------------------------------------
RV = ("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P2.54mm_Vertical")
CD = ("Capacitor_THT", "C_Disc_D5.0mm_W2.5mm_P5.00mm")

jout = add("Connector_PinHeader_2.54mm", "PinHeader_1x03_P2.54mm_Vertical",
           "J_OUT", "Preamp", 33, 14, rot=90)
wire(jout, {"1": "+5V", "2": "AUDIO_OUT", "3": "GND"})
rf = add(RV[0], RV[1], "R_FILTER", "10R", 6, 4)
wire(rf, {"1": "+5V", "2": "+5VF"})
cf = add("Capacitor_THT", "CP_Radial_D6.3mm_P2.50mm", "C_FILTER", "100uF", 11, 5)
wire(cf, {"1": "+5VF", "2": "GND"})
cdec = add(CD[0], CD[1], "C_dec", "100nF", 26, 5)
wire(cdec, {"1": "+5VF", "2": "GND"})

# ---- virtual ground -------------------------------------------------------
r3 = add(RV[0], RV[1], "R3", "10k", 8, 9)
wire(r3, {"1": "+5VF", "2": "VREF_DIV"})
r4 = add(RV[0], RV[1], "R4", "10k", 8, 14)
wire(r4, {"1": "VREF_DIV", "2": "GND"})
c3 = add("Capacitor_THT", "CP_Radial_D5.0mm_P2.00mm", "C3", "10uF", 12, 12)
wire(c3, {"1": "VREF_DIV", "2": "GND"})

# ---- input network (keep PZ node tight) -----------------------------------
jin = add("Connector_PinHeader_2.54mm", "PinHeader_1x02_P2.54mm_Vertical",
          "J_IN", "Piezo", 3, 14, rot=90)
wire(jin, {"1": "PZ", "2": "VREF"})
r1 = add(RV[0], RV[1], "R1", "4.7M", 8, 20)
wire(r1, {"1": "PZ", "2": "VREF"})
c1 = add(CD[0], CD[1], "C1", "100pF", 12, 20)
wire(c1, {"1": "PZ", "2": "VREF"})
d1 = add("Diode_THT", "D_DO-35_SOD27_P7.62mm_Horizontal", "D1", "1N4148", 18, 22)
wire(d1, {"1": "PZ", "2": "VREF"})
d2 = add("Diode_THT", "D_DO-35_SOD27_P7.62mm_Horizontal", "D2", "1N4148", 18, 25)
wire(d2, {"1": "VREF", "2": "PZ"})

# ---- gain network ---------------------------------------------------------
r5 = add(RV[0], RV[1], "R5", "100k", 18, 4)
wire(r5, {"1": "AUDIO_OUT", "2": "FB"})
r6 = add(RV[0], RV[1], "R6", "10k", 27, 12)
wire(r6, {"1": "FB", "2": "GLEG"})
r7 = add(RV[0], RV[1], "R7", "1k", 27, 17)
wire(r7, {"1": "GLEG", "2": "GLEGC"})
c4 = add(CD[0], CD[1], "C4", "100nF", 27, 22)
wire(c4, {"1": "GLEGC", "2": "GND"})

# ---- mounting holes (2x M2.5) ---------------------------------------------
for ref, (x, y) in {"H1": (3, 3), "H2": (W - 3, 3)}.items():
    add("MountingHole", "MountingHole_2.7mm_M2.5", ref, "M2.5", x, y)

# ---- board outline (Edge.Cuts) --------------------------------------------
pts = [(0, 0), (W, 0), (W, H), (0, H), (0, 0)]
for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
    seg = pcbnew.PCB_SHAPE(board)
    seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
    seg.SetStart(V(x1, y1))
    seg.SetEnd(V(x2, y2))
    seg.SetLayer(pcbnew.Edge_Cuts)
    seg.SetWidth(MM(0.15))
    board.Add(seg)

# ---- GND pour both layers + stitching vias (quiet ground, as on carrier) --
for layer in (pcbnew.F_Cu, pcbnew.B_Cu):
    z = pcbnew.ZONE(board)
    z.SetLayer(layer)
    z.SetNet(net("GND"))
    z.SetLocalClearance(MM(0.25))
    z.SetMinThickness(MM(0.25))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    z.SetThermalReliefGap(MM(0.3))
    z.SetThermalReliefSpokeWidth(MM(0.4))
    poly = z.Outline()
    poly.NewOutline()
    for (x, y) in [(0.5, 0.5), (W - 0.5, 0.5), (W - 0.5, H - 0.5), (0.5, H - 0.5)]:
        poly.Append(MM(x), MM(y))
    board.Add(z)

def _gnd_via(x, y):
    v = pcbnew.PCB_VIA(board)
    v.SetPosition(V(x, y))
    v.SetDrill(MM(0.3))
    v.SetWidth(MM(0.6))
    v.SetNet(net("GND"))
    v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
    board.Add(v)

_boxes = []
for f in board.GetFootprints():
    bb = f.GetBoundingBox(False, False)
    _boxes.append((pcbnew.ToMM(bb.GetLeft()) - 0.8, pcbnew.ToMM(bb.GetTop()) - 0.8,
                   pcbnew.ToMM(bb.GetRight()) + 0.8, pcbnew.ToMM(bb.GetBottom()) + 0.8))
def _clear(x, y):
    if x < 1.2 or y < 1.2 or x > W - 1.2 or y > H - 1.2:
        return False
    return not any(l <= x <= r and t <= y <= b for (l, t, r, b) in _boxes)

_nvia = 0
yy = 4.0
while yy < H - 1.2:
    xx = 4.0
    while xx < W - 1.2:
        if _clear(xx, yy):
            _gnd_via(xx, yy)
            _nvia += 1
        xx += 6.0
    yy += 6.0

# Zones left UNFILLED (headless ZONE_FILLER segfaults in this build); KiCad
# refills on plot, and "Fill All Zones" (B) renders them in the editor.
pcbnew.SaveBoard(OUT, board)
print("wrote", OUT)
print("footprints:", len(board.GetFootprints()), " nets:", len(_nets),
      " stitching vias:", _nvia)
