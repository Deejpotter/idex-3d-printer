# Bill of materials

All prices **AUD including GST**, read from supplier product data on **11 November 2026**.

- **verified** — price and stock read from the supplier’s own live product data.
- **estimate** — my own figure. A placeholder, not a quote.

Quantities come from the parametric Fusion model. The frame is 520 mm wide because the
IDEX carriages carry two MGN12H blocks each — see [design-notes.md](design-notes.md) §4.

Every cut length and part count below is listed against its CAD component in
`docs/bom.json` (`cuts`). `scripts/check_model.py` check 11 measures those components in
the model and fails if a length, a count or a stocked size disagrees. Edit `bom.json`,
then run `node scripts/genbom.js`.

## A. Frame

| Part | Qty | Unit | Line | Source | Confidence |
|---|---:|---:|---:|---|---|
| 4040 V-slot black - 2 x 500 (uprights) + 2 x 530 (base rails) = 2.06 m | 1 | $90.00 | $90.00 | [RM Components](https://rmcomponents.com.au/products/copy-of-2020-silver-t-slot-aluminium-profile-20-series) | estimate |
| 2040 V-slot black - 2 x 520 (top tie, X beam) + 2 x 440 (base cross) = 1.92 m | 1 | $44.00 | $44.00 | [RM Components](https://rmcomponents.com.au/products/2040-black-v-slot-aluminium-profile-20-series) | estimate |
| 2020 V-slot black - 2 x 530 (bed rails) = 1.06 m | 1 | $15.00 | $15.00 | [RM Components](https://rmcomponents.com.au/products/2020-black-v-slot-aluminium-profile-20-series) | estimate |
| M5 drop-in T-nuts, 20 pc | 4 | $8.00 | $32.00 | [DREMC](https://store.dremc.com.au/products/20pc-t-slot-hammer-head-nuts) | verified |
| Black angle corner connector (2020 ends only) | 8 | $4.50 | $36.00 | — | estimate |
| M5 button screws, 8/12/16/20 mm assortment | 1 | $25.00 | $25.00 | — | estimate |

**Subtotal: $242.00**

## B. X gantry

| Part | Qty | Unit | Line | Source | Confidence |
|---|---:|---:|---:|---|---|
| LDO SLR12H MGN12H rail + 1 carriage, 500 mm Z1 | 1 | $85.45 | $85.45 | [DREMC](https://store.dremc.com.au/products/ldo-slr12h-mgn12h-linear-rail-with-carriage) | verified |
| Extra MGN12H carriage blocks (3 more for 2 x 2-block carriages) | 3 | $15.00 | $45.00 | — | estimate, AliExpress |
| LDO NEMA 17 42STH48-2504AC | 2 | $34.95 | $69.90 | [DREMC](https://store.dremc.com.au/products/ldo-nema-17-motor-ldo-42sth48-2504ac) | verified |
| Gates 2GT 20T pulley, 5 mm bore, 6 mm belt | 2 | $11.00 | $22.00 | [DREMC](https://store.dremc.com.au/products/ldo-2gt-pulleys) | verified |
| Gates 2GT 20T toothed idler, 6 mm | 4 | $7.45 | $29.80 | [DREMC](https://store.dremc.com.au/products/ldo-gt2-2gt-20t-toothed-idler-6mm-wide) | verified |

**Subtotal: $252.15**

## C. Toolheads

| Part | Qty | Unit | Line | Source | Confidence |
|---|---:|---:|---:|---|---|
| Trianglelab V6 hotend pre-assembled, 24 V | 2 | $45.00 | $90.00 | [DREMC](https://store.dremc.com.au/products/v6-hotend-pre-assembled-compatible-for-prusa-i3-mk3-s-trianglelab) | verified |
| LDO Orbiter v2.5 extruder (motor included) | 2 | $105.45 | $210.90 | [DREMC](https://store.dremc.com.au/products/ldo-orbiter-v2-5-extruder) | verified |
| 5015 blower fan 24 V (part cooling) | 2 | $19.50 | $39.00 | [DREMC](https://store.dremc.com.au/products/5015-24v-blower-fan-by-dremc) | verified |
| 4010 axial hotend fan 24 V | 2 | $8.00 | $16.00 | — | verified |
| ADXL345 accelerometer (shared, for input shaping) | 1 | $4.95 | $4.95 | [DREMC](https://store.dremc.com.au/products/adxl345-accelerometer-3-axis-gy-291) | verified |

**Subtotal: $360.85**

## D. Y and bed

| Part | Qty | Unit | Line | Source | Confidence |
|---|---:|---:|---:|---|---|
| LDO SLR12H MGN12H rail + carriage, 450 mm Z1 | 2 | $79.45 | $158.90 | [DREMC](https://store.dremc.com.au/products/ldo-slr12h-mgn12h-linear-rail-with-carriage) | verified |
| LDO NEMA 17 42STH48-2504AC | 1 | $34.95 | $34.95 | [DREMC](https://store.dremc.com.au/products/ldo-nema-17-motor-ldo-42sth48-2504ac) | verified |
| Gates 2GT 20T pulley 5 mm bore + 2 idlers | 1 | $25.90 | $25.90 | — | verified |
| Aluminium heated bed, 235 x 235 x 3 mm, 24 V, bonded heater | 1 | $49.95 | $49.95 | [DREMC](https://store.dremc.com.au/products/creality-heated-hot-bed-kit-for-ender-3-series) | verified, **out of stock** |
| Magnetic sheet 235x235, high-temp 3M | 1 | $11.95 | $11.95 | [DREMC](https://store.dremc.com.au/products/magnetic-sheet-with-3m-adhesive) | verified |
| Light Satin PEI spring steel plate 235x235 | 1 | $36.45 | $36.45 | [DREMC](https://store.dremc.com.au/products/dremc-light-satin-pei-spring-steel-build-plate-3d-printers) | verified |
| Bed carrier bars - 235 x 35 x 5 mm aluminium flat, 2 off | 1 | $25.00 | $25.00 | — | estimate |
| Silicone levelling spacers, 4 pc | 1 | $11.00 | $11.00 | [DREMC](https://store.dremc.com.au/products/4pc-heatbed-silicone-leveling-column-for-ender-3-and-cr-10-series) | verified |

**Subtotal: $354.10**

## E. Z axis

| Part | Qty | Unit | Line | Source | Confidence |
|---|---:|---:|---:|---|---|
| 8 mm TR8 lead screw / ACME, 500 mm | 2 | $27.50 | $55.00 | [RM Components](https://rmcomponents.com.au/products/copy-of-t8-8mm-lead-screw-please-select-the-length-you-require-1) | verified |
| POM anti-backlash nut TR8x8 | 2 | $5.55 | $11.10 | [DREMC](https://store.dremc.com.au/products/dremc-pom-lead-screw-nuts-with-anti-backlash-nut) | verified |
| LDO SLR12H MGN12H rail + carriage, 350 mm Z1 | 2 | $65.45 | $130.90 | [DREMC](https://store.dremc.com.au/products/ldo-slr12h-mgn12h-linear-rail-with-carriage) | verified |
| LDO NEMA 17 42STH48-2504AC | 1 | $34.95 | $34.95 | [DREMC](https://store.dremc.com.au/products/ldo-nema-17-motor-ldo-42sth48-2504ac) | verified |
| 2GT 20T pulley 8 mm bore (on each screw) | 2 | $11.00 | $22.00 | [DREMC](https://store.dremc.com.au/products/ldo-2gt-pulleys) | verified |
| 2GT 20T pulley 5 mm bore (motor) | 1 | $11.00 | $11.00 | [DREMC](https://store.dremc.com.au/products/ldo-2gt-pulleys) | verified |
| 2GT 20T toothed idler 6 mm (belt link tensioner) | 2 | $7.45 | $14.90 | [DREMC](https://store.dremc.com.au/products/ldo-gt2-2gt-20t-toothed-idler-6mm-wide) | verified |
| F688Z flange bearing 8x16x5 (2 pc) - screw top support | 1 | $6.00 | $6.00 | [DREMC](https://store.dremc.com.au/products/f688z-flange-deep-groove-ball-bearing-8x16x5mm) | verified |

**Subtotal: $285.85**

## F. Belt stock

| Part | Qty | Unit | Line | Source | Confidence |
|---|---:|---:|---:|---|---|
| Gates Powergrip RF 2GT 6 mm belt, 6 m (X x2, Y, Z link) | 1 | $59.00 | $59.00 | [DREMC](https://store.dremc.com.au/products/gates-powergrip%C2%AE-rf-2gt-6mm-timing-belt) | verified |

**Subtotal: $59.00**

## G. Electronics

| Part | Qty | Unit | Line | Source | Confidence |
|---|---:|---:|---:|---|---|
| BTT Octopus Pro V1.1 (H723) - 8 driver slots, standalone | 1 | $115.00 | $115.00 | [DREMC](https://store.dremc.com.au/products/bigtreetech-octopus-pro-v1-1-h723-chip) | verified |
| Raspberry Pi 4 (2 GB) to run Klipper, over USB | 1 | $85.00 | $85.00 | — | estimate |
| BTT TMC2209 V1.3 drivers, 8-pack | 1 | $79.45 | $79.45 | [DREMC](https://store.dremc.com.au/products/bigtreetech-tmc2209-v1-3-stepper-motor-driver) | verified |
| Mean Well LRS-350-24 - 24 V, 14.6 A, 350 W | 1 | $74.65 | $74.65 | [DREMC](https://store.dremc.com.au/products/mean-well-lrs-350-24-24v-350w-power-supply) | verified |
| Omron D2F-5L endstop switch | 4 | $5.45 | $21.80 | [DREMC](https://store.dremc.com.au/products/omron-d2f-5l-switch) | verified |
| ADXL345 accelerometer (on the Pi SPI) | 1 | $4.95 | $4.95 | [DREMC](https://store.dremc.com.au/products/adxl345-accelerometer-3-axis-gy-291) | verified |
| Wiring, Wago blocks, ferrules, IEC inlet, drag chain | 1 | $80.00 | $80.00 | — | estimate |

**Subtotal: $460.85**

## Total

| Sub-assembly | Subtotal |
|---|---:|
| A. Frame | $242.00 |
| B. X gantry | $252.15 |
| C. Toolheads | $360.85 |
| D. Y and bed | $354.10 |
| E. Z axis | $285.85 |
| F. Belt stock | $59.00 |
| G. Electronics | $460.85 |
| **Total** | **$2014.80** |

Call it **$1,900 to $2,100** once the estimated lines firm up. Anything already on
hand comes off the top, mostly from the Frame and Electronics groups.

## Not costed here

- Individual screws and T-nuts beyond one assortment line.
- Printed parts: motor mounts, idler brackets, belt clamps, carriage bodies, Z nut mounts. Free to make, but they have to be designed.
- Bed levelling hardware and a probe.
- An enclosure.

## Known sourcing gaps

- **235 × 235 24 V heated bed** — both DREMC options were out of stock on 11 Nov 2026. [Jaycar lists an equivalent](https://www.jaycar.com.au/replacement-hot-bed-plate-kit-for-ender-3-v3-ke-and-se/p/001074) around $58 but blocks automated reading, so check it yourself.
- **Nothing is now unbuyable except the bed.** The board was changed from the Manta M8P to the Octopus Pro for exactly this reason — see [design-notes.md](design-notes.md) §12.
- **Bare MGN12H carriage blocks** — the only Australian listing found is [HIWIN Precision H at $105](https://store.dremc.com.au/products/hiwin-mgn12h-carriage-block), and it is out of stock. Source overseas, or buy whole rail-and-carriage sets at $85.45.

