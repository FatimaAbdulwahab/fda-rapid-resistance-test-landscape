# Provenance

**Universe of devices.** openFDA 510(k) endpoint (data last updated 2026-10-26), queried 2026-11-06 and re-run by the author the same day:

```
https://api.fda.gov/device/510k.json?search=product_code:PAM&limit=100   # GP bacteria + resistance markers, PBC
https://api.fda.gov/device/510k.json?search=product_code:PEN&limit=100   # GN bacteria + resistance markers, PBC
https://api.fda.gov/device/510k.json?search=product_code:PEO&limit=100   # yeast, PBC (reviewed; excluded)
https://api.fda.gov/device/510k.json?search=product_code:PRH&limit=100   # PBC ID + AST kit
https://api.fda.gov/device/510k.json?search=product_code:SAN&limit=100   # automated AST for PBC
https://api.fda.gov/device/510k.json?search=product_code:QZX&limit=100   # PBC processor for AST inoculum
https://api.fda.gov/device/510k.json?search=product_code:NQX&limit=100   # MRSA/SA NAAT (filtered to blood culture)
https://api.fda.gov/device/510k.json?search=product_code:OUS&limit=100   # MRSA/MSSA blood culture test
https://api.fda.gov/device/510k.json?search=product_code:MYI&limit=100   # MRSA/mecA tests incl. mecA XpressFISH (added v1.0.0)
```

`openfda/<number>.json` holds the record returned for each submission by `search=k_number:<number>`.

**Content.** Each family's targets and limitations come from the one FDA document named in `extraction_log.csv`, read on 2026-11-06. The FDA document server blocks scripted downloads, so the PDFs are not stored here; each URL is in the log.

**Not used.** Manufacturer websites, package inserts, and published evaluations. Those would add current labeling and performance data but are outside the dataset's stated source (FDA decision summaries).
