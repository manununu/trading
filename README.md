# Trading
:information_source: Check out the repository from [terukusu](https://github.com/terukusu/download-tick-from-dukascopy) for downloading data (dukascopy)
## Moving Average Convergence Divergence (MACD)
### Description
This is a tool to evaluate the best two EMA's for the MACD strategy. The result is the sum of all delta values.
### Usage
```bash
python3 MACD.py -h
```

```bash
python3 MACD.py -f sample_data/GBPJPY_20191201_20200327/sub_data.csv -m 1000 -n 100 -p 4 -g -o out.csv 
```
### Example output
```
[+] Reading in data..
[+] Calculating EMAs...
[+] Calculating best EMAs... |################################| 100/100
-------------------------------
[+] Best indicator: EMA500 / EMA1000
[+] Result: 1.64
-------------------------------
[+] Writing results to: out.csv
[+] Showing plot of results..
```
