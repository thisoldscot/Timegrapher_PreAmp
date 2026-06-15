# Timegrapher Piezo Pre-Amplifier — DESIGN

Compact **through-hole** piezo pre-amplifier that replaces the bench AD828. It
sits **at the pickup** and drives a single AC audio signal down a short shielded
3-wire lead into the carrier HAT's `J2` "Preamp" header (**+5V / AUDIO_IN / GND**,
see `../carrier/gen_pcb.py`). The carrier already AC-couples and re-biases
`AUDIO_IN` into the PCM1808 (`C_in_l` 1 µF + `R_bl` 22 k → VREF1), so this board's
job is simply: **piezo → bias → amplify → single-ended AC out.**

Built from parts on hand (MCP602-I/P DIP-8, axial 1/4 W metal-film resistors,
1N4148 diodes, disc/film/electrolytic caps). Generated the same way as the
carrier: `gen_sch.py` (kiutils) + `gen_pcb.py` (pcbnew), with `Preamp.kicad_sym`
for the op-amp symbol. **Run the generators with KiCad CLOSED.**

> Replaces the "Piezo preamp board (AD828)" off-board line in `../carrier/BOM.md`.

---

## 1. Why MCP602

The AD828 is a bipolar-input part; its input bias/current noise into the piezo's
high source impedance was a real contributor to the bench noise floor. The
**MCP602** is a CMOS rail-to-rail op-amp (~1 pA input bias current, single 5 V),
which suits the high-Z piezo far better and runs happily on the carrier's 5 V
rail. Both halves of the dual are used (see §3).

## 2. Signal chain

```
 piezo ─┬─ R1 4.7M ─┐            MCP602-A (gain ~10x, HP-shaped)
        ├─ C1 100pF ┤ all to     +IN(3)┌────────┐OUT(1) ── AUDIO_OUT ── J_OUT.2
        ├─ D1 ▷|────┤ VREF        ──────┤        ├──────────────┬──────────────
        └─ D2 |◁────┘ (2.5V)      -IN(2)└────────┘              │
                                   │                            R5 100k (feedback)
                                   └────── R6 10k ── R7 1k ── C4 100nF ── GND
                                          (gain-set leg, AC-grounded via C4)

 VREF buffer (MCP602-B):  +5VF ─ R3 10k ─┬─ R4 10k ─ GND
                                         ├─ C3 10µF ─ GND
                                    VREF_DIV ─ +IN(5) ┌──┐ OUT(7) ─ VREF
                                                 -IN(6)┴──┘   (unity buffer)
 Power:  J_OUT.1 +5V ─ R_FILTER 10Ω ─┬─ +5VF (op-amp VDD pin 8, divider)
                                     ├─ C_FILTER 100µF ─ GND
                                     └─ C_dec 100nF ─ GND
```

## 3. Improvements over the source design doc (approved)

1. **Active virtual ground (uses the 2nd op-amp).** The source design left
   op-amp B (pins 5/6/7) floating — bad practice for CMOS (drift/oscillation) and
   a wasted half. Here **U1-B is a unity-gain buffer** driving the 2.5 V `VREF`
   from the R3/R4 divider. This gives a **low-impedance, quiet bias rail** for the
   high-Z input network and the diode clamps → better hum/PSRR. Same part count.
2. **High-pass corner corrected & tuned.** The doc claimed "7.2 Hz"; with R6+R7
   (11 k) and the original 22 nF the AC-gain corner is actually **~660 Hz**. We
   set **C4 = 100 nF → ~145 Hz**. Below the corner gain is ×1, above it ×~10, so
   the stage gives ~×10 to the tick's transient while leaving 50/60 Hz mains hum
   at unity — i.e. an **~10× tick-to-hum improvement at the output** (the bench
   noise floor was largely mains pickup on the high-Z node). 100 nF (vs 22 nF)
   lowers the corner so more of the tick's body is amplified.
3. **Added VDD decoupling (`C_dec` 100 nF).** The source schematic had none; a
   ceramic right at pin 8 is standard and cheap.
4. **Gain kept tunable.** `R5` (100 k) is the single gain knob. With the new
   pin-coupled flexing pickup the signal is far larger than the loose-disc AD828
   setup, so ×10 is a sane start; raise `R5` (e.g. 220 k → ×21) if ticks are weak.

## 4. Net list (pad → net) — authoritative, mirrors `gen_sch.py`/`gen_pcb.py`

