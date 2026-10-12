# How Efficiently Do Korean Racing Betting Markets Reflect Public Information? A Pre-Registered Test of Seven Pool Types

2026-10-12 · Jungrun Kim

In Korean horse racing (Seoul and Busan-Gyeongnam, 2019–2026), trifecta pool prices are substantially improved by information from the trio and exacta pools, and on final odds the mispricing exceeds the 27% takeout. By contrast, the win and trio pools are efficient with respect to public information, and training-record features did not pass pre-registered tests.

## Abstract

This study tests the informational efficiency of seven pari-mutuel pool types in Korean horse racing. The data cover 12,824 races at Seoul and Busan-Gyeongnam from January 2019 to October 2026: race results, final odds for every combination in every pool, and daily training records. With a fundamental conditional logit model as the baseline, a multi-pool conditional logit that uses each pool's implied probabilities as features is trained on 2024 races and evaluated on 3,104 races from 2025 onward. There are three findings. First, the win pool is corrected, modestly but robustly, by place-pool information (per-race log-likelihood +0.003 to +0.005, passing three stages of validation). Second, the trio pool is efficient but the trifecta pool is not. Estimating trifecta combination probabilities from trio and exacta pool information alone is +0.027 per race more accurate than the trifecta pool itself, and in the combined model the trifecta pool's own weight is only 0.10. A final-odds backtest of the pre-registered rule (combined probability × odds > 1.2) returned +47% after the 27.3% takeout (95% CI +8% to +93%), but 57% of profit is concentrated in the top 20 hits. Third, training records published only in Korea (swimming, daily training, routine regularity) show consistent signs but fail the pre-registered criteria. The trifecta pool's inefficiency is interpreted as a consequence of pool thinness (about 925 combinations per race, median turnover about KRW 530 million). Accounting for market impact using pool turnover by bet type, a stake of KRW 10,000 per combination yields +35%, with breakeven at about KRW 56,000 per combination. However, value is spread thinly over 35–47 low-popularity combinations per race, cannot be captured by shortlisting candidates in probability order, and cannot be identified from the published odds of the 40 most popular combinations alone. The accuracy gain (+0.019) is retained using only the trio and exacta pools.

## 1. Introduction

### 1.1 How this study began

This study began in the broadcast booth. The author produces and presents the Korea Racing Authority's international race broadcasts, has delivered more than 1,000 live race broadcasts, and studies applied AI in the M.S. in Artificial Intelligence program at Yonsei University. Watching the odds board race after race raised two questions.

First, KRA publishes every day, as open public data, material that almost no other jurisdiction releases: racehorses' daily training records and swimming-training records (Korea Racing Authority, 2026). Academic handicapping models rely mainly on race-result variables such as past performance, jockey, trainer and race conditions (Bolton & Chapman, 1986; Benter, 1994), and we found no study that tests market efficiency with daily training time or swimming records. If these data carry information the market has not yet priced, they would be features absent from the literature. In particular, we wanted to test a trackside intuition: that a steady training routine is itself a sign of a healthy horse in stable condition.

Second, from the track it is plain that the amount of money differs greatly across bet types. In the trifecta, money is spread thinly over hundreds of combinations, the racecourse displays odds only for the 40 most popular combinations, and trifecta odds barely move even just before the close. The suspicion was that information about the same race may be priced differently in different pools.

The study's first result was the place gap. A single variable, the degree to which relative support in the win and place pools diverges, carried information beyond the fundamental model and win odds, and passed all three independent validations (Section 4). From then on, the central aim of the study was **to find anything more significant than the place gap**. We tested, in turn, Korea-only training records (swimming, seven daily-training features, routine regularity), race-result combinations that prior studies had not placed in one model (running style × track condition × distance, opponent composition, first-up × jockey), and market-response combinations (three-way disagreement, place gap by horse situation). **None of them surpassed the place gap or added information on top of it.** The training-load feature, chosen after seeing results, vanished in the sealed holdout (Section 7), and the pre-registered routine hypothesis had the expected sign but was not statistically confirmed.

That failure redirected the study. If the market already digests public fundamental information, the remaining inefficiency may lie not in missing information but in the structure of the market itself: how money is distributed across pools. KRA's publication of final odds for every combination in all seven bet types made the second question testable. In the trifecta pool, information from the other pools alone improved per-race log-likelihood by +0.027 (Section 5). This is not new information about horses; it is a pricing inefficiency in which information already in the market fails to reach a thin pool, and because the prediction target differs (the 1st–2nd–3rd combination rather than the winner) it cannot be compared directly with the place gap. As information about horses, the most significant signal this study found remained the place gap.

### 1.2 Related literature

Racetrack betting markets, as prediction markets with quickly resolved outcomes and publicly posted prices, have long been a classic setting for tests of market efficiency. Surveying the field, Sauer (1998) concluded: "First, prices set in these markets, to a first approximation, are efficient forecasts of outcomes." This study asks where that first approximation breaks down. The related literature falls into three strands.

**Biases in the win pool.** Ali (1977) and Thaler & Ziemba (1988) documented the favorite–longshot bias, in which longshots are overvalued in the win pool. Snowberg & Wolfers (2010) summarize the pattern as "longshots are overbet, while favorites are underbet," and, using exacta, quinella and trifecta prices jointly, show that it stems from misperception of probabilities rather than risk-love. The place-gap result in Section 4 is evidence that place-pool information partially corrects this bias.

**Cross-pool inconsistency.** Hausch, Ziemba & Rubinstein (1981) used win-pool probabilities to find mispricing in the place and show pools and showed that cross-pool inconsistencies can be turned into profit. Studying the same race sold at several tracks, Hausch & Ziemba (1990) reported that "The data suggest that the odds vary, and they often vary dramatically, allowing arbitrage opportunities." Asch & Quandt (1987) tested the efficiency and profitability of exotic bets such as the exacta. Sections 5–6 of this study move that framework from win-versus-exotic comparisons to comparisons among exotic pools (pricing the trifecta from the trio and exacta).

**Probability models.** Bolton & Chapman (1986) laid down the basic form of modern handicapping models: "A multinomial logit model of the horse racing process is posited and estimated on a data base of 200 races." Extending this in practice, Benter (1994) argued that "what is needed is a way to combine the judgements of two experts, (i.e. the fundamental model and the public)," and proposed a log-linear combination of fundamental and market probabilities. The baseline in Section 3.2 follows these two studies.

Finishing-order probabilities start with Harville (1973), who framed the problem as "assessing the probabilities of the various possible orders of finish of a horse race" and gave a formula that computes them from win probabilities alone. Benter (1994), however, observed that under this formula "The tendency is for low probability horses to finish second and third more often than predicted," and Lo & Bacon-Shone (1994) likewise reported that "the probabilities produced by the Harville model have a systematic bias for the strongest and weakest horses." Section 3.4 follows this correction and estimates stage-wise exponents λ₂, λ₃.

The literature leaves two gaps. First, cross-pool comparisons have mostly evaluated exotic pools against the win pool; pricing exotic pools from one another has not been studied. Second, Korean racing is a rare market that publishes, as open public data, final odds for every combination in all seven bet types together with daily training records, yet no study has used these data to test efficiency.

### 1.3 Research questions

This study answers three questions. (1) Does place-pool information contain information beyond the win pool and a fundamental model? (2) Are trio and trifecta pool prices improved by other pools and the fundamental model, and if so, does the improvement exceed the takeout? (3) Do training records published only in Korea contain information the market fails to reflect? To prevent false discoveries from multiple comparisons, feature definitions and decision criteria were fixed in writing in advance and scored only once (pre-registration), and all rejected results are reported.

### 1.4 Scope of the investigation

Before presenting results, we state the scope of the testing that led to these conclusions. There were 18 formal tests (Appendix A). Fourteen were feature tests for win-pool prediction, and only the place gap passed (two tests: the test period and the sealed holdout). The other twelve (seven on training records, five on race-result and market-response combinations) all failed. Of the four tests on combination pools, the two adding other information to the trifecta pool passed, the trio pool was more accurate than the alternatives, and the pre-registered primary test (does the fundamental model add information on top of all market pools?) was rejected. All rejected results are reported in the main text and appendices.

