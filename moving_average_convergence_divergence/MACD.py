# -*- encoding: utf-8 -*-
import pandas as pd
from datetime import datetime as dt
import argparse 
import os
from statistics import mean, median
from progress.bar import Bar
import multiprocessing
import plotly.express as px
import plotly.graph_objs as go

dir = os.getcwd()

def calc_emas(df, start, maxema, steps):
    for i in range(start, maxema+1):
        if(i % steps == 0 and i != 0):
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

    indicator_name_sum = short_ema + '_' + long_ema + '_SUM'
    indicator_name_avg = short_ema + '_' + long_ema + '_AVG'
    indicator_name_med = short_ema + '_' + long_ema + '_MED'
    indicator_result_sum = sum(deltas)
    indicator_result_avg = mean(deltas)
    indicator_result_med = median(deltas)
    return {indicator_name_sum: indicator_result_sum, 
            indicator_name_avg: indicator_result_avg, 
            indicator_name_med: indicator_result_med}

def main():

    # Argument parser
    parser = argparse.ArgumentParser(description='Get most profitable moving averages for MACD strategy.') 
    parser.add_argument('-f', '--file', type=argparse.FileType('r'), help='Input csv file with no header and the following columns: date, open, high, low, close.')
    parser.add_argument('-o', '--outfile', default=None, help='Specify output file to save results in CSV format.')
    parser.add_argument('-m', '--maxema', default=100, help='Specify the maximum EMA. Default: 100.')
    parser.add_argument('-n', '--steps', default=10, help='Specify step size. Default: 10. E.g. when maximum EMA is 6 and step size equals 2, EMAs 2/4/6 are used.')
    parser.add_argument('-s', '--start', default=0, help='Specify EMA to start with. Default: 0.')
    parser.add_argument('-p', '--processes', default=4, help='Specify number of cores used for multiprocessing. Default: 4.')
    parser.add_argument('-g', '--graph', default=None, help='Specify whether the results should be visualized by sum, average or median')
    parser.add_argument('-d', '--debug', nargs=2, help='Set this flag to run debug mode. If this flag is set, only the two given EMAs getting calculated with verbose output.')
    args = parser.parse_args()

    # Variables
    filename = args.file
    outfile = os.path.splitext(str(args.outfile))[0]
    maxema = int(args.maxema)
    steps = int(args.steps) 
    start = int(args.start)
    n_processes = int(args.processes)
    pool = multiprocessing.Pool(processes=n_processes)
    plot_by = args.graph
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
    try:
        calc_emas(df, start, maxema, steps)
    except:
        print('[!] Error while calculating EMAs. Check provided values..')

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
    results_sum = results[results['indicator'].str.contains('SUM')]
    results_avg = results[results['indicator'].str.contains('AVG')]
    results_med = results[results['indicator'].str.contains('MED')]
    print('-------------------------------')
    print('[+] Best indicator (sum): ' + 
        results['indicator'][results_sum.result.idxmax()] + 
        ' | Result: ' + 
        str(round(results_sum.result.max(), 2)))
    print('[+] Best indicator (average): ' + 
        results['indicator'][results_avg.result.idxmax()] + 
        ' | Result: ' + 
        str(round(results_avg.result.max(), 2)))
    print('[+] Best indicator (median): ' + 
        results['indicator'][results_med.result.idxmax()] + 
        ' | Result: ' + 
        str(round(results_med.result.max(), 2)))
    print('-------------------------------')
    if outfile != 'None':
        outfile_sum = outfile + '_SUM.csv'
        outfile_avg = outfile + '_AVG.csv'
        outfile_med = outfile + '_MED.csv' 
        print('[+] Writing SUM results to: ' + outfile_sum)
        print('[+] Writing AVG results to: ' + outfile_avg)
        print('[+] Writing MED results to: ' + outfile_med)
        results_sum.to_csv(outfile_sum)
        results_avg.to_csv(outfile_avg)
        results_med.to_csv(outfile_med)
    if plot_by != None:
        print('[+] Showing plot of results..')
        # Plot results
        if(plot_by == 'sum'):
            fig = px.line(results_sum, x='indicator', y='result')
        elif(plot_by == 'average'):
            fig = px.line(results_avg, x='indicator', y='result')
        elif(plot_by == 'median'):
            fig = px.line(results_med, x='indicator', y='result')
        else:
            print('[!] Error in plotting results..')
            exit()
        
        fig.show()

if __name__=='__main__':
    main()