| Ref | Value | Pad → net |
|---|---|---|
| **U1** | MCP602-I/P | 1 `AUDIO_OUT`, 2 `FB`, 3 `PZ`, 4 `GND`, 5 `VREF_DIV`, 6 `VREF`, 7 `VREF`, 8 `+5VF` |
| R_FILTER | 10 Ω | 1 `+5V`, 2 `+5VF` |
| C_FILTER | 100 µF | 1 `+5VF`, 2 `GND` |
| C_dec | 100 nF | 1 `+5VF`, 2 `GND` |
| R3 | 10 k | 1 `+5VF`, 2 `VREF_DIV` |
| R4 | 10 k | 1 `VREF_DIV`, 2 `GND` |
| C3 | 10 µF | 1 `VREF_DIV`, 2 `GND` |
| R1 | 4.7 M | 1 `PZ`, 2 `VREF` |
| C1 | 100 pF | 1 `PZ`, 2 `VREF` |
| D1 | 1N4148 | 1 `PZ`, 2 `VREF` |
| D2 | 1N4148 | 1 `VREF`, 2 `PZ` |
| R5 | 100 k | 1 `AUDIO_OUT`, 2 `FB` |
| R6 | 10 k | 1 `FB`, 2 `GLEG` |
| R7 | 1 k | 1 `GLEG`, 2 `GLEGC` |
| C4 | 100 nF | 1 `GLEGC`, 2 `GND` |
| J_IN | piezo (2-pin) | 1 `PZ`, 2 `VREF` |
| J_OUT | to carrier (3-pin) | 1 `+5V`, 2 `AUDIO_OUT`, 3 `GND` |

`D1`/`D2` are an anti-parallel clamp: they limit the `PZ` node to ≈ ±0.6 V around
`VREF`, protecting the CMOS inputs (and the ADC) from piezo spikes without
clipping normal small ticks.

## 5. Component values & rationale

- **R1 4.7 M** — input bias to `VREF` and, with the piezo's ~15 nF native
  capacitance, sets the **input high-pass ≈ 2 Hz** (keeps the tick's body).
- **C1 100 pF (NP0)** — small RF/EMI shunt across the input. (It does *not* form a
  meaningful LPF against the piezo's much larger capacitance — the source doc's
  rationale was off — but it's a harmless, worthwhile RF bleed.)
- **R3/R4 10 k + C3 10 µF** — 2.5 V divider, buffered by U1-B.
- **R5 100 k / (R6 10 k + R7 1 k)** — non-inverting gain ≈ 1 + 100k/11k ≈ **10.1×**.
- **C4 100 nF** — DC-blocks the gain leg (DC gain = 1, output parks at `VREF`) and
  sets the **~145 Hz** AC-gain corner with R6+R7.
- **R_FILTER 10 Ω + C_FILTER 100 µF** — RC filter (~160 Hz) cleaning the incoming
  5 V; the op-amp draws ~hundreds of µA so the 10 Ω drop is negligible.
- **C_dec 100 nF** — local VDD bypass at pin 8.

## 6. Output coupling

`AUDIO_OUT` is taken **directly** from OUT-A (parked at 2.5 V DC). The carrier's
`C_in_l` (1 µF) blocks that DC and its `R_bl` re-biases into the ADC, so no output
cap is needed for the carrier. The load the op-amp actually sees is a **series**
cap into 22 k (not a shunt cap), so there's no capacitive-load stability concern
and no series isolation resistor is required.

> **Standalone PCM1808-module bench use:** if you drive a bare PCM1808 module
> input that is *not* already AC-coupled, add a 1 µF series cap from `AUDIO_OUT`
> to the module's LIN. Most modules already couple, so usually unnecessary.

## 7. Board / layout plan

- 2-layer, **~32 × 24 mm** target, GND pour both sides + stitching vias (same
  approach as the carrier).
- **U1** central (DIP-8, socket optional/recommended). Axial resistors mounted
  **vertically** (`P2.54mm_Vertical`) to keep the footprint tight.
- **J_IN** (2-pin) on one short edge nearest the piezo; **J_OUT** (3-pin) on the
  opposite edge toward the carrier lead.
- Keep the **`PZ` / +IN node tiny** and surround it with the GND/VREF pour — it's
  the high-impedance antenna node; short traces here matter most for hum.
- Two M2.5 mounting holes.

## 8. Connectors

Default to 0.1″ pin headers (2-pin in, 3-pin out) for easy hand assembly. To mate
the carrier's JST-PH lead directly, swap `J_OUT` to a through-hole JST-PH 3-pin
(`B3B-PH-K-S`) — pinout **1=+5V, 2=AUDIO_IN(=AUDIO_OUT), 3=GND** matches the
carrier's `J2`.

## 9. Bring-up (multimeter, before connecting the ADC)

1. **Supply:** pin 8 → pin 4 reads ~5 V (after the 10 Ω, expect ~4.9–5.0 V).
2. **Bias:** `VREF_DIV` and `VREF` both ≈ 2.5 V; `VREF` (buffered) should track
   the divider closely and stiffly.
3. **Output offset:** OUT-A (pin 1) ≈ 2.5 V at rest. 0 V or 5 V ⇒ a feedback/short
   fault.
4. **Signal:** flick the piezo — scope/`AUDIO_DIAG` should show a large transient.
   With the firmware diagnostic, expect `env/nf` well past threshold on a tick
   once the pickup is pin-coupled.

## 10. Generate

```
# schematic (default Python + kiutils)
python gen_sch.py
# board (KiCad's bundled Python)
"C:/Program Files/KiCad/9.0/bin/python.exe" gen_pcb.py
```

Then open in KiCad (was CLOSED during generation), **Edit → Fill All Zones (B)**,
finish placement/routing, run DRC/ERC, and plot. Do **not** re-annotate in KiCad
(refs are fixed in the generators to keep sch/pcb/BOM in sync) — re-run the
generator instead.
