// docs/bom.json -> docs/bom.md
//
// bom.json is the source: prices, supplier links, the variant actually priced,
// stock state, and every cut length tied to its CAD component. Edit that, then:
//     node scripts/genbom.js
// scripts/check_model.py check 11 measures the `cuts` against the Fusion model
// and check 12 adds up the `power` block, so the BOM cannot drift from the CAD.

const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const B = JSON.parse(fs.readFileSync(path.join(root, 'docs/bom.json'), 'utf8'));

const money = n => '$' + n.toFixed(2);

const host = u => {
  if (!u) return '—';
  const h = new URL(u).hostname.replace(/^www\./, '');
  const name = { 'store.dremc.com.au': 'DREMC', 'rmcomponents.com.au': 'RM Components',
                 'core-electronics.com.au': 'Core Electronics',
                 'aliexpress.com': 'AliExpress' }[h] || h;
  return '[' + name + '](' + u + ')';
};

const stockTag = s => ({ in: 'in stock', out: '**out of stock**', 'n/a': '—' }[s] || s);

const out = [
  '# Bill of materials', '',
  `All prices **${B.meta.currency}**, read from supplier product data on **${B.meta.priced_on}**.`, '',
  '- **verified** — price, option and stock read from the supplier’s own live product data on that date.',
  '- **estimate** — my own figure. A placeholder, not a quote.', '',
  B.meta.note, '',
  `## The overseas column`, '',
  `Every line was also priced on **AliExpress** on **${B.meta.ali_priced_on}**, in a logged-out`,
  'Australian session, with the named option selected on the listing page.', '',
  B.meta.ali_note, '',
  'Every cut length and part count is listed against its CAD component in `docs/bom.json`.',
  '`scripts/check_model.py` check 11 measures those components in the model and fails if a',
  'length, a count or a stocked size disagrees; check 12 adds up the 24 V load against the',
  'power supplies. Edit `bom.json`, then run `node scripts/genbom.js`.', '',
];

// Every line a bundled AliExpress line swallows, so the two columns compare
// like for like rather than crediting a saving twice.
const byItem = {};
for (const items of Object.values(B.groups))
  for (const r of items) (byItem[r.item] = byItem[r.item] || []).push(r);
const auSideOf = r => {
  let v = r.line;
  if (r.ali && r.ali.covers) for (const o of byItem[r.ali.covers] || []) v += o.line;
  return v;
};
// Plan price: the AliExpress list price, except where that is dearer than simply
// buying it here. Never pay more overseas than at home.
const planOf = r => {
  const a = r.ali;
  if (!a) return r.line;
  if (a.reason === 'bundled' || a.reason === 'owned') return 0;
  if (!a.sourced) return r.line;
  return Math.min(a.line, auSideOf(r));
};

let grand = 0, planGrand = 0, saleGrand = 0, keptLocal = 0;
const subs = [];
const notes = [];
const aliNotes = [];
for (const [g, items] of Object.entries(B.groups)) {
  let sub = 0, planSub = 0;
  out.push('## ' + g, '');
  out.push('| Part | Option priced | Qty | Line | Source | Stock | Conf. | AliExpress | Read as |');
  out.push('|---|---|---:|---:|---|---|---|---:|---|');
  for (const r of items) {
    sub += r.line;
    planSub += planOf(r);
    const a = r.ali || {};
    if (a.sourced) {
      saleGrand += Math.min(a.sale_line, auSideOf(r));
      // a sourced line whose list price loses to the local one is still bought here
      if (planOf(r) >= auSideOf(r) - 0.004) keptLocal += planOf(r);
    } else if (a.reason !== 'bundled') { saleGrand += r.line; keptLocal += r.line; }

    let item = r.item;
    if (r.note) { notes.push([g, r.item, r.note]); item += ' [^' + notes.length + ']'; }

    let aliCell, readCell;
    if (a.sourced) {
      aliCell = a.line > auSideOf(r) ? '~~' + money(a.line) + '~~ dearer'
                                     : '[' + money(a.line) + '](' + a.url + ')';
      readCell = a.read + (a.seller && a.seller !== 'generic' ? ', ' + a.seller : '');
      if (a.note) { aliNotes.push([g, r.item, a.note]); readCell += ' [^a' + aliNotes.length + ']'; }
    } else {
      aliCell = a.reason === 'bundled' ? 'in the line above' : '—';
      readCell = a.why || '';
    }

    out.push('| ' + [item, r.variant || '—', r.qty, money(r.line),
                     host(r.url), stockTag(r.stock), r.conf, aliCell, readCell].join(' | ') + ' |');
  }
  out.push('', '**Subtotal: ' + money(sub) + '** locally, **' + money(planSub) +
               '** buying overseas where it wins.', '');
  grand += sub;
  planGrand += planSub;
  subs.push([g, sub, planSub]);
}

out.push('## Total', '', '| Sub-assembly | Australian retail | Overseas where it wins |',
         '|---|---:|---:|');
