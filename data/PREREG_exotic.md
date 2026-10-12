# Pre-registration: multi-pool combination model (2026-10-12 12:15 UTC, before seeing results)

English translation. The original Korean document, as written at the time stamped above, is `PREREG_exotic.ko.md`.

- Combination: conditional logit over every ordered combination in a race. Features = log[ model HB combination probability, trifecta pool, trio pool, exacta pool (1st·2nd), quinella pool (1st·2nd), quinella place pool (sum over three pairs), win pool → HB combination ].
- Weight training: 2024 races only (ridge 0.01). Evaluation: races 2025-01 ~ 2026-09 (not used in training).
- Primary test (accuracy): "model + all market pools" vs. "all market pools"; the lower bound of the 95% CI of the per-race log-likelihood gain on trifecta outcomes must be > 0.
- Backtest rule (fixed): flat one unit on every trifecta combination with combined probability × actual odds > 1.2. No race filter. Secondary: the same rule on the trio.
  The 2025~ backtest is for reference (that period was seen once before). The official return test uses races from 2026-10 onward.
- Race selection (by maximum-EV segment) is labelled exploratory; any rule change is made only on data from 2026-10 onward.
