# Indoor heat exposure and building form: R04 reproducibility package

This repository contains the **public, non-sensitive reproducibility layer**
for the R04 global indoor-heat analysis. It includes path-independent analysis
code, compact derived tables, selected derived figures, source links, and the
runbook needed to regenerate the reported summaries after the licensed input
products have been obtained locally.

The package does **not** redistribute raw third-party data, building footprints,
weather files, full Parquet products, active manuscript files, round logs,
credentials, or private local paths. The results are modelled and bounded by
the R04 evidence ledger; they do not estimate mortality, health causality,
electricity demand, or grid impacts.

## Release contents

- `src/`: deterministic summary code, including the WP-C model-form extension;
- `derived/tables/`: compact key metrics, selected sensitivity results, MC
  ranges, geometry QA, and WP-C summaries;
- `derived/figures/`: selected publication-ready derived PNGs and the WP-C
  diagnostic figure;
- `configs/`: documented scenario and boundary configuration;
- `DATASETS_AND_LINKS.csv`: upstream products, versions, access links and
  redistribution notes;
- `REPRODUCIBLE_RUNBOOK.md`: environment, commands, checks and claim limits.

## Main R04 result anchor

The QA-passed v3 run covers 1,904 centres and 18,352 centre--LCZ archetype
rows, representing 2.429919 billion modelled residents. The main estimates are
2,750.672 billion uncooled person-hours above 30 °C per year and 217.968 million
cooled residents crossing 32 °C operative temperature within six hours of
cooling loss. See `derived/tables/r04_results_key_metrics.csv` for definitions
and source keys.

## WP-C extension

The deterministic extension compares the existing `main_v3`, `svf_none_v3`,
`ach_open_lo_v3`, `ach_open_hi_v3`, and `loss_rank2_v3` city products. It does
not rerun the global pipeline. The fan-allowance value uses the model's 31.8 °C
proxy and must not be read as a health threshold.

## Licensing

- Source code under `src/` is licensed **MIT** (see `LICENSE`).
- Derived tables and figures under `derived/` are licensed **CC BY 4.0** (see
  `LICENSE-DATA-CC-BY-4.0.txt`). Upstream data remain under their own terms.
- The paper's author list and DOI metadata are intentionally not inferred from
  the private manuscript; confirm those human metadata fields before minting a
  DOI or citing the package as a final paper release.

## Citation

Use `CITATION.cff` for machine-readable citation metadata. The repository URL
is `https://github.com/Johnsonlijian/indoor-heat-building-form-global-r04`.

