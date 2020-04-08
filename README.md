# Trading
:information_source: Check out the repository from [terukusu](https://github.com/terukusu/download-tick-from-dukascopy) for downloading data (dukascopy)
## Moving Average Convergence Divergence (MACD)
### Usage
```bash
python3 MACD.py -h
```

```bash
python3 MACD.py -f sample_data/GBPJPY_20191201_20200327/sub_data.csv -m 1500 -n 50 -o sub_1500_50.csv
```
### Example output
```
[i] Reading in data..

[i] Calculating EMAs...

[i] Processing... |################################| 100/100

-------------------------------------------

[+] Writing Results to sub_1500_50.csv
[+] Best result: 9.51
[+] Best indicator: EMA1750:EMA2000
```
