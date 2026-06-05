# Retrieval Benchmark Suite V1

## Category: Regulatory

### Query: "What is the minimum investment for SIFs?"
**Route:** `rag`

#### Before Reranking (Raw Cosine)
1. `https://sif.itiamc.com/` (Tier 3) | Base: 0.8479
2. `https://sif.itiamc.com/` (Tier 3) | Base: 0.8177
3. `https://groww.in/mutual-funds/arudha-equity-long-short-fund-direct-growth` (Tier 4) | Base: 0.8085
4. `https://groww.in/mutual-funds/apex-hybrid-long-short-fund-direct-growth` (Tier 4) | Base: 0.8080
5. `https://groww.in/mutual-funds/wsif-equity-long-short-fund-direct-growth` (Tier 4) | Base: 0.8073
6. `https://groww.in/mutual-funds/isif-hybrid-long-short-fund-direct-growth` (Tier 4) | Base: 0.8070
7. `https://groww.in/mutual-funds/isif-equity-ex-top-100-long-short-fund-direct-growth` (Tier 4) | Base: 0.8068
8. `https://groww.in/mutual-funds/titanium-hybrid-long-short-fund-direct-growth` (Tier 4) | Base: 0.8066
9. `https://groww.in/mutual-funds/sapphire-equity-long-short-sif-direct-growth` (Tier 4) | Base: 0.8059
10. `https://groww.in/mutual-funds/dynasif-active-asset-allocator-long-short-fund-direct-growth` (Tier 4) | Base: 0.8043

#### After Reranking (Boosted)
1. `sebi-sebi-circular` | Auth: regulator | Tier: 1 | Base: 0.7633 | Boosted: 1.1449
2. `sebi-sebi-circular-5` | Auth: regulator | Tier: 1 | Base: 0.7584 | Boosted: 1.1375
3. `sebi-sebi-circular-5` | Auth: regulator | Tier: 1 | Base: 0.7566 | Boosted: 1.1349
4. `sebi-sebi-circular-3` | Auth: regulator | Tier: 1 | Base: 0.7414 | Boosted: 1.1122
5. `sebi-sebi-circular-5` | Auth: regulator | Tier: 1 | Base: 0.7328 | Boosted: 1.0992
6. `sebi-sebi-circular-3` | Auth: regulator | Tier: 1 | Base: 0.7320 | Boosted: 1.0980
7. `sebi-sebi-circular` | Auth: regulator | Tier: 1 | Base: 0.7308 | Boosted: 1.0962
8. `sebi-sebi-circular-3` | Auth: regulator | Tier: 1 | Base: 0.7305 | Boosted: 1.0957
9. `sebi-sebi-circular-3` | Auth: regulator | Tier: 1 | Base: 0.7288 | Boosted: 1.0932
10. `sebi-sebi-circular` | Auth: regulator | Tier: 1 | Base: 0.7258 | Boosted: 1.0886

**Authority % in Top 10:** 100.0%

### Query: "What is the maximum unhedged short exposure?"
**Route:** `rag`

#### Before Reranking (Raw Cosine)
1. `https://www.sbimf.com/magnumsif` (Tier 3) | Base: 0.6988
2. `sebi-sebi-circular-5` (Tier 1) | Base: 0.6958
3. `sebi-sebi-circular-5` (Tier 1) | Base: 0.6728
4. `sebi-sebi-circular` (Tier 1) | Base: 0.6728
5. `sebi-sebi-circular` (Tier 1) | Base: 0.6714
6. `external--uncategorized-isid-1` (Tier 2) | Base: 0.6679
7. `sebi-sebi-circular-5` (Tier 1) | Base: 0.6560
8. `sebi-sebi-circular` (Tier 1) | Base: 0.6560
9. `sebi-sebi-circular-5` (Tier 1) | Base: 0.6552
10. `https://www.sbimf.com/magnumsif` (Tier 3) | Base: 0.6475

#### After Reranking (Boosted)
1. `sebi-sebi-circular-5` | Auth: regulator | Tier: 1 | Base: 0.6958 | Boosted: 1.0436
2. `sebi-sebi-circular-5` | Auth: regulator | Tier: 1 | Base: 0.6728 | Boosted: 1.0092
3. `sebi-sebi-circular` | Auth: regulator | Tier: 1 | Base: 0.6728 | Boosted: 1.0092
4. `sebi-sebi-circular` | Auth: regulator | Tier: 1 | Base: 0.6714 | Boosted: 1.0070
5. `sebi-sebi-circular-5` | Auth: regulator | Tier: 1 | Base: 0.6560 | Boosted: 0.9839
6. `sebi-sebi-circular` | Auth: regulator | Tier: 1 | Base: 0.6560 | Boosted: 0.9839
7. `sebi-sebi-circular-5` | Auth: regulator | Tier: 1 | Base: 0.6552 | Boosted: 0.9828
8. `sebi-sebi-circular-5` | Auth: regulator | Tier: 1 | Base: 0.6397 | Boosted: 0.9595
9. `sebi-sebi-circular` | Auth: regulator | Tier: 1 | Base: 0.6397 | Boosted: 0.9595
10. `sebi-sebi-circular` | Auth: regulator | Tier: 1 | Base: 0.6273 | Boosted: 0.9409

