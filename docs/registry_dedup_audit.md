# Registry Deduplication Audit

## Fund Count Delta: 28 -> 32
The fund count increased from 28 to 32 because the new extraction pipeline pulls from 3 sources (Groww, INDmoney, Official AMCs) instead of just 1. While the deduplication engine successfully merged overlapping entries, 4 completely unique funds were discovered on INDmoney/Official sites that were unlisted or hidden on Groww.

## AMC Count Delta: 14 -> 11
The AMC count decreased from 14 to 11 due to aggressive brand normalization in the deduplication engine. Previously, raw scrapes treated variations as separate entities:
- 'ICICI', 'ICICI Prudential', 'ICICI Pru' -> Merged into **ICICI**
- 'Tata', 'Tata Mutual Fund' -> Merged into **Tata**
- 'Quant', 'Quant AMC' -> Merged into **Quant**

## Canonical Merging Example
If 'Titanium Long Short' existed on Groww and INDmoney, the registry unified them into a single object under `fund_id: titanium-long-short` with distinct URL properties instead of creating duplicates.