subs.forEach(([g, s, p]) => out.push('| ' + g + ' | ' + money(s) + ' | ' + money(p) + ' |'));
out.push('| **Total** | **' + money(grand) + '** | **' + money(planGrand) + '** |', '');
const gst = (planGrand - keptLocal) * 0.10;
out.push('Buying everything from Australian stock costs **' + money(grand) + '**, GST included and',
         'delivered. Taking the overseas line wherever it is cheaper brings the parts to **' +
         money(planGrand) + '**, of which ' + money(keptLocal) + ' is still bought here. AliExpress',
         'prices exclude GST, so add about ' + money(gst) + ' at checkout: call it **' +
         money(planGrand + gst) + '** all up, plus whatever shipping applies.', '',
         'Those AliExpress figures are **list** prices. On ' + B.meta.ali_priced_on + ' the same basket',
         'rang up at ' + money(saleGrand) + ' on sale — but part of that gap is a first-order voucher',
         'that does not repeat, so the list column is the one to plan against. See',
         '`docs/budget-build.md`.', '');

const est = Object.values(B.groups).flat().filter(r => r.conf === 'estimate');
const estSum = est.reduce((a, r) => a + r.line, 0);
out.push(`Of that, ${money(grand - estSum)} is verified against live supplier data and ` +
         `${money(estSum)} is estimated across ${est.length} lines ` +
         '(extrusion and flat bar cut to length, the extra carriage blocks, and loose wiring).',
         'Anything already on hand comes off the top.', '');

// ---- 24 V power budget -------------------------------------------------
const P = B.power;
const totalW = P.loads.reduce((a, l) => a + l.qty * l.watts, 0);
out.push('## 24 V power budget', '',
         'A single 350 W supply does not fit this machine: two hotends and a 270 W bed come to',
         `${totalW.toFixed(1)} W. The bed therefore gets its own supply, and no supply is loaded`,
         `past ${(P.max_load_fraction * 100).toFixed(0)}% of its rating.`, '');
out.push('| Load | Qty | W each | Total W | Rail | Where the figure comes from |');
out.push('|---|---:|---:|---:|---|---|');
for (const l of P.loads) {
  out.push('| ' + [l.load, l.qty, l.watts, (l.qty * l.watts).toFixed(1), l.rail, l.source].join(' | ') + ' |');
}
out.push('', '| Supply | Rating | Load | Loaded |', '|---|---:|---:|---:|');
for (const s of P.supplies) {
  const load = P.loads.filter(l => l.rail === s.rail).reduce((a, l) => a + l.qty * l.watts, 0);
  out.push('| ' + [s.name + ' (' + s.rail + ')', s.watts + ' W', load.toFixed(1) + ' W',
                   (100 * load / s.watts).toFixed(0) + '%'].join(' | ') + ' |');
}
out.push('', P.off_budget, '');

out.push('## Not costed here', '',
  '- Individual screws and T-nuts beyond the packs listed.',
  '- Printed parts: motor mounts, idler brackets, belt clamps, carriage bodies, Z nut mounts. Free to make, but they have to be designed.',
  '- A bed probe.',
  '- An enclosure.', '');

out.push('## Known sourcing gaps', '',
  '- **MGN12H carriage blocks** are the one real gap. The model needs 10; the five rails bring five. ' +
  'The only Australian listing found is [HIWIN Precision H at $105.00](https://store.dremc.com.au/products/hiwin-mgn12h-carriage-block), out of stock. ' +
  'Either buy five more overseas, or buy five 300 mm rail-and-carriage sets at $55.95 and keep the spare rails.',
  '- **Extrusion and flat bar are cut to length**, and neither supplier publishes a per-mm rate on the ' +
  'storefront — the calculator on the RM Components listing returns $0.00 — so those four lines need a quote.',
  '- **The 235 x 235 heated bed is gone from both DREMC listings.** The 255 x 245 CR-6 SE assembly is in ' +
  'stock and is what the model now uses; it carries the 235 sheets with margin to spare.',
  '- Several in-stock-today choices are a second pick: the 2-wire 4010 fan, 10 mm M5 screws, ' +
  'the 32 GB SD card and the 350 mm Z rail were all out of stock, so the BOM takes the next option up.', '');

const foot = []
  .concat(notes.map(([g, item, n], i) => `[^${i + 1}]: ${g} — ${item}: ${n}.`))
  .concat(aliNotes.map(([g, item, n], i) => `[^a${i + 1}]: AliExpress, ${item}: ${n}.`));
fs.writeFileSync(path.join(root, 'docs/bom.md'),
  out.join('\n') + (foot.length ? '\n' + foot.join('\n') + '\n' : '\n'));
console.log('bom.md written; local ' + money(grand) + ', overseas-where-it-wins ' + money(planGrand) +
            ', sale-price basket ' + money(saleGrand) + '; ' + foot.length + ' notes');