**Authority % in Top 10:** 100.0%

### Query: "What are SEBI's eligibility criteria?"
**Route:** `rag`

#### Before Reranking (Raw Cosine)
1. `sebi-sebi-circular-5` (Tier 1) | Base: 0.7300
2. `sebi-sebi-circular-3` (Tier 1) | Base: 0.7097
3. `sebi-sebi-circular` (Tier 1) | Base: 0.7047
4. `external--uncategorized-isid` (Tier 2) | Base: 0.6871
5. `quant-mutual-fund-isid` (Tier 2) | Base: 0.6871
6. `external--uncategorized-isid-1` (Tier 2) | Base: 0.6843
7. `sebi-sebi-circular-3` (Tier 1) | Base: 0.6768
8. `external--uncategorized-isid-1` (Tier 2) | Base: 0.6736
9. `sebi-sebi-circular-3` (Tier 1) | Base: 0.6708
10. `quant-mutual-fund-isid` (Tier 2) | Base: 0.6652

#### After Reranking (Boosted)
1. `sebi-sebi-circular-5` | Auth: regulator | Tier: 1 | Base: 0.7300 | Boosted: 1.0950
2. `sebi-sebi-circular-3` | Auth: regulator | Tier: 1 | Base: 0.7097 | Boosted: 1.0645
3. `sebi-sebi-circular` | Auth: regulator | Tier: 1 | Base: 0.7047 | Boosted: 1.0570
4. `sebi-sebi-circular-3` | Auth: regulator | Tier: 1 | Base: 0.6768 | Boosted: 1.0153
5. `sebi-sebi-circular-3` | Auth: regulator | Tier: 1 | Base: 0.6708 | Boosted: 1.0063
6. `sebi-sebi-circular-3` | Auth: regulator | Tier: 1 | Base: 0.6560 | Boosted: 0.9840
7. `sebi-sebi-circular-3` | Auth: regulator | Tier: 1 | Base: 0.6539 | Boosted: 0.9808
8. `sebi-sebi-circular-3` | Auth: regulator | Tier: 1 | Base: 0.6466 | Boosted: 0.9699
9. `sebi-sebi-circular` | Auth: regulator | Tier: 1 | Base: 0.6328 | Boosted: 0.9491
10. `sebi-sebi-circular-3` | Auth: regulator | Tier: 1 | Base: 0.6230 | Boosted: 0.9345

**Authority % in Top 10:** 100.0%

## Category: Product

### Query: "What is Titanium Hybrid Long-Short Fund?"
**Route:** `rag`

#### Before Reranking (Raw Cosine)
1. `https://www.tatamutualfund.com/titanium-sif` (Tier 3) | Base: 0.8175
2. `https://groww.in/mutual-funds/titanium-hybrid-long-short-fund-direct-growth` (Tier 4) | Base: 0.8112
3. `https://www.tatamutualfund.com/titanium-sif` (Tier 3) | Base: 0.8103
4. `icici-prudential-amc-factsheet` (Tier 2) | Base: 0.7740
5. `https://apexsif.adityabirlacapital.com/strategies/apex-hybrid-long-short-fund` (Tier 3) | Base: 0.7680
6. `https://apexsif.adityabirlacapital.com/strategies/apex-hybrid-long-short-fund` (Tier 3) | Base: 0.7675
7. `https://groww.in/mutual-funds/titanium-hybrid-long-short-fund-direct-growth` (Tier 4) | Base: 0.7559
8. `https://groww.in/mutual-funds/titanium-hybrid-long-short-fund-direct-growth` (Tier 4) | Base: 0.7520
9. `icici-prudential-amc-factsheet` (Tier 2) | Base: 0.7438
10. `https://apexsif.adityabirlacapital.com/strategies/apex-hybrid-long-short-fund` (Tier 3) | Base: 0.7362

#### After Reranking (Boosted)
1. `icici-prudential-amc-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.7740 | Boosted: 0.9288
2. `icici-prudential-amc-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.7438 | Boosted: 0.8925
3. `icici-prudential-amc-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.7357 | Boosted: 0.8828
4. `icici-prudential-amc-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.7289 | Boosted: 0.8747
5. `quant-mutual-fund-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.7267 | Boosted: 0.8721
6. `external--uncategorized-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.7245 | Boosted: 0.8694
7. `quant-mutual-fund-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.7244 | Boosted: 0.8693
8. `icici-prudential-amc-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.7240 | Boosted: 0.8688
9. `quant-mutual-fund-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.7134 | Boosted: 0.8560
10. `dsp-mutual-fund-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.7110 | Boosted: 0.8532

**Authority % in Top 10:** 100.0%

### Query: "Explain Sapphire Equity Long-Short SIF."
**Route:** `rag`

