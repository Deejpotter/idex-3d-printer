const fs = require('fs');
const D = 'https://store.dremc.com.au/products/';
const R = 'https://rmcomponents.com.au/products/';
const G = JSON.parse(fs.readFileSync(__dirname + '/../docs/bom.json', 'utf8'));

const L = {
 'LDO SLR12H MGN12H rail + 1 carriage, 500 mm Z1': D+'ldo-slr12h-mgn12h-linear-rail-with-carriage',
 'LDO SLR12H MGN12H rail + carriage, 350 mm Z1': D+'ldo-slr12h-mgn12h-linear-rail-with-carriage',
 'LDO SLR12H MGN12H rail + carriage, 450 mm Z1': D+'ldo-slr12h-mgn12h-linear-rail-with-carriage',
 'LDO SLR12H MGN12H rail + carriage, 400 mm Z1': D+'ldo-slr12h-mgn12h-linear-rail-with-carriage',
 'LDO NEMA 17 42STH48-2504AC': D+'ldo-nema-17-motor-ldo-42sth48-2504ac',
 'Gates 2GT 20T pulley, 5 mm bore, 6 mm belt': D+'ldo-2gt-pulleys',
 'Gates 2GT 20T toothed idler, 6 mm': D+'ldo-gt2-2gt-20t-toothed-idler-6mm-wide',
 'Trianglelab V6 hotend pre-assembled, 24 V': D+'v6-hotend-pre-assembled-compatible-for-prusa-i3-mk3-s-trianglelab',
 'LDO Orbiter v2.5 extruder (motor included)': D+'ldo-orbiter-v2-5-extruder',
 '5015 blower fan 24 V (part cooling)': D+'5015-24v-blower-fan-by-dremc',
 'ADXL345 accelerometer (shared, for input shaping)': D+'adxl345-accelerometer-3-axis-gy-291',
 'Creality 235x235 aluminium heated bed kit, 24 V': D+'creality-heated-hot-bed-kit-for-ender-3-series',
 'Magnetic sheet 235x235, high-temp 3M': D+'magnetic-sheet-with-3m-adhesive',
 'Light Satin PEI spring steel plate 235x235': D+'dremc-light-satin-pei-spring-steel-build-plate-3d-printers',
 '8 mm TR8 lead screw / ACME, 500 mm': R+'copy-of-t8-8mm-lead-screw-please-select-the-length-you-require-1',
 'POM anti-backlash nut TR8x8': D+'dremc-pom-lead-screw-nuts-with-anti-backlash-nut',
 '2GT 20T pulley 8 mm bore (on each screw)': D+'ldo-2gt-pulleys',
 '2GT 20T pulley 5 mm bore (motor)': D+'ldo-2gt-pulleys',
 '2GT 20T toothed idler 6 mm (belt link tensioner)': D+'ldo-gt2-2gt-20t-toothed-idler-6mm-wide',
 'F688Z flange bearing 8x16x5 (2 pc) - screw top support': D+'f688z-flange-deep-groove-ball-bearing-8x16x5mm',
 'Gates Powergrip RF 2GT 6 mm belt, 6 m (X x2, Y, Z link)': D+'gates-powergrip%C2%AE-rf-2gt-6mm-timing-belt',
 'BTT Octopus Pro V1.1 (H723) - 8 driver slots, standalone': D+'bigtreetech-octopus-pro-v1-1-h723-chip',
 'BTT TMC2209 V1.3 drivers, 8-pack': D+'bigtreetech-tmc2209-v1-3-stepper-motor-driver',
 'Mean Well LRS-350-24 - 24 V, 14.6 A, 350 W': D+'mean-well-lrs-350-24-24v-350w-power-supply',
 'ADXL345 accelerometer (on the Pi SPI)': D+'adxl345-accelerometer-3-axis-gy-291',
 'Aluminium heated bed, 235 x 235 x 3 mm, 24 V, bonded heater': D+'creality-heated-hot-bed-kit-for-ender-3-series',
 'Silicone levelling spacers, 4 pc': D+'4pc-heatbed-silicone-leveling-column-for-ender-3-and-cr-10-series',
 'BTT TMC2209 V1.3 driver, 8-pack': D+'bigtreetech-tmc2209-v1-3-stepper-motor-driver',
 'Mean Well LRS-350-24, 24 V 350 W': D+'mean-well-lrs-350-24-24v-350w-power-supply',
 'Omron D2F-5L endstop switch': D+'omron-d2f-5l-switch',
 'M5 drop-in T-nuts, 20 pc': D+'20pc-t-slot-hammer-head-nuts',
 '4040 V-slot black - 2 x 500 (uprights) + 2 x 530 (base rails) = 2.06 m': R+'copy-of-2020-silver-t-slot-aluminium-profile-20-series',
 '2040 V-slot black - 2 x 520 (top tie, X beam) + 2 x 440 (base cross) = 1.92 m': R+'2040-black-v-slot-aluminium-profile-20-series',
 '2020 V-slot black - 2 x 530 (bed rails) = 1.06 m': R+'2020-black-v-slot-aluminium-profile-20-series',
};

