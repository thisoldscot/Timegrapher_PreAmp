#!/usr/bin/env python
"""Generate TimegrapherPreamp.kicad_sch (KiCad 9) — through-hole piezo preamp.

MCP602 dual op-amp: A = non-inverting gain stage, B = unity buffer for the 2.5 V
virtual ground. Replaces the bench AD828. Drives a single AC signal into the
carrier HAT's J2 "Preamp" header (+5V / AUDIO_IN / GND).

Same toolchain/conventions as ../carrier/gen_sch.py:
  * net tags (global labels) or power ports dropped on each used pin endpoint
  * MCP602 lives in the local Preamp.kicad_sym (single-unit 8-pin symbol)
  * references are FIXED here and mirror gen_pcb.py 1:1 — do NOT re-annotate in
    KiCad; re-run this generator instead.

Run with the default Python (kiutils):  python gen_sch.py
"""
import os, uuid
from kiutils.schematic import Schematic
from kiutils.items.schitems import (SchematicSymbol, GlobalLabel, Position,
    SymbolProjectInstance, SymbolProjectPath, HierarchicalSheetInstance,
    NoConnect, Connection)
from kiutils.items.common import Property, Stroke, Effects
from kiutils.symbol import SymbolLib

HERE = os.path.dirname(os.path.abspath(__file__))
SYMDIR = r"C:/Program Files/KiCad/9.0/share/kicad/symbols"
PROJ = "TimegrapherPreamp"
OUT = os.path.join(HERE, "TimegrapherPreamp.kicad_sch")

sch = Schematic().create_new()
sch.version = "20230121"
sch.uuid = str(uuid.uuid4())
sch.paper.paperSize = "A4"

GRID = 1.27
def snap(v):
    return round(v / GRID) * GRID

POWER_SYM = {"+5V", "GND"}                       # drawn as power ports
FLAG_NETS = {"+5V", "+5VF", "GND", "VREF"}       # rails that need a PWR_FLAG

def _libfile(lib):
    return (HERE if lib == "Preamp" else SYMDIR) + "/" + lib + ".kicad_sym"

_libcache = {}
def get_pins(lib, name):
    key = lib + ":" + name
    if key not in _libcache:
        sl = SymbolLib.from_file(_libfile(lib))
        s = next(x for x in sl.symbols if x.entryName == name)
        s.libId = key; s.libraryNickname = lib; s.entryName = name
        if not any(getattr(x, "libId", None) == key for x in sch.libSymbols):
            sch.libSymbols.append(s)
        _libcache[key] = {p.number: (p.position.X, p.position.Y)
                          for u in s.units for p in u.pins}
    return _libcache[key]

def _wire(x1, y1, x2, y2):
    if (x1, y1) == (x2, y2):
        return
    c = Connection(type="wire",
                   points=[Position(snap(x1), snap(y1)),
                           Position(snap(x2), snap(y2))],
                   stroke=Stroke(width=0))
    c.uuid = str(uuid.uuid4())
    sch.graphicalItems.append(c)

_pwr_n = 0
def _add_symbol(lib, name, ref, value, fp, x, y, angle=0, in_bom=True):
    get_pins(lib, name)
    sym = SchematicSymbol()
    sym.libraryNickname = lib; sym.entryName = name; sym.libId = lib + ":" + name
    sym.position = Position(snap(x), snap(y), angle); sym.unit = 1
    sym.uuid = str(uuid.uuid4())
    sym.inBom = in_bom; sym.onBoard = True
    fp_prop = Property(key="Footprint", value=fp, id=2, position=Position(snap(x), snap(y), 0))
    fp_prop.effects = Effects(hide=True)
    sym.properties = [
        Property(key="Reference", value=ref, id=0, position=Position(snap(x) + 2.54, snap(y) - 5.08, 0)),
        Property(key="Value", value=value, id=1, position=Position(snap(x) + 2.54, snap(y) + 5.08, 0)),
        fp_prop,
    ]
    sym.instances = [SymbolProjectInstance(name=PROJ,
        paths=[SymbolProjectPath(sheetInstancePath="/", reference=ref, unit=1)])]
    sch.schematicSymbols.append(sym)
    return sym

def _net_tag(net, x, y, ang):
    global _pwr_n
    if net in POWER_SYM:
        _pwr_n += 1
        _add_symbol("power", net, "#PWR%02d" % _pwr_n, net, "",
                    x, y, angle=ang, in_bom=False)
    else:
        gl = GlobalLabel(text=net, position=Position(snap(x), snap(y), ang))
        gl.uuid = str(uuid.uuid4())
        sch.globalLabels.append(gl)

def _outward(px, py):
    if abs(px) >= abs(py):
        dx = -1 if px < 0 else 1
        return dx, 0, (180 if dx < 0 else 0)
    dy = -1 if py > 0 else 1
    return 0, dy, (90 if dy < 0 else 270)

