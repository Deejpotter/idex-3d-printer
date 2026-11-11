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
| Y axis (the bed) | 1.27 kg | 51.9 Hz | 5,948 mm/s² |
| Y axis, with the in-stock 255 × 245 plate (§21) | 1.34 kg | 50.6 Hz | **5,646 mm/s²** |

**The bed is still the slowest axis.** `max_accel` in `printer.cfg` is set to
5,600 for that reason. Raising it further means stiffening the bed again.

See §12 for how the bed got from 4,255 to 5,948 mm/s², and for the correction
to the stiffness figure that made the earlier number wrong.

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
- `occurrences.addExistingComponent(component, matrix)` applies the matrix
  **relative to the previous occurrence of that component**, so a list of
  placements accumulates. Add at identity and set `transform2` afterwards.
- `snapshots.add()` silently reverts the transform of some referenced
  occurrences — it did for every NEMA 17 while leaving the pulleys alone. The
  fix is to wrap the part in a native component and transform the wrapper.
- A sketch on `xZConstructionPlane` has its second axis along **−Z**, so a
  feature placed at +z lands at −z and cuts nothing. The failed cut leaves an
  unhealthy "No target body!" feature in the timeline.

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

## 10. What the completed model added

Everything in the machine is now modelled: X motors, idlers, belts and mounts;
the Y rails, blocks, bed carrier, heated bed, motor, idler and belt; the Z belt
link, screw bearing blocks and motor; and the electronics bay behind the frame.

| Sub-assembly | Parts | Mass |
|---|---:|---:|
| A — Frame | 7 | 3,684 g |
| B — X gantry | 16 | 1,745 g |
| C — Toolhead A | 6 | 518 g |
| C — Toolhead B | 6 | 518 g |
| D — Y and bed | 17 | 3,811 g |
| E — Z axis | 26 | 1,921 g |
| G — Electronics | 2 | 2,291 g |
| **Total** | **80 bodies** | **14.51 kg** |

Overall envelope with motors and the electronics bay: 556 × 583 × 598 mm.

Real parts inserted from the hub: both lead screws, both anti-backlash nut
blocks, four NEMA 17 motors, six GT2 pulleys, five GT2 idlers and four 688ZZ
bearings. Everything else is native geometry.

**No clean free STEP exists for three parts.** The MGN12H carriage block, the
Orbiter v2.5 and the V6 are all modelled as simplified solids carrying a
density chosen to hit the datasheet mass:

- The hub's own MGN12H models are **1,027 and 1,186 bodies** — every ball
  modelled. Unusable in an assembly that needs ten of them. Both the rail and
  the block are instead drawn from the HIWIN MGN12 datasheet: a 14-point rail
  section with ball grooves and top chamfers, and a proper C-section block.
  The rail section computes **0.694 kg/m** against HIWIN's published ~0.72,
  which is the check that the profile is right.
- Searching turned up only paid marketplace STEP or community redraws of
  uncertain provenance for all three. A wrong STEP is worse than an honest
  simplified solid with the right envelope and the right mass.

### Interference after completion

Seven overlaps remain, and every one is a shaft or belt meeting a part that
would carry a bore in reality:

| Count | Volume | What |
|---:|---:|---|
| 2 | 992 mm³ | lead screw through its pulley — **see below** |
| 1 | 384 mm³ | Z motor shaft through its pulley |
| 4 | 70–122 mm³ | belt runs tangent to pulleys and idlers |

The four 4,320 mm³ rail/block overlaps are gone: the carriage blocks are now
modelled as the C-section they actually are, so they wrap the rail instead of
passing through it.

Fifteen others were fixed: the X motor pulleys fouled their own mount plates,
both X idlers and the Y idler fouled their brackets, and the Z screw bearing
blocks had no bore. All now corrected.

**The lead screw / pulley overlap is a real finding, not a simplification.**
The hub pulley has a **6.35 mm bore** and the TR8 screw is **8 mm**. The BOM
already specifies an 8 mm bore pulley for the screws; the model is using the
wrong master because that is what the hub holds. Buy the 8 mm bore part.

## 12. Design changes after review

### The bed was over-built, and the first fix would have made it worse

The bed was a **6 mm 235 × 235 carrier plate** (895 g) carrying a **6 mm heated
bed** (1,060 g). Both were guesses. The real Creality part is **3 mm**.

The obvious move — delete the carrier, drop the bed to 3 mm — is wrong, and the
numbers say why. Carrier stiffness computed from geometry, `k = 48EI/L³` over
the 200 mm rail spacing:

| Carrier | k | Moving mass | k_total | f | Accel |
|---|---:|---:|---:|---:|---:|
| 235 × 6 plate + 6 mm bed (original) | 1,751 kN/m | 2,169 g | 164.8 | 43.9 Hz | 4,255 |
| 2 bars 40 × 3 | 293 kN/m | 1,199 g | 112.3 | 48.7 Hz | 5,243 |
| **2 bars 35 × 5** | **521 kN/m** | **1,269 g** | **134.9** | **51.9 Hz** | **5,948** |
| 2 bars 30 × 6 | 666 kN/m | 1,275 g | 142.9 | 53.3 Hz | 6,273 |
| full 235 × 3 plate | 438 kN/m | 1,494 g | 128.5 | 46.7 Hz | 4,815 |

