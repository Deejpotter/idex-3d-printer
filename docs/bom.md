# Bill of materials

All prices **AUD inc GST**, read from supplier product data on **2026-11-11**.

- **verified** — price, option and stock read from the supplier’s own live product data on that date.
- **estimate** — my own figure. A placeholder, not a quote.

Every "verified" line was read from the supplier's own live product data on the date above, including the variant named in the Option column and its stock state. "estimate" is my own figure and is not a quote.

## The overseas column

Every line was also priced on **AliExpress** on **2026-11-12**, in a logged-out
Australian session, with the named option selected on the listing page.

AliExpress lines were read in a logged-out Australian session on the date above, with the named variant selected on the listing page. Two prices are recorded: the listing’s LIST price, which is what the BOM totals, and the SALE price showing that day. The sale prices are not safe to total - a first-order voucher floors them at A$1.49, so a 5 m and a 10 m belt both showed A$1.49, and the discount does not repeat on a second order. All AliExpress prices EXCLUDE GST ("Tax excluded, add at checkout") and shipping, where the Australian column is GST-inclusive and delivered. "read" says how firm each figure is: variant = the exact option was selected on the listing and the price read off it; listing = a fixed-spec listing with no ambiguous option; band = taken across several listings, not pinned to one variant.

Every cut length and part count is listed against its CAD component in `docs/bom.json`.
`scripts/check_model.py` check 11 measures those components in the model and fails if a
length, a count or a stocked size disagrees; check 12 adds up the 24 V load against the
power supplies. Edit `bom.json`, then run `node scripts/genbom.js`.

## A. Frame