def place(lib, name, ref, value, fp, x, y, netmap, nc_rest=False, angle=0):
    sym = _add_symbol(lib, name, ref, value, fp, x, y, angle)
    pins = get_pins(lib, name)
    for num, (px, py) in pins.items():
        sx, sy = snap(x + px), snap(y - py)
        if num in netmap:
            dx, dy, ang = _outward(px, py)
            _net_tag(netmap[num], sx, sy, ang)
        elif nc_rest:
            n = NoConnect(position=Position(sx, sy))
            n.uuid = str(uuid.uuid4())
            sch.noConnects.append(n)
    return sym

def pwr_flag(net, x, y):
    _add_symbol("power", "PWR_FLAG", "#FLG%02d" % (len(sch.schematicSymbols)),
                "PWR_FLAG", "", x, y, in_bom=False)
    _net_tag(net, x, y, 90)

FP = {
    "dip8":   "Package_DIP:DIP-8_W7.62mm",
    "rvert":  "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P2.54mm_Vertical",
    "do35":   "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal",
    "cdisc":  "Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm",
    "cp5":    "Capacitor_THT:CP_Radial_D5.0mm_P2.00mm",
    "cp63":   "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm",
    "hdr2":   "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical",
    "hdr3":   "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
}

# ---- U1: MCP602 (A = gain, B = VREF buffer) -------------------------------
place("Preamp", "MCP602", "U1", "MCP602-I/P", FP["dip8"], 150, 100, {
    "1": "AUDIO_OUT", "2": "FB", "3": "PZ", "4": "GND",
    "5": "VREF_DIV", "6": "VREF", "7": "VREF", "8": "+5VF"})

# ---- Power input + filter (J_OUT.1 +5V -> R_FILTER -> +5VF) ----------------
place("Connector_Generic", "Conn_01x03", "J_OUT", "Preamp", FP["hdr3"],
      60, 150, {"1": "+5V", "2": "AUDIO_OUT", "3": "GND"})
place("Device", "R", "R_FILTER", "10R",   FP["rvert"], 80, 60,  {"1": "+5V",  "2": "+5VF"})
place("Device", "C", "C_FILTER", "100uF", FP["cp63"],  100, 60, {"1": "+5VF", "2": "GND"})
place("Device", "C", "C_dec",    "100nF", FP["cdisc"], 175, 70, {"1": "+5VF", "2": "GND"})

# ---- Virtual ground: divider + U1-B buffer --------------------------------
place("Device", "R", "R3", "10k",   FP["rvert"], 110, 80,  {"1": "+5VF",     "2": "VREF_DIV"})
place("Device", "R", "R4", "10k",   FP["rvert"], 110, 115, {"1": "VREF_DIV", "2": "GND"})
place("Device", "C", "C3", "10uF",  FP["cp5"],   125, 115, {"1": "VREF_DIV", "2": "GND"})

# ---- Input network (high-Z PZ node, all referenced to VREF) ---------------
place("Device", "R", "R1", "4.7M",  FP["rvert"], 110, 145, {"1": "PZ", "2": "VREF"})
place("Device", "C", "C1", "100pF", FP["cdisc"], 125, 145, {"1": "PZ", "2": "VREF"})
place("Device", "D", "D1", "1N4148", FP["do35"], 95, 170,  {"1": "PZ", "2": "VREF"})
place("Device", "D", "D2", "1N4148", FP["do35"], 120, 170, {"1": "VREF", "2": "PZ"})
place("Connector_Generic", "Conn_01x02", "J_IN", "Piezo", FP["hdr2"],
      60, 145, {"1": "PZ", "2": "VREF"})

# ---- Gain network ----------------------------------------------------------
place("Device", "R", "R5", "100k", FP["rvert"], 150, 60,  {"1": "AUDIO_OUT", "2": "FB"})
place("Device", "R", "R6", "10k",  FP["rvert"], 150, 130, {"1": "FB",    "2": "GLEG"})
place("Device", "R", "R7", "1k",   FP["rvert"], 150, 150, {"1": "GLEG",  "2": "GLEGC"})
place("Device", "C", "C4", "100nF", FP["cdisc"], 150, 170, {"1": "GLEGC", "2": "GND"})

# ---- supply-rail PWR_FLAGs -------------------------------------------------
# +5V is fed in from the connector (an input), and +5VF/VREF are driven through
# passives/the buffer output, so each gets a flag to satisfy ERC.
pwr_flag("+5V",  60, 185)
pwr_flag("+5VF", 80, 45)
pwr_flag("VREF", 200, 145)
pwr_flag("GND",  60, 195)

if not sch.sheetInstances:
    sch.sheetInstances.append(HierarchicalSheetInstance(instancePath="/", page="1"))

sch.to_file(OUT)
print("wrote", OUT, "symbols:", len(sch.schematicSymbols),
      "labels:", len(sch.globalLabels), "no-connects:", len(sch.noConnects))