| Item | Scope |
| --- | --- |
| Period | 2019-01 ~ 2026-10 (Seoul and Busan-Gyeongnam) |
| Races / starters | 12,824 races / 143,239 starters |
| Final odds | Every combination in seven bet types, about 1,400 combinations per race |
| Training records | Daily training 2,465,789 rows, swimming 183,612 rows |
| Pool turnover by bet type | 86,028 rows (11,907 trifecta races) |
| Evaluation races | Win pool 3,132 races, combination pools 3,104 races (2025-01~2026-09); sealed holdouts 1,629 + 3,813 races |
| Evaluation combinations | 3,348,982 trio and trifecta combinations (single-source comparison); about 2.9 million ordered-combination rows (multi-pool evaluation) |
| Formal tests | 18: 4 passed, 11 rejected, 1 borderline, 1 selection bias, 1 market better |
| Win-pool feature tests | 14: place gap passed twice; all 7 training-record tests and 5 race-result/market-response combination tests failed |
| Pre-registered or sealed-holdout scoring | 4 (#10, #11, #14, #18) |
| Exploratory analyses | 6 simple-blend backtests (E.2), 10 multi-pool backtests (E.3), 3 race-selection segments (E.6), 8 market-impact scenarios (E.8), 4 top-40-odds strategies (9.1), 4 shortlist sizes (9.2), 6 input-pool combinations (9.3), analysis of 98 trainers (D.5) |

## 2. Data

All data were collected from the Korea Racing Authority (KRA) open APIs on the Korean public data portal, data.go.kr (Korea Racing Authority, 2026). The sample is thoroughbred racing at Seoul and Busan-Gyeongnam; Yeongcheon, which has many anomalous records from its early opening period, and Jeju, which races a different breed, are excluded. The 347 races with win odds recorded as 9999.9 (mostly Busan-Gyeongnam in 2020) are treated as odds errors and excluded.

| Data | API | Range | Size |
| --- | --- | --- | --- |
| Race results (finishing order, sectional times, win and place odds, weight carried, ratings, etc.) | API4_3 | 2019-01 ~ 2026-10 | 12,824 races, 143,239 starters |
| Final odds (every combination in win, place, quinella, exacta, quinella place, trio, trifecta) | API160_1 | 2019-01 ~ 2026-10 | about 1,400 combinations per race |
| Daily training records (training time, rider type) | API18_1 | 2019-01 ~ 2026-10 | 2,465,789 rows |
| Swimming training | API216 | 2020-03 ~ 2026-10 | 183,612 rows |
| Pool turnover by bet type | API179_1 | 2019-01 ~ (collection ongoing) | 7 rows per race |

The final-odds data contain closing odds for every combination, not only the winning one, so each pool's implied probability distribution can be reconstructed. The odds of winning combinations were confirmed to match KRA's official payouts using Seoul races on 11 October 2026. The takeout backed out from the odds is 27.3% for the trifecta and 27.0% for the trio. Since 2025, trifecta pool turnover has a median of KRW 527 million (10th percentile KRW 363 million, 90th percentile KRW 681 million); yearly medians grew from KRW 406 million in 2019 to KRW 573 million in 2026 at Seoul and from KRW 292 million to KRW 515 million at Busan-Gyeongnam. In 2021, with races run without spectators due to COVID-19, the median was only KRW 60–70 million.

The sample is split as follows: fundamental model training 2019–2023, combination-weight training 2024, evaluation January 2025 – September 2026. For the final check of training features, periods never used in the analysis (November 2025 – September 2026, and 2019–2021) were sealed as holdouts and used only once.

## 3. Methods

In race r, horses i = 1, …, n start. The final odds for combination c in pool X are written O^X_c.

### 3.1 Pool implied probabilities and takeout

Each pool's implied probabilities are the reciprocals of the odds normalized to sum to one within the race, and the takeout follows from the sum before normalization.

```latex
\\pi^X_c = \\frac{1/O^X_c}{\\sum_{c'} 1/O^X_{c'}}, \\qquad t^X = 1 - \\frac{1}{\\sum_{c'} 1/O^X_{c'}}
```

The win-pool implied probability is written w_i and the relative support share in the place pool q_i.

### 3.2 Baseline: combining the fundamental model with the market

The conditional logit probability p^L_i, trained on 78 variables covering past performance, jockey, trainer and race conditions, is combined with the win-market probability w_i in the manner of Benter (1994). The weights were estimated on 2024 races (α = 0.182, β = 0.884).

```latex
p^C_i = \\frac{\\exp(\\alpha \\ln p^L_i + \\beta \\ln w_i)}{\\sum_j \\exp(\\alpha \\ln p^L_j + \\beta \\ln w_j)}
```

### 3.3 Place gap

The degree to which relative support in the win and place pools diverges is defined as a single variable and added on top of the baseline in a conditional logit. The coefficient on the asymmetric term max(g, 0) was estimated at zero and dropped from the final model.

```latex
g_i = \\ln \\frac{q_i}{w_i}, \\qquad P(i) = \\frac{\\exp(b_0 \\ln p^C_i + b_1 g_i)}{\\sum_j \\exp(b_0 \\ln p^C_j + b_1 g_j)}
```

### 3.4 Finishing-order probabilities: Harville–Benter correction

From the win-probability vector p, the probability of the 1st–2nd–3rd ordered combination (i, j, k) is computed with the Harville (1973) formula augmented by stage-wise exponents λ₂, λ₃. Exponents below one flatten the probabilities at the 2nd and 3rd stages, reducing the overestimation of longshots finishing in the minor places. The exponents were estimated by maximizing the log-likelihood of actual finishing orders in 2019–2024. A trio probability is the sum of the six ordered-combination probabilities of the same three horses.

```latex
P_{HB}(i,j,k \\mid p, \\lambda) = p_i \\cdot \\frac{p_j^{\\lambda_2}}{\\sum_{m \\neq i} p_m^{\\lambda_2}} \\cdot \\frac{p_k^{\\lambda_3}}{\\sum_{m \\notin \\{i,j\\}} p_m^{\\lambda_3}}
```

### 3.5 Multi-pool combination: combination-level conditional logit

This is the core model of the study, hereafter referred to as the **Ryoonicorn Theorem**. Every ordered combination c = (i, j, k) in a race is treated as a choice alternative, and for each information source f the log of the probability π_f(c) it assigns to that combination is used as a feature. There are seven sources: π₁ = Harville–Benter combination probability from the fundamental model's win probabilities, π₂ = trifecta pool, π₃ = trio pool (the set {i, j, k}), π₄ = exacta pool (i, j), π₅ = quinella pool ({i, j}), π₆ = product of the quinella place pool probabilities of the three pairs {i,j}, {i,k}, {j,k}, π₇ = Harville–Benter combination probability from the win pool's win probabilities.

```latex
P_\\beta(c \\mid r) = \\frac{\\exp\\left(\\sum_{f=1}^{7} \\beta_f \\ln \\pi_f(c)\\right)}{\\sum_{c' \\in \\mathcal{C}_r} \\exp\\left(\\sum_{f=1}^{7} \\beta_f \\ln \\pi_f(c')\\right)}, \\qquad \\mathcal{C}_r = \\{(i,j,k): i \\neq j \\neq k\\}
```

The weights are obtained by maximizing the log-likelihood of the actual 1st–2nd–3rd combination c*_r in 2024 races with an L2 penalty (λ = 0.01). A weight vector that puts 1 on a single source is that pool's stand-alone model, so the additional information of each source is measured as the log-likelihood difference between models with and without it.

```latex
\\hat{\\beta} = \\arg\\max_{\\beta} \\sum_{r \\in \\mathcal{R}_{2024}} \\ln P_\\beta(c^*_r \\mid r) - \\lambda \\|\\beta\\|^2
```

### 3.6 Evaluation metrics and tests

Accuracy is measured as the mean log probability assigned to the actual outcome over R evaluation races, and two models are compared by the mean per-race difference Δ with a 95% confidence interval from a race-level bootstrap (3,000 replications). An improvement is accepted only when the lower bound of the confidence interval is above zero. The win-pool analysis uses the probability assigned to the winner; the combination-pool analysis uses the probability assigned to the actual 1st–2nd–3rd combination.

```latex
\\Delta = \\frac{1}{R} \\sum_{r=1}^{R} \\left[ \\ln P_{\\text{new}}(c^*_r) - \\ln P_{\\text{base}}(c^*_r) \\right]
```

Calibration by segment is assessed with the A/E ratio, actual wins divided by expected wins. A value above one means horses in that segment won more often than expected.

```latex
\\text{A/E}(G) = \\frac{\\sum_{i \\in G} \\mathbf{1}[i \\text{ wins}]}{\\sum_{i \\in G} \\hat{p}_i}
```

### 3.7 Value betting rule (pre-registered)

One flat unit is bet on every combination whose combined probability times actual odds (net of takeout) exceeds 1.2. The threshold of 1.2 and "no race filter" were fixed in writing before the results were seen. Return is total payout divided by the number of bets minus one, with confidence intervals from a race-level bootstrap (1,000 replications). Calibration of the combined probabilities is checked by comparing the expected number of hits among the selected bets, ΣP̂(c), with the actual number of hits.

```latex
\\text{EV}_c = \\hat{P}(c) \\cdot O_c > 1.2, \\qquad \\text{ROI} = \\frac{\\sum_{c \\in B} \\mathbf{1}[c \\text{ hits}] \\cdot O_c}{|B|} - 1
```

## 4. Finding 1: The win pool is corrected by place-pool information

Adding the place gap g to the baseline model improved the winner's log-likelihood significantly in all three independent validations. The estimated coefficients are b₀ = 1.149 and b₁ = 0.315, so a horse whose place-pool support share is twice its win-pool share gains about 24% in relative weight. b₀ > 1 means the baseline probabilities are slightly too flat; taken together, the two effects lower longshots overall while rescuing only those horses on which money concentrates in the place pool.

| Validation | Races | Per-race log-likelihood gain | 95% CI |
| --- | --- | --- | --- |
| Test (2025-01~2026-09, weights trained on 2019~2024) | 3,132 | +0.0028 | +0.0009 ~ +0.0048 |
| Walk-forward (2023, 2024, 2025, each trained on the preceding period) | 4,974 | +0.0024 | +0.0008 ~ +0.0040 |
| Sealed holdout (2025-11~2026-09, pre-registered) | 1,629 | +0.0046 | +0.0015 ~ +0.0076 |

The gain amounts to 40–70% of the margin by which the baseline model beat win odds alone (+0.0065). The effect comes from longshots. Splitting the place-versus-win support gap into quintiles, the top 20% (horses relatively more supported in the place pool, mean win rate 2.1%) have A/E of 1.086 against the baseline model and 1.067 against the win market, while the bottom 20% have 0.974 and 0.988 respectively. This is consistent with place-pool information partially correcting the win pool's favorite–longshot bias. By year, the gain was positive in every year except 2019.

This result applies the cross-pool inconsistency logic of Hausch, Ziemba & Rubinstein (1981) in the reverse direction (place → win). Because the Korean place bet pays on a top-three finish (fields of eight or more), it is closer to the Hong Kong market than to the US place bet, which pays on a top-two finish.

## 5. Finding 2: The trio pool is efficient; the trifecta pool is not

### 5.1 Harville–Benter correction exponents

Estimated on 9,271 races from 2019–2024, the exponents are λ₂ = 0.763, λ₃ = 0.640 for the fundamental model and λ₂ = 0.773, λ₃ = 0.652 for the win pool. Both are well below one, in the same direction as international studies (Lo & Bacon-Shone, 1994) finding that the plain Harville formula overestimates longshots' probabilities of finishing 2nd and 3rd.

### 5.2 Single-source comparison

On 3,104 races from 2025 onward, the log probability assigned to the actual 1st–2nd–3rd combination was compared across information sources. The reference is the implied probability of the pool for that bet type.

| Source | Trio (154 combinations/race) | Trifecta (925 combinations/race) |
| --- | --- | --- |
| Fundamental model → combination | −0.046 (−0.057 ~ −0.035) | −0.006 (−0.019 ~ +0.007) |
| Win pool → combination | −0.070 (−0.082 ~ −0.059) | −0.032 (−0.046 ~ −0.018) |
| Own pool odds (reference) | 0 | 0 |
| Model and own pool, 50:50 blend | −0.010 (−0.016 ~ −0.005) | +0.016 (+0.009 ~ +0.023) |

Trio pool prices are more accurate than the fundamental model and get worse when the model is blended in. The trifecta pool is on par with the fundamental model, and blending the two is more accurate than the market.

### 5.3 Multi-pool combination weights

Weights estimated on 1,761 races in 2024. For predicting trifecta combinations, the trifecta pool's own weight is only 0.1, while the trio and exacta pools carry most of the information. The negative weight on the quinella pool is a correction term arising from collinearity with the exacta pool.

| Source | Market pools only | Model + market pools |
| --- | --- | --- |
| Fundamental model → combination | — | +0.760 |
| Trifecta pool | +0.098 | +0.090 |
| Trio pool | +0.650 | +0.594 |
| Exacta pool | +0.668 | +0.529 |
| Quinella pool | −0.324 | −0.253 |
| Quinella place pool | −0.043 | −0.082 |
| Win pool → combination | +0.106 | −0.514 |

### 5.4 Evaluation: trifecta-combination log-likelihood (2025-01~2026-09, 3,104 races)

| Model | Per-race log-likelihood | vs. all market pools combined (95% CI) |
| --- | --- | --- |
| Raw trifecta pool odds | −5.618 | — |
| Trifecta pool only (scale-corrected) | −5.617 | −0.027 (−0.034 ~ −0.020) |
| Fundamental model only | −5.624 | −0.034 (−0.044 ~ −0.024) |
| Model + trifecta pool | −5.602 | −0.012 (−0.018 ~ −0.006) |
| All market pools combined (no model) | −5.590 | 0 (reference) |
| Model + all market pools | −5.587 | +0.003 (−0.001 ~ +0.008) |

Two points stand out. First, combining the other market pools alone is +0.027 per race more accurate than the trifecta pool itself, more than five times the gain obtained from the place gap in the win pool. Second, the pre-registered primary test (model + all market pools vs. all market pools) did not pass. The information that the fundamental model added over the trifecta pool alone (+0.016 in Section 5.2) is already contained in the trio and exacta pools. In short, the trifecta pool's inefficiency is not an absence of fundamental information; it is the failure of information already in the market to be reflected in the prices of a thin pool.

## 6. Finding 3: Value betting on final odds beats the takeout, but profit is concentrated in jackpots

The pre-registered rule (combined probability × actual odds > 1.2, flat one unit, no race filter) was scored on final odds. Actual odds include the 27.3% takeout, so the expected return of random betting is −27.3%.

| Period · model | Bets | Hits (model expected) | Return | 95% CI |
| --- | --- | --- | --- | --- |
| 2024 (training year, reference) · model + market pools | 41,321 | 43 (42.5) | +13.8% | −34% ~ +63% |
| 2025-01~2026-09 · model + market pools | 88,305 | 117 (111.2) | +47.1% | +8% ~ +93% |
| 2025-01~2026-09 · market pools only | 54,298 | 64 (62.1) | +58.7% | −4% ~ +129% |
| 2025-01~2026-09 · trio (reference) | 1,746 | 2 (5.5) | −92.0% | — |

Three points. First, the number of hits matches the model's expectation, so the combined probabilities remain calibrated on the selected combinations. Accordingly, the model's expected return (+37%) and the realized return (+47%) lie in the same range. Second, the profit arises even when only market pools are combined; the source is cross-pool inconsistency, not the fundamental model. Third, by half-year the return was +15% in H1 2025, +65% in H2 2025, +60% in H1 2026 and +52% in H2 2026, positive in all four periods.

The distribution of returns, however, resembles a lottery. The median odds of the combinations bet are 1,919, and their median trifecta-pool implied probability is 0.038%, one third of the uniform probability (0.108%). An average of 29 bets per race hits once every 26 races, and of the 117 hits the top 20 account for 57% of payouts. Excluding those 20, the return is −37%. In the trio pool the same rule loses money, consistent with the efficiency result in Section 5.

An exploratory analysis selecting races by their maximum per-race expected value showed no consistent pattern in returns across segments, so race selection is not part of the rule.

## 7. Finding 4: Training-record features do not pass pre-registered tests

KRA publishes racehorses' daily training time, rider type and swimming-training records every day. Three features tested whether these data contain information beyond the baseline model and the place gap. The decision criterion is that the lower bound of the 95% confidence interval for the per-race log-likelihood gain be above zero.

| Feature | Definition | Validation period | Races | Gain (95% CI) | Decision |
| --- | --- | --- | --- | --- | --- |
| Swimming sessions | Days with swimming in the 14 days before the race | 2025-01~2026-09 | 3,140 | +0.0006 (−0.0002 ~ +0.0015) | Rejected |
| Training-load change | Training time in the previous 14 days vs. daily average 15–60 days before (log difference) | Walk-forward 2023~2025 | 4,974 | +0.0023 (+0.0007 ~ +0.0037) | Hypothesis selected |
| Training-load change | Same | Sealed 2025-11~2026-09 | 1,629 | −0.0005 (−0.0035 ~ +0.0026) | Rejected |
| Routine regularity | Coefficient of variation of weekly training days over the previous 8 weeks, relative to the same trainer's average | Sealed 2019-03~2021-12 | 3,813 | +0.0004 (−0.0007 ~ +0.0016) | Rejected |

Training-load change was chosen among seven candidates after seeing walk-forward results, so it carried selection bias, and the gain vanished in the sealed holdout. Routine regularity was scored once on the sealed holdout after its definition and criteria were fixed in writing. The coefficient had the hypothesized sign (−0.052), and A/E from the most regular quintile relative to the trainer down was 1.07, 1.03, 1.07, 0.97, 0.97, nearly replicating the pattern in 2022–2026 (1.06, 1.04, 1.06, 0.99, 0.97), but with an effect size about one tenth of the place gap it was not statistically confirmed. A pooled approximation over the two independent periods is +0.0005 (95% CI −0.0004 ~ +0.0014), implying about an 87% probability that the effect is positive.

Incidentally, differences between trainers explain 19.5% of the variation in weekly training days, and trainers with a regular style were themselves unrelated to performance (correlation −0.07 across 78 trainers). Any routine signal, therefore, reflects the condition of individual horses within the same stable, not the trainer's habits. The formal conclusion of this section is that "the Korean racing market already largely reflects public training information."

## 8. Discussion and limitations

### 8.1 Why only the trifecta pool is inefficient

The trio pool carries KRW 0.7–1.1 billion over 154 combinations per race; the trifecta carries around KRW 500 million over 925. The average amount per combination differs by a factor of about nine, and in the trifecta about 20% of a race's combinations have so little money that they hit the odds cap (9999.9). Small bets by individual bettors move combination-level prices substantially. The interpretation that information about the same horses is reflected in prices in the thick pools (trio, exacta) but buried in noise in the thin pool matches the combination weights (trifecta pool 0.1, trio and exacta pools 0.6–0.7). This extends the cross-pool inconsistency framework of Hausch, Ziemba & Rubinstein (1981) to comparisons among exotic pools, and is a stronger claim in that it is reproduced from market information alone, without a fundamental model.

### 8.2 Why backtest returns cannot be read as real-world returns

First, the final-odds assumption. Bets are placed before the close, and odds at that time differ from final odds. Second, market impact. Value combinations are those with almost no money on them, so the bettor's own stake lowers the odds. With total pool S, takeout t, and amount already on combination c, A_c = S(1 − t)/O_c, the odds after adding a stake B are:

```latex
O'_c = \\frac{(S + B)(1 - t)}{A_c + B}, \\qquad A_c = \\frac{S(1-t)}{O_c}
```

Using pool turnover by bet type (API179_1), this correction was applied to all 3,104 races in the evaluation period. The median amount already on the selected combinations is KRW 185,000; a stake of KRW 10,000 per combination lowers odds by 5.1% and reduces the return from +47.1% to +34.5%. At KRW 30,000 per combination the return is +18.0%, and at KRW 100,000 it is −10.7%. The stake at which the model's expected return reaches zero is about KRW 56,000 per combination, or about KRW 1.63 million per race (Appendix E.8). Market impact thus does not change the result for small stakes, but caps the strategy's capacity at a few hundred thousand to about a million won per race. Third, variance. Twenty of the 117 hits account for 57% of profit, so a backtest of about 3,000 races necessarily has wide confidence intervals. Fourth, the period from 2025 onward is clean for accuracy evaluation, but for return evaluation it had already been viewed once in the backtest of the simple blend model.

### 8.3 Multiple comparisons and pre-registration

This study experienced selection bias directly with the training-load change feature: a feature significant in walk-forward testing disappeared in the sealed holdout. All subsequent tests were scored once after definitions, training periods and decision criteria were fixed in writing, and all rejected results are reported. Signals visible only in subgroups, such as the swimming-training effect seen only at Busan-Gyeongnam (A/E 1.09), are recorded as hypotheses only.

### 8.4 Design of follow-up validation

Races from October 2026 onward serve as the official confirmation period, with the following fixed: (1) combination weights remain the 2024 estimates; (2) the accuracy test is the log-likelihood difference between all market pools combined and the trifecta pool alone; (3) the return is that of the EV 1.2 rule with the market-impact correction. Judging real-world feasibility additionally requires prospective validation that records odds just before the close.

## 9. Feasibility under information constraints

KRA does not provide live odds during betting through its public API, and at the racetrack only the odds of the 40 most popular trifecta combinations are displayed. Using the same data, we examined whether the inefficiency in Sections 5–6 can be exploited under this constraint. The analysis in this section is exploratory, post-dating pre-registration, and reuses the evaluation period from 2025 onward.

### 9.1 The odds of the 40 most popular combinations are not enough to identify value combinations

Of the combinations selected by the pre-registered rule, 99.3% lie outside the 40 most popular (median odds of the 40th combination 138, median odds of selected combinations 1,919). For combinations outside the top 40, only a lower bound on their odds ("higher than the 40th") is known.

| Strategy (when only the top 40 trifecta odds are known) | Bets per race | Hits (expected) | Return (95% CI) |
| --- | --- | --- | --- |
| Reference: EV > 1.2 with all odds known | 29.1 | 117 (111) | +47.1% (+7 ~ +96) |
| A. Outside top 40 & probability × 40th odds > 1.0 (guaranteed lower bound) | 1.6 | 10 (10.2) | +28.0% (−49 ~ +127) |
| B. Top 5 by probability outside top 40 | 5.0 | 85 (94) | −13.0% (−31 ~ +6) |
| B. Top 15 by probability outside top 40 | 15.0 | 248 (243) | −9.7% (−21 ~ +1) |
| C. EV > 1.2 inside top 40 | 1.9 | 7 (7.9) | −0.4% (−76 ~ +89) |

Combinations the model rates as likely are rated as likely by the market too, so their odds are low; value is scattered among low-popularity combinations ranked roughly 100–300 by probability. Strategies that choose combinations by probability alone without seeing odds (B) therefore lose, and the guaranteed-lower-bound strategy (A) yields only 1–2 bets per race, too few for a reliable sample. Identifying value combinations requires those combinations' trifecta odds.

### 9.2 Shortlisting candidates is not possible

Even with trifecta odds known, buying EV > 1.2 combinations only within the top K candidates by probability captures almost none of the profit. In 487 twelve-runner races (1,320 combinations each), the share of total profit captured for K = 5, 10, 20, 30 was 0%, 0%, 0% and 1%, while unrestricted buying meant 46.7 combinations per race and one hit every 23 races. Value is not concentrated in a few combinations but spread thinly over dozens, consistent with the interpretation in Section 8.1 that the trifecta pool's inefficiency stems not from errors in particular combinations but from noise across a thin pool. The number of combinations bought is controlled only by the EV threshold: in twelve-runner races, a threshold of 1.2 gives about 47 per race and 1.4 about 35.

### 9.3 Reducing input pools: trio and exacta are sufficient

Recording all seven pools for every race is impractical on site. Combination models with fewer input pools were compared in the same way (trained 2024, evaluated 2025 onward).

| Input pools | Accuracy vs. trifecta pool (95% CI) | EV > 1.2 bets | Hits (expected) | Return (95% CI) |
| --- | --- | --- | --- | --- |
| Trio only | −0.084 (−0.102 ~ −0.067) | 485,935 | 448 (861) | −8.2% |
| Trio + win | −0.006 (−0.018 ~ +0.005) | 257,139 | 214 (343) | −10.9% |
| Trio + exacta | +0.019 (+0.010 ~ +0.029) | 149,106 | 197 (244) | (−4 ~ +54) |
| Trio + exacta + win | +0.020 (+0.011 ~ +0.029) | 134,701 | 162 (206) | +14.1% |
| All market pools | +0.027 (+0.020 ~ +0.034) | 54,298 | 64 (62) | +58.7% |
| Model + all market pools | +0.030 (+0.021 ~ +0.038) | 88,305 | 117 (111) | +47.1% |

The trio carries "which three horses" and the exacta "the order of 1st and 2nd", so together they yield the trifecta order. The two-pool model is about 30% less accurate than the full model and, with hits at 81% of expectation, somewhat overestimates probabilities, so the threshold is raised to 1.4 when using it. In twelve-runner races, the two-pool model with threshold 1.4 bought 34.5 combinations per race, hit once every 41 races, and returned +43.4% (95% CI −56% ~ +180%).

### 9.4 Operating rule and prospective validation design

From the results above, the following rule is derived and applied in prospective validation from October 2026. Seven minutes before the close, photograph the full-combination odds screens for the trio, exacta and trifecta, and check the recognized odds by whether each pool's sum of 1/odds matches 1/(1 − t). Compute every combination's probability with the two-pool model, multiply by trifecta odds, and buy every combination with EV > 1.4 (about 35–47 per race, with no human additions or removals). Stakes are limited to KRW 1,000–10,000 per combination (breakeven KRW 56,000 per Section 8.2). For each race, record the odds seven minutes before, final odds and whether it hit, and assess separately (1) the gap between seven-minute and final odds, (2) agreement between hits and model expectation (calibration), (3) the primary accuracy test, and (4) the return. Field experience suggests trifecta odds do not move much before the close, but since only KRW 100,000–200,000 is on the selected combinations, (1) is to be confirmed empirically. Because the strategy is the mechanical, repeated purchase of dozens of combinations rather than the selection of a few, execution presupposes means of acquiring all combination odds at once and placing many bets at once.

## 10. Conclusion

The efficiency of Korean racing betting markets divides along pool thickness. The win and trio pools reflect public information well, and the information added by the fundamental model and public training records is small or unconfirmed. The trifecta pool, by contrast, fails to price even the information already in the trio and exacta pools, and on final odds the gap exceeds the 27% takeout. The study contributes three things: a method for measuring inconsistency among exotic pools with a combination-level conditional logit; an efficiency test of all-bet-type combination odds and training records that is possible only with Korean public data; and a validation procedure that, through pre-registration, reports rejected results as well. Even after accounting for market impact, expected value remains positive up to tens of thousands of won per combination, but value is spread thinly across dozens of low-popularity combinations per race, so candidates cannot be shortlisted, and identification requires trifecta odds for every combination. This inefficiency is therefore statistically clear but costly to execute, which appears to be why it persists in the market. Prospective validation recording pre-close odds (Section 9.4) remains.

## Appendix A. Full list of tests performed (2026-10-12)

All gains are per-race log-likelihood differences; parentheses are 95% confidence intervals. The baseline for win-pool analyses is the baseline model (p^C); baselines for combination-pool analyses are given in the table.

| # | Feature / model | Baseline | Validation period | Races | Gain (95% CI) | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Swimming training (days in previous 7/14/30, sessions) | Baseline | 2025~ test | 3,140 | +0.0006 (−0.0002 ~ +0.0015) | Rejected |
| 2 | Place gap g | Baseline | 2025~ test | 3,132 | +0.0028 (+0.0009 ~ +0.0048) | Passed |
| 3 | Running style × track moisture × distance | Baseline | 2025~ test | 3,132 | +0.0004 (−0.0002 ~ +0.0009) | Rejected |
| 4 | Opponent composition (pace contention) | Baseline | 2025~ test | 3,132 | +0.0007 (+0.00002 ~ +0.0014) | Borderline |
| 5 | First-up × same jockey | Baseline | 2025~ test | 3,132 | 0.0000 (−0.0010 ~ +0.0009) | Rejected |
| 6 | Three-way disagreement (place, win, model) | Baseline + g | 2025~ test | 3,132 | +0.0001 (−0.0007 ~ +0.0010) | Rejected |
| 7 | Place gap × horse situation (first-up, jockey change, debut, class rise) | Baseline + g | 2025~ test | 3,132 | +0.0005 (−0.0001 ~ +0.0011) | Rejected |
| 8 | Seven daily-training features jointly | Baseline + g | Walk-forward 2023~2025 | 4,974 | +0.0017 (−0.0002 ~ +0.0037) | Rejected |
| 9 | Training-load change (selected from 8) | Baseline + g | Walk-forward 2023~2025 | 4,974 | +0.0023 (+0.0007 ~ +0.0037) | Selection bias |
| 10 | Place gap (final check) | Baseline | Sealed 2025-11~2026-09 | 1,629 | +0.0046 (+0.0015 ~ +0.0076) | Passed |
| 11 | Training-load change (final check) | Baseline | Sealed 2025-11~2026-09 | 1,629 | −0.0005 (−0.0035 ~ +0.0026) | Rejected |
| 12 | Four routine features jointly (gaps, weekly days, start time, intensity variation) | Baseline + g | Walk-forward 2023~2026 | 6,603 | +0.0005 (−0.0006 ~ +0.0016) | Rejected |
| 13 | Routine: weekly training-day regularity alone | Baseline + g | Walk-forward 2023~2026 | 6,603 | +0.0006 (−0.0007 ~ +0.0019) | Rejected (coefficient negative in all 4) |
| 14 | Routine: weekly regularity relative to trainer (pre-registered) | Baseline + g | Sealed 2019-03~2021-12 | 3,813 | +0.0004 (−0.0007 ~ +0.0016) | Rejected |
| 15 | Trio: model and trio pool 50:50 | Trio pool | 2025~ test | 3,104 | −0.010 (−0.016 ~ −0.005) | Market better |
| 16 | Trifecta: model and trifecta pool 50:50 | Trifecta pool | 2025~ test | 3,104 | +0.016 (+0.009 ~ +0.023) | Passed |
| 17 | Trifecta: all market pools combined | Trifecta pool | 2025~ test | 3,104 | +0.027 (+0.020 ~ +0.034) | Passed |
| 18 | Trifecta: model + all market pools (pre-registered primary test) | All market pools | 2025~ test | 3,104 | +0.003 (−0.001 ~ +0.008) | Rejected |

Only the place gap (2, 10) and adding other pools' information to the trifecta pool (16, 17) passed. The fundamental model adds information relative to the trifecta pool alone (16), but that information disappears once the trio and exacta pools are included (18).

### A.1 Data and sample sizes by experiment

Numbers match the table in Appendix A. "Starters" are horse-level observations (race × horse); "races" are the choice units of the conditional logit. All experiments exclude races with win odds of 9999.9 (347 races) and Yeongcheon and Jeju, and the conditional logits use only races with exactly one winner.

| # | Experiment | Data used | Training sample | Evaluation sample |
| --- | --- | --- | --- | --- |
| Baseline | Fundamental model p^C (prior study) | Race results API4_3, 140,836 starters (Seoul 82,223, Busan-Gyeongnam 58,314; 299 at Yeongcheon excluded) | Conditional logit 2019~2023; combination weights 1,770 races in 2024 | 2025-01~ 3,140 races |
| 1 | Swimming training | Race results + swimming training API216, 183,612 rows (aggregated by horse and date, then joined); races from 30 days after swimming records begin (2020-04) | 2020-04~2024 (race count not tallied) | 2025-01~ 3,140 races; starter-segment table 115,846 starters (Seoul 67,792, Busan-Gyeongnam 48,054) |
| 2 | Place gap | Place odds (plcOdds) from race results; 100% of races have place odds | 2019~2024, 9,323 races | 2025-01~2026-09, 3,132 races (Seoul 1,860, Busan-Gyeongnam 1,272); quintile table 135,399 starters |
| 3 | Running style × track moisture × distance | Average early position (early_avg3), track moisture (moist), distance from race results | 2019~2024 | 2025-01~ 3,132 races |
| 4 | Opponent composition | Distribution of early_avg3 among starters in the same race, closing ability (close_avg3) | 2019~2024 | 2025-01~ 3,132 races |
| 5 | First-up × jockey | first_up, jk_same, h_starts from race results | 2019~2024 | 2025-01~ 3,132 races |
| 6 | Three-way disagreement | Place gap g, model–win gap (starters with p^L only) | 2019~2024 | 2025-01~ 3,132 races; joint-support table 135,399 starters (joint support 63,794, place only 38,110, model only 11,315, neither 22,180) |
| 7 | Place gap × horse situation | g × first_up, long_layoff, jk_same, debut, cls_chg | 2019~2024 | 2025-01~ 3,132 races |
| 8, 9 | Seven daily-training features, training-load change | Daily training API18_1, 2022-01~2025-10 (that period out of 1,590,059 rows) → aggregated by horse and date; races 2022-02~2025-10, 69,105 starters, 100% with training records in the previous 60 days | Walk-forward: 2022 → 2023 (1,770), 2022~23 → 2024 (1,770), 2022~24 → 2025.1~10 (1,434); fixed split trains on 5,083 races | Total 4,974 races (Seoul 2,940, Busan-Gyeongnam 2,034); fixed split 1,434 races in 2025 |
| 10, 11 | Final check of place gap and training-load change | As above, adding training records for 2025-11~2026-09 (32,013–41,426 rows per month); races 2022-02~2026-09, 86,357 starters | 2022-02~2025-10, 6,517 races | 2025-11~2026-09, 1,629 races (mean field 10.6), 17,252 starters |
| 12, 13 | Four routine features, weekly regularity alone | Daily training from 2022-01 only (2019~2021 sealed); races 2022-03~2026-09, 85,036 starters, of which 48.0% eligible for routine (6+ of 8 weeks) | Four walk-forward steps: up to the start of the next period | 2023 1,770 + 2024 1,770 + 2025.1~10 1,434 + 2025.11~26.9 1,629 = 6,603 races |
| 14 | Weekly regularity relative to trainer (pre-registered) | All daily training 2019-01~2026-10, 2,465,789 rows; races: 85,036 training + 43,374 scoring starters; routine-eligible share 66.4% in training, 58.5% in scoring; 90.8% of scoring-period trainers have a training-period average | 2022-03~2026-09, 8,044 races | 2019-03~2021-12, 3,813 races (Seoul 2,241, Busan-Gyeongnam 1,572; 2019 1,598, 2020 962, 2021 1,253) |
| Trainer analysis | D.5 | 56,426 routine-eligible starters (2022~2026), 98 trainers; ranking table covers 78 trainers with 150+ starters | — | — |
| 15, 16 | Trio and trifecta 50:50 blends | Final odds API160_1 files from 2025 onward, trio and trifecta only; races with 7+ starters and exactly one horse each in 1st, 2nd, 3rd | Win probabilities 12,455 races; HB exponents 2019~2024, 9,271 races | 2025-01~2026-09, 3,104 races, 3,348,982 combinations (trio 154 per race, trifecta 925) |
| 17, 18 | Multi-pool combination | Final-odds files 2024~2026, all combinations in five bet types (trifecta, trio, exacta, quinella, quinella place); races with more than 30% missing trifecta or trio odds excluded | 1,761 races in 2024 (about 1.6 million combination rows) | 2025-01~2026-09, 3,104 races (about 2.9 million ordered-combination rows) |
| Backtest | E.3~E.6 | As above; only combinations with odds > 0 are eligible | — | 2024, 1,760 races (reference); 2025~, 3,103 races; bets and hits in E.3 |
| Turnover | E.7 | Turnover API179_1, 2019-01~2026-10, Seoul and Busan-Gyeongnam, 86,028 rows (trifecta 11,907 races); E.8 matches all 3,104 races of the 2025~ evaluation | — | — |

The baseline model was trained on 2019–2023, so p^C in that period is in-sample. In the scoring period of experiment 14 (2019–2021) the baseline is therefore more favorable than in reality, which works against the feature being tested. Conversely, if 2024 is included in the training period of experiments 8–9, the combination weights use a p^C fitted to the same year and may be slightly optimistic.

## Appendix B. Details of the baseline model and the place gap

### B.1 Baseline model performance (prior study, for reference)

The baseline model is a conditional logit trained on 78 variables built from race results (speed figures, recent finishing positions and in-the-money rates, previous-race odds, jockey/trainer/owner win rates, changes in distance and class, weight carried, rating, body weight, gate, track condition, layoff length); it does not include training data.

| Model | Test 3,140 races pseudo-R² | Top-pick win rate |
| --- | --- | --- |
| Market odds | 0.236 | 37.6% |
| Conditional logit | 0.188 | 32.6% |
| GBDT | 0.186 | 32.1% |
| Logit + market combined (p^C) | 0.238 | 37.2% |

The combined model's improvement over the market is +0.0065 per race (95% CI +0.0027 ~ +0.0102). The 347 races with win odds recorded as 9999.9 are included in this model's training and should be excluded on retraining.

### B.2 Place gap: conditional logit coefficients

| Term | Trained 2019~2024 | Trained 2022-03~2025-10 (for final check) |
| --- | --- | --- |
| log p^C | +1.149 | +1.166 |
| g (place gap) | +0.315 | +0.372 |
| max(g, 0) | −0.0001 | — |

### B.3 A/E by place-gap quintile (2019~2026, 135,399 starters)

| Quintile | Starters | Win rate | Baseline expected win rate | A/E (market) | A/E (model) | Top-3 rate |
| --- | --- | --- | --- | --- | --- | --- |
| Underrated in place pool (bottom 20%) | 27,080 | 25.3% | 25.9% | 0.988 | 0.974 | 54.2% |
| 2 | 27,080 | 10.0% | 9.6% | 1.023 | 1.033 | 32.0% |
| 3 | 27,079 | 5.4% | 5.2% | 1.012 | 1.037 | 21.6% |
| 4 | 27,080 | 3.3% | 3.3% | 0.969 | 0.998 | 16.7% |
| Overrated in place pool (top 20%) | 27,080 | 2.1% | 1.9% | 1.067 | 1.086 | 13.6% |

### B.4 Improvement by year (2019~2024 is the training period, for reference)

| Year | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gain | −0.0024 | +0.0174 | +0.0096 | +0.0000 | +0.0036 | +0.0032 | +0.0011 | +0.0049 |

### B.5 Model comparison in the final-check period (2025-11~2026-09, 1,629 races)

| Model | pseudo-R² | Gain vs. baseline (95% CI) |
| --- | --- | --- |
| Market odds only | 0.2499 | −0.0057 (−0.0106 ~ −0.0010) |
| Baseline model | 0.2523 | 0 |
| + place gap | 0.2543 | +0.0046 (+0.0015 ~ +0.0076) |
| + training-load change | 0.2521 | −0.0005 (−0.0035 ~ +0.0026) |
| + place gap + training-load change | 0.2541 | +0.0042 (−0.0002 ~ +0.0084) |

By racecourse, the place gap gives +0.0030 (−0.0010 ~ +0.0070) at Seoul and +0.0070 (+0.0020 ~ +0.0118) at Busan-Gyeongnam.

## Appendix C. Rejected feature combinations and market-response combinations

Within the existing race-results data, combinations that prior studies had not placed together in one model were tested. Training 2019~2024, evaluation 3,132 races from 2025 onward.

### C.1 Race-results combinations (baseline: baseline model)

| Combination | Component features | Gain (95% CI) | Seoul | Busan-Gyeongnam |
| --- | --- | --- | --- | --- |
| 1. Running style × track moisture × distance | Early-pace tendency × moisture, × Seoul, × sprint, × sprint × Seoul, × moisture × sprint | +0.0004 (−0.0002 ~ +0.0009) | +0.0006 | +0.0001 |
| 2. Opponent composition | Lone front-runner, front-runner × number of other front-runners, closing ability × pace contention, share of horses ahead | +0.0007 (+0.00002 ~ +0.0014) | +0.0002 | +0.0013 |
| 3. First-up × jockey | First-up × same jockey, first-up × jockey change | 0.0000 (−0.0010 ~ +0.0009) | +0.0007 | −0.0010 |
| 1+2+3 all | 11 features | +0.0011 (−0.0003 ~ +0.0024) | +0.0015 | +0.0004 |

Combination 2 was not significant in the training period (+0.0002), and its test confidence interval's lower bound sits at zero, so it is classified as borderline. The coefficient sign indicated that front-runners are disadvantaged the more other front-runners there are (−0.015), but the closing ability × pace contention term came out counter-intuitive (−0.026).

### C.2 Market-response combinations (baseline: baseline model + place gap)

| Combination | Component features | Gain (95% CI) |
| --- | --- | --- |
| Three-way disagreement | g × (model − win), joint place-and-model support, joint support × g | +0.0001 (−0.0007 ~ +0.0010) |
| Place gap × horse situation | g × first-up, g × long layoff, g × jockey change, g × debut, g × class rise | +0.0005 (−0.0001 ~ +0.0011) |

Horses rated above the win market by both the place pool and the baseline model (63,794 starters, win rate 4.3%) won 5.6% more often than the model expected (A/E 1.056), but this effect is already explained by the place gap alone. Only for horses returning from a long layoff was the coefficient on g positive (+0.011).

These results converge on the conclusion that, within public race results and odds, recombining features does not easily get past information the market has already digested.

## Appendix D. Training-data descriptive statistics and per-feature details

### D.1 Swimming training (2020-03 ~ 2026-10, 183,612 records)

Swimming takes place only from March to November, with about 70% concentrated in April–August. There are no records on Mondays or Tuesdays. A session averages 2.5 laps at Seoul and 1.9 at Yeongnam (Busan-Gyeongnam), and the median number of swimming days per horse per season is 13 (maximum 160).

| Year | Seoul swim sessions | Seoul horses | Yeongnam swim sessions | Yeongnam horses |
| --- | --- | --- | --- | --- |
| 2020 | 57,374 | 812 | 20,964 | 572 |
| 2021 | 71,174 | 903 | 16,752 | 521 |
| 2022 | 48,054 | 780 | 17,767 | 543 |
| 2023 | 32,607 | 662 | 18,450 | 522 |
| 2024 | 32,809 | 649 | 18,697 | 518 |
| 2025 | 33,731 | 677 | 13,446 | 424 |
| 2026 (through 10/11) | 32,525 | 641 | 11,436 | 365 |

A/E by swimming days in the previous 14 days (vs. market, 2020-04~2026-09): overall 0.994 for 0 days, 1.058 for 1–2, 1.071 for 3–5, 1.020 for 6+. At Busan-Gyeongnam alone, horses that swam had A/E of 1.09 (95% CI 1.02~1.17), but at Seoul it was 1.01 (0.94~1.06); since this emerged after examining several subgroups, it is recorded only as a hypothesis.

### D.2 Daily training records (2019-01 ~ 2026-10, 2,465,789 rows)

Descriptive statistics for 1–11 October 2026. 97% of training sessions start between 6 and 8 a.m., and a horse trains on average 6 days out of 10. Training time (trTerm) matches end time minus start time in 100% of records.

| Racecourse | Training records | Horses | Mean training time | Jockey-ridden share | Trainer-ridden |
| --- | --- | --- | --- | --- | --- |
| Seoul | 7,610 | 1,281 | 12.6 min | 31.9% | 2.5% |
| Yeongnam (Busan-Gyeongnam) | 5,411 | 899 | 13.5 min | 16.0% | 1.5% |
| Jeju | 2,892 | 543 | 15.1 min | 34.1% | 11.8% |

| Entry status | Records | Mean training time | Jockey-ridden share |
| --- | --- | --- | --- |
| Entered this week | 3,953 | 12.2 min | 50.8% |
| Entered in a stakes race | 288 | 13.8 min | 39.2% |
| Entered next week | 11,666 | 13.7 min | 18.5% |

In the week before racing, training gets shorter and the share ridden by jockeys more than doubles. However, whether the assigned jockey rode the horse beforehand (previous 7 days) was unrelated to performance (ridden: 52,356 starters, A/E 1.001; not ridden: 16,749 starters, A/E 0.996).

### D.3 Walk-forward test of seven daily-training features (baseline: baseline model + place gap)

| Test year | Races | Gain (95% CI) |
| --- | --- | --- |
| 2023 (trained on 2022 only) | 1,770 | −0.0005 (−0.0042 ~ +0.0031) |
| 2024 | 1,770 | +0.0035 (+0.0007 ~ +0.0064) |
| 2025 | 1,434 | +0.0023 (−0.0014 ~ +0.0060) |
| Total | 4,974 | +0.0017 (−0.0002 ~ +0.0037) |

| Feature | 2023 coefficient | 2024 coefficient | 2025 coefficient |
| --- | --- | --- | --- |
| Assigned jockey rode (7 days) | +0.028 | +0.004 | −0.021 |
| Jockey rode (7 days) | +0.019 | +0.013 | +0.016 |
| Training days (14 days) | +0.047 | +0.024 | +0.009 |
| Training minutes (14 days) | −0.026 | −0.032 | −0.009 |
| Change vs. usual | −0.081 | −0.064 | −0.088 |
| Days since last training | −0.010 | −0.041 | −0.044 |
| Track sessions (14 days) | −0.126 | +0.033 | +0.056 |

Only change vs. usual had the same sign and similar size in all three years, and including it alone gave a walk-forward gain of +0.0023 (+0.0007 ~ +0.0037). It then vanished in the sealed holdout at −0.0005 (Section 7). The feature definition also had a problem: "usual" was taken as on-course training 15–60 days earlier, so horses resting off-course registered as zero, and as a result 55–64% of starters fell into the "large increase" bin.

### D.4 Four routine-regularity features (pre-registered, walk-forward 2023~2026, 6,603 races)

Eligible horses are those with training records in at least 6 of the 8 weeks before the race (48% of starters).

| Feature | Definition | Gain alone (98.75% CI) | Coefficient (4 fits) | Quintile A/E (regular → irregular) |
| --- | --- | --- | --- | --- |
| Training gaps | Number of gaps of 4+ days | −0.0002 (−0.0005 ~ +0.0002) | −0.039 −0.006 −0.005 +0.009 | 1.02 1.01 1.02 1.02 1.06 |
| Weekly training-day variation | Coefficient of variation of days per week over 8 weeks | +0.0006 (−0.0007 ~ +0.0019) | −0.081 −0.067 −0.075 −0.067 | 1.10 1.05 1.02 0.98 0.98 |
| Start-time variation | Standard deviation of start time across training days | +0.0001 (−0.0004 ~ +0.0005) | −0.025 −0.026 −0.021 −0.022 | 1.02 0.99 1.10 1.06 0.94 |
| Intensity variation | Coefficient of variation of total time per training day | 0.0000 (−0.0001 ~ +0.0002) | −0.011 +0.003 +0.010 +0.014 | 1.01 1.00 1.02 1.07 1.02 |

### D.5 Trainer analysis (2022~2026, 56,426 eligible starters, 98 trainers)

Differences between trainers explain 19.5% of the variation in weekly training days. The most regular trainers (150+ starters) were 토니 (Tony; Seoul, variation 0.35), 울즐리 (Woolsley; Busan-Gyeongnam, 0.42), 토마스 (Thomas; Busan-Gyeongnam, 0.46) and 리카디 (Ricardi; Seoul, 0.46), and the most irregular were 송문길 (Song Mun-gil, 0.72), 박종곳 (Park Jong-got, 0.72) and 이준철 (Lee Jun-cheol, 0.69).

| Basis of comparison | Quintile A/E (regular → irregular) |
| --- | --- |
| Is the trainer's style regular? (trainer average) | 1.07 0.99 0.99 1.06 1.00 |
| Is the horse relatively regular within the same trainer? (relative to trainer average) | 1.06 1.04 1.06 0.99 0.97 |

The correlation between a trainer's average variation and the trainer's A/E is −0.07 (78 trainers), i.e. no relationship; any effect comes from the relative regularity of individual horses within the same stable. Fixing the definition on this observation and scoring it once on 2019~2021 produced the −0.052 coefficient and +0.0004 gain in Section 7. Quintile A/E in the scoring period was 1.073, 1.034, 1.067, 0.974, 0.971, almost the same as in 2022~2026.

## Appendix E. Details of the combination-pool analysis

### E.1 Finishing-order hit rates (2025~ test, 3,132 races, mean field 10.6)

| Target | Bet type | Market odds | Baseline model | Random (11 runners) |
| --- | --- | --- | --- | --- |
| Top pick finishes top 3 | Place | 69.2% | 68.6% | 27.3% |
| 2+ of top 3 picks finish top 3 |  | 60.5% | 60.9% |  |
| 1st and 2nd, any order | Quinella | 18.0% | 18.0% | 1.8% |
| 1st to 3rd, any order | Trio | 10.8% | 11.3% | 0.6% |
| 1st to 3rd, exact order | Trifecta | 2.7% | 3.1% | 0.1% |

### E.2 Simple-blend (50:50) value betting on final odds (2025~, 3,104 races)

The first backtest, before the multi-pool combination, using the geometric mean of the fundamental model's combination probability and the pool's implied probability. No profit was made at this stage.

| Bet type · probability | Threshold | Bets | Hits | Return (95% CI) |
| --- | --- | --- | --- | --- |
| Trifecta · blend | 1.0 | 228,522 | 141 | −22.5% (−40 ~ −3) |
| Trifecta · blend | 1.3 | 16,937 | 8 | +38.8% (−63 ~ +201) |
| Trifecta · model alone | 1.0 | 603,683 | 582 | −6.4% (−18 ~ +6) |
| Trifecta · model alone | 1.3 | 244,743 | 158 | −16.0% (−36 ~ +4) |
| Trio · blend | 1.0 | 29,180 | 66 | −34.5% (−58 ~ −5) |
| Trio · model alone | 1.0 | 89,071 | 338 | −28.2% (−45 ~ −8) |

The model-alone trifecta return of −6.4% is 21 percentage points better than random (−27.5%) but does not beat the takeout. The blended probabilities at this stage were not calibrated (73 combinations per race had EV > 1), and the results changed after calibration with the multi-pool conditional logit.

### E.3 Multi-pool value betting by threshold (final odds)

| Period · model · bet type | Threshold | Bets / races | Hits (model expected) | Return (95% CI) | Model expected return |
| --- | --- | --- | --- | --- | --- |
| 2024 · model + market · trifecta | 1.0 | 146,596 / 1,760 | 177 (177.9) | +17.7% (−11 ~ +47) | +16.0% |
| 2024 · model + market · trifecta | 1.2 | 41,321 / 1,685 | 43 (42.5) | +13.8% (−34 ~ +63) | +36.6% |
| 2024 · model + market · trifecta | 1.5 | 6,683 / 960 | 4 (5.8) | −31.5% (−96 ~ +69) | +68.5% |
| 2025~ · model + market · trifecta | 1.0 | 285,148 / 3,103 | 383 (389.9) | +24.6% (+4 ~ +46) | +17.2% |
| 2025~ · model + market · trifecta | 1.2 | 88,305 / 3,031 | 117 (111.2) | +47.1% (+8 ~ +93) | +37.4% |
| 2025~ · model + market · trifecta | 1.5 | 15,450 / 1,940 | 14 (16.9) | +69.3% (−47 ~ +244) | +68.7% |
| 2025~ · market only · trifecta | 1.0 | 216,887 / 3,103 | 281 (275.7) | +26.5% (+3 ~ +52) | +14.4% |
| 2025~ · market only · trifecta | 1.2 | 54,298 / 2,957 | 64 (62.1) | +58.7% (−4 ~ +129) | +34.2% |
| 2025~ · model + market · trio | 1.0 | 14,518 / 2,150 | 48 (60.9) | −23.7% (−58 ~ +24) | +9.5% |
| 2025~ · model + market · trio | 1.2 | 1,746 / 497 | 2 (5.5) | −92.0% | +29.4% |

In the trifecta, hits match the model's expectation, but in the trio actual hits are about half of expected. The trio pool is more accurate than the combined model, so combinations the model sees as "value" are often the model's own errors.

### E.4 Return by half-year (threshold 1.2, trifecta)

| Half-year | Model + market: bets / hits / return | Market only: bets / hits / return |
| --- | --- | --- |
| H1 2025 | 25,560 / 34 / +14.7% | 16,356 / 21 / +33.8% |
| H2 2025 | 27,095 / 31 / +64.5% | 16,386 / 21 / +116.9% |
| H1 2026 | 23,782 / 29 / +59.5% | 15,415 / 12 / +40.6% |
| H2 2026 (through September) | 11,868 / 23 / +52.4% | 6,141 / 10 / +15.6% |

### E.5 Profit concentration (threshold 1.2, trifecta, 2025~)

| Item | Model + market | Market only |
| --- | --- | --- |
| Bets / hits | 88,305 / 117 | 54,298 / 64 |
| Median / maximum odds of hits | 636 / 10,000 | 673 / 10,000 |
| Share of payout from top 5 hits | 29% | 43% |
| Share of payout from top 20 hits | 57% | 76% |
| Return excluding top 5 | +4.8% | −10.0% |
| Return excluding top 20 | −36.6% | −61.6% |
| Odds of combinations bet: median / 75th / 95th percentile | 1,919 / 3,952 / 8,788 | 1,943 / 3,900 / 8,448 |
| Median trifecta-pool implied probability of combinations bet | 0.038% | 0.037% |

The uniform probability per combination is 0.108%. The bets are on combinations carrying less than a third of the average amount in the trifecta pool.

### E.6 Exploratory race selection (tertiles of per-race maximum EV, cut-offs 1.43 / 1.65)

| Segment | 2024: races / bets / hits / return | 2025~: races / bets / hits / return |
| --- | --- | --- |
| 1 (low maximum EV) | 587 / 3,060 / 5 / +104.5% | 793 / 5,171 / 12 / +75.0% |
| 2 | 587 / 10,015 / 14 / +114.3% | 1,090 / 21,227 / 23 / −5.8% |
| 3 (high maximum EV) | 587 / 28,246 / 24 / −31.7% | 1,221 / 61,907 / 82 / +62.9% |

The segment pattern does not agree between the two periods, so no race-selection rule is adopted.

### E.7 Pool turnover by bet type (sample and yearly medians)

Values in KRW 100 million (억 원).

| Race | Win | Place | Exacta | Quinella | Quinella place | Trio | Trifecta |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1R | 0.25 | 0.50 | 1.64 | 5.68 | 0.84 | 7.31 | 4.09 |
| 5R | 0.39 | 0.60 | 2.82 | 8.33 | 1.33 | 10.98 | 6.00 |

Yearly median trifecta pool turnover over the full period (2019-01~2026-10, 11,907 trifecta races), in KRW 100 million.

| Year | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Seoul | 4.06 | 3.02 | 0.68 | 4.45 | 4.49 | 4.86 | 5.21 | 5.73 |
| Busan-Gyeongnam | 2.92 | 2.09 | 0.63 | 3.58 | 3.29 | 4.20 | 4.33 | 5.15 |

### E.8 Backtest with market impact (2025~, all 3,104 races matched to turnover, threshold 1.2)

Existing amount per combination A_c = S(1−t)/O_c, odds after stake B O'_c = (S+B)(1−t)/(A_c+B), t = 0.273. Combinations are selected by pre-impact EV and settled at post-impact odds.

| Model | Stake per combination | Outlay per race | Odds drop (median) | Return (95% CI) | Model expected |
| --- | --- | --- | --- | --- | --- |
| Model + market | KRW 0 | 0 | 0% | +47.1% (+7 ~ +96) | +37.4% |
| Model + market | KRW 1,000 | KRW 29,000 | 0.5% | +45.6% (+3 ~ +91) | +36.2% |
| Model + market | KRW 5,000 | KRW 146,000 | 2.6% | +40.2% (+2 ~ +84) | +31.9% |
| Model + market | KRW 10,000 | KRW 291,000 | 5.1% | +34.5% (−2 ~ +80) | +27.1% |
| Model + market | KRW 30,000 | KRW 874,000 | 13.9% | +18.0% (−9 ~ +51) | +12.8% |
| Model + market | KRW 100,000 | KRW 2.91 million | 35.0% | −10.7% (−29 ~ +10) | −14.3% |
| Market only | KRW 10,000 | KRW 184,000 | 5.1% | +41.5% (−9 ~ +106) | +24.5% |
| Market only | KRW 30,000 | KRW 551,000 | 13.9% | +20.4% (−20 ~ +73) | +10.6% |

The median amount already on the selected combinations is KRW 185,000. The stake at which the model's expected return reaches zero is about KRW 56,000 per combination (about KRW 1.63 million per race) for model + market, and about KRW 52,000 (about KRW 950,000 per race) for market only. This calculation keeps the assumption of betting with knowledge of final odds and does not reflect pre-close odds movements.

## References

- Ali, M. M. (1977). Probability and utility estimates for racetrack bettors. *Journal of Political Economy*, 85(4), 803–815.
- Asch, P., & Quandt, R. E. (1987). Efficiency and profitability in exotic bets. *Economica*, 54(215), 289–298.
- Benter, W. (1994). Computer-based horse race handicapping and wagering systems: A report. In D. B. Hausch, V. S. Y. Lo, & W. T. Ziemba (Eds.), *Efficiency of Racetrack Betting Markets*. Academic Press.
- Bolton, R. N., & Chapman, R. G. (1986). Searching for positive returns at the track: A multinomial logit model for handicapping horse races. *Management Science*, 32(8), 1040–1060.
- Harville, D. A. (1973). Assigning probabilities to the outcomes of multi-entry competitions. *Journal of the American Statistical Association*, 68(342), 312–316.
- Hausch, D. B., & Ziemba, W. T. (1990). Arbitrage strategies for cross-track betting on major horse races. *Journal of Business*, 63(1), 61–78.
- Hausch, D. B., Ziemba, W. T., & Rubinstein, M. (1981). Efficiency of the market for racetrack betting. *Management Science*, 27(12), 1435–1452.
- Korea Racing Authority. (2026). Race results (API4_3), integrated final odds (API160_1), daily training records (API18_1), swimming training (API216), racing turnover and final odds (API179_1). *Public Data Portal (data.go.kr)*, retrieved 12 October 2026.
- Lo, V. S. Y., & Bacon-Shone, J. (1994). A comparison between two models for predicting ordering probabilities in multiple-entry competitions. *Journal of the Royal Statistical Society: Series D (The Statistician)*, 43(2), 317–327.
- Sauer, R. D. (1998). The economics of wagering markets. *Journal of Economic Literature*, 36(4), 2021–2064.
- Snowberg, E., & Wolfers, J. (2010). Explaining the favorite–long shot bias: Is it risk-love or misperceptions? *Journal of Political Economy*, 118(4), 723–746.
- Thaler, R. H., & Ziemba, W. T. (1988). Anomalies: Parimutuel betting markets: Racetracks and lotteries. *Journal of Economic Perspectives*, 2(2), 161–174.
