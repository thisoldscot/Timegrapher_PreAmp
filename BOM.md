# BOM — Timegrapher Piezo Pre-Amplifier (through-hole, hand-assembled)

Compact 2-layer THT board built from parts on hand. Values follow `DESIGN.md`.
Resistors are 1/4 W metal-film, mounted **vertically** (`P2.54mm_Vertical`) to
save area. No LCSC/PCBA fields — this board is hand-soldered, not fab-assembled.

| Ref | Qty | Value | Footprint | Notes |
|---|---|---|---|---|
| U1 | 1 | **MCP602-I/P** dual CMOS op-amp | `Package_DIP:DIP-8_W7.62mm` | A = gain stage, B = VREF buffer. Use a DIP-8 socket to avoid soldering heat into the part |
| SOCKET1 | 1 | DIP-8 socket (optional) | (same holes as U1) | recommended; not a separate footprint |
| R1 | 1 | 4.7 MΩ 1% | `Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P2.54mm_Vertical` | high-Z input bias → VREF; sets ~2 Hz input HP with the piezo cap |
| R3 | 1 | 10 kΩ 1% | `…P2.54mm_Vertical` | VREF divider top |
| R4 | 1 | 10 kΩ 1% | `…P2.54mm_Vertical` | VREF divider bottom |
| R5 | 1 | 100 kΩ 1% | `…P2.54mm_Vertical` | **gain knob** (feedback). 220 k → ×21 if ticks weak |
| R6 | 1 | 10 kΩ 1% | `…P2.54mm_Vertical` | gain-set leg |
| R7 | 1 | 1 kΩ 1% | `…P2.54mm_Vertical` | gain-leg series / HP shaping |
| R_FILTER | 1 | 10 Ω | `…P2.54mm_Vertical` | 5 V RC supply filter |
| D1, D2 | 2 | **1N4148** | `Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal` | anti-parallel input clamp to VREF |
| C1 | 1 | 100 pF NP0/C0G | `Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm` | input RF shunt |
| C4 | 1 | **100 nF** film/X7R | `Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm` | gain-leg DC block; ~145 Hz HP corner (was 22 nF/660 Hz in the source doc) |
| C_dec | 1 | 100 nF ceramic | `Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm` | VDD decoupling at pin 8 |
| C3 | 1 | 10 µF electrolytic | `Capacitor_THT:CP_Radial_D5.0mm_P2.00mm` | VREF divider decouple |
| C_FILTER | 1 | 100 µF electrolytic | `Capacitor_THT:CP_Radial_D6.3mm_P2.50mm` | 5 V bulk |
| J_IN | 1 | 2-pin header | `Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical` | piezo: 1=PZ, 2=VREF (shield) |
| J_OUT | 1 | 3-pin header | `Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical` | to carrier J2: 1=+5V, 2=AUDIO_IN, 3=GND |
| H1, H2 | 2 | M2.5 mounting hole | `MountingHole:MountingHole_2.7mm_M2.5` | no symbol (DRC "extra footprint" expected) |

## Notes
- **C4 changed to 100 nF** (from the source doc's 22 nF) to put the high-pass at
  ~145 Hz — see `DESIGN.md §3`. If you only have 22 nF, the board still works
  (corner ~660 Hz, a touch more low-end roll-off).
- Swap `J_OUT` to a THT **JST-PH 3-pin** (`Connector_JST:JST_PH_B3B-PH-K_1x03_P2.00mm_Vertical`)
  to mate the carrier's JST-PH lead directly.
- Footprint names are stock KiCad 9 libs; if `gen_pcb.py` reports a missing
  footprint, adjust the name to the one present in your install.

## Off-board
| Item | Notes |
|---|---|
| 27 mm piezo disc + centre pin/stud pickup | rim-supported, ceramic-down, brass-up — see chat notes |
| Short shielded 2-conductor lead | piezo → J_IN (signal + shield→VREF) |
| Short shielded 3-conductor lead | J_OUT → carrier J2 (+5V / signal / GND) |
