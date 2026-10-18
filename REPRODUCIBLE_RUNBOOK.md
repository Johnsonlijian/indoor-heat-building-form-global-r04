# Reproducible runbook

## Environment

Use Python 3.11 or newer with `pandas`, `pyarrow`, `numpy` and `matplotlib`.
The R04 analysis was executed with a local Python environment containing
`pandas 2.3.3`, `pyarrow 25.0.1` and NumPy. Do not place credentials in the
repository. Upstream data are obtained separately under their own licences.

## Recreate the WP-C extension

1. Stage the QA-passed city products in a local directory with these exact
   filenames: `tierA_exposure_city_main_v3.parquet`,
   `tierA_exposure_city_svf_none_v3.parquet`,
   `tierA_exposure_city_ach_open_lo_v3.parquet`,
   `tierA_exposure_city_ach_open_hi_v3.parquet`, and
   `tierA_exposure_city_loss_rank2_v3.parquet`.
2. Run:

   ```bash
   python src/reproduce_wpc_summary.py --input-dir /path/to/city_products --out outputs
   ```

3. Confirm that the script reports exactly 1,904 centres for every scenario,
   writes the scenario totals/deltas, paired quantiles, fan-allowance summary,
   and a diagnostic PNG.

The compact release tables under `derived/tables/` are a checked snapshot of
this computation. The full Parquet products, raw forcing, and geometry are not
part of this repository.

## QA and interpretation

- Check Parquet readability before running the script and compare the centre ID
  sets exactly; do not impute missing centre products.
- Interpret `uncooled_personhours_h_top30` as a modelled annual burden above
  30 °C operative temperature, not a health outcome.
- Interpret the 31.8 °C fan allowance as a model-form proxy, not a clinical or
  comfort standard.
- WP-D is currently a blocked feasibility extension. Do not run the private-path
  fetch scripts from the research workspace and do not write to the remote
  NatureHeat input tree.