const conf = n => {
  if (!n) return 'verified';
  if (n === 'est') return 'estimate';
  if (n === 'out of stock') return 'verified, **out of stock**';
  if (n === 'AliExpress') return 'estimate, AliExpress';
  if (n === 'not at DREMC') return 'estimate, **not stocked locally**';
  return n;
};

const out = [
 '# Bill of materials', '',
 'All prices **AUD including GST**, read from supplier product data on **11 November 2026**.', '',
 '- **verified** — price and stock read from the supplier\u2019s own live product data.',
 '- **estimate** — my own figure. A placeholder, not a quote.', '',
 'Quantities come from the parametric Fusion model. The frame is 520 mm wide because the',
 'IDEX carriages carry two MGN12H blocks each — see [design-notes.md](design-notes.md) §4.', '',
 'Every cut length and part count below is listed against its CAD component in',
 '`docs/bom.json` (`cuts`). `scripts/check_model.py` check 11 measures those components in',
 'the model and fails if a length, a count or a stocked size disagrees. Edit `bom.json`,',
 'then run `node scripts/genbom.js`.', ''
];

let grand = 0; const subs = [];
for (const g of Object.keys(G)) {
  let sub = 0;
  out.push('## ' + g, '');
  out.push('| Part | Qty | Unit | Line | Source | Confidence |');
  out.push('|---|---:|---:|---:|---|---|');
  for (const r of G[g]) {
    sub += r.line;
    const url = L[r.item];
    const src = url ? '[' + (url.includes('dremc') ? 'DREMC' : 'RM Components') + '](' + url + ')' : '—';
    out.push('| ' + r.item + ' | ' + r.qty + ' | $' + r.unit.toFixed(2) + ' | $' + r.line.toFixed(2) + ' | ' + src + ' | ' + conf(r.note) + ' |');
  }
  out.push('', '**Subtotal: $' + sub.toFixed(2) + '**', '');
  grand += sub; subs.push([g, sub]);
}

out.push('## Total', '', '| Sub-assembly | Subtotal |', '|---|---:|');
subs.forEach(([g, s]) => out.push('| ' + g + ' | $' + s.toFixed(2) + ' |'));
out.push('| **Total** | **$' + grand.toFixed(2) + '** |', '');
out.push('Call it **$1,900 to $2,100** once the estimated lines firm up. Anything already on',
         'hand comes off the top, mostly from the Frame and Electronics groups.', '');
out.push('## Not costed here', '',
 '- Individual screws and T-nuts beyond one assortment line.',
 '- Printed parts: motor mounts, idler brackets, belt clamps, carriage bodies, Z nut mounts. Free to make, but they have to be designed.',
 '- Bed levelling hardware and a probe.',
 '- An enclosure.', '');
out.push('## Known sourcing gaps', '',
 '- **235 × 235 24 V heated bed** — both DREMC options were out of stock on 11 Nov 2026. [Jaycar lists an equivalent](https://www.jaycar.com.au/replacement-hot-bed-plate-kit-for-ender-3-v3-ke-and-se/p/001074) around $58 but blocks automated reading, so check it yourself.',
 '- **Nothing is now unbuyable except the bed.** The board was changed from the Manta M8P to the Octopus Pro for exactly this reason — see [design-notes.md](design-notes.md) §12.',
 '- **Bare MGN12H carriage blocks** — the only Australian listing found is [HIWIN Precision H at $105](' + D + 'hiwin-mgn12h-carriage-block), and it is out of stock. Source overseas, or buy whole rail-and-carriage sets at $85.45.', '');

fs.writeFileSync(__dirname + '/../docs/bom.md', out.join('\n') + '\n');
console.log('bom.md written; total $' + grand.toFixed(2));
