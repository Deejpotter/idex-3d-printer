# Design notes

Engineering findings for the IDEX printer, in the order they were established.
Figures that have been checked are stated plainly; figures that have not are
marked. Several earlier conclusions in this project turned out to be wrong and
the corrections are kept here rather than quietly deleted.

## 1. What actually limits the speed

Stiffnesses in series: the floppiest link sets the answer.

```
1/k_total = 1/k_belt + 1/k_mount + 1/k_gantry
f = (1/2pi) * sqrt(k/m)
accel [mm/s2] ~= f^2 * 2.21
```

| Link | Stiffness | Note |
|---|---|---|
| GT2 6 mm belt, both spans | 513 kN/m | |
| Toolhead on ONE MGN12H block | 141 kN/m | the limiting link on the original design |
| Toolhead on TWO MGN12H blocks | 282 kN/m | |
| 2040 gantry beam at 480 mm | 478 kN/m | scales as 1/L^3 |
| 2040 gantry beam at 520 mm | 376 kN/m | the cost of longer carriages |

Result:

| Machine | Moving mass | f | Accel |
|---|---|---|---|
| Original: 1 block, 1.42 kg toolhead | 1.42 kg | 40.0 Hz | 3,541 mm/s² |
| This design: 2 blocks, 518 g toolhead | 0.518 kg | 77.5 Hz | 13,259 mm/s² |
| Y axis (the bed) | 1.83 kg | 41.6 Hz | **3,823 mm/s²** |

**The bed is now the slowest axis.** `max_accel` in `printer.cfg` is set to 3,800
for that reason. Raising it means stiffening the bed, not the gantry.

Motor torque is not the constraint: an LDO 42STH48-2504AC at 0.45 N·m holding,
derated to 60% at speed, pushes about 42 N through a 20-tooth GT2 pulley, which
is 82,000 mm/s² on the toolhead and 23,000 mm/s² on the bed. Both are far above
the structural limits.

## 2. A correction: blind-bolting into extrusion ends is NOT weak

An earlier version of this analysis claimed the upright-to-base joint was the
speed limiter and that corner brackets were worth +51%. That was wrong, and the
error was a single-bolt model applied to a four-bolt joint.

A preloaded bolted butt joint is effectively rigid until the applied moment
overcomes the clamp force and the faces separate. Four M5 bolts at ±10 mm,
preloaded to a conservative 2.5 kN each, resist about **130 N·m**. The moment
this machine actually applies at an upright foot is about **3 N·m** — a factor
of forty inside the limit.

| Upright foot | Pair stiffness | Gain |
|---|---|---|
| 4 blind bolts, as drawn | 478 kN/m | — |
| Plus a gusset on the loaded face | 636 kN/m | +5% |
| Plus gussets on both faces | 670 kN/m | +6% |
| A perfectly rigid welded foot | 724 kN/m | +7% |

Even replacing the foot with a weld buys 7%. The joint is fine.

**But the rule is not universal.** Measured off the real profiles:

| Profile | Section area | Tapped bores |
|---|---|---|
| 40 × 40 V-slot | 458.46 mm² | **four**, Ø4.6, at (±10, ±10) |
| 20 × 40 V-slot | 299.99 mm² | two, Ø4.2, at (0, ±10) |
| 20 × 20 V-slot | 171.40 mm² | **one**, Ø4.2, dead centre |

The 2020 has a single central bore — that genuinely is the weak single-bolt case.
**Corner-bracket the 2020 ends; don't bother on the 4040 uprights.**

## 3. The one real defect at the feet is screw length

Thread engagement for M5 into 6063 aluminium through a 2.2 mm wall:

| Screw | Engagement | Verdict |
|---|---|---|
| M5 × 8 | 5.8 mm | too short — below 2 × diameter |
| M5 × 12 | 9.8 mm | marginal |
| **M5 × 16** | 13.8 mm | correct |

Preload is the entire reason a blind joint is stiff, so too little thread turns a
good joint into the floppy one the wrong analysis described. Use M5 × 16 at the feet.

## 4. Where the two carriage blocks go

Two arrangements were considered. The toolhead's centre of mass sits about 40 mm
forward of the rail; accelerating along X at that offset makes a moment about Z.

- **Blocks separated along X** resist that moment directly with a force couple.
- **Blocks separated along Z** (two rails on the beam) cannot make a couple about
  Z at all, so they do not help the dominant mode.

So the blocks go in line along X. The cost is beam length — the carriage grows to
100 mm and the beam with it:

| Arrangement | Beam | k_total | Accel | Gain |
|---|---|---|---|---|
| 1 block, 480 mm beam | 480 | 89.8 | 4,411 | — |
| 2 blocks in line, 520 mm beam | 520 | 122.6 | 6,021 | +37% |
| 2 blocks in line, 560 mm beam | 560 | 113.4 | 5,569 | +26% |

(Those accelerations are for a 1.14 kg toolhead, the figure used while choosing
the arrangement. The built toolhead is lighter, which is why §1 is higher.)

The beam-lengthening penalty is real: at 560 mm, a third of the gain is given
back. `end_allow` was trimmed from 50 to 30 mm to hold the beam at 520.

## 5. The gantry height is set by the toolhead

