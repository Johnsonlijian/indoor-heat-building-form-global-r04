# R04 WP-C/D extension analysis contract

Date: 2026-10-18  
Status: deterministic local extension; no change to the v3 main run

## WP-C question and estimands

WP-C asks how much the already-QA'd global exposure estimates change under
four model-form stressors: removal of LCZ neighbour shading (`svf_none_v3`),
lower open-window air exchange (`ach_open_lo_v3`), the retained high-air-change
baseline (`ach_open_hi_v3`), and the second non-overlapping 72-h cooling-loss
window (`loss_rank2_v3`). The estimands are the population-summed annual
uncooled person-hours above 30 deg C, the population summed cooled residents
crossing 32 deg C operative temperature within 6/12/24 h of cooling loss, and
the fan-allowance proxy (`>31.8 deg C`) reported for the baseline only.

All scenario comparisons are paired by `ID_UC_G0` across the 1,904-centre frame.
Scenario differences are reported as absolute and percent change relative to
`main_v3`; no causal interpretation is assigned to these model-form changes.
The fan allowance is a thermal-model proxy, not a health or comfort threshold.

## Inputs and transformations

Inputs are local, already-QA'd city Parquets under the R04 stage output tree:
`tierA_exposure_city_{main_v3,svf_none_v3,ach_open_lo_v3,ach_open_hi_v3,loss_rank2_v3}.parquet`.
Only the named columns are read. Population sums are divided by 1e12 (person-h)
or 1e6 (people) for compact reporting. Pairwise quantiles use finite centre
values after an inner ID join; missing values are reported and are never
imputed. There is no random seed because the analysis is deterministic.

## Outputs and claim boundary

The script writes compact CSV/JSON summaries and one diagnostic figure to this
round's `outputs/`. These products support a supplementary sensitivity paragraph
and release-package documentation. They do not replace the main v3 estimates,
do not create observational validation, and do not extend the geographic frame.

WP-D is a feasibility and data-boundary assessment only. The current round may
not fetch or write to remote input trees; unavailable GBA/Overture tiles are
therefore recorded as blocked rather than substituted.