| Part | Option priced | Qty | Line | Source | Stock | Conf. | AliExpress | Read as |
|---|---|---:|---:|---|---|---|---:|---|
| 4040 V-slot black (20 series) - 2 x 500 uprights + 2 x 530 base rails = 2.06 m [^1] | — | 1 | $90.00 | [RM Components](https://rmcomponents.com.au/products/copy-of-2020-silver-t-slot-aluminium-profile-20-series) | — | estimate | — | cut-to-length metal: too heavy to ship economically |
| 2040 V-slot black - 2 x 520 top tie and X beam + 2 x 440 base cross = 1.92 m [^2] | — | 1 | $44.00 | [RM Components](https://rmcomponents.com.au/products/2040-black-v-slot-aluminium-profile-20-series) | — | estimate | — | cut-to-length metal: too heavy to ship economically |
| 2020 V-slot black - 2 x 530 bed rails = 1.06 m [^3] | — | 1 | $15.00 | [RM Components](https://rmcomponents.com.au/products/2020-black-v-slot-aluminium-profile-20-series) | — | estimate | — | cut-to-length metal: too heavy to ship economically |
| M5 drop-in T-slot nuts, 20 pc [^4] | M5 | 4 | $32.00 | [DREMC](https://store.dremc.com.au/products/20pc-t-slot-hammer-head-nuts) | in stock | verified | — | cheaper or equal locally, or wanted next week rather than next month |
| 20 series right-angle V-slot bracket, black | — | 8 | $26.40 | [RM Components](https://rmcomponents.com.au/products/20-series-right-angle-v-slot-bracket-black) | in stock | verified | — | cheaper or equal locally, or wanted next week rather than next month |
| M5 socket head cap screws CL12.9, 25 pc - one pack each of 8, 12 and 16 mm [^5] | 8 mm / 12 mm / 16 mm | 3 | $32.85 | [DREMC](https://store.dremc.com.au/products/m5-hex-socket-head-cap-screws-shcs-cl12-9-25pc) | in stock | verified | — | cheaper or equal locally, or wanted next week rather than next month |

**Subtotal: $240.25** locally, **$240.25** buying overseas where it wins.

## B. X gantry

| Part | Option priced | Qty | Line | Source | Stock | Conf. | AliExpress | Read as |
|---|---|---:|---:|---|---|---|---:|---|
| LDO SLR12H / MGN12H stainless rail with carriage, 500 mm | 500mm / Z1 | 1 | $85.45 | [DREMC](https://store.dremc.com.au/products/ldo-slr12h-mgn12h-linear-rail-with-carriage) | in stock | verified | [$38.01](https://www.aliexpress.com/item/1005004908405311.html) | variant [^a1] |
| MGN12H carriage blocks, 5 extra (10 blocks in the model, 5 come with the rails) [^6] | — | 5 | $90.00 | — | — | estimate | [$66.25](https://www.aliexpress.com/item/1005004908405311.html) | variant [^a2] |
| LDO NEMA 17 42STH48-2504AC | — | 2 | $69.90 | [DREMC](https://store.dremc.com.au/products/ldo-nema-17-motor-ldo-42sth48-2504ac) | in stock | verified | [$49.94](https://www.aliexpress.com/item/1005008382622751.html) | listing, STEPPERONLINE [^a3] |
| Gates 2GT 20T pulley, 5 mm bore, 6 mm belt | 20T Pulley with 5mm bore 6mm Belt | 2 | $22.00 | [DREMC](https://store.dremc.com.au/products/ldo-2gt-pulleys) | in stock | verified | [$8.10](https://www.aliexpress.com/item/1005006217674592.html) | variant |
| Gates 2GT 20T toothed idler, 6 mm [^7] | Toothed Idler 6mm 20 Teeth 5mm ID | 2 | $14.90 | [DREMC](https://store.dremc.com.au/products/ldo-gt2-2gt-20t-toothed-idler-6mm-wide) | in stock | verified | [$4.04](https://www.aliexpress.com/item/32817328238.html) | variant [^a4] |

**Subtotal: $282.25** locally, **$166.34** buying overseas where it wins.

## C. Toolheads

| Part | Option priced | Qty | Line | Source | Stock | Conf. | AliExpress | Read as |
|---|---|---:|---:|---|---|---|---:|---|
| Trianglelab V6 hotend, pre-assembled, 24 V | Pre-Assembled | 2 | $90.00 | [DREMC](https://store.dremc.com.au/products/v6-hotend-pre-assembled-compatible-for-prusa-i3-mk3-s-trianglelab) | in stock | verified | [$49.52](https://www.aliexpress.com/item/4000289104191.html) | variant [^a5] |
| LDO Orbiter v2.5 extruder, motor included | — | 2 | $210.90 | [DREMC](https://store.dremc.com.au/products/ldo-orbiter-v2-5-extruder) | in stock | verified | ~~$338.94~~ dearer | listing, Mellow [^a6] |
| 5015 blower fan 24 V, part cooling | 2 Wire | 2 | $39.00 | [DREMC](https://store.dremc.com.au/products/5015-24v-blower-fan-by-dremc) | in stock | verified | [$20.20](https://www.aliexpress.com/item/1005007527291283.html) | listing, Mellow [^a7] |
| 4010 axial fan 24 V, hotend heatsink [^8] | 3 wire (Tachometer Output) | 2 | $41.00 | [DREMC](https://store.dremc.com.au/products/4010-axial-fan-24v-by-dremc) | in stock | verified | [$12.00](https://www.aliexpress.com/item/1005009510109669.html) | band, Creality [^a8] |

**Subtotal: $380.90** locally, **$292.62** buying overseas where it wins.

## D. Y and bed

| Part | Option priced | Qty | Line | Source | Stock | Conf. | AliExpress | Read as |
|---|---|---:|---:|---|---|---|---:|---|
| LDO SLR12H / MGN12H stainless rail with carriage, 450 mm | 450mm / Z1 | 2 | $158.90 | [DREMC](https://store.dremc.com.au/products/ldo-slr12h-mgn12h-linear-rail-with-carriage) | in stock | verified | [$69.20](https://www.aliexpress.com/item/1005004908405311.html) | variant |
| LDO NEMA 17 42STH48-2504AC | — | 1 | $34.95 | [DREMC](https://store.dremc.com.au/products/ldo-nema-17-motor-ldo-42sth48-2504ac) | in stock | verified | [$24.97](https://www.aliexpress.com/item/1005008382622751.html) | listing, STEPPERONLINE |
| Gates 2GT 20T pulley, 5 mm bore, 6 mm belt | 20T Pulley with 5mm bore 6mm Belt | 1 | $11.00 | [DREMC](https://store.dremc.com.au/products/ldo-2gt-pulleys) | in stock | verified | [$4.05](https://www.aliexpress.com/item/1005006217674592.html) | variant |
| Gates 2GT 20T toothed idler, 6 mm | Toothed Idler 6mm 20 Teeth 5mm ID | 1 | $7.45 | [DREMC](https://store.dremc.com.au/products/ldo-gt2-2gt-20t-toothed-idler-6mm-wide) | in stock | verified | [$2.02](https://www.aliexpress.com/item/32817328238.html) | variant |
| Heated bed assembly, 255 x 245 mm, 24 V ~270 W (CR-6 SE) [^9] | — | 1 | $55.95 | [DREMC](https://store.dremc.com.au/products/heated-hot-bed-kit-for-cr-6-se) | in stock | verified | [$28.99](https://www.aliexpress.com/item/1005008388623164.html) | variant [^a9] |
| Magnetic sheet 235 x 235, high-temp 3M adhesive | 235x235 Ender 3 / 5 | 1 | $11.95 | [DREMC](https://store.dremc.com.au/products/magnetic-sheet-with-3m-adhesive) | in stock | verified | [$29.39](https://www.aliexpress.com/item/1005009531110545.html) | listing [^a10] |
| Light satin PEI spring steel plate, 235 x 235 | 235x235 K1/Ender 3 V3 | 1 | $36.45 | [DREMC](https://store.dremc.com.au/products/dremc-light-satin-pei-spring-steel-build-plate-3d-printers) | in stock | verified | in the line above | included in the AliExpress line for "Magnetic sheet 235 x 235, high-temp 3M adhesive" |
| Bed carrier bars - 6061 flat bar, 2 off at 235 x 35 x 5 mm [^10] | — | 1 | $24.20 | [RM Components](https://rmcomponents.com.au/products/6061-aluminium-flat-bar-6-x-50-mm-thickness-x-width-custom-length-available) | — | estimate | — | cut-to-length metal: too heavy to ship economically |
| Silicone bed levelling spacers, 4 pc | — | 1 | $11.00 | [DREMC](https://store.dremc.com.au/products/4pc-heatbed-silicone-leveling-column-for-ender-3-and-cr-10-series) | in stock | verified | — | cheaper or equal locally, or wanted next week rather than next month |

**Subtotal: $351.85** locally, **$193.82** buying overseas where it wins.

## E. Z axis

| Part | Option priced | Qty | Line | Source | Stock | Conf. | AliExpress | Read as |
|---|---|---:|---:|---|---|---|---:|---|
| 8 mm metric lead screw / ACME, 500 mm | — | 2 | $55.00 | [RM Components](https://rmcomponents.com.au/products/copy-of-t8-8mm-lead-screw-please-select-the-length-you-require-1) | in stock | verified | [$27.22](https://www.aliexpress.com/item/1005010553221988.html) | variant [^a11] |
| POM lead screw nut with anti-backlash nut, TR8x8 | TR8X8 Square | 2 | $11.10 | [DREMC](https://store.dremc.com.au/products/dremc-pom-lead-screw-nuts-with-anti-backlash-nut) | in stock | verified | in the line above | included in the AliExpress line for "8 mm metric lead screw / ACME, 500 mm" |
| LDO SLR12H / MGN12H stainless rail with carriage, 400 mm [^11] | 400mm / Z1 | 2 | $138.90 | [DREMC](https://store.dremc.com.au/products/ldo-slr12h-mgn12h-linear-rail-with-carriage) | in stock | verified | [$62.38](https://www.aliexpress.com/item/1005004908405311.html) | variant |
| LDO NEMA 17 42STH48-2504AC | — | 1 | $34.95 | [DREMC](https://store.dremc.com.au/products/ldo-nema-17-motor-ldo-42sth48-2504ac) | in stock | verified | [$24.97](https://www.aliexpress.com/item/1005008382622751.html) | listing, STEPPERONLINE |
| Gates 2GT 20T pulley, 8 mm bore, 6 mm belt - one on each lead screw | 20T Pulley with 8mm bore 6mm Belt | 2 | $22.00 | [DREMC](https://store.dremc.com.au/products/ldo-2gt-pulleys) | in stock | verified | [$8.54](https://www.aliexpress.com/item/1005006217674592.html) | variant [^a12] |
| Gates 2GT 20T pulley, 5 mm bore, 6 mm belt - Z motor | 20T Pulley with 5mm bore 6mm Belt | 1 | $11.00 | [DREMC](https://store.dremc.com.au/products/ldo-2gt-pulleys) | in stock | verified | [$4.05](https://www.aliexpress.com/item/1005006217674592.html) | variant |
| Gates 2GT 20T toothed idler, 6 mm - Z link belt tensioners | Toothed Idler 6mm 20 Teeth 5mm ID | 2 | $14.90 | [DREMC](https://store.dremc.com.au/products/ldo-gt2-2gt-20t-toothed-idler-6mm-wide) | in stock | verified | [$4.04](https://www.aliexpress.com/item/32817328238.html) | variant |
| F688Z flange bearing 8x16x5, 2 pc per pack - screw end supports [^12] | — | 2 | $12.00 | [DREMC](https://store.dremc.com.au/products/f688z-flange-deep-groove-ball-bearing-8x16x5mm) | in stock | verified | [$5.50](https://www.aliexpress.com/item/10000116112946.html) | band [^a13] |

**Subtotal: $299.85** locally, **$136.70** buying overseas where it wins.

## F. Belt stock

| Part | Option priced | Qty | Line | Source | Stock | Conf. | AliExpress | Read as |
|---|---|---:|---:|---|---|---|---:|---|
| Gates Powergrip RF 2GT 6 mm timing belt, 6 m | 6000mm (6m) | 1 | $59.00 | [DREMC](https://store.dremc.com.au/products/gates-powergrip%C2%AE-rf-2gt-6mm-timing-belt) | in stock | verified | [$9.19](https://www.aliexpress.com/item/1005008463979470.html) | variant [^a14] |

**Subtotal: $59.00** locally, **$9.19** buying overseas where it wins.

## G. Electronics

| Part | Option priced | Qty | Line | Source | Stock | Conf. | AliExpress | Read as |
|---|---|---:|---:|---|---|---|---:|---|
| BigTreeTech Octopus Pro V1.1 (H723) - 8 driver slots | — | 1 | $115.00 | [DREMC](https://store.dremc.com.au/products/bigtreetech-octopus-pro-v1-1-h723-chip) | in stock | verified | ~~$211.22~~ dearer | variant, BigTreeTech [^a15] |
| BigTreeTech TMC2209 V1.3 stepper drivers, 8 pack | 8x | 1 | $79.45 | [DREMC](https://store.dremc.com.au/products/bigtreetech-tmc2209-v1-3-stepper-motor-driver) | in stock | verified | in the line above | included in the AliExpress line for "BigTreeTech Octopus Pro V1.1 (H723) - 8 driver slots" |
| Mean Well LRS-350-24 - bed supply, 270 W of 350 W | — | 1 | $74.65 | [DREMC](https://store.dremc.com.au/products/mean-well-lrs-350-24-24v-350w-power-supply) | in stock | verified | — | mains-side part: a no-name supply or IEC inlet behind a 270 W bed is not worth the saving |
| Mean Well LRS-200-24 - motion, hotends and logic, 142 W of 211 W [^13] | — | 1 | $69.00 | [DREMC](https://store.dremc.com.au/products/mean-well-lrs-200-24-24v-8-8a-enclosed-power-suply) | in stock | verified | — | mains-side part: a no-name supply or IEC inlet behind a 270 W bed is not worth the saving |
| Raspberry Pi 4 Model B, 2 GB - runs Klipper over USB [^14] | — | 1 | $109.33 | [Core Electronics](https://core-electronics.com.au/raspberry-pi-4-model-b-2gb.html) | in stock | verified | — | cheaper or equal locally, or wanted next week rather than next month |
| Official Raspberry Pi 4 USB-C power supply, 5.1 V 15.3 W | — | 1 | $11.90 | [Core Electronics](https://core-electronics.com.au/raspberry-pi-4-official-power-supply-usb-c-5v-15w-white.html) | in stock | verified | — | cheaper or equal locally, or wanted next week rather than next month |
| Official Raspberry Pi 64 GB A2 micro SD card [^15] | — | 1 | $47.50 | [Core Electronics](https://core-electronics.com.au/raspberry-pi-a2-class-sd-card-64-gb.html) | in stock | verified | — | cheaper or equal locally, or wanted next week rather than next month |
| Omron D2F-5L endstop switch | — | 4 | $21.80 | [DREMC](https://store.dremc.com.au/products/omron-d2f-5l-switch) | in stock | verified | [$5.81](https://www.aliexpress.com/item/1005006964029745.html) | band [^a16] |
| ADXL345 accelerometer, 3 axis - shared, for input shaping [^16] | — | 1 | $4.95 | [DREMC](https://store.dremc.com.au/products/adxl345-accelerometer-3-axis-gy-291) | in stock | verified | — | cheaper or equal locally, or wanted next week rather than next month |
| Wago 221-413 lever terminal block, 3 way | 221-413 3 Way | 6 | $17.70 | [DREMC](https://store.dremc.com.au/products/wago-221-series-terminal-block) | in stock | verified | — | cheaper or equal locally, or wanted next week rather than next month |
| Wiring, ferrules, IEC inlet with switch and fuse, drag chain, sleeving | — | 1 | $70.00 | — | — | estimate | — | mains-side part: a no-name supply or IEC inlet behind a 270 W bed is not worth the saving |

**Subtotal: $621.28** locally, **$605.29** buying overseas where it wins.

## Total

| Sub-assembly | Australian retail | Overseas where it wins |
|---|---:|---:|
| A. Frame | $240.25 | $240.25 |
| B. X gantry | $282.25 | $166.34 |
| C. Toolheads | $380.90 | $292.62 |
| D. Y and bed | $351.85 | $193.82 |
| E. Z axis | $299.85 | $136.70 |
| F. Belt stock | $59.00 | $9.19 |
| G. Electronics | $621.28 | $605.29 |
| **Total** | **$2235.38** | **$1644.21** |

Buying everything from Australian stock costs **$2235.38**, GST included and
delivered. Taking the overseas line wherever it is cheaper brings the parts to **$1644.21**, of which $1085.83 is still bought here. AliExpress
prices exclude GST, so add about $55.84 at checkout: call it **$1700.05** all up, plus whatever shipping applies.

Those AliExpress figures are **list** prices. On 2026-11-12 the same basket
rang up at $1135.48 on sale — but part of that gap is a first-order voucher
that does not repeat, so the list column is the one to plan against. See
`docs/budget-build.md`.

Of that, $1902.18 is verified against live supplier data and $333.20 is estimated across 6 lines (extrusion and flat bar cut to length, the extra carriage blocks, and loose wiring).
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
[^7]: B. X gantry — Gates 2GT 20T toothed idler, 6 mm: one idler per X belt: each belt loops from its motor pulley to a single idler at the far end, and that one idler turns both runs. The BOM said 4 until check 13 counted the model..
[^8]: C. Toolheads — 4010 axial fan 24 V, hotend heatsink: the 2-wire version is $19.50 but was out of stock.
[^9]: D. Y and bed — Heated bed assembly, 255 x 245 mm, 24 V ~270 W (CR-6 SE): replaces the 235 x 235 Ender 3 bed, which is out of stock at both DREMC listings. Bigger than the 235 print area, so it carries the sheets with margin.
[^10]: D. Y and bed — Bed carrier bars - 6061 flat bar, 2 off at 235 x 35 x 5 mm: nearest stocked section is 6 x 50 mm, cut and trimmed to 35 x 5; price is the listing base, not a quote.
[^11]: E. Z axis — LDO SLR12H / MGN12H stainless rail with carriage, 400 mm: 350 mm would also fit but is out of stock; 400 mm gives 355 mm of Z travel against a 230 mm build.
[^12]: E. Z axis — F688Z flange bearing 8x16x5, 2 pc per pack - screw end supports: 4 bearings in the model, 2 per pack.
[^13]: G. Electronics — Mean Well LRS-200-24 - motion, hotends and logic, 142 W of 211 W: second supply added after the 24 V budget came to 412 W: two hotends and a 270 W bed do not fit one 350 W unit.
[^14]: G. Electronics — Raspberry Pi 4 Model B, 2 GB - runs Klipper over USB: Pi 5 2 GB is $125.52 and is not needed for Klipper.
[^15]: G. Electronics — Official Raspberry Pi 64 GB A2 micro SD card: the 32 GB card is $32.18 but was out of stock.
[^16]: G. Electronics — ADXL345 accelerometer, 3 axis - shared, for input shaping: one only, moved between toolheads; the earlier BOM counted it twice.
[^a1]: AliExpress, LDO SLR12H / MGN12H stainless rail with carriage, 500 mm: generic, not LDO; 4.7 over 130 reviews, 2,000+ sold. Reviewers all say to degrease and re-grease before use.
[^a2]: AliExpress, MGN12H carriage blocks, 5 extra (10 blocks in the model, 5 come with the rails): this closes the one real sourcing gap - no Australian listing has these in stock.
[^a3]: AliExpress, LDO NEMA 17 42STH48-2504AC: 2.0 A against the LDO part’s 2.5 A, same 48 mm body and ~59 N.cm holding torque; buy the 5-pack, the machine needs 5.
[^a4]: AliExpress, Gates 2GT 20T toothed idler, 6 mm: bore 3 mm, not 5 mm - the bracket has to suit, or pay ~A$3.50 for the 5 mm-bore listing.
[^a5]: AliExpress, Trianglelab V6 hotend, pre-assembled, 24 V: only 9 reviews, and one reports a 24 V cartridge shipped against a 12 V order - check what arrives.
[^a6]: AliExpress, LDO Orbiter v2.5 extruder, motor included: list price is ABOVE the Australian one, so only the sale price wins. 5.0 over 101 reviews, 1,000+ sold. Lesson 4 says not to buy these at all: the Titan already owned costs nothing, and the bed limits the machine either way.
[^a7]: AliExpress, 5015 blower fan 24 V, part cooling: the named-brand fan; no-name 5015s are about a third of this.
[^a8]: AliExpress, 4010 axial fan 24 V, hotend heatsink: read as a band across four listings, not pinned to one variant.
[^a9]: AliExpress, Heated bed assembly, 255 x 245 mm, 24 V ~270 W (CR-6 SE): NOT the same part: 235 x 235 against 255 x 245, and a bare plate rather than an assembly. Taking it costs 20 mm of build_x and 10 mm of build_y. No 255 x 245 heated bed was found on AliExpress at all.
[^a10]: AliExpress, Magnetic sheet 235 x 235, high-temp 3M adhesive: one line replaces two: magnet plus sheet. Three sellers quote 255 x 245 at exactly A$29.39, and it is textured both sides.
[^a11]: AliExpress, 8 mm metric lead screw / ACME, 500 mm: includes a nut, so it replaces the nut line too - but a plain brass nut, not the POM anti-backlash nut. Add ~A$5 each for anti-backlash, or accept Z backlash.
[^a12]: AliExpress, Gates 2GT 20T pulley, 8 mm bore, 6 mm belt - one on each lead screw: the 8 mm bore the model still shows as a 6.35 mm stand-in.
[^a13]: AliExpress, F688Z flange bearing 8x16x5, 2 pc per pack - screw end supports: a 10-pack covers both packs the BOM lists; read as a band.
[^a14]: AliExpress, Gates Powergrip RF 2GT 6 mm timing belt, 6 m: 10 m for a sixth of the price of 6 m of Gates. Not Gates Powergrip: core material and tooth form are the seller’s word.
[^a15]: AliExpress, BigTreeTech Octopus Pro V1.1 (H723) - 8 driver slots: the bundle covers the driver line as well. 4.9 over 54 ratings, 1,000+ sold. Board alone is A$160.79 list / A$58.94 on sale.
[^a16]: AliExpress, Omron D2F-5L endstop switch: a 5-pack covers all four axes; not an Omron switch. Read as a band.