Two thin 3 mm bars are **six times floppier** than the plate they replace. The
mass saving still wins, but far less than it looks. Stiffness goes as t³, so
going from 3 mm to 5 mm bars costs 70 g and buys 78% more carrier stiffness.

**35 × 5 bars it is**, at 111 g each. The bed stack is now carrier bars (5) +
silicone levelling spacers (2.5) + aluminium bed with bonded heater (3) +
magnetic sheet (1) + PEI spring steel (0.5), which keeps `bed_top` at exactly
93 mm so nothing else in the machine moves.

**Correction:** the 3,219 mm/s² quoted earlier used an *assumed* 400 kN/m for
the carrier. Computing it from the actual plate geometry gives 1,751 kN/m and
4,255 mm/s² for the original bed. The real gain from this change is
**4,255 → 5,948, +40%** — not the +85% that comparing against the old wrong
number would suggest.

### Board changed: Manta M8P → Octopus Pro

The Manta M8P needs a CB1 or CM4 compute module in its socket, and **no
Australian supplier stocks the CB1**. That made the single most important part
of the BOM unbuyable.

| | Manta M8P v2.0 | **Octopus Pro V1.1** |
|---|---|---|
| Board | $145 | **$115, in stock** |
| Host | CB1 not stocked; CM4 ~$76 | any Raspberry Pi over USB, ~$85 |
| Driver slots | 8 | 8 |
| MCU | STM32H723 | STM32H723 |
| Total | ~$221, blocked | **~$200, all in stock** |

Cheaper, in stock, and the separate Pi is easier to replace or debug. It also
solves the accelerometer: the Octopus Pro has no ADXL header, but the Pi's own
SPI does the job, which the Manta route would have needed anyway.

