# Organization notes

## What was preserved

The reorganization keeps the original architectural pattern rather than
replacing it:

- `ChartAnalyzer` is the common contract.
- A registry discovers analyzers dynamically.
- Each analyzer owns three concerns that belong together: dataframe
  applicability, simple insight detection, and optional rendering.
- The orchestrator retains the original dictionary output contract.
- `@insight` metadata is retained, applied more consistently, and exposed as a catalog.
- The original SQL experiments remain available, with the two simpler parsers
  consolidated into a QueryDef-oriented context module.

## What changed

- Shared thresholds moved to `settings.py`.
- Shared numeric helpers moved to `statistics.py`.
- The large driver file was divided into column inference, engine, output,
  registry, analyzers, SQL parsing, and demo datasets.
- Analyzer filenames now describe their actual contents.
- Type annotations and several return-value mismatches were corrected.
- Histogram tests were separated into individually decorated insight functions.
- Line and scatter insight functions now also carry `@insight` metadata.
- Discovery order is stable, which makes tests and output reproducible.
- File paths and the runnable demonstration are no longer hard-coded to
  `C:\MapRock` or `C:\temp`.

## Deliberately not changed

This is an organization pass, not a statistical redesign. The October
thresholds and basic methods remain intact, including:

- trend based on mean first difference relative to baseline standard deviation;
- spike detection using robust z-scores of first differences;
- inflection detection based on pre/post windows and a sustained-sign test;
- correlation threshold of `0.7`;
- KMeans selection using silhouette score;
- bar dominance and dispersion thresholds.

Those methods deserve a later validation pass with real BI query results, but
changing them here would blur organization with model revision.

## Known next steps

1. Define structured insight objects rather than parsing meaning back from
   human-readable messages.
2. Store threshold, score, affected columns, detected interval, and analyzer
   metadata explicitly for the ISG `QueryDef`.
3. Separate visualization compatibility from insight-function applicability;
   some functions may apply even when a visualization would not be recommended
   to a human analyst.
4. Add pie/composition insights such as dominance, concentration, and long-tail
   structure rather than leaving pie as rendering-only.
5. Connect SQL-derived dice, metrics, filters, and lineage to the dataframe
   columns used by each detected insight.
