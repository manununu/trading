# -*- encoding: utf-8 -*-
import pandas as pd
from datetime import datetime as dt
import re
import argparse
import os
from progress.bar import Bar

dir = os.getcwd()


def main():

    # Argument parser
    parser = argparse.ArgumentParser(description='Get most profitable moving averages for MACD strategy.') 
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), help='Input csv file with no header and the following columns: date, high, low, close')
    #parser.add_argument('-o', '--output', default=dir+'/output.csv', help='Specify output file for results. Default: output.csv')
    parser.add_argument('-m', '--maxema', default=100, help='Specify the maximum EMA')
    parser.add_argument('-n', '--steps', default=10, help='Specify step size. E.g. when maximum EMA is 6 and step size equals 2, EMAs 2/4/6 are used.')
    args = parser.parse_args()

    # Variables
    filename = args.file
    maxema = int(args.maxema)
    steps = int(args.steps) 
    
    # Checking arguments
    if(filename == None):
        print('[?] Use python3 MACD.py --help for more information..')
        exit()
    
    if(maxema % steps != 0):
        print('[!] Error: Max.EMA % steps =! 0..')
        exit()

    # Read data
    print('')
    print('[i] Reading in data..')
    print('')
    try:
        df = pd.read_csv(args.file, names=['date', 'open', 'high', 'low', 'close'], index_col=False)
    except:
        print('[!] Error: read_csv(). Please check file permissions and format..')
        exit()
    
    # Calculating EMA's
    print('[i] Calculating EMAs...')
    print('')
    for i in range(steps, maxema+1):
        if(i % steps ==0):
            col_name = 'EMA' + str(i)
            df[col_name] = df['close'].ewm(span=i, adjust=False).mean()

    # Start testing
    results = pd.DataFrame(columns=['indicators', 'result'])
    price_changes = []
    deltas = []
    delta = 0
   
    with Bar('[i] Processing...') as bar:
        for short_ema in df.columns[5:]:
            short_ema_index = int(''.join(filter(str.isdigit, short_ema)))
            for long_ema in df.columns[5:]:
                long_ema_index = int(''.join(filter(str.isdigit, long_ema)))
                if short_ema_index < long_ema_index:
                    initial_state = 1 if df[short_ema][maxema] > df[long_ema][maxema] else 0
                    # Go through df
                    for i in range(maxema,df.shape[0]):
                        if df[short_ema][i] > df[long_ema][i]:
                            state = 1
                        else:
                            state = 0
                        if state != initial_state:
                            price_changes.append(i)
                            if state == 1:
                                if(len(price_changes)>1):
                                    delta = round(df['low'][price_changes[-2]] - df['high'][i], 2)
                                    deltas.append(delta)
                            else:
                                if(len(price_changes)>1):
                                    delta = round(df['low'][i] - df['high'][price_changes[-2]], 2)
                                    deltas.append(delta)
                            initial_state = state
                    indicator_name = short_ema + ':' + long_ema
                    indicator_result = sum(deltas)
                    results = results.append({'indicators': indicator_name, 'result': indicator_result}, ignore_index=True)
            progress = round((1/len(df.columns[5:]))*100, 2)
            bar.next(progress)
        print('')
        print('')
        print('-------------------------------------------')
        print('')
        print('[+] Best result: ' + str(round(results.result.max(), 2)))
        print('[+] Best indicator: ' + results['indicators'][results.result.idxmax()])

if __name__=='__main__':
    main()