#### Before Reranking (Raw Cosine)
1. `https://groww.in/mutual-funds/sapphire-equity-long-short-sif-direct-growth` (Tier 4) | Base: 0.7731
2. `https://www.tatamutualfund.com/titanium-sif` (Tier 3) | Base: 0.7626
3. `https://www.tatamutualfund.com/titanium-sif` (Tier 3) | Base: 0.7514
4. `https://groww.in/mutual-funds/sapphire-equity-long-short-sif-direct-growth` (Tier 4) | Base: 0.7343
5. `https://apexsif.adityabirlacapital.com/strategies/apex-hybrid-long-short-fund` (Tier 3) | Base: 0.7333
6. `https://www.360.one/dyna-sif` (Tier 3) | Base: 0.7286
7. `franklin-templeton-kim` (Tier 2) | Base: 0.7260
8. `https://sif.itiamc.com/` (Tier 3) | Base: 0.7152
9. `https://www.wealthcompanyamc.in/wsif/funds/wsif-equity-long-short-fund/` (Tier 3) | Base: 0.7142
10. `https://sif.itiamc.com/` (Tier 3) | Base: 0.7140

#### After Reranking (Boosted)
1. `franklin-templeton-kim` | Auth: official_amc | Tier: 2 | Base: 0.7260 | Boosted: 0.8712
2. `quant-mutual-fund-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.7021 | Boosted: 0.8425
3. `icici-prudential-amc-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.7017 | Boosted: 0.8421
4. `franklin-templeton-kim` | Auth: official_amc | Tier: 2 | Base: 0.7011 | Boosted: 0.8413
5. `icici-prudential-amc-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.6987 | Boosted: 0.8384
6. `franklin-templeton-kim` | Auth: official_amc | Tier: 2 | Base: 0.6928 | Boosted: 0.8313
7. `quant-mutual-fund-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.6878 | Boosted: 0.8254
8. `external--uncategorized-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.6874 | Boosted: 0.8248
9. `icici-prudential-amc-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.6867 | Boosted: 0.8240
10. `quant-mutual-fund-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.6862 | Boosted: 0.8234

**Authority % in Top 10:** 100.0%

### Query: "What strategies does qSIF offer?"
**Route:** `rag`

#### Before Reranking (Raw Cosine)
1. `quant-mutual-fund-factsheet` (Tier 2) | Base: 0.7441
2. `external--uncategorized-factsheet` (Tier 2) | Base: 0.7425
3. `external--uncategorized-isid-1` (Tier 2) | Base: 0.7270
4. `https://groww.in/mutual-funds/qsif-equity-long-short-fund-direct-plan-growth` (Tier 4) | Base: 0.7245
5. `external--uncategorized-isid` (Tier 2) | Base: 0.7197
6. `quant-mutual-fund-isid` (Tier 2) | Base: 0.7197
7. `quant-mutual-fund-factsheet` (Tier 2) | Base: 0.7101
8. `quant-mutual-fund-isid` (Tier 2) | Base: 0.7094
9. `external--uncategorized-isid` (Tier 2) | Base: 0.7094
10. `https://groww.in/mutual-funds/qsif-equity-long-short-fund-direct-plan-growth` (Tier 4) | Base: 0.7017

#### After Reranking (Boosted)
1. `quant-mutual-fund-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.7441 | Boosted: 0.8929
2. `external--uncategorized-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.7425 | Boosted: 0.8910
3. `external--uncategorized-isid-1` | Auth: official_amc | Tier: 2 | Base: 0.7270 | Boosted: 0.8723
4. `external--uncategorized-isid` | Auth: official_amc | Tier: 2 | Base: 0.7197 | Boosted: 0.8636
5. `quant-mutual-fund-isid` | Auth: official_amc | Tier: 2 | Base: 0.7197 | Boosted: 0.8636
6. `quant-mutual-fund-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.7101 | Boosted: 0.8521
7. `quant-mutual-fund-isid` | Auth: official_amc | Tier: 2 | Base: 0.7094 | Boosted: 0.8513
8. `external--uncategorized-isid` | Auth: official_amc | Tier: 2 | Base: 0.7094 | Boosted: 0.8513
9. `quant-mutual-fund-factsheet` | Auth: official_amc | Tier: 2 | Base: 0.6925 | Boosted: 0.8310
10. `external--uncategorized-isid-1` | Auth: official_amc | Tier: 2 | Base: 0.6917 | Boosted: 0.8300

**Authority % in Top 10:** 100.0%

## Category: Market Inventory

### Query: "What SIFs exist?"
**Route:** `discovery`

- **Result:** Successfully bypassed vector retrieval.
- **Vectors Retrieved:** 0

### Query: "Show all Tata SIFs."
**Route:** `discovery`

- **Result:** Successfully bypassed vector retrieval.
- **Vectors Retrieved:** 0

### Query: "Which SIFs are live?"
**Route:** `discovery`

- **Result:** Successfully bypassed vector retrieval.
- **Vectors Retrieved:** 0

## Category: Comparison

### Query: "Compare iSIF and Titanium."
**Route:** `comparison`

- **Result:** Successfully bypassed vector retrieval.
- **Vectors Retrieved:** 0

### Query: "Compare Hybrid Long-Short vs Equity Long-Short."
**Route:** `comparison`

- **Result:** Successfully bypassed vector retrieval.
- **Vectors Retrieved:** 0

