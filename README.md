# Trading

:information_source: Check out the repository from [terukusu](https://github.com/terukusu/download-tick-from-dukascopy) for downloading data (dukascopy)

---
## Moving Average Convergence Divergence (MACD)
### Description
Get the most profitable exponential moving averages for MACD strategy. 

### Install 
Install python3 and python3-pip.
To install the dependencies run the following command:
```
pip3 install -r requirements.txt
```

### Usage
```bash
python3 MACD.py -h # for help
```

```
python3 MACD.py -f sample_data/GBPJPY_20191201_20200327/sub_data.csv -m 1000 -n 100 -p 4 -g -o out.csv 

[+] Reading in data..
[+] Calculating EMAs..
[+] Calculating best EMAs.. |################################| 100/100
-------------------------------
[+] Best indicator: EMA500 / EMA1000
[+] Result: 1.64
-------------------------------
[+] Writing results to: out.csv
[+] Showing plot of results..
```

### Debug mode
```
python3 MACD.py -f sample_data/GBPJPY_20191201_20200327/sub_data.csv -d 2000 2500

[+] Reading in data..
[!] Debug mode..
[i] Bullish..
[i] 2020-03-20 09:06:00 130.411 130.454 130.39700000000002 130.451 127.7955010083138 127.795216688086
[i] Last delta: 3.352
[i] Current sum of deltas:  3.352
- - - - - - - - - - - - - - - - - - - -
[i] Bearish..
[i] 2020-03-23 19:36:00 128.079 128.121 128.063 128.111 128.40650801732858 128.40655156239202
[i] Last delta: -2.391
[i] Current sum of deltas:  0.9609999999999999
- - - - - - - - - - - - - - - - - - - -
[i] Bullish..
[i] 2020-03-24 08:26:00 128.994 129.005 128.945 128.963 128.38283764761138 128.38279999159985
[i] Last delta: -0.942
[i] Current sum of deltas:  0.018999999999999906
- - - - - - - - - - - - - - - - - - - -
# # # # # # # # # # # # # # # # # # # #
[i] Final result: 0.018999999999999906
```
---
