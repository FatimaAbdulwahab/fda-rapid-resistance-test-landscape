#!/usr/bin/env python3
"""Integrity checks for the dataset. Exits non-zero on any failure.
    python3 scripts/validate.py
"""
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "data")
errors = []


def read(n):
    with open(os.path.join(D, n), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


fams = read("device_families.csv")
subs = read("submissions.csv")
targets = read("targets.csv")
ast = read("ast_indications.csv")
lims = read("labeled_limitations.csv")

fid = {f["family_id"] for f in fams}
num = re.compile(r"^(K\d{6}|DEN\d{6})$")
TCLASS = {"organism", "pan_target", "resistance_marker", "resistance_phenotype"}

if len(fid) != len(fams):
    errors.append("duplicate family_id")
for s in subs:
    if s["family_id"] not in fid: errors.append(f"submissions: unknown family {s['family_id']}")
    if not num.match(s["submission_number"]): errors.append(f"submissions: bad number {s['submission_number']}")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", s["decision_date"]): errors.append(f"submissions: bad date {s['submission_number']}")
    if not os.path.exists(os.path.join(ROOT, "provenance", "openfda", s["submission_number"] + ".json")):
        errors.append(f"provenance missing for {s['submission_number']}")
sub_nums = {s["submission_number"] for s in subs}
for f in fams:
    src = f["extraction_source_document"]
    if src not in sub_nums: errors.append(f"{f['family_id']}: source {src} not in submissions.csv")
    used = [s for s in subs if s["family_id"] == f["family_id"] and s["used_as_extraction_source"] == "yes"]
    if len(used) != 1: errors.append(f"{f['family_id']}: expected exactly one extraction source, found {len(used)}")
    if not any(l["family_id"] == f["family_id"] for l in lims): errors.append(f"{f['family_id']}: no limitation rows")
    is_ast = f["category"].startswith("phenotypic_ast")
    if is_ast and not any(a["family_id"] == f["family_id"] for a in ast): errors.append(f"{f['family_id']}: AST device without indications")
    if not is_ast and not any(t["family_id"] == f["family_id"] and t["target_class"] in ("resistance_marker", "resistance_phenotype") for t in targets):
        errors.append(f"{f['family_id']}: molecular/screen device without resistance target")
src_of = {f["family_id"]: f["extraction_source_document"] for f in fams}
for name, rows in (("targets", targets), ("ast_indications", ast), ("labeled_limitations", lims)):
    seen = set()
    for r in rows:
        if r["family_id"] not in fid: errors.append(f"{name}: unknown family {r['family_id']}")
        if r["source_document"] != src_of.get(r["family_id"]): errors.append(f"{name}: source mismatch for {r['family_id']}")
        if not r.get("source_page"): errors.append(f"{name}: missing page for {r['family_id']}")
        key = tuple(r.values())
        if key in seen: errors.append(f"{name}: duplicate row {key[:3]}")
        seen.add(key)
for t in targets:
    if t["target_class"] in ("resistance_marker", "resistance_phenotype") and not t["marker_family"].strip():
        errors.append(f"targets: missing marker_family for {t['family_id']} {t['target_normalized']}")
    if t["target_class"] not in TCLASS: errors.append(f"targets: bad class {t['target_class']}")
    if not t["target_as_written"].strip() or not t["target_normalized"].strip(): errors.append("targets: empty label")

for a in ast:
    if not a["organism_normalized"].strip(): errors.append(f"ast_indications: missing organism_normalized {a['family_id']}")
print(f"{len(fams)} families, {len(subs)} submissions, {len(targets)} targets, {len(ast)} AST indications, {len(lims)} limitations")
if errors:
    print("FAILED:"); [print("  -", e) for e in errors]; sys.exit(1)
print("All checks passed.")