`printer.cfg` is rewritten against
[BigTreeTech's Octopus Pro reference config](https://github.com/bigtreetech/BIGTREETECH-OCTOPUS-V1.0/blob/master/Firmware/Klipper/generic-bigtreetech-octopus-pro-v1.1.cfg).
One departure, flagged in the file: BTT writes Driver3's `enable_pin` without
the leading `!` where every other driver has one. TMC2209 enable is active low,
so it is inverted here — check the motor actually enables before trusting it.

### Considered and rejected

- **Sherpa Mini + pancake motor** ($92/head) instead of the Orbiter ($105/head).
  Saves $27 across two heads and is perhaps 20 g lighter each, but flow is
  lower and it is a kit to assemble rather than a finished unit. Published
  weights for both disagree wildly between sources — anywhere from 95 to 148 g
  — so the weight argument is not solid enough to act on.
- **CR-6 SE bed kit** (255 × 245, $55.95, in stock) instead of the 235 × 235
  that is out of stock. Rejected here because `build_x` and `build_y` did not
  propagate downstream. **Adopted in §21** once they did — it is now the bed.

## 13. The parametric claim only covers the frame

Measured, not assumed. Driving `build_x` and `build_y` to 300 mm:

| Part | Follows? |
|---|---|
| X beam, uprights, base, top tie, bed rails | **yes** |
| X rail, carriage blocks, toolheads, hotends | no |
| Y rails, bed carrier, heated bed | no |
| Lead screws, Z plates, Z rails | no |
| Electronics | no |

The frame grows correctly and everything mounted to it stays where it was.
The reason is simple: the frame members are rigid-jointed to a parametric
layout skeleton, while everything added afterwards is placed at a fixed
transform.

What *does* propagate correctly is the vertical stack: `bed_top` is built from
the real layer thicknesses, and `gantry_z = bed_top + th_drop`, so changing the
bed construction moves the gantry to match. That is why the bed rebuild above
kept `bed_top` at 93 mm deliberately — so the beam would not move away from
toolheads that cannot follow it.

**Do not treat this model as parametric beyond the frame** until every
sub-assembly is jointed to the layout the way the frame members are.

## 14. The mounting audit

Interference checking says no two parts share space. It says nothing about
whether they can be **bolted together**. Measuring where the V-slots actually
are, by probing the traced profiles point by point:

| Interface | Slot centres | Rail centre | Verdict |
|---|---:|---:|---|
| Z rails on the 4040 upright face | 10.0 and 30.0 | 20.0 | **could not be bolted** |
| X rail on the 2040 beam face | 178.0 and 198.0 | 188.0 | **could not be bolted** |
| Y rails on the 2020 bed rails | 160.0 | 160.0 | correct |
| Upright feet into the base rail | 10.0 and 30.0 | 10.0, 30.0 | correct |
| Z motor onto the top tie underside | 255.0 and 275.0 | 238.0 | misses both |

A 2020 face has **one** slot, dead centre. A 40 mm face has **two**, at ±10 from
centre, with nothing between them. Centring a 12 mm rail on a 40 mm face — which
is what looks right — puts it exactly where there is no slot. The Y rails were
fine only because they happen to sit on 2020.

Both rails have been moved onto the measured slot centres (x 30/490, z 198), and
the carriage blocks and belt A with them.

### Twelve brackets float

Asking whether each bracket touches any frame member at all:

| Bracket | Clearance to nearest frame member |
|---|---:|
| X motor mounts (2) | 20 mm |
| X idler brackets (2) | 18 mm |
| Y motor mount | 46 mm |
| Y idler bracket | 8 mm |
| Z screw blocks (4) | 6 mm |
| PSU and control board | 2 mm |

Every one is hanging in space. They were placed to be in the right *place* and
nothing checked they could be *attached*. They are placeholders for printed
parts that do not exist yet, but the model should not pretend otherwise.

## 15. Can the heated bed bolt to the carriages? No.

6061 grows 23.6 µm/m/K. From 20 °C to 100 °C:

| Span | Growth |
|---|---:|
| Between the two rail centres (200 mm) | **0.378 mm** |
| Between the two carrier bars (105 mm) | 0.198 mm |
| Across the full bed (235 mm) | 0.444 mm |

The bed plate's axial stiffness is `EA/L` = 243 kN/mm, so holding back 0.378 mm
takes **92 kN**. Nothing survives that — the plate bows or the carriages are
destroyed. An MGN12 carriage is a preloaded ball bearing with microns of
clearance; it has no business absorbing a third of a millimetre.

**So the bed is never bolted to the blocks.** The stack is bed → silicone
spacers → carrier bars → blocks, and the spacers are the compliant element.
Each takes half the growth, 0.189 mm of shear. An M3 through a 4.5 mm clearance
hole gives 0.75 mm of float per side, which is ample.

### What the audit did find

The two carrier bars were **independent** — nothing tied them together in Y,
which is the driving direction, except the bed sitting on compliant spacers.
Pull on the belt and the pair racks. Added: a **spine between the bars making an
H-frame** (66 g) and a **belt clamp on the spine** (9 g), so belt load goes into
a closed structure rather than through a silicone puck.

Moving bed mass is now 1,344 g, up from 1,269 g for the spine and clamp.

## 16. Where every remaining dimension came from

| Part | Source | What it gave |
|---|---|---|
| **Orbiter v2.5** | **measured from a real STEP** — the A4T Orbiter extruder adapter, Armchair Heavy Industries, GitHub | 2 × M3 clearance Ø3.4 at **37.0 mm centres** (x −17.50 and +19.50, both y 0), filament bore Ø4.4 at the origin |
| E3D V6 | RepRap wiki groove-mount convention | Ø16 boss, **Ø12 groove × 4.64 wide**, heatsink Ø22.3 × 26 |
| NEMA 17 | NEMA standard | 42.3 square, **31.0 × 31.0** bolt pattern, Ø22 pilot boss |
| MGN12 / MGN12H | HIWIN datasheet | rail 12 × 8 on 25 pitch; block 27 × 45.4 × 13, M3 on 20 × 20 |
| 5015 blower | SOFASCO sDB5015 drawing | 51.5 × 51.5 × 15, 2 × Ø4.0 |
| Octopus Pro | BTT publish an official STEP — **24 MB, 113,000 points** | rejected; board drawn at its published 160 × 100 |
| Mean Well LRS-350-24 | Mean Well datasheet | 215 × 115 × 30 |

No vendor publishes the Orbiter's hole pattern and no official CAD exists. But the
A4T toolhead ships a 203 KB STEP of its *Orbiter adapter*, and an adapter is
nothing but the interface. Importing it and reading the cylinder axes gave the
pattern exactly — and it is **asymmetric**, 17.5 mm one side of the filament bore
and 19.5 mm the other.

The Octopus STEP is worth recording as a negative result: official, correct, and
**unusable** at 24 MB for a part that contributes an outline and four holes. That
is the trap §rule 3 was written for.

## 17. Every bracket now lands on a slot

| Bracket | Was | Bolts to |
|---|---:|---|
| X motor mounts (2) | 20 mm clear | beam top / underside, slot y = 216 |
| X idler brackets (2) | 18 mm clear | beam top / underside, slot y = 216 |
| Y motor mount | 46 mm clear | base cross front face, slots z = 10 and 30 |
| Y idler bracket | 8 mm clear | base cross back face, slots z = 10 and 30 |
| Z screw blocks (4) | 6 mm clear | upright and base rail inner faces |
| PSU and control board | 2 mm clear | a new electronics panel, itself bolted to the base cross |

Each is an L-bracket: a foot lying flat on a frame face over a measured slot, a
web, and a plate carrying the part. The webs are **split either side of the
pulleys** they reach past — the first attempt drove a solid web straight through
the X pulleys and idlers.

Landing them created six new clashes at once: both motor mounts through their own
pulleys, both idler brackets through their idlers, the Y motor through its own
plate, and the rebuilt Z screw blocks losing the bores they had. All found by
measurement. **Interference is back to seven**, all the original
shaft-or-belt-through-bore class, and **zero brackets float**.

### Two bugs worth recording

- `'Y motor mount'` also starts with `'Y motor'`. A prefix match meant to move the
  motor moved the mount too, translating a part already in absolute coordinates by
  a further (260, 480, 42) and parking it 480 mm outside the machine. Caught by
  rendering, not by any check — which is an argument for always looking at the
  picture as well as the numbers.
- A float test that keyed frame members by name collapsed the two uprights into
  one, so a bracket correctly touching the left upright read as 126 mm from "the"
  upright. The test was wrong, not the model.

## 18. A more reliable way than looking at it

Every fault in this project was found by measuring, and every one that got in
was placed by eye. Screenshots do not tell you whether a rail is centred on a
slot, whether a bracket touches anything, or whether a parameter reaches the
part it is meant to drive.

`scripts/check_model.py` asserts the design rules instead. Run it as a Fusion
script with the assembly open. Current result:

```
PASS  nozzle A at bed_top                   nozzle z=93.00  bed_top=93.00
PASS  nozzle B at bed_top                   nozzle z=93.00  bed_top=93.00
PASS  PEI top at bed_top                    PEI top z=93.00
PASS  all brackets touch the frame          11 brackets, floating: none
PASS  X rail centred on a beam slot         rail centre z=198.0, slots at 178.0, 198.0
PASS  interference is the known set only    7 found: 992 992 384 122 122 70 70
FAIL  timeline healthy                      1 unhealthy of 391
PASS  toolhead A parks clear of build area  nozzle x=110.0, build area 145.0..375.0
PASS  toolhead B parks clear of build area  nozzle x=410.0, build area 145.0..375.0
```

The single failure is the stale `Capture Position` entry, which is suppressed
and has no geometric effect.

### Parameter coverage, measured

The check that matters flexes each driving parameter and counts what actually
moved. The model is parametric only to the extent this number is high:

| Parameter | Followed | Pinned | Coverage |
|---|---:|---:|---:|
| `build_x` 230 → 300 | 6 | 52 | **10%** |
| `build_y` 235 → 305 | 7 | 50 | **12%** |
| `upright_h` 500 → 570 | 2 | 54 | **4%** |

So the honest figure is **4–12%**, not "parametric". Only the frame members
follow, because only they are rigid-jointed to the layout skeleton. Everything
added since sits at a fixed transform.

### The fix has a name

This is [skeletal modelling](https://help.autodesk.com/cloudhelp/2023/ENU/Inventor-Help/files/GUID-0435FE9D-6283-4CE0-813B-BD9B0BE5778C.htm),
Autodesk's own term for top-down design: one skeleton part carries the layout
sketches, datums and driving parameters, and every component references *only*
that skeleton. [Autodesk's large-assembly
guidance](https://help.autodesk.com/cloudhelp/2025/ENU/Inventor-Help/files/GUID-456388EE-9B7F-442E-B917-B76BDE016FD2.htm)
splits it per sub-assembly for anything this size, and the practitioner
consensus adds one rule worth stating plainly: **no sibling part may reference
another sibling** — shared interfaces are published through the skeleton.

The model already has the right bones. The `Layout` component is a skeleton; it
just stops at the frame. Extending it means a datum body per interface — X rail
seat, Y rail seats, Z rail seats, bed stack, each motor face — and a rigid joint
from every part to its datum instead of a baked transform.

**Correction:** I first reported that there was no in-house method to copy,
having looked at only one source. That was wrong — see §19.

## 19. Separate the drivers from everything else

There is an established pattern for configurable product families, and it is a
layer above skeletal modelling: **the driving values do not live in the CAD.**
They live in a spreadsheet, the model reads its sizes from it, a small app
validates every value *before* writing, and the BOM is generated from the same
source.

Two things in that pattern matter more than the tooling:

- **A handful of drivers, not dozens.** A whole parametric workbench can run on
  six: width, length, height, shelf height, top thickness, top overhang.
  Everything else is a formula.
- **Validation runs before the model regenerates**, not after. If a value fails a
  rule nothing is written, and the message names the field that failed.

### What my parameters actually looked like

| | Count |
|---|---:|
| Bare numbers someone has to choose | **33** |
| Expressions that follow from something | 8 |

Worse, an audit of what each one actually drives found **twelve parameters that
drive nothing at all** — decoration that reads as design intent. And decoration
rots: `z_screw_x` still said 33 mm long after the lead screws moved to x = 60 in
the slot-centre fix. Anyone reading the parameter list would have believed it.

### Applied

- `z_screw_x` corrected to 60 mm.
- Four parameters converted from bare numbers to expressions: `bed_sz = build_y`,
  `bed_rail_spacing = bed_sz - 35 mm`, `block_pitch = mgn_block_len + 10 mm`,
  `z_plate_w = p40 + 40 mm`.
- Every parameter labelled by class in its comment, so the kinds are visible in
  the dialog: **`[DRIVER]`** (someone chooses it), **`[PART]`** (a fact about a
  bought component), **`[DERIVED]`** (follows), **`[NOT WIRED]`** (drives nothing
  yet — stated rather than hidden).
- Two checks added to `check_model.py`: **every parameter drives something**
  (currently FAIL, 11 of 41) and **driver values are in range**, with explicit
  rules — `carriage_w` must fit two MGN12H blocks, `bed_sz` cannot be smaller than
  the build area, `gantry_z` cannot sit below `bed_top`.
- The extrusion cut list now derives from the drivers rather than being typed:

```
4040 upright      x2   500.0 mm      4040 total  2060 mm
4040 base rail    x2   530.0 mm      2040 total  1920 mm
2040 base cross   x2   440.0 mm      2020 total  1060 mm
2040 top tie      x1   520.0 mm
2040 X beam       x1   520.0 mm
2020 bed rail     x2   530.0 mm
```

### What this changes about the plan

Skeletal modelling (§18) is still the right structure for *positions*. This is the
layer above: the drivers should be few, separated, validated up front, and the BOM
should fall out of them. Fusion does the derived layer natively through
expressions, so no spreadsheet is needed here — the discipline of separating
drivers from everything else is the part worth copying.

## 20. Skeleton-driven: every part tied, every rule re-checked at other sizes

§18 and §19 ended with the model "frame parametric, everything else pinned" -
parameter coverage 4-12%. That is now fixed, following the plan in
[skeleton-plan.md](skeleton-plan.md).

### What was built

- A grounded **`Skeleton`** component with **no solid bodies**: construction
  planes offset from its origin by parameter expressions (`frame_w`,
  `( frame_d - p40 ) / 2`, `gantry_z - th_drop`, ...), anchor points at
  three-plane intersections, and a **seat** (joint origin) for every part.
- **Every part is rigid-jointed to a seat on the Skeleton - 91 of 91**, never to
  a sibling part. The old `Layout` component (15 pasted bodies with no parameters
  behind them, which is why only the frame ever moved) is deleted.
- The seats sit on the Skeleton side, oriented to the part's existing pose and
  offset to its origin, so referenced (read-only) bought parts tie exactly the
  same way as native ones, and no part geometry had to be rebuilt.
- Lengths from equations: X / Y / Z rails (`x_rail_length`, `y_rail_length`,
  `z_rail_length`), all eight belt runs (`x_belt_run`, `y_belt_run`,
  `z_belt_run`), the bed stack and carrier bars (`bed_sz`, centred on the bed),
  the Z carriage plates (`z_plate_w/t/h`), the toolhead plates
  (`carriage_w + 10 mm`, `th_plate_t/h`), the MGN12H block (`mgn_block_len`).
  Every sketch that was touched is now fully constrained.
- `bed_sz = max(build_x; build_y)` - its own comment already said it had to be
  at least both.

### How "nothing moved" was proven

Before any change, every part's world bounding box went to a baseline file.
After every batch, `scripts/nothing_moved.py` compared all 87 parts against it.
Each joint was also checked as it was made: the part's transform before and
after had to match to 0.00001 mm, or the whole batch rolled back. Every batch
passed. The one exception was deliberate (the X rail change below).

`scripts/skeleton_tie.py` is the reusable engine that does the tying.

### What the checks say now

`check_model.py`: **14 / 14 at nominal size.** Check 8 was rewritten, because the
old one was wrong: it scored a part as a failure if it did not move when
`build_x` grew, but the frame grows from its left, front and floor, so the left
upright *should* stay put. The new check 8 is two parts - every part tied, and
checks 1-5 and 7 re-run with each driver flexed:

| Flex | Result |
|---|---|
| `build_x` 230 → 300 | all rules hold; toolhead B parks at x = 480 |
| `build_y` 235 → 305 | all rules hold; frame 670 deep, bed 305 |
| `upright_h` 500 → 570 | **one rule fails**: the bought 500 mm lead screws no longer reach the base block |

The `upright_h` failure is the right answer, not a bug: the screws are bought
parts and do not stretch. A driver rule now says so up front - `upright_h`
needs `z_screw_len` lead screws.

### Things found on the way

- **Check 9 never worked.** Its regex had literal backspace characters where
  `\b` word boundaries belonged, so it could not match any parameter name. The
  "11 of 41 drive nothing" figure in §19 did not come from that code. Fixed; it
  now really reports **0 of 47**. The backspaces came from shell quoting, and the
  same thing happened again while fixing it.
- **The BOM had drifted from the model.** It listed a 500 mm X rail, 350 mm Y
  rails and 400 mm Z rails; the model had 520, 450 and 350. The 2040 line said
  480 / 400 mm cuts where the model has 520 / 440. Corrected, and the BOM source
  (`docs/bom.json`) now lists every cut against its CAD component. **Check 11**
  measures those components and fails on any length, count or stocked-size
  mismatch.
- **A 520 mm MGN12 rail is not sold.** DREMC stocks LDO rails in 300, 320, 330,
  350, 400, 450 and 500 mm (read 11 Nov 2026). The X rail is now
  `x_beam_len - 20 mm` = 500, centred with 10 mm clear at each end. Check 11
  enforces stocked lengths, so a size that needs a 570 mm rail fails the BOM line.
- **Why cuts kept saying "No target body".** The hidden parts-library copy of a
  component counts as its first occurrence, which makes its bodies invisible, and
  cuts skip invisible bodies. This was also behind the earlier rail and boss hole
  failures. The library copies of the three rails were removed, and the rail
  components renamed `MGN12 rail X / Y / Z` now that their lengths are not fixed.
- The stale `Capture Position` (`Position8`) is deleted. Every part is held by a
  joint now, so it had nothing left to hold. Timeline: 0 unhealthy.
- Three note-only parameters were removed from the model because no geometry
  exists for them: `foot_bolt_pitch` / `foot_bolt_len` (M5 x 16 into the 4040
  end bores, four on 20 mm centres) and `mgn_block_w` (27 mm). The values are
  kept here.

### Known limits

- The Y and Z rail **mounting holes do not follow the length.** Fusion would not
  pattern a feature inside these nested, multi-copy components through the API,
  so their hole sets stay as modelled. The X rail's holes are a proper pattern
  whose count follows `x_rail_length`.
- The Skeleton has many named planes (`X: frame_w - 10 mm`), one per distinct
  offset. Offsets that are facts of a part (a motor centre 10 mm from the beam
  end) are written into the plane expression rather than given a parameter each.

## 21. Pricing it against live listings, and what that changed in the model

Every line of the BOM was re-read from the suppliers' own product data on
11 November 2026, variant by variant, including stock state. Eight lines were
wrong, and three of them changed the design.

### What the BOM had wrong

| Line | Was | Is | Why |
|---|---|---|---|
| 4010 hotend fan | $8.00, marked verified | **$20.50** | the $8.00 was never read from anywhere; marking it verified was the worse error |
| Raspberry Pi 4 2 GB | $85.00 estimate | **$109.33** | Core Electronics, in stock. Plus $11.90 for the official supply and $47.50 for a card, neither of which was costed |
| Extra MGN12H blocks | 3 | **5** | the model has 10 blocks and the five rails bring five. Off by two since the second block per carriage was added |
| ADXL345 | counted twice | **once** | one accelerometer, moved between toolheads |
| F688Z bearings | 1 pack | **2 packs** | four bearings in the model, two per pack |
| Y pulley and idler | one $25.90 bundle | **$11.00 + $7.45** | the bundle said two idlers; the model has one |
| 2040 extrusion | 480 / 400 mm cuts | **520 / 440 mm** | drifted from the model (§20) |
| Corner brackets | $4.50 estimate | **$3.30** | RM Components list the 20-series black bracket |

The total goes from A$1,990.80 to **A$2,250.28**, of which A$333.20 is still
estimated: the four cut-to-length lines and loose wiring. Both extrusion
suppliers price cut lengths through a calculator app that returns $0.00 on the
storefront, so those four lines genuinely need a quote — which is worth saying
plainly rather than leaving a confident-looking number.

### Three parts that changed the design

**The heated bed was the only unbuyable part.** Both DREMC 235 × 235 listings
are out of stock. The CR-6 SE assembly — 255 × 245 mm, 24 V ~270 W — is in
stock at $55.95, so the model now uses it, with the 235 sheets centred on it and
margin all round. It costs 68 g of moving mass, which takes the bed's accel
limit from 5,948 to 5,646 mm/s², and `max_accel` in `printer.cfg` drops to
5,600 to match. A slightly slower machine that can be built beats a faster one
that cannot.

**The 350 mm Z rail is out of stock; 400 mm is not.** `z_rail_length` is now
`upright_h - 100 mm`, so the Z rails are 400 mm: in stock, and 355 mm of travel
against a 230 mm build instead of 305 mm.

**A 520 mm MGN12 rail is not sold at all.** DREMC stock LDO rails in 300, 320,
330, 350, 400, 450 and 500 mm. The X rail is `x_beam_len - 20 mm` = 500 mm,
centred on the beam.

### The checks that would have caught all of it

Four new numeric checks, bringing `check_model.py` to **16 of 16 at nominal
size**:

- **Check 11 now counts carriage blocks** — rails' carriages plus the extras
  line must equal the blocks in the model. It fails on the old count of 3.
- **Check 11 enforces stocked sizes**, from lists in `bom.json`: rails
  300–500 mm, sheets 125–355 mm, lead screws 300/400/500/800 mm.
- **Check 12 is a 24 V power budget**, see below.
- A driver rule now says the bought heated plate must be at least as big as the
  sheets, so growing the build past the bought bed fails up front.
- **Check 4b** puts the Z motor mount's bolts on real top-tie slots (below).

Checks 10, 11 and 12 moved into a `rules()` function that the flex loop calls
too, so a size change is now asked the buying questions as well as the geometric
ones. That is what turned up the real size envelope:

| Flex | Geometry | Buyable |
|---|---|---|
| `build_x` 230 → 300 | passes | **no** — needs a 570 mm X rail and 300 mm sheets, neither stocked, and the bought plate is too small |
| `build_y` 235 → 305 | passes | **no** — same sheet and plate limits |
| `upright_h` 500 → 570 | lead screws no longer reach | **no** — needs a 470 mm Z rail (450 or 500 are stocked) and 570 mm screws |

So **230 × 235 is not an arbitrary build volume: it is the largest this parts
list allows.** The binding constraint is the 500 mm rail and the 235 mm sheet,
not the frame.

### The Z motor had no mount, and could not have had one

The last open geometric fault. The Z motor sat with its top face against the
top tie's underside, bolted to nothing: the tie's slots are at y = 255 and 275,
and a NEMA 17's bolt pattern is 31 mm square, so **no rotation or offset of the
motor can put two of its four bolts on two slots 20 mm apart.** Every other
motor in the machine already had a bracket; this one was the exception.

So it gets one: `Z motor mount`, a 60 × 76 × 6 mm plate against the tie
underside, carrying

- four M3 clearance holes on the motor's `nema_bolt` pattern and a Ø23 pilot
  bore for its boss, with the motor hanging underneath, and
- four M5 clearance holes at y = 255 and 275 — **on the slots**, measured.

Both its sketches are fully constrained and every hole position is an expression
on `frame_d`, `p40`, `p20`, `z_mount_y` and `nema_bolt`, so the bolts stay on
the slots when the frame changes.

Adding a 6 mm plate under the tie pushes the motor down 6 mm, and the Z link
belt has to follow or it will not run true. The three skeleton planes that
carry the Z belt plane — the motor, the three pulleys, the two idlers and the
two belt runs — now subtract `z_mount_t`, so all eight parts dropped together
and nothing else moved. That is the whole point of the skeleton: one thickness
parameter, eight parts, one edit.

**Check 4b** measures it: the M5 hole axes against the slot centres found by
walking the tie's underside. It reported the holes 2.8 mm off on the first run,
which was the check's own fault — it read a point on the hole's surface instead
of the axis, and 2.8 mm is the hole radius plus rounding. Worth recording,
because a check that is wrong in the pessimistic direction is the kind you
believe.

### The 24 V supply does not fit

Adding up the loads was overdue:

| Load | Qty | W each | Total |
|---|---:|---:|---:|
| Heated bed | 1 | 270 | 270.0 |
| V6 hotend heater | 2 | 40 | 80.0 |
| NEMA 17 via TMC2209 | 6 | 8 | 48.0 |
| 5015 part fan | 2 | 2.8 | 5.6 |
| 4010 hotend fan | 2 | 1.5 | 3.0 |
| Octopus Pro | 1 | 5 | 5.0 |
| | | | **411.6 W** |

A single LRS-350-24 is **118% loaded**, and it was undersized at the old 220 W
bed too (362 W) — two hotends is what breaks it. The fix is a second supply:
LRS-350-24 for the bed alone (77%) and LRS-200-24 for motion, hotends and the
board (67%), $69.00 more. Nothing above 80% of rating, which is what check 12
asserts. The Pi keeps its own 5 V supply and is off the 24 V budget entirely.

The stepper figure (8 W each) is the one estimate in that table; everything else
is a rating off a datasheet or a supplier listing. Even at 4 W per motor the
single supply still fails.

## 22. Nothing was attached to its belt

The open items listed "belt clamps where the belts meet the carriages are not
modelled" as a detail still to draw. It was not a detail. **Not one belt in the
machine was connected to the thing it drives.**

### What check 4c found

A new check asserts the obvious: every belt run must touch a clamp, and that
clamp must end up on the carriage — bolted to it, or with the belt sandwiched
between the two. First run:

```
FAIL  every belt is clamped to what it drives   6 belt runs;
      Belt A lower has no X belt clamp A;  Belt A upper has no X belt clamp A;
      Belt B lower has no X belt clamp B;  Belt B upper has no X belt clamp B;
      Y belt run 1 is 15.0 mm clear of Y belt clamp;
      Y belt run 2 is 15.0 mm clear of Y belt clamp
```

The X axis had no clamps at all. The Y belt clamp existed, was tied to the
skeleton, had passed every check for weeks — and floated **15 mm above the belt
it was named after**. It was a 24 × 20 × 7 block with an undimensioned sketch,
placed by eye at `bed_top - 19`, and nothing had ever asked it to touch
anything.

### Why the X belts could not have been clamped as drawn

The two X belts run at different heights, because each is wrapped round its own
motor pulley: belt A on the centreline `gantry_z + 57` (225 mm), belt B on
`gantry_z - 7` (161 mm). Each belt presents two runs, 17.4 mm apart — the two
tangents of a 20-tooth pulley — so a toolhead has to grip a 22.8 mm band.

The toolhead plate ran from 153 to 223. Belt A's upper run sits at 233–234.4,
**ten millimetres above the top of the plate**, and belt B's lower run at
151.6–153 is a millimetre below the bottom. Neither carriage could reach its own
belt. The plate was 70 mm tall because `th_plate_h` was set to 70 mm, and no
rule had ever connected that number to the belts.

### The fix

- `th_plate_h` is now `( x_belt_a_z - x_belt_b_z ) + x_belt_sep + belt_t + 6 mm`
  — 88.8 mm, spanning **both** belt planes with 3 mm clear at each end. One
  plate design serves both toolheads, which is what an IDEX wants anyway.
- **`X belt clamp A` and `X belt clamp B`**, 30 × 6 × 22.8 mm, each centred on
  its own belt centreline and sitting `belt_w` behind the plate's back face, so
  the belt is clamped between plate and clamp. Both sketches fully constrained.
- **`Y belt clamp`** rebuilt: 28 × 20 × 28, from `y_belt_bot` up to the carrier
  spine's underside, straddling both Y runs. It grips the belts rather than
  hovering over them, which adds two 168 mm³ overlaps to the expected
  interference set — the same "belt through a part that grips it" class as the
  four pulley overlaps already there.

Nothing else moved: the three changed parts were the only ones the baseline
flagged. **17 of 17 checks pass**, 94 of 94 parts tied.

The cost is 65 g per toolhead — the taller plate and the clamp — taking it from
506 to 571 g. X falls from 13,259 to about 11,765 mm/s². **The machine does not
slow down**, because the bed still limits it at 5,646.

## 23. The bed's stiffness numbers do not reproduce

The top open item has been "the bed is the slowest axis, stiffer carrier bars
are the next lever" since §12. Before spending anything on bars, the number
behind it was checked. It does not survive.

§12 gives carrier stiffness "computed from geometry, `k = 48EI/L³` over the
200 mm rail spacing":

| Carrier | §12 says | 48EI/L³, bending about Y (t³, gravity) | about Z (in-plane, the way Y accelerates) |
|---|---:|---:|---:|
| 2 bars 40 × 3 | 293 kN/m | 75 kN/m | 13,248 kN/m |
| 2 bars 35 × 5 | 521 kN/m | 302 kN/m | 14,792 kN/m |
| 2 bars 30 × 6 | 666 kN/m | 447 kN/m | 11,178 kN/m |

Neither column is the published one, and the ratios settle it: §12's steps are
**1.78 and 1.28**, thickness-cubed gives 4.05 and 1.48, width-cubed gives 1.12
and 0.76. No span, axis or count reproduces it. The figures are not wrong by a
factor — they are not the output of the stated method at all.

### What the right axis says

The bed accelerates along **Y**. The carrier bars span along **X** between the
rail blocks. A Y-direction load therefore bends them about the Z axis, on
`I = t·w³/12` — width cubed, not thickness cubed. For the 35 × 5 bars that is
17,864 mm⁴ each and **14,792 kN/m** for the pair.

Putting the Y chain together the way Lesson 2 does — belt, clamp and carrier in
series:

| Belt clamp | Chain total | f | Accel |
|---|---:|---:|---:|
| printed, 25 kN/m | 23.7 kN/m | 21.2 Hz | 990 mm/s² |
| ribbed printed, 60 | 52.9 kN/m | 31.6 Hz | 2,211 mm/s² |
| aluminium, 150 | 112.3 kN/m | 46.1 Hz | 4,693 mm/s² |
| aluminium, short and wide, 400 | 210.9 kN/m | 63.2 Hz | 8,817 mm/s² |

**The carrier bars contribute 0.16% of the compliance. The belt clamp
contributes 94.7%.**

### Two conclusions that change the plan

1. **Stiffer carrier bars buy nothing.** Going 35 × 5 → 30 × 6, which §12 chose
   not to do and listed as worth +5%, is in the direction that matters actually
   **worse** — 11,178 against 14,792 kN/m, because the bar gets narrower and
   width is what counts. Either way it is lost in the noise behind the clamp.
2. **The Y belt clamp is the bed.** It is 95% of the compliance, it is the part
   that was floating in mid-air until §22, and it is the one thing worth
   designing properly. Short, wide, aluminium, bolted to the carrier spine on
   as large a footprint as fits.

This is Lesson 2 doing its job again: the floppiest spring wins, and it was
never the one being argued about.

### Acting on it: the clamp redesigned

The clamp block itself was never the problem. A solid 28 x 20 aluminium block
cantilevered 28 mm is **176,000 kN/m** — four hundred times stiffer than the
belt. What flexes is the **bolted joint**, and the build spec's own figures put
that at 25 kN/m printed, 60 ribbed, ~150 for aluminium bolted properly.

A joint resists belt pull as a moment about its bolt pattern, so the lever is
everything. The old clamp was 28 x 20 with two bolts about 14 mm apart. The new
one keeps the same web down to the belt but adds a **60 mm flange with four
bolts at ±22 mm**, spread across the carrier spine's full footprint — a lever
3.1x longer, so about **ten times** the moment stiffness for 50 g of aluminium.

| | Bed mass | Chain | f | Accel |
|---|---:|---:|---:|---:|
| old: 28 × 20 block, 2 bolts at ±7 mm | 1,379 g | 112.3 kN/m | 45.4 Hz | 4,557 mm/s² |
| **new: 28 × 60 flange, 4 bolts at ±22 mm** | 1,429 g | 179.4 kN/m | 56.4 Hz | **7,027 mm/s²** |

**+54% on the limiting axis for 50 g.** X is 11,765, so the bed still sets the
machine — but it sets it at about 7,000 rather than 4,600.

Note what that means for `max_accel`. The old clamp would not have supported the
5,600 the config asks for; the new one has headroom over it. The setting does
not change, because it is now **conservative instead of optimistic**, and
because all of this is still a calculation. Measure it before raising it.

### What is still unverified

The 5,646 mm/s² figure the machine was set to is inherited from §12 and rests
on its 521 kN/m carrier, which does not reproduce. The chain above replaces it
with something derived from stated geometry, but two of its three terms —
belt at 460 kN/m and the bolted joint at 150/300 — are rules of thumb from the
build spec, not measurements. So the bed's limit is now **bounded rather than
known**: 4,600 with the old clamp, about 7,000 with the new one, and the
difference is entirely one bracket.

`max_accel` stays at 5,600. The honest next step is `RESONANCE_TEST` on Y on the
built machine, not another calculation.

## 11. Still open

- **The bed's acceleration limit is not reliably known** (§23). The 5,646 mm/s²
  figure rests on a carrier stiffness that cannot be reproduced; the chain is
  95% belt clamp, and that clamp has not been designed. Measure it with the
  input shaper on the built machine.
- The bed's limit is bounded, not measured: ~7,000 mm/s² with the redesigned
  clamp, ~4,600 with the old one (§23). Run `RESONANCE_TEST` on Y before
  trusting either.
- Y and Z rail mounting holes do not follow their lengths (§20).
- Four BOM lines are cut-to-length and need a supplier quote (§21).
- Five MGN12H carriage blocks have no in-stock Australian source (§21).
- The 255 × 245 plate's mass is scaled from the 235 × 235 part by area; the
  supplier does not publish it.
- The Z screw pulleys are modelled with the 6.35 mm bore hub part. The real part
  is the 8 mm bore variant, which is now in the BOM; the model still shows the
  stand-in.
- Uprights taller than 500 mm need longer lead screws; the model flags it (§20).
- The brackets are plain plates. They carry the right interfaces — every one
  lands on a measured slot and every belt is gripped — but only the Y belt
  clamp has been shaped for stiffness rather than drawn as a block.
- Bed levelling hardware (springs or silicone spacers) is not modelled.
- Wiring and drag chain are not modelled.
- No printed part has been designed. The brackets in the model are plain plates
  standing in for parts that still have to be drawn, and the carriage and Z
  plates are solid rectangles that would really carry cutouts and hole patterns.
- `safe_distance` and the park positions are derived from the model, not measured.
