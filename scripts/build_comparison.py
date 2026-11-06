#!/usr/bin/env python3
"""Build the public comparison tables (comparison/*.csv) and the static
GitHub Pages view (docs/index.html) from the curated data/ files.

Standard library only. Run from the repository root:
    python3 scripts/build_comparison.py
"""
import csv
import html
import os
from collections import OrderedDict, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "comparison")
DOCS = os.path.join(ROOT, "docs")
VERSION = open(os.path.join(ROOT, "VERSION")).read().strip()


def read(name):
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(name, header, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


fams = read("device_families.csv")
subs = read("submissions.csv")
targets = read("targets.csv")
ast = read("ast_indications.csv")
lims = read("labeled_limitations.csv")

src_date = {s["submission_number"]: s["decision_date"] for s in subs}
fam_by_id = OrderedDict((f["family_id"], f) for f in fams)
molecular = [f["family_id"] for f in fams if not f["category"].startswith("phenotypic_ast")]
phenotypic = [f["family_id"] for f in fams if f["category"].startswith("phenotypic_ast")]


def pivot(rows, key_col, fam_ids, cell):
    table = OrderedDict()
    for r in rows:
        table.setdefault(r[key_col], {}).setdefault(r["family_id"], []).append(cell(r))
    out = []
    for key in sorted(table, key=str.lower):
        cells = [("; ".join(sorted(set(table[key].get(fid, []))))) for fid in fam_ids]
        out.append([key, sum(1 for c in cells if c)] + cells)
    return out


# 1. resistance markers / phenotypes by device
res_rows = [t for t in targets if t["target_class"] in ("resistance_marker", "resistance_phenotype")]
res_fams = [fid for fid in fam_by_id if any(t["family_id"] == fid for t in res_rows)]
markers = pivot(res_rows, "target_normalized", res_fams, lambda r: r["target_as_written"])
write("resistance_targets_by_device.csv", ["resistance_target", "n_devices"] + res_fams, markers)
# 1b. grouped by marker family (combined and separate assays counted together)
families = pivot(res_rows, "marker_family", res_fams, lambda r: r["target_as_written"])
write("resistance_target_families_by_device.csv", ["marker_family", "n_devices"] + res_fams, families)

# 2. organisms and pan targets by device (identification targets)
org_rows = [t for t in targets if t["target_class"] in ("organism", "pan_target")]
org_fams = [fid for fid in fam_by_id if any(t["family_id"] == fid for t in org_rows)]
orgs = pivot(org_rows, "target_normalized", org_fams, lambda r: r["target_as_written"])
write("identification_targets_by_device.csv", ["identification_target", "n_devices"] + org_fams, orgs)

# 3. antimicrobials by phenotypic AST device (count of indicated organisms)
drug_tab = defaultdict(lambda: defaultdict(int))
for a in ast:
    drug_tab[a["antimicrobial"]][a["family_id"]] += 1
drugs = []
for d in sorted(drug_tab, key=str.lower):
    cells = [drug_tab[d].get(fid, 0) or "" for fid in phenotypic]
    drugs.append([d, sum(1 for c in cells if c)] + cells)
write("ast_antimicrobials_by_device.csv", ["antimicrobial", "n_devices"] + phenotypic, drugs)

# 4. organism x antimicrobial -> which devices (phenotypic AST)
oa = defaultdict(set)
for a in ast:
    for org in a["organism_normalized"].split("; "):
        oa[(org, a["antimicrobial"])].add(a["family_id"])
oa_rows = [[o, d, len(v), "; ".join(sorted(v))] for (o, d), v in sorted(oa.items(), key=lambda x: (x[0][0].lower(), x[0][1].lower()))]
write("ast_organism_antimicrobial_devices.csv", ["organism_normalized", "antimicrobial", "n_devices", "devices"], oa_rows)

# 5. device summary incl. what labeling says about a negative result
lim_by = defaultdict(list)
for l in lims:
    lim_by[l["family_id"]].append(l)


def has(fid, t):
    return any(l["limitation_type"] == t for l in lim_by[fid])


def neg_marker_status(fid):
    f = fam_by_id[fid]
    if f["category"].startswith("phenotypic_ast"):
        return "n/a (phenotypic AST)"
    if has(fid, "negative_marker_not_susceptibility"):
        if any("not always" in l["text"] for l in lim_by[fid] if l["limitation_type"] == "negative_marker_not_susceptibility"):
            return "states it (hedged: 'do not always indicate susceptibility')"
        return "states negative marker result does not indicate susceptibility"
    if has(fid, "non_target_mechanisms_referenced"):
        return "not in IFU; FDA review refers to a package-insert limitation"
    return "no such statement found in source document"


summary = []
for fid, f in fam_by_id.items():
    n_res = sum(1 for t in targets if t["family_id"] == fid and t["target_class"] in ("resistance_marker", "resistance_phenotype"))
    n_id = sum(1 for t in targets if t["family_id"] == fid and t["target_class"] in ("organism", "pan_target"))
    n_drug = len({a["antimicrobial"] for a in ast if a["family_id"] == fid})
    summary.append([
        fid, f["device_name"], f["manufacturer"], f["category"], f["gram_scope"], f["organism_id_by_device"],
        n_id, n_res, n_drug, neg_marker_status(fid),
        "yes" if has(fid, "negative_does_not_exclude_infection") else "not stated",
        "yes" if has(fid, "resistance_detection_unknown") else "not stated",
        "yes" if has(fid, "polymicrobial_not_indicated") else "not stated",
        "yes" if has(fid, "subculture_required") else "not stated",
        f["extraction_source_document"], src_date.get(f["extraction_source_document"], ""),
    ])
sum_header = ["family_id", "device_name", "manufacturer", "category", "gram_scope", "organism_id_by_device",
              "n_identification_targets", "n_resistance_targets", "n_antimicrobials",
              "negative_resistance_marker_statement", "negative_result_may_miss_untargeted_pathogens",
              "resistance_detection_unknown_for_some_combinations", "polymicrobial_not_indicated",
              "subculture_required_statement", "source_document", "source_decision_date"]
write("device_summary.csv", sum_header, summary)


# ---------------------------------------------------------------- docs/index.html
def table(header, rows, cls=""):
    h = "".join(f"<th>{html.escape(str(c))}</th>" for c in header)
    b = "".join("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="wrap"><table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'


def tick_rows(rows):
    return [[r[0], r[1]] + ["✓" if c else "" for c in r[2:]] for r in rows]


short = {fid: fid.replace("_", " ") for fid in fam_by_id}
lim_rows = [[l["family_id"], l["limitation_type"].replace("_", " "), l["text"], l["source_document"], l["source_page"]]
            for l in lims if l["limitation_type"] in ("negative_marker_not_susceptibility", "negative_does_not_exclude_infection",
                                                       "no_negative_result_statement_found", "resistance_detection_unknown",
                                                       "marker_false_negative_possible", "non_target_mechanisms_referenced")]

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Rapid Resistance Test Landscape</title>
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--muted:#5f5d57;--line:#dcd8cf;--head:#efece4;--accent:#8a3b12}}
@media (prefers-color-scheme:dark){{:root{{--bg:#161614;--fg:#ecebe6;--muted:#a7a49b;--line:#3a3934;--head:#24231f;--accent:#e08a5a}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}}
main{{max-width:1200px;margin:0 auto;padding:24px 16px 64px}}
h1{{font-size:1.6rem;margin:.2em 0}} h2{{font-size:1.15rem;margin-top:2.2em;border-bottom:1px solid var(--line);padding-bottom:.3em}}
p,li{{max-width:75ch}} .muted{{color:var(--muted)}} a{{color:var(--accent)}}
.wrap{{overflow-x:auto;border:1px solid var(--line);border-radius:6px;margin:.8em 0}}
table{{border-collapse:collapse;font-size:13px;min-width:100%}}
th,td{{border-bottom:1px solid var(--line);padding:5px 8px;text-align:left;vertical-align:top}}
th{{background:var(--head);position:sticky;top:0;white-space:nowrap}}
table.matrix td:not(:first-child){{text-align:center}}
input{{font:inherit;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:transparent;color:var(--fg);width:min(100%,360px)}}
.note{{border-left:3px solid var(--accent);padding:.4em .9em;background:var(--head)}}
</style></head><body><main>
<p class="muted">Version {html.escape(VERSION)} &middot; Fatima Abdulwahab &middot; data from public FDA decision summaries and openFDA</p>
<h1>FDA-cleared rapid resistance test landscape</h1>
<p>What each FDA-cleared or De Novo-authorized rapid blood culture identification/resistance panel and rapid phenotypic susceptibility system detects, and what its own FDA document says a negative result does and does not rule out. Every row traces to a 510(k) or De Novo number and page.</p>
<p class="note">This is a regulatory-labeling reference, not a performance comparison. It does not say which test is better, and labeling of later submissions may differ from the source document cited. Check the current package insert before acting on any entry.</p>
<p><input id="q" type="search" placeholder="Filter all tables (e.g. KPC, faecium, meropenem)" aria-label="Filter tables"></p>

<h2>Devices and what their labeling says about negative results</h2>
{table(sum_header, summary)}
<p class="muted">Counting rule: a device is counted as stating that a negative marker result does not indicate susceptibility if its FDA document says so in any wording. Great Basin's wording is weaker ("do not always indicate"). mecA XpressFISH has no such sentence, but its FDA review refers to a package-insert limitation on resistance from mechanisms other than mecA.</p>

<h2>Resistance targets by marker family</h2>
<p class="muted">Combined and separate assays grouped together (e.g. mecA, mecC and mecA/mecC all count under mec). ✓ = named.</p>
{table(["marker family", "n devices"] + [short[x] for x in res_fams], tick_rows(families), "matrix")}

<h2>Resistance targets as labeled</h2>
<p class="muted">Genes and resistance phenotypes as each source document names them. ✓ = named.</p>
{table(["resistance target", "n devices"] + [short[x] for x in res_fams], tick_rows(markers), "matrix")}

<h2>Organism identification targets by device</h2>
{table(["identification target", "n devices"] + [short[x] for x in org_fams], tick_rows(orgs), "matrix")}

<h2>Antimicrobials on phenotypic AST systems</h2>
<p class="muted">Number of organisms (as listed in the Indications for Use) for which each antimicrobial is indicated.</p>
{table(["antimicrobial", "n devices"] + [short[x] for x in phenotypic], drugs, "matrix")}

<h2>Which rapid AST systems cover an organism and drug</h2>
<p class="muted">Organism names normalized across devices (e.g. K. pneumoniae and K. pneumoniae group merged; genus groups split into the species they list). Type an organism or drug in the filter.</p>
{table(["organism", "antimicrobial", "n devices", "devices"], oa_rows)}

<h2>Negative-result and detection limitations (FDA text)</h2>
{table(["device", "type", "text", "document", "page"], lim_rows)}

<p class="muted" style="margin-top:3em">Full data, codebook and provenance: see the repository README. License: CC BY 4.0.</p>
</main>
<script>
const q=document.getElementById('q');
q.addEventListener('input',()=>{{const v=q.value.toLowerCase();
document.querySelectorAll('tbody tr').forEach(tr=>{{tr.style.display=!v||tr.textContent.toLowerCase().includes(v)?'':'none'}})}});
</script></body></html>"""
os.makedirs(DOCS, exist_ok=True)
with open(os.path.join(DOCS, "index.html"), "w", encoding="utf-8") as f:
    f.write(page)
print(f"comparison tables: {len(families)} marker families, {len(markers)} resistance targets, {len(orgs)} ID targets, {len(drugs)} antimicrobials; docs/index.html written")
