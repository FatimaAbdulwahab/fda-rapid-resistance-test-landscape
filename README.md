# FDA-Cleared Rapid Resistance Test Landscape

An open, device-by-target dataset of FDA-cleared and De Novo-authorized **rapid molecular blood culture identification and resistance panels** and **rapid phenotypic susceptibility systems**, extracted from public FDA decision summaries. Every row records the 510(k) or De Novo number it came from, the decision date, and the page.

**Version 1.0.0** · DOI: assigned by Zenodo on release (add here once minted)

Author: Fatima Abdulwahab, M.S., MLS(ASCP)<sup>CM</sup> · Independent researcher, Dallas, Texas · ORCID [0009-0008-2298-8386](https://orcid.org/0009-0008-2298-8386)

## Why this exists

A community hospital laboratory choosing or reviewing a rapid blood culture test has no single public table showing what each FDA-cleared test detects and what its own labeling says about a negative result. That information is public, but it is spread across dozens of FDA PDFs. This dataset puts it in one place, with a source citation on every line.

## What is covered

| Group | Device families | Submissions |
|---|---|---|
| Molecular blood culture ID panels with resistance markers | 12 | 18 |
| *S. aureus* / MRSA tests on positive blood culture (5 molecular, 1 phenotypic) | 6 | 10 |
| Rapid phenotypic AST direct from positive blood culture | 6 | 12 |
| **Total** | **24** | **40** (decision dates 2007–2026) |

The full list is in `data/device_families.csv`. Scope rules and records reviewed but left out are in `data/exclusions.csv`. The universe was drawn from openFDA product codes PAM, PEN, PEO, PRH, SAN, QZX, NQX, OUS and MYI (openFDA data last updated 2026-10-26).

## A first finding

Of the 18 molecular and MRSA-screen device families, **9 have an FDA document stating that a negative resistance-marker result does not indicate susceptibility**; one of these (Great Basin) uses weaker wording ("do not always indicate"). **The other 9 have no such sentence** in the document reviewed; for one of them (mecA XpressFISH) the FDA review refers indirectly to a package-insert limitation on non-mecA resistance. All nine without the sentence were cleared 2007–2019. Four documents (ePlex GP and GN, QIAstat-Dx GPF and GN) also say a negative result may reflect a pathogen the panel does not target. See `comparison/device_summary.csv`. This describes the FDA documents, not current package inserts, which may say more.

## Files

```
data/
  device_families.csv      one row per device family; extraction source and specimen text
  submissions.csv          every in-scope 510(k)/De Novo with product code and dates (openFDA)
  targets.csv              organism, pan, resistance-gene and resistance-phenotype targets:
                           as written, normalized, and grouped by marker family
  ast_indications.csv      antimicrobial x organism indications for phenotypic AST systems,
                           as listed and normalized
  labeled_limitations.csv  FDA text on negative results, subculture, polymicrobial samples, etc.
  exclusions.csv           records and product codes reviewed and excluded, with reasons
comparison/                derived tables (rebuilt by scripts/build_comparison.py)
  device_summary.csv
  resistance_target_families_by_device.csv
  resistance_targets_by_device.csv
  identification_targets_by_device.csv
  ast_antimicrobials_by_device.csv
  ast_organism_antimicrobial_devices.csv
docs/index.html            public comparison page (GitHub Pages), filterable
provenance/
  README.md                openFDA queries used
  extraction_log.csv       source URL, access date, method, review status and notes per device
  openfda/*.json           raw openFDA record for every submission
scripts/
  validate.py              integrity checks (run before every release)
  build_comparison.py      rebuilds comparison/ and docs/ from data/
CODEBOOK.md  REVIEW.md  CITATION.cff  .zenodo.json  LICENSE  CHANGELOG.md
```

## Rebuild and check

Python 3.8+, standard library only.

```
python3 scripts/validate.py
python3 scripts/build_comparison.py
```

## Quality review

On 2026-11-06 the author re-ran every openFDA query (no new clearances in scope), confirmed all submission fields against live openFDA records, reproduced every derived file byte-for-byte from a fresh copy, and checked 15 device families against their FDA PDFs, including the full drug-by-organism lists for Accelerate, VITEK REVEAL and Selux. Fixes from that review are in `CHANGELOG.md`; per-family status is in `provenance/extraction_log.csv`; details are in `REVIEW.md`.

## How to read it, and what it is not

- **Labeling, not performance.** The dataset records what each FDA document says a device detects and what it says about its results. It does not compare accuracy, and it does not rank tests.
- **One source document per device family.** Each family was extracted from one decision summary, usually the most recent full one. Other submissions are listed in `submissions.csv` but were not re-extracted, so current labeling may differ. Always check the current package insert.
- **"Not found" is not "absent from labeling."** A "no statement found" row describes the FDA document reviewed only.
- **Commercial availability was not assessed.** Some cleared devices are no longer sold.
- **Normalized names are for comparison only.** `target_as_written` and `organism_as_listed` keep the source wording; normalized and family columns merge equivalent labels so rows line up across devices.

## Known limitations of v1.0.0

- Verigene BC-GP was extracted from the sponsor's 510(k) summary (K122514) because decision summary DEN120014 could not be retrieved from the FDA server.
- For ASTar (pp. 6–8) and PhAST (p. 6), the full lists of "alternate method before reporting" and "ability to detect resistance is unknown" combinations are summarized, not fully transcribed.
- Page numbers come from text extraction and may be off by one in places.

## Related work by the author

- Project 1: U.S. Rapid Panel Resistance Marker Concordance Benchmark — github.com/FatimaAbdulwahab/us-rapid-panel-amr-concordance
- Project 2: Reference Isolate Verification Crosswalk — github.com/FatimaAbdulwahab/ar-isolate-bank-panel-crosswalk

## Citation

Abdulwahab F. *FDA-Cleared Rapid Resistance Test Landscape* (v1.0.0) [Data set]. Zenodo. 2026. DOI to be added on release. See `CITATION.cff`.

## License

Data and documentation: CC BY 4.0. Scripts: MIT. FDA source documents are U.S. government works. Contact: abdulwahabfatima43@gmail.com
