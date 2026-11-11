# Skeleton rewire - plan

Converts the model from "frame parametric, everything else pinned" (parameter
coverage 4-12%) to skeleton-driven, following the established method:

1. **Sizes live in parameters.** No size is typed into a dimension.
2. **Names are the glue.** One name per driver, used everywhere.
3. **The BOM mirrors the CAD, with a check line** that fails when they drift.
4. **Position from a skeleton, length from an equation.** Every part is tied to
   the skeleton, never to a sibling part.
5. **Nothing moves during the rewire.** Every parameter starts at the current
   value; positions are compared before and after each phase.

Restore point: Fusion **v11**.

## Target

| | Now | Target |
|---|---:|---:|
| Skeleton | 15 solid bodies, 0 planes | **no solids**, construction planes + anchor points |
| Parts tied to the skeleton | 11 / 88 (12%) | **all** |
| Parameter coverage, `build_x` / `build_y` / `upright_h` | 10% / 12% / 4% | **> 90%** |
| Parameters that drive nothing | 11 | **0** |

## Skeleton

A grounded component `Skeleton` with no bodies. Construction planes offset from
its origin planes by parameter expressions:

| Plane | Axis | Expression | Now |
|---|---|---|---:|
| `frame_left` / `frame_right` | X | `0` / `frame_w` | 0 / 520 |
| `centre_x` | X | `frame_w / 2` | 260 |
| `frame_front` / `frame_back` | Y | `0` / `frame_d` | 0 / 530 |
| `upright_face` | Y | `(frame_d - p40) / 2` | 245 |
| `gantry_face` | Y | `beam_y` | 206 |
| `floor` / `base_top` / `frame_top` | Z | `0` / `base_h` / `base_h + upright_h` | 0 / 40 / 540 |
| `gantry_floor` | Z | `gantry_z` | 168 |
| `bed_rail_top` | Z | `base_h + p20` | 60 |
| `bed_surface` | Z | `bed_top` | 93 |

**Anchors** are construction points at the intersection of three planes, so an
anchor follows every plane that defines it. Each part is tied to one anchor.

## New length parameters (all equal to today's lengths)

| Name | Expression | Now | Drives |
|---|---|---:|---|
| `x_rail_length` | `x_beam_len` | 520 | X rail |
| `y_rail_length` | `frame_d - 80 mm` | 450 | Y rails x2 |
| `z_rail_length` | `upright_h - 150 mm` | 350 | Z rails x2 |
| `x_belt_run` | `x_beam_len - 50 mm` | 470 | X belt runs x4 |
| `y_belt_run` | `frame_d - 120 mm` | 410 | Y belt runs x2 |
| `z_belt_run` | `frame_w - 150 mm` | 370 | Z belt runs x2 |

## Phases

| # | Phase | Done when |
|---|---|---|
| 0 | Baseline: every part's world box to `before.json` | file written |
| 1 | Build the skeleton planes, anchors and length parameters | planes at the values above; nothing tied yet, so nothing moves |
| 2 | **Prove on the X rail alone** - parametric length, tied to an anchor | nothing moved; flexing `build_x` changes its length and position |
| 3 | Bought and master parts (rails, blocks, motors, pulleys, idlers, bearings, screws, nut blocks) tied to anchors | nothing moved, per sub-assembly |
| 4 | Native parts rebuilt at their own origin with dimensioned sketches, then tied to anchors | nothing moved, per sub-assembly |
| 5 | Frame members re-tied from the Layout solids to the skeleton; Layout deleted | nothing moved; no solid skeleton remains |
| 6 | `check_model.py` - nothing moved vs baseline, coverage, interference, brackets, nozzle | coverage > 90%; all other checks as before |
| 7 | BOM check line against model lengths | check passes |
| 8 | Save, export, document, commit | pushed |

## Why prove on one part first

Fusion joints are not Inventor constraints. A joint aligns two coordinate
systems, so a part with a rotated placement can be re-oriented by the joint
unless the joint preserves its current pose. Referenced hub parts have also
misbehaved once already (motor transforms reverting on snapshot). Phase 2 finds
out which joint type holds position and orientation before 77 parts depend on it.

## Not in scope

- No spreadsheet. Fusion expressions are the derived layer.
- No renames of existing parameters.
- No configurator app.
- Lead screws stay 500 mm bought parts; they do not stretch with `upright_h`.
