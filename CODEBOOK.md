# Codebook

All files are UTF-8 CSV with a header row. `family_id` links every file. In every file that has it, `source_document` is the 510(k)/De Novo number the row was taken from, and `source_page` is the page or section of that document (from text extraction; may be off by one).

## data/device_families.csv
| Column | Meaning |
|---|---|
| family_id | Stable ID for a device family (one assay/kit across its submissions) |
| device_name | Name as given in the extraction source |
| manufacturer | Manufacturer; later owner in parentheses where known |
| category | `molecular_bcid_panel`, `molecular_staph_mrsa`, `phenotypic_mrsa_screen`, `phenotypic_ast`, `phenotypic_ast_with_id` |
| technology | Detection principle, short description |
| gram_scope | Organism groups covered (GP, GN, yeast/fungi; pan targets in parentheses) |
| organism_id_by_device | Whether the device itself identifies the organism; if not, how ID is supplied |
| extraction_source_document | The one 510(k)/De Novo document all targets and limitations for this family were taken from |
| extraction_source_type | FDA decision summary, or sponsor 510(k) summary where the decision summary was unavailable |
| extraction_source_url | URL of that document on accessdata.fda.gov |
| specimen_text_verbatim | Specimen wording from the source ("..." marks omitted words; square brackets mark curator insertions) |
| specimen_page | Page or section in the source |

## data/submissions.csv
All fields except `family_id` and `used_as_extraction_source` are copied from openFDA (`provenance/openfda/*.json`).
| Column | Meaning |
|---|---|
| submission_number | 510(k) (K + 6 digits) or De Novo (DEN + 6 digits) number |
| device_name_openfda, applicant_openfda | Device and applicant names as openFDA records them |
| product_code | FDA three-letter product code |
| decision_code | SESE = substantially equivalent (cleared); DENG = De Novo granted |
| decision_date, date_received | FDA decision date and date the submission was received (YYYY-MM-DD) |
| clearance_type | Traditional, Special, Abbreviated, or Direct (De Novo) |
| used_as_extraction_source | `yes` for exactly one submission per family |

## data/targets.csv
| Column | Meaning |
|---|---|
| target_class | `organism`, `pan_target` (broad assay such as Pan Gram-Negative or a Candida group), `resistance_marker` (gene or mRNA), `resistance_phenotype` (e.g. MRSA, ESBL confirmation) |
| target_as_written | Wording in the source document, including source typos |
| target_normalized | Harmonized label for cross-device comparison. Combined assays stay combined (e.g. BCID2 `mecA/mecC`). OXA assays are named by group wherever the source names one anywhere in the document (ePlex: OXA-23, OXA-48-like; LIAISON BCN: OXA-48-like, p.4). Verigene BC-GN names no group in its IFU: `OXA (group not specified in IFU)` |
| marker_family | Resistance rows only: groups combined and separate assays (e.g. mecA, mecC, mecA/mecC → `mec (mecA/mecC)`; vanA, vanB, vanA/vanB → `van (vanA/vanB)`; mcr, mcr-1 → `mcr`; MRSA genotype or phenotype calls → `methicillin resistance (phenotype)`) |
| resistance_result_reported_with | Resistance rows: the organism(s) the source says a result is reported with or attributed to; `not stated...` where it does not say |

## data/ast_indications.csv
One row per antimicrobial x organism listed in the Indications for Use of a phenotypic AST system.
| Column | Meaning |
|---|---|
| antimicrobial | Harmonized name with hyphens (e.g. Piperacillin-tazobactam) |
| organism_as_listed | Source grouping kept (e.g. "Klebsiella spp. (K. pneumoniae, K. oxytoca)") |
| organism_normalized | Aligned name(s); multiple names separated by "; ". Species and "group/complex" variants merged (K. pneumoniae and K. pneumoniae group → `Klebsiella pneumoniae (incl. group)`); genus groups that list their species are split into those species |

## data/labeled_limitations.csv
| limitation_type | Meaning |
|---|---|
| negative_marker_not_susceptibility | Source says a negative/Not Detected resistance result does not (or does not always) indicate susceptibility |
| negative_does_not_exclude_infection | Source says a negative result may reflect a pathogen the test does not detect |
| positive_does_not_exclude_coinfection | Source says positive results do not rule out co-infection with untargeted organisms |
| no_negative_result_statement_found | Curator note: no negative-result statement found in the document reviewed |
| non_target_mechanisms_referenced | FDA review refers to a limitation on resistance from mechanisms the test does not target |
| marker_may_not_be_from_causative_agent | Detected gene may not belong to the organism causing disease |
| marker_reported_only_with_associated_organism | Reporting rule tying a gene result to a detected organism |
| mixed_growth_marker_not_attributed | In mixed growth the gene is not attributed to a specific organism |
| marker_false_negative_possible | Source names situations where a marker may be missed |
| mixed_culture_may_miss_organisms | Mixed cultures may not have every organism identified |
| specimen_restriction | Specimens that should not be tested, or uses the test is not intended for |
| polymicrobial_not_indicated | AST results not valid or not to be reported for polymicrobial samples |
| alternate_method_before_reporting | Drug/organism combinations needing another method before reporting |
| resistance_detection_unknown | Combinations where ability to detect resistance is unknown (too few resistant isolates studied) |
| subculture_required | Subculture still needed (for AST, untargeted organisms, typing, etc.) |
| not_for_monitoring | Not intended to monitor treatment |

`text_status`: `verbatim_from_FDA_document` (line breaks joined; "..." marks omitted text; square brackets are curator additions) or `note_by_curator`.

## data/exclusions.csv
| Column | Meaning |
|---|---|
| submission | 510(k) number, or a description of a group of records (e.g. "product code MYI (other)") |
| device_name | Device or group name |
| product_code | FDA product code(s) |
| reason | Why it is outside scope |

## comparison/ (derived; do not edit by hand)
- `device_summary.csv`: counts per device and flags for each limitation type. `negative_resistance_marker_statement` takes one of: states it; states it (hedged); not in IFU but FDA review refers to a package-insert limitation; no such statement found; n/a (phenotypic AST).
- `resistance_target_families_by_device.csv`, `resistance_targets_by_device.csv`, `identification_targets_by_device.csv`: cells hold the source wording; blank = not named in that device's source.
- `ast_antimicrobials_by_device.csv`: cells give the number of indicated organism entries.
- `ast_organism_antimicrobial_devices.csv`: for each normalized organism and antimicrobial, which AST systems are indicated.
