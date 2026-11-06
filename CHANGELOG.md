# Changelog

## 1.0.0 — 2026-11-06
First public release. 24 device families, 40 submissions (2007–2026), 314 target rows, 841 antimicrobial-organism indications, 95 labeled-limitation rows.

Changes after author review (see `REVIEW.md`):
- Added mecA XpressFISH (AdvanDx, K140619, product code MYI); MYI added to the openFDA queries.
- LIAISON PLEX BCN OXA target normalized to OXA-48-like (K243013 p.4); Verigene BC-GN OXA labeled "group not specified in IFU".
- BD MAX StaphSR (K132822) exclusion reason: nasal swab specimen.
- New `marker_family` column in `targets.csv` and new `comparison/resistance_target_families_by_device.csv`, so combined and separate assays (e.g. mecA/mecC vs mecA) count together.
- New `organism_normalized` column in `ast_indications.csv`; the organism-by-antimicrobial lookup now aligns organisms across devices.
- Negative-statement status now distinguishes hedged wording (Great Basin) and indirect references (mecA XpressFISH); counting rule documented.
- Exclusions added for out-of-scope product-code groups (nasal/skin MRSA NAATs, PBP2a and colony tests, isolate/rectal carbapenemase tests).
- Selux quote ellipsis; KeyPath page reference; codebook completed.
- `VERIFICATION_CHECKLIST.md` replaced by `REVIEW.md`.

## 0.9.0 — 2026-11-06 (release candidate)
- First complete extraction: 23 device families, 39 submissions, 311 target rows, 841 antimicrobial-organism indications, 90 labeled-limitation rows.
