# Trading
:information_source: Check out the repository from [terukusu](https://github.com/terukusu/download-tick-from-dukascopy) for downloading data (dukascopy)
## Moving Average Convergence Divergence (MACD)
### Usage
```bash
python3 MACD.py -h
```

```bash
python3 MACD.py -f sample_data/GBPJPY_20191201_20200327/data.csv -m 1500 -n 50
```
### Example output
```bash
[i] Reading in data..

[i] Calculating EMAs...

[i] Processing... |############################### | 100/100

-------------------------------------------

[+] Best result: -41.34
[+] Best indicator: EMA50:EMA100
```
