# WP-D extension boundary and re-entry plan

Status: **BLOCKED / not part of the v3 result** (2026-10-18)

The R04 local stage has no GBA tile manifest or fetched GBA outputs, and no
local Overture-extra output directory. The candidate local cache locations
were checked and were absent or unreachable. No raw geometry is included here.

The existing fetch scripts are not release-ready as written: the GBA script
contains private absolute paths and uses Source Cooperative S3; the Overture
script writes to a remote NatureHeat input location outside the local output
boundary and is therefore not executed.

A local DNS probe on 2026-10-18 could not resolve `source.coop`,
`beta.source.coop`, `us-west-2.opendata.source.coop`, or `api.github.com`
(`getaddrinfo failed`). This is a connectivity limitation, not evidence that
upstream products do not exist. No substitute geometry was downloaded or
imputed, and no GBA/Overture result is included in the manuscript or public
release package.

## Re-entry conditions

1. Make a documented network route available for the upstream source, or stage
   a licence-compatible local copy without changing the remote input tree.
2. Generate and QA a centre-to-tile manifest from the same 1,904-centre frame.
3. Redirect both fetchers to a local round output directory and parameterise
   all paths; retain source release/version and checksums.
4. Run a pilot on at least three centres spanning geometry-coverage classes,
   then run the full extension only after Parquet readability, CRS, footprint
   count, height missingness and centre coverage pass.
5. Treat any resulting GBA/Overture geometry as a separate extension; it must
   not overwrite `geometry_v3` or change the current QA'd main estimates.
