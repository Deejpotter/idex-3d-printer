# Bill of materials

All prices **AUD inc GST**, read from supplier product data on **2026-11-11**.

- **verified** — price, option and stock read from the supplier’s own live product data on that date.
- **estimate** — my own figure. A placeholder, not a quote.

Every "verified" line was read from the supplier's own live product data on the date above, including the variant named in the Option column and its stock state. "estimate" is my own figure and is not a quote.

Every cut length and part count is listed against its CAD component in `docs/bom.json`.
`scripts/check_model.py` check 11 measures those components in the model and fails if a
length, a count or a stocked size disagrees; check 12 adds up the 24 V load against the
power supplies. Edit `bom.json`, then run `node scripts/genbom.js`.

## A. Frame

| Part | Option priced | Qty | Unit | Line | Source | Stock | Confidence |
|---|---|---:|---:|---:|---|---|---|
| 4040 V-slot black (20 series) - 2 x 500 uprights + 2 x 530 base rails = 2.06 m [^1] | — | 1 | $90.00 | $90.00 | [RM Components](https://rmcomponents.com.au/products/copy-of-2020-silver-t-slot-aluminium-profile-20-series) | — | estimate |
| 2040 V-slot black - 2 x 520 top tie and X beam + 2 x 440 base cross = 1.92 m [^2] | — | 1 | $44.00 | $44.00 | [RM Components](https://rmcomponents.com.au/products/2040-black-v-slot-aluminium-profile-20-series) | — | estimate |
| 2020 V-slot black - 2 x 530 bed rails = 1.06 m [^3] | — | 1 | $15.00 | $15.00 | [RM Components](https://rmcomponents.com.au/products/2020-black-v-slot-aluminium-profile-20-series) | — | estimate |
| M5 drop-in T-slot nuts, 20 pc [^4] | M5 | 4 | $8.00 | $32.00 | [DREMC](https://store.dremc.com.au/products/20pc-t-slot-hammer-head-nuts) | in stock | verified |
| 20 series right-angle V-slot bracket, black | — | 8 | $3.30 | $26.40 | [RM Components](https://rmcomponents.com.au/products/20-series-right-angle-v-slot-bracket-black) | in stock | verified |
| M5 socket head cap screws CL12.9, 25 pc - one pack each of 8, 12 and 16 mm [^5] | 8 mm / 12 mm / 16 mm | 3 | $10.95 | $32.85 | [DREMC](https://store.dremc.com.au/products/m5-hex-socket-head-cap-screws-shcs-cl12-9-25pc) | in stock | verified |

**Subtotal: $240.25**

## B. X gantry

| Part | Option priced | Qty | Unit | Line | Source | Stock | Confidence |
|---|---|---:|---:|---:|---|---|---|
| LDO SLR12H / MGN12H stainless rail with carriage, 500 mm | 500mm / Z1 | 1 | $85.45 | $85.45 | [DREMC](https://store.dremc.com.au/products/ldo-slr12h-mgn12h-linear-rail-with-carriage) | in stock | verified |
| MGN12H carriage blocks, 5 extra (10 blocks in the model, 5 come with the rails) [^6] | — | 5 | $18.00 | $90.00 | — | — | estimate |
| LDO NEMA 17 42STH48-2504AC | — | 2 | $34.95 | $69.90 | [DREMC](https://store.dremc.com.au/products/ldo-nema-17-motor-ldo-42sth48-2504ac) | in stock | verified |
| Gates 2GT 20T pulley, 5 mm bore, 6 mm belt | 20T Pulley with 5mm bore 6mm Belt | 2 | $11.00 | $22.00 | [DREMC](https://store.dremc.com.au/products/ldo-2gt-pulleys) | in stock | verified |
| Gates 2GT 20T toothed idler, 6 mm | Toothed Idler 6mm 20 Teeth 5mm ID | 4 | $7.45 | $29.80 | [DREMC](https://store.dremc.com.au/products/ldo-gt2-2gt-20t-toothed-idler-6mm-wide) | in stock | verified |

**Subtotal: $297.15**

## C. Toolheads

| Part | Option priced | Qty | Unit | Line | Source | Stock | Confidence |
|---|---|---:|---:|---:|---|---|---|
| Trianglelab V6 hotend, pre-assembled, 24 V | Pre-Assembled | 2 | $45.00 | $90.00 | [DREMC](https://store.dremc.com.au/products/v6-hotend-pre-assembled-compatible-for-prusa-i3-mk3-s-trianglelab) | in stock | verified |
| LDO Orbiter v2.5 extruder, motor included | — | 2 | $105.45 | $210.90 | [DREMC](https://store.dremc.com.au/products/ldo-orbiter-v2-5-extruder) | in stock | verified |
| 5015 blower fan 24 V, part cooling | 2 Wire | 2 | $19.50 | $39.00 | [DREMC](https://store.dremc.com.au/products/5015-24v-blower-fan-by-dremc) | in stock | verified |
| 4010 axial fan 24 V, hotend heatsink [^7] | 3 wire (Tachometer Output) | 2 | $20.50 | $41.00 | [DREMC](https://store.dremc.com.au/products/4010-axial-fan-24v-by-dremc) | in stock | verified |

**Subtotal: $380.90**

## D. Y and bed

| Part | Option priced | Qty | Unit | Line | Source | Stock | Confidence |
|---|---|---:|---:|---:|---|---|---|
| LDO SLR12H / MGN12H stainless rail with carriage, 450 mm | 450mm / Z1 | 2 | $79.45 | $158.90 | [DREMC](https://store.dremc.com.au/products/ldo-slr12h-mgn12h-linear-rail-with-carriage) | in stock | verified |
| LDO NEMA 17 42STH48-2504AC | — | 1 | $34.95 | $34.95 | [DREMC](https://store.dremc.com.au/products/ldo-nema-17-motor-ldo-42sth48-2504ac) | in stock | verified |
| Gates 2GT 20T pulley, 5 mm bore, 6 mm belt | 20T Pulley with 5mm bore 6mm Belt | 1 | $11.00 | $11.00 | [DREMC](https://store.dremc.com.au/products/ldo-2gt-pulleys) | in stock | verified |
| Gates 2GT 20T toothed idler, 6 mm | Toothed Idler 6mm 20 Teeth 5mm ID | 1 | $7.45 | $7.45 | [DREMC](https://store.dremc.com.au/products/ldo-gt2-2gt-20t-toothed-idler-6mm-wide) | in stock | verified |
| Heated bed assembly, 255 x 245 mm, 24 V ~270 W (CR-6 SE) [^8] | — | 1 | $55.95 | $55.95 | [DREMC](https://store.dremc.com.au/products/heated-hot-bed-kit-for-cr-6-se) | in stock | verified |
| Magnetic sheet 235 x 235, high-temp 3M adhesive | 235x235 Ender 3 / 5 | 1 | $11.95 | $11.95 | [DREMC](https://store.dremc.com.au/products/magnetic-sheet-with-3m-adhesive) | in stock | verified |
| Light satin PEI spring steel plate, 235 x 235 | 235x235 K1/Ender 3 V3 | 1 | $36.45 | $36.45 | [DREMC](https://store.dremc.com.au/products/dremc-light-satin-pei-spring-steel-build-plate-3d-printers) | in stock | verified |
| Bed carrier bars - 6061 flat bar, 2 off at 235 x 35 x 5 mm [^9] | — | 1 | $24.20 | $24.20 | [RM Components](https://rmcomponents.com.au/products/6061-aluminium-flat-bar-6-x-50-mm-thickness-x-width-custom-length-available) | — | estimate |
| Silicone bed levelling spacers, 4 pc | — | 1 | $11.00 | $11.00 | [DREMC](https://store.dremc.com.au/products/4pc-heatbed-silicone-leveling-column-for-ender-3-and-cr-10-series) | in stock | verified |

**Subtotal: $351.85**

## E. Z axis

| Part | Option priced | Qty | Unit | Line | Source | Stock | Confidence |
|---|---|---:|---:|---:|---|---|---|
| 8 mm metric lead screw / ACME, 500 mm | — | 2 | $27.50 | $55.00 | [RM Components](https://rmcomponents.com.au/products/copy-of-t8-8mm-lead-screw-please-select-the-length-you-require-1) | in stock | verified |
| POM lead screw nut with anti-backlash nut, TR8x8 | TR8X8 Square | 2 | $5.55 | $11.10 | [DREMC](https://store.dremc.com.au/products/dremc-pom-lead-screw-nuts-with-anti-backlash-nut) | in stock | verified |
| LDO SLR12H / MGN12H stainless rail with carriage, 400 mm [^10] | 400mm / Z1 | 2 | $69.45 | $138.90 | [DREMC](https://store.dremc.com.au/products/ldo-slr12h-mgn12h-linear-rail-with-carriage) | in stock | verified |
| LDO NEMA 17 42STH48-2504AC | — | 1 | $34.95 | $34.95 | [DREMC](https://store.dremc.com.au/products/ldo-nema-17-motor-ldo-42sth48-2504ac) | in stock | verified |
| Gates 2GT 20T pulley, 8 mm bore, 6 mm belt - one on each lead screw | 20T Pulley with 8mm bore 6mm Belt | 2 | $11.00 | $22.00 | [DREMC](https://store.dremc.com.au/products/ldo-2gt-pulleys) | in stock | verified |
| Gates 2GT 20T pulley, 5 mm bore, 6 mm belt - Z motor | 20T Pulley with 5mm bore 6mm Belt | 1 | $11.00 | $11.00 | [DREMC](https://store.dremc.com.au/products/ldo-2gt-pulleys) | in stock | verified |
| Gates 2GT 20T toothed idler, 6 mm - Z link belt tensioners | Toothed Idler 6mm 20 Teeth 5mm ID | 2 | $7.45 | $14.90 | [DREMC](https://store.dremc.com.au/products/ldo-gt2-2gt-20t-toothed-idler-6mm-wide) | in stock | verified |
| F688Z flange bearing 8x16x5, 2 pc per pack - screw end supports [^11] | — | 2 | $6.00 | $12.00 | [DREMC](https://store.dremc.com.au/products/f688z-flange-deep-groove-ball-bearing-8x16x5mm) | in stock | verified |

**Subtotal: $299.85**

## F. Belt stock

| Part | Option priced | Qty | Unit | Line | Source | Stock | Confidence |
|---|---|---:|---:|---:|---|---|---|
| Gates Powergrip RF 2GT 6 mm timing belt, 6 m | 6000mm (6m) | 1 | $59.00 | $59.00 | [DREMC](https://store.dremc.com.au/products/gates-powergrip%C2%AE-rf-2gt-6mm-timing-belt) | in stock | verified |

**Subtotal: $59.00**

## G. Electronics

| Part | Option priced | Qty | Unit | Line | Source | Stock | Confidence |
|---|---|---:|---:|---:|---|---|---|
| BigTreeTech Octopus Pro V1.1 (H723) - 8 driver slots | — | 1 | $115.00 | $115.00 | [DREMC](https://store.dremc.com.au/products/bigtreetech-octopus-pro-v1-1-h723-chip) | in stock | verified |
| BigTreeTech TMC2209 V1.3 stepper drivers, 8 pack | 8x | 1 | $79.45 | $79.45 | [DREMC](https://store.dremc.com.au/products/bigtreetech-tmc2209-v1-3-stepper-motor-driver) | in stock | verified |
| Mean Well LRS-350-24 - bed supply, 270 W of 350 W | — | 1 | $74.65 | $74.65 | [DREMC](https://store.dremc.com.au/products/mean-well-lrs-350-24-24v-350w-power-supply) | in stock | verified |
| Mean Well LRS-200-24 - motion, hotends and logic, 142 W of 211 W [^12] | — | 1 | $69.00 | $69.00 | [DREMC](https://store.dremc.com.au/products/mean-well-lrs-200-24-24v-8-8a-enclosed-power-suply) | in stock | verified |
| Raspberry Pi 4 Model B, 2 GB - runs Klipper over USB [^13] | — | 1 | $109.33 | $109.33 | [Core Electronics](https://core-electronics.com.au/raspberry-pi-4-model-b-2gb.html) | in stock | verified |
| Official Raspberry Pi 4 USB-C power supply, 5.1 V 15.3 W | — | 1 | $11.90 | $11.90 | [Core Electronics](https://core-electronics.com.au/raspberry-pi-4-official-power-supply-usb-c-5v-15w-white.html) | in stock | verified |
| Official Raspberry Pi 64 GB A2 micro SD card [^14] | — | 1 | $47.50 | $47.50 | [Core Electronics](https://core-electronics.com.au/raspberry-pi-a2-class-sd-card-64-gb.html) | in stock | verified |
| Omron D2F-5L endstop switch | — | 4 | $5.45 | $21.80 | [DREMC](https://store.dremc.com.au/products/omron-d2f-5l-switch) | in stock | verified |
| ADXL345 accelerometer, 3 axis - shared, for input shaping [^15] | — | 1 | $4.95 | $4.95 | [DREMC](https://store.dremc.com.au/products/adxl345-accelerometer-3-axis-gy-291) | in stock | verified |
| Wago 221-413 lever terminal block, 3 way | 221-413 3 Way | 6 | $2.95 | $17.70 | [DREMC](https://store.dremc.com.au/products/wago-221-series-terminal-block) | in stock | verified |
| Wiring, ferrules, IEC inlet with switch and fuse, drag chain, sleeving | — | 1 | $70.00 | $70.00 | — | — | estimate |

**Subtotal: $621.28**

## Total

| Sub-assembly | Subtotal |
|---|---:|
| A. Frame | $240.25 |
| B. X gantry | $297.15 |
| C. Toolheads | $380.90 |
| D. Y and bed | $351.85 |
| E. Z axis | $299.85 |
| F. Belt stock | $59.00 |
| G. Electronics | $621.28 |
| **Total** | **$2250.28** |

Of that, $1917.08 is verified against live supplier data and $333.20 is estimated across 6 lines (extrusion and flat bar cut to length, the extra carriage blocks, and loose wiring).
Anything already on hand comes off the top.

## 24 V power budget

A single 350 W supply does not fit this machine: two hotends and a 270 W bed come to
411.6 W. The bed therefore gets its own supply, and no supply is loaded
past 80% of its rating.

| Load | Qty | W each | Total W | Rail | Where the figure comes from |
|---|---:|---:|---:|---|---|
| Heated bed, CR-6 SE 24 V assembly | 1 | 270 | 270.0 | bed | supplier listing: 24V ~270W |
| V6 hotend heater cartridge | 2 | 40 | 80.0 | motion | E3D V6 24 V cartridge rating |
| NEMA 17 via TMC2209 | 6 | 8 | 48.0 | motion | estimate at 1.2 A RMS, 1 ohm per phase, plus driver loss |
| 5015 part cooling blower | 2 | 2.8 | 5.6 | motion | 0.12 A at 24 V |
| 4010 hotend fan | 2 | 1.5 | 3.0 | motion | 0.06 A at 24 V |
| Octopus Pro board, drivers idle | 1 | 5 | 5.0 | motion | estimate |

| Supply | Rating | Load | Loaded |
|---|---:|---:|---:|
| Mean Well LRS-350-24 (bed) | 350 W | 270.0 W | 77% |
| Mean Well LRS-200-24 (motion) | 211 W | 141.6 W | 67% |

The Raspberry Pi runs from its own 5 V USB-C supply, not the 24 V rails.

## Not costed here

- Individual screws and T-nuts beyond the packs listed.
- Printed parts: motor mounts, idler brackets, belt clamps, carriage bodies, Z nut mounts. Free to make, but they have to be designed.
- A bed probe.
- An enclosure.

## Known sourcing gaps

- **MGN12H carriage blocks** are the one real gap. The model needs 10; the five rails bring five. The only Australian listing found is [HIWIN Precision H at $105.00](https://store.dremc.com.au/products/hiwin-mgn12h-carriage-block), out of stock. Either buy five more overseas, or buy five 300 mm rail-and-carriage sets at $55.95 and keep the spare rails.
- **Extrusion and flat bar are cut to length**, and neither supplier publishes a per-mm rate on the storefront — the calculator on the RM Components listing returns $0.00 — so those four lines need a quote.
- **The 235 x 235 heated bed is gone from both DREMC listings.** The 255 x 245 CR-6 SE assembly is in stock and is what the model now uses; it carries the 235 sheets with margin to spare.
- Several in-stock-today choices are a second pick: the 2-wire 4010 fan, 10 mm M5 screws, the 32 GB SD card and the 350 mm Z rail were all out of stock, so the BOM takes the next option up.

[^1]: A. Frame — 4040 V-slot black (20 series) - 2 x 500 uprights + 2 x 530 base rails = 2.06 m: cut to length; the storefront calculator publishes no per-mm rate, so ask for a quote.
[^2]: A. Frame — 2040 V-slot black - 2 x 520 top tie and X beam + 2 x 440 base cross = 1.92 m: cut to length, as above.
[^3]: A. Frame — 2020 V-slot black - 2 x 530 bed rails = 1.06 m: cut to length, as above.
[^4]: A. Frame — M5 drop-in T-slot nuts, 20 pc: RM Components list an M5 20-series drop-in spring T-nut 20 pc at $5.49 if you are already ordering extrusion there.
[^5]: A. Frame — M5 socket head cap screws CL12.9, 25 pc - one pack each of 8, 12 and 16 mm: the 10 mm length was out of stock.
[^6]: B. X gantry — MGN12H carriage blocks, 5 extra (10 blocks in the model, 5 come with the rails): AliExpress. The only Australian listing found is HIWIN Precision H at $105.00 each, out of stock; a 300 mm LDO rail-and-carriage set at $55.95 is the in-stock local fallback.
[^7]: C. Toolheads — 4010 axial fan 24 V, hotend heatsink: the 2-wire version is $19.50 but was out of stock.
[^8]: D. Y and bed — Heated bed assembly, 255 x 245 mm, 24 V ~270 W (CR-6 SE): replaces the 235 x 235 Ender 3 bed, which is out of stock at both DREMC listings. Bigger than the 235 print area, so it carries the sheets with margin.
[^9]: D. Y and bed — Bed carrier bars - 6061 flat bar, 2 off at 235 x 35 x 5 mm: nearest stocked section is 6 x 50 mm, cut and trimmed to 35 x 5; price is the listing base, not a quote.
[^10]: E. Z axis — LDO SLR12H / MGN12H stainless rail with carriage, 400 mm: 350 mm would also fit but is out of stock; 400 mm gives 355 mm of Z travel against a 230 mm build.
[^11]: E. Z axis — F688Z flange bearing 8x16x5, 2 pc per pack - screw end supports: 4 bearings in the model, 2 per pack.
[^12]: G. Electronics — Mean Well LRS-200-24 - motion, hotends and logic, 142 W of 211 W: second supply added after the 24 V budget came to 412 W: two hotends and a 270 W bed do not fit one 350 W unit.
[^13]: G. Electronics — Raspberry Pi 4 Model B, 2 GB - runs Klipper over USB: Pi 5 2 GB is $125.52 and is not needed for Klipper.
[^14]: G. Electronics — Official Raspberry Pi 64 GB A2 micro SD card: the 32 GB card is $32.18 but was out of stock.
[^15]: G. Electronics — ADXL345 accelerometer, 3 axis - shared, for input shaping: one only, moved between toolheads; the earlier BOM counted it twice.
