# Trading
:information_source: Check out the repository from [terukusu](https://github.com/terukusu/download-tick-from-dukascopy) for downloading data (dukascopy)
## Moving Average Convergence Divergence (MACD)
### Description
Command line tool to evaluate the best two EMA's for the MACD strategy.
### Usage
```bash
python3 MACD.py -h
```

```bash
python3 MACD.py -f sample_data/GBPJPY_20191201_20200327/sub_data.csv -m 500 -n 20 -o out.csv
```
### Example output
```
[+] Reading in data..
[+] Calculating EMAs...
[+] Calculating best EMAs... |################################| 100/100
[+] Writing results to: out.csv
```
