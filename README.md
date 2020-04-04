# trading

## moving average convergence divergence

```bash
python3 MACD.py -h
usage: MACD.py [-h] [-f FILE] [-o OUTPUT] [-m MAXEMA] [-n STEPS]

Get most profitable moving averages for MACD strategy.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Input csv file with no header and the following
                        columns: date, high, low, close
  -o OUTPUT, --output OUTPUT
                        Specify output file for results. Default: output.csv
  -m MAXEMA, --maxema MAXEMA
                        Specify the maximum EMA
  -n STEPS, --steps STEPS
                        Specify step size. E.g. when maximum EMA is 6 and step
                        size equals 2, EMAs 2/4/6 are used.
```

