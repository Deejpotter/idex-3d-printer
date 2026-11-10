# IDEX 3D printer

A dual-extruder (IDEX) 3D printer built from V-slot aluminium extrusion, designed
around a parametric Fusion 360 model rather than a pile of guesses. This repo holds
the model exports, the engineering analysis, a priced bill of materials and the
Klipper configuration.

**Status: design complete, nothing built.** Every sub-assembly is modelled:
frame, X gantry, two toolheads, Y axis and bed, Z axis, electronics.

| | |
|---|---|
| Build volume | 230 × 235 × 230 mm |
| Kinematics | Cartesian, IDEX, moving bed (Y) |
| Frame | 4040 / 2040 / 2020 V-slot, 520 × 530 × 560 mm |
| Motion | MGN12H linear rail on every axis, GT2 6 mm belts |
| Z | One motor, belt-linked to two TR8×8 lead screws |
| Electronics | BTT Manta M8P V2.0 + CB1, 6 × TMC2209, 24 V |
| Toolhead mass | 518 g each (modelled) |
| Moving bed mass | 2.18 kg (modelled) |
| Frame mass | 4.48 kg; complete modelled machine **14.51 kg**, 80 bodies |
| Estimated cost | ~A$1,934 inc. GST |

## What's here

```
docs/
  build-spec.html    the full write-up: 15 sections, from "why it's slow" to the BOM
  design-notes.md    engineering findings, corrections, and what is still unverified
  bom.md             bill of materials with supplier links and AUD prices
cad/
  idex-printer-assembly.f3d    Fusion archive (open this one to edit)
  idex-printer-assembly.step   portable STEP export
  parameters.csv             the 38 driving parameters
  mass-report.csv            per-part mass
klipper/
  printer.cfg        full machine config for the Manta M8P V2.0
  idex-macros.cfg    toolchange, copy and mirror modes, start/end
```

![Assembly](docs/assembly.png)

Open `docs/build-spec.html` in a browser — it is the readable version of everything
below.

## The design in one paragraph

The starting point was an existing dual-extruder design that modelled out at about
3,500 mm/s². The limiting part was not the frame and not the belts: it was the
**toolhead**, a 1.42 kg mass hanging off a single MGN12H carriage block. Replacing the
Titan extruders and Chimera hotend with Orbiter v2.5 direct drives and separate V6
hotends, and putting **two** carriage blocks under each toolhead, takes the moving mass
to 518 g. The X axis then models out around 13,200 mm/s² — at which point the **bed**
becomes the slowest axis at about 3,200 mm/s², and that is what the Klipper config is
set to.

## Everything is driven by parameters

The Fusion model has 38 user parameters. Change `build_x`, `build_y`, `build_z`,
`upright_h` or `carriage_w` and the frame, the gantry height and the build envelope all
follow. This is verified by flexing, not by assumption — see
[design-notes.md](docs/design-notes.md).

Two parameters are worth knowing about:

- **`x_beam_len = build_x + 2·carriage_w + 2·park_gap + 2·end_allow`** — on an IDEX the
  beam has to be long enough to park both toolheads clear of the build area. Making the
  carriages wider makes the whole machine wider.
- **`gantry_z = bed_top + th_drop`** — the gantry height is set by the toolhead, not
  chosen. Modelling the toolhead properly moved the beam 68 mm; before that, the nozzle
  sat inside the bed.

## Licence

MIT for the configuration and scripts. The CAD is published so others can build from
it; attribution is appreciated but not required.
