# Geometry v3 QA snapshot

- Status: PASS for the R04 local product.
- Measured geometry rows: 10,396 centre--LCZ rows.
- Centres with measured rows: 1,854 of 1,904.
- Target IDs without a valid measured row after exclusions: 50.
- Imputation: none. The exposure product retains all 1,904 centre IDs through
  the documented form-geometry fallback.
- Remote input boundary: read-only; this release contains only the compact QA
  summary and no geometry Parquet.

The full hash manifest and geometry Parquet remain local project artifacts and
are intentionally excluded from this public package.
