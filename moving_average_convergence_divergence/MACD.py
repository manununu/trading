# -*- encoding: utf-8 -*-
import pandas as pd
from datetime import datetime as dt
import argparse 
import os
from progress.bar import Bar
import multiprocessing
import plotly.express as px
import plotly.graph_objs as go

dir = os.getcwd()

def calc_emas(df, steps, maxema):
    for i in range(steps, maxema+1):
        if(i % steps ==0):
            col_name = 'EMA' + str(i)
            df[col_name] = df['close'].ewm(span=i, adjust=False).mean()

def calc_best_emas(df, short_ema, long_ema, debug):
    deltas = []
    price_changes = []
    delta = 0
    maxema = int(''.join(filter(str.isdigit, long_ema)))
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
                    delta = round(df['low'][price_changes[-2]] - df['high'][i], 6)
                    deltas.append(delta)
                    if debug:
                        print('[i] Bullish..')
                        print('[i] ' + ' '.join(map(str, list(df.iloc[i]))))
                        print('[i] Last delta: ' + str(delta))
                        print('[i] Current sum of deltas: ', str(sum(deltas)))
                        print('- ' * 20)
            else:
                if(len(price_changes)>1):
                    delta = round(df['low'][i] - df['high'][price_changes[-2]], 6)
                    deltas.append(delta)
                    if debug:
                        print('[i] Bearish..')
                        print('[i] ' + ' '.join(map(str, list(df.iloc[i]))))
                        print('[i] Last delta: ' + str(delta))
                        print('[i] Current sum of deltas: ', str(sum(deltas)))
                        print('- ' * 20)

            initial_state = state
    indicator_name = short_ema + ' / ' + long_ema
    indicator_result = sum(deltas)
    return {indicator_name: indicator_result}

def main():

    # Argument parser
    parser = argparse.ArgumentParser(description='Get most profitable moving averages for MACD strategy.') 
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), help='Input csv file with no header and the following columns: date, open, high, low, close')
    parser.add_argument('-o', '--outfile', default=None, help='Specify output file to save results in CSV format.')
    parser.add_argument('-m', '--maxema', default=100, help='Specify the maximum EMA. Default: 100')
    parser.add_argument('-n', '--steps', default=10, help='Specify step size. Default: 10. E.g. when maximum EMA is 6 and step size equals 2, EMAs 2/4/6 are used.')
    parser.add_argument('-p', '--processes', default=4, help='Specify number of cores used for multiprocessing. Default: 4.')
    parser.add_argument('-g', '--graph', action='store_true', help='Set this flag to get a plot of results.')
    parser.add_argument('-d', '--debug', nargs=2, help='Set this flag to run debug mode. If this flag is set, only the two given EMAs getting calculated with verbose output.')
    args = parser.parse_args()

    # Variables
    filename = args.file
    outfile = args.outfile
    maxema = int(args.maxema)
    steps = int(args.steps) 
    n_processes = int(args.processes)
    pool = multiprocessing.Pool(processes=n_processes)
    plot = args.graph
    results = {}
    
    # Checking arguments
    if(filename == None):
        print('[?] Use python3 MACD.py --help for more information..')
        exit()
    if(maxema % steps != 0):
        print('[!] Error: Max.EMA % steps =! 0..')
        exit()

    # Read data
    print('[+] Reading in data..')
    try:
        df = pd.read_csv(args.file, names=['date', 'open', 'high', 'low', 'close'], index_col=False)
    except:
        print('[!] Error: read_csv(). Please check file permissions and format..')
        exit()

    # Checking if default values were used
    if(maxema == 100 and steps == 10 and args.debug == None):
        print('[i] Default values used for max_ema and steps..')
    
    ## Debug mode
    if args.debug != None:
        print('[!] Debug mode..')
        debug_short_ema_num, debug_long_ema_num = args.debug
        debug_short_ema = "EMA" + debug_short_ema_num
        debug_long_ema = "EMA" + debug_long_ema_num
        df[debug_short_ema] = df['close'].ewm(span=int(debug_short_ema_num), adjust=False).mean()
        df[debug_long_ema] = df['close'].ewm(span=int(debug_long_ema_num), adjust=False).mean()
        result = calc_best_emas(df, debug_short_ema, debug_long_ema, True)
        result = pd.DataFrame(result.items(), columns=['indicator', 'result'])
        print('# ' * 20)
        print('[i] Final result: ' + str(result['result'][0]))
        # Plot
        fig = px.line(df, x='date', y='close')
        fig.add_trace(go.Scatter(
            x=df['date'], 
            y=df[debug_short_ema],
            name=debug_short_ema
        ))
        fig.add_trace(go.Scatter(
            x=df['date'], 
            y=df[debug_long_ema],
            name=debug_long_ema
        ))
        fig.update_layout(
            xaxis_type="category"
        )
        fig.show()
        exit() 

    ## Regular mode 
    # Calculating EMA's
    print('[+] Calculating EMAs..')
    calc_emas(df, steps, maxema)

    # Start processing
    current_progress = 0
    with Bar('[+] Calculating best EMAs..') as bar:
        progress = 1 / sum([x-1 for x in list(range(1,len(df.columns[5:])+1))]) * 100
        for short_ema in df.columns[5:]:
            short_ema_index = int(''.join(filter(str.isdigit, short_ema)))
            for long_ema in df.columns[5:]:
                long_ema_index = int(''.join(filter(str.isdigit, long_ema)))
                if short_ema_index < long_ema_index:
                    process = pool.apply_async(calc_best_emas, args=(df, short_ema, long_ema, False), callback=results.update)
                    process.wait()
                    bar.next(progress)
                    current_progress += progress
                    if(current_progress > 99):
                        bar.next(100-current_progress)

    results = pd.DataFrame(results.items(), columns=['indicator', 'result'])
    print('-------------------------------')
    print('[+] Best indicator: ' + results['indicator'][results.result.idxmax()])
    print('[+] Result: ' + str(round(results.result.max(), 2)))
    print('-------------------------------')
    if outfile != None:
        print('[+] Writing results to: ' + str(outfile))
        results.to_csv(outfile)
    if plot==True:
        print('[+] Showing plot of results..')
        # Creating plot
        fig = px.line(results, x='indicator', y='result')
        fig.add_shape(
            # Line Horizontal
                type="line",
                x0=0,
                y0=results.result.max(),
                x1=results.result.idxmax(),
                y1=results.result.max(),
                line=dict(
                    color='red',
                    width=1,
                    dash="dashdot",
                )
        )
        fig.add_shape(
            # Line Vertical 
                type="line",
                x0=results.result.idxmax(),
                y0=results.result.min(),
                x1=results.result.idxmax(),
                y1=results.result.max(),
                line=dict(
                    color='red',
                    width=1,
                    dash="dashdot",
                )
        )
        fig.show()

if __name__=='__main__':
    main()
