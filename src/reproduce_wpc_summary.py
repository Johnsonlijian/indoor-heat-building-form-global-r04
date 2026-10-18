"""Reproduce compact WP-C summaries from staged QA-passed city Parquets."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SCENARIOS = {
    "main_v3": "tierA_exposure_city_main_v3.parquet",
    "svf_none_v3": "tierA_exposure_city_svf_none_v3.parquet",
    "ach_open_lo_v3": "tierA_exposure_city_ach_open_lo_v3.parquet",
    "ach_open_hi_v3": "tierA_exposure_city_ach_open_hi_v3.parquet",
    "loss_rank2_v3": "tierA_exposure_city_loss_rank2_v3.parquet",
}
SUM_COLS = {
    "uncooled_personhours_h_top30": 1e12,
    "uncooled_personhours_h_top30fan": 1e12,
    "cooled_pop_loss_lt6h_top32": 1e6,
    "cooled_pop_loss_lt12h_top32": 1e6,
    "cooled_pop_loss_lt24h_top32": 1e6,
}


def quantiles(values: pd.Series) -> dict[str, float | int | None]:
    x = pd.to_numeric(values, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if x.empty:
        return {"n": 0, "q05": None, "q50": None, "q95": None}
    q = x.quantile([0.05, 0.50, 0.95])
    return {"n": int(x.size), "q05": float(q.iloc[0]), "q50": float(q.iloc[1]), "q95": float(q.iloc[2])}


def run(input_dir: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    frames = {tag: pd.read_parquet(input_dir / filename) for tag, filename in SCENARIOS.items()}
    ids = set(frames["main_v3"]["ID_UC_G0"])
    if len(ids) != 1904:
        raise ValueError(f"main_v3 has {len(ids)} centres; expected 1904")
    for tag, frame in frames.items():
        if set(frame["ID_UC_G0"]) != ids:
            raise ValueError(f"{tag} does not cover the exact main centre set")

    rows = []
    for tag, frame in frames.items():
        row = {"scenario": tag, "n_centres": int(frame["ID_UC_G0"].nunique())}
        for col, scale in SUM_COLS.items():
            row[col] = float(frame[col].sum() / scale)
        rows.append(row)
    totals = pd.DataFrame(rows).set_index("scenario")
    base = totals.loc["main_v3"]
    delta = totals.copy()
    for col in SUM_COLS:
        delta[f"{col}_delta"] = totals[col] - base[col]
        delta[f"{col}_pct"] = 100.0 * (totals[col] / base[col] - 1.0)
    totals.reset_index().to_csv(out_dir / "wpC_scenario_totals.csv", index=False)
    delta.reset_index().to_csv(out_dir / "wpC_scenario_deltas.csv", index=False)

    paired = []
    main = frames["main_v3"].set_index("ID_UC_G0")
    for tag, frame in frames.items():
        if tag == "main_v3":
            continue
        joined = main.join(frame.set_index("ID_UC_G0"), lsuffix="_main", rsuffix=f"_{tag}")
        for col in ("uncooled_personhours_h_top30", "cooled_pop_loss_lt6h_top32", "cooled_pop_loss_lt24h_top32"):
            paired.append({"scenario": tag, "metric": col, **quantiles(joined[f"{col}_{tag}"] - joined[f"{col}_main"])})
    pd.DataFrame(paired).to_csv(out_dir / "wpC_paired_delta_quantiles.csv", index=False)

    fan = frames["main_v3"]
    top30 = float(fan["uncooled_personhours_h_top30"].sum() / 1e12)
    top30fan = float(fan["uncooled_personhours_h_top30fan"].sum() / 1e12)
    reduction_bn = float((fan["uncooled_personhours_h_top30"] - fan["uncooled_personhours_h_top30fan"]).sum() / 1e12)
    reduction = float(100.0 * (fan["uncooled_personhours_h_top30"] - fan["uncooled_personhours_h_top30fan"]).sum() / fan["uncooled_personhours_h_top30"].sum())
    fan_pct = 100.0 * (fan["uncooled_personhours_h_top30"] - fan["uncooled_personhours_h_top30fan"]) / fan["uncooled_personhours_h_top30"].replace(0, np.nan)
    (out_dir / "wpC_fan_allowance_summary.json").write_text(json.dumps({
        "total_top30_personhours_bn": top30,
        "total_top30fan_personhours_bn": top30fan,
        "fan_allowance_reduction_bn": reduction_bn,
        "fan_allowance_reduction_pct": reduction,
        "centre_reduction_pct_quantiles": quantiles(fan_pct),
        "threshold_c": 31.8,
        "interpretation": "thermal-model fan-allowance proxy; not a health threshold",
    }, indent=2), encoding="utf-8")

    plot = delta.reset_index().query("scenario != 'main_v3'")
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.5), constrained_layout=True)
    axes[0].bar(plot.scenario, plot.uncooled_personhours_h_top30_pct, color="#4472C4")
    axes[0].set_ylabel("Uncooled person-hours change (%)")
    axes[1].bar(plot.scenario, plot.cooled_pop_loss_lt6h_top32_pct, color="#ED7D31")
    axes[1].set_ylabel("Cooled population <6 h change (%)")
    for ax in axes:
        ax.axhline(0, color="black", linewidth=0.7)
        ax.tick_params(axis="x", rotation=45, labelsize=8)
        ax.grid(axis="y", alpha=0.25)
    fig.savefig(out_dir / "wpC_model_form_sensitivity.png", dpi=220)
    plt.close(fig)

    (out_dir / "wpC_extension_manifest.json").write_text(json.dumps({
        "status": "PASS", "centre_count": 1904, "scenarios": list(SCENARIOS),
        "source_boundary": "staged local derived products only",
    }, indent=2), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    run(args.input_dir, args.out)

