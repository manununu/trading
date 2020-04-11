import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

def calc_emas(df, steps, maxema):
    for i in range(steps, maxema+1):
        if(i % steps ==0):
            col_name = 'EMA' + str(i)
            df[col_name] = df['close'].ewm(span=i, adjust=False).mean()

def calc_best_emas(df, short_ema, long_ema):
    deltas = []
    price_changes = []
    delta = 0
    maxema = int(''.join(filter(str.isdigit, str(long_ema))))
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
            else:
                if(len(price_changes)>1):
                    delta = round(df['low'][i] - df['high'][price_changes[-2]], 6)
                    deltas.append(delta)
            initial_state = state
    indicator_name = short_ema + ' / ' + long_ema
    indicator_result = sum(deltas)
    return {indicator_name: indicator_result}

df = pd.read_csv('sample_data/GBPJPY_20191201_20200327/data.csv', index_col=False, names=['date', 'open', 'high', 'low', 'close'])

calc_emas(df, 100, 15000)
print(calc_best_emas(df, "EMA1000", "EMA9000"))

'''
fig = px.line(df,x="date", y="close")
fig.add_trace(go.Scatter(
    x=df['date'], 
    y=df['EMA1100'],
    name='EMA1100'
))
fig.add_trace(go.Scatter(
    x=df['date'], 
    y=df['EMA8400'],
    name='EMA8400'
))

fig.update_layout(
    xaxis_type="category"
)

fig.show()
'''