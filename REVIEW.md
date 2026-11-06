# Review record

## Author review, 2026-11-06 (before v1.0.0)

**Reproducibility.** `validate.py` passed. `build_comparison.py` run on a fresh copy produced files identical to those shipped in v0.9.0, including `docs/index.html`.

**openFDA.** All eight product-code queries re-run (openFDA last updated 2026-10-26). Every field in `submissions.csv` matched the saved JSON and the live records. No new clearances in those codes.

**Counts.** README family and submission counts, the 2007–2026 date range, CHANGELOG totals, and the headline negative-statement split all matched the data.

**Against FDA PDFs.** 15 families checked, plus K140619 and K132822; for some families only one or two items were checked.
- Targets matched: BCID, iC-GN, QIAstat GN, Great Basin, ePlex GN, Verigene BC-S, Verigene BC-GN, LIAISON BCN (except the OXA label, fixed).
- Full drug-by-organism lists matched: Accelerate (95 rows), VITEK REVEAL (149), Selux (131).
- "No negative-result statement" confirmed: BC-S, BC-GN, iC-GN, Xpert, KeyPath.

**Public page.** Works at phone width; filter works.

**Findings and resolution**

| # | Finding | Resolution in v1.0.0 |
|---|---|---|
| 1 | mecA XpressFISH (K140619, product code MYI) in scope but missing | Added as family `ADVANDX_MECA_XPRESSFISH`; MYI added to queries; other MYI records listed in exclusions |
| 2 | LIAISON BCN OXA named on p.4 as blaOXA48-like | Normalized to `OXA-48-like`; Verigene BC-GN note changed to "not specified in IFU" |
| 3 | BD MAX StaphSR (K132822) is for nasal swabs | Exclusion reason updated with the source wording |
| 4 | Verigene BC-GP decision summary DEN120014 not retrievable | Still open; listed under Known limitations |
| 5 | Combined vs separate marker labels undercount shared targets | `marker_family` column and family-level comparison table added |
| 6 | Organism spellings split drug-by-organism rows | `organism_normalized` column added; lookup table rebuilt on it |
| 7 | Great Basin wording weaker than others | Separate status value and counting-rule footnote |
| 8 | Selux quote cut at a comma without "..." | Ellipsis added |
| 9 | Codebook missing columns | submissions, exclusions and source_page described |
| 10 | KeyPath subculture sentence page | Sentence appears in both intended use (p.2) and indications (p.3); page set to pp.2-3 |
| 11 | Out-of-scope codes not explained | Exclusions rows added for nasal/skin MRSA NAATs, PBP2a/colony tests, Carba-R-type tests |

## Sign-off

The author confirmed the dataset for release on 2026-11-06. Corrections are welcome as GitHub issues and will go into a 1.0.x release.