`gantry_z = bed_top + th_drop`, where `th_drop` (75 mm) is the distance from the
X beam underside to the nozzle tip.

Before the toolhead existed as geometry, the gantry sat at a placeholder height of
`base_h + 60` = 100 mm. Modelling the real toolhead put the **nozzle 68 mm below
the top of the bed**. It is now driven by the parameter instead of guessed.

This is the clearest argument for modelling before buying.

## 6. Corrections to earlier figures

| Claim | Was | Is | Why |
|---|---|---|---|
| Frame mass | 12.985 kg | **4.484 kg** | every component had inherited Fusion's default Steel; density was 7850 instead of 2700 |
| Layout jig mass | 143.8 kg | **18 g** | the hidden parametric skeleton was steel blocks; it now carries a 1 kg/m³ material |
| Upright foot joint | +51% available | **+7%** | single-bolt model applied to a four-bolt joint, see §2 |
| Second MGN12H block | "about $8" | $8 on AliExpress, **$105 at Australian retail** | the gain is real; the price was not a local one |
| Assembly occurrence count | 77 | 294 | 77 was the Frame's child count quoted as the whole |
| Fastener count | 140 | 153 | |

Verification of the mass correction: the 2020 member computes 0.463 kg/m against
OpenBuilds' published 0.47 kg/m, and the 4040 upright at 500 mm computes 618.9 g
(458.46 mm² × 500 mm × 2.7 g/cm³ = 618.9 g).

## 7. What the model is, and what it is not

**Is:**
- 38 driving parameters; lengths *and* positions follow them, held by rigid joints
  to a grounded layout skeleton.
- Real V-slot cross-sections, traced from the actual profiles and re-drawn
  natively, within 0.003 mm² of the originals.
- Real hub parts for the lead screws, anti-backlash nut blocks and the Z motor.
- Verified by flexing: `upright_h` at 620, 440 and back to 500 moves the top tie
  to 660–680, 480–500, 540–560 with the envelope tracking and a clean timeline.

**Is not:**
- Fastener-complete. The frame carries one screw assortment line, not 153 parts.
- Printed-part complete. Motor mounts, idler brackets, belt clamps and the Z nut
  mounts do not exist yet.
- Free of simplifications. Interference analysis reports **4 overlaps of exactly
  4320 mm³**, which is the simplified carriage blocks passing through the rails
  they would really wrap. That is deliberate. Any *other* interference is a fault.
- Mass-accurate from CAD alone. Imported STEP has no iron, copper or magnets in
  it: the NEMA 17's own geometry computes 520 g against a real 390 g. Simplified
  and imported parts therefore carry a per-part density chosen to hit the
  datasheet mass. The frame, rails and plates use real materials.

## 8. Fusion API notes, for anyone scripting this

- `root.allOccurrences` gives world-space positions. `occurrence.component.occurrences`
  does not, and reading bounding boxes from the latter silently returns stale or
  local coordinates.
- A metal appearance is coloured by **`metal_f0`**, not `surface_albedo`. Setting
  `surface_albedo` renders the whole frame as a black silhouette.
- `occurrence.transform2` can only be set on a proxy obtained from the root
  component (`createForAssemblyContext`), and in a parametric design the change
  must be committed with `snapshots.add()` *before* any `computeAll()`, or it is
  silently discarded.
- `addTwoPointRectangle` via the API adds **zero** geometric constraints, unlike
  the UI. Sketches need explicit horizontal/vertical constraints to be fully
  defined.
- A script that raises an exception has **all** of its changes rolled back,
  including parameters added earlier in the same script.
- A rigid joint between two planar faces picks its own rotation about the face
  normal. On a non-square profile it lands 90° out; set `JointInput.angle`
  explicitly and search 0/90/180/270.

## 9. Commissioning — before the first print

Nothing in `klipper/printer.cfg` has run on hardware. In order:

1. Flash the Manta M8P V2.0 for STM32H723, 128 KiB bootloader, 25 MHz crystal.
2. Replace the `[mcu] serial:` path with the real one from `ls /dev/serial/by-id/*`.
3. Check every motor direction one axis at a time with `FORCE_MOVE`, before homing.
4. Verify each endstop with `QUERY_ENDSTOPS` before allowing a homing move.
5. Confirm the two carriages cannot collide: `safe_distance: 110` assumes 110 mm
   carriage plates. Measure yours.
6. `PID_CALIBRATE` both hotends and the bed. The values in the config are
   placeholders copied from the reference config.
7. Calibrate `rotation_distance` on both extruders. 4.637 is the Orbiter nominal.
8. Measure the T0→T1 offsets with a calibration print and set them in `T1`.
9. `SHAPER_CALIBRATE` each toolhead. The model predicts ~77 Hz on X and ~42 Hz on
   Y. If the measured numbers are far off, the machine is not built as drawn —
   find out why before raising `max_accel`.

## 10. Still open

- The Z motor has no mount modelled; it floats above the top tie.
- The X motors, idlers, belts and pulleys are not modelled.
- The bed carrier, levelling hardware and Y motor mount are not modelled.
- The bed is the slowest axis and nothing has been done about it.
- `safe_distance` and the park positions are derived from the model, not measured.
- No source in Australia currently stocks the 235 × 235 24 V heated bed.
