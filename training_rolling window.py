import keras
import pandas as pd
import numpy as np
from oandapyV20 import API
import oandapyV20.endpoints.instruments as oanda_instruments
print('Please run the file in the Python Shell.\nInputs:')
m_token = input('Oanda account tocken:')
acc_id = input('account ID:')
api = API(access_token=m_token)
instrument=input('Currency Pair: ')
granularity=input('The desired time frame (Oanda format): '
def historical_data(instrument, granularity, Ask_Bid):
    r = oanda_instruments.InstrumentsCandles(instrument=instrument,
                                             params=dict(count=4800, granularity=granularity, price=Ask_Bid))
    res = None
    while res is None:
        try:
            res = api.request(r)
        except:
            pass
    if Ask_Bid == 'A':
        return pd.DataFrame(
            index=[pd.to_datetime(res['candles'][i[0]]['time']) for i in enumerate(res['candles'])],
            columns=['ask'],
            data=[float(res['candles'][i[0]]['ask']['c']) for i in enumerate(res['candles'])])
    if Ask_Bid == 'B':
        return pd.DataFrame(
            index=[pd.to_datetime(res['candles'][i[0]]['time']) for i in enumerate(res['candles'])],
            columns=['bid'],
            data=[float(res['candles'][i[0]]['bid']['c']) for i in enumerate(res['candles'])])

train_data=historical_data(instrument,granularity,'A')['ask']
print('history loaded')
window_length=30
trajectory_matrix=pd.DataFrame(index=[i for i in range(len(train_data)-window_length)],
                                      columns=[i for i in range(window_length)])
for i in trajectory_matrix.index:
    for j in trajectory_matrix.keys():
        trajectory_matrix[j][i]=train_data[i+j]
print('trajectory made')
predictors=np.array(trajectory_matrix.iloc[:,0:28])
target=np.array(trajectory_matrix[29])
print('target and prediction created')
input_shape=trajectory_matrix.shape[1]
optimizer=keras.optimizers.adam(lr=0.000001)
model=keras.models.Sequential()
model.add(keras.layers.Dense(200,
                             activation='linear',
                             input_shape=(input_shape,)))
model.add(keras.layers.Dense(300,
                             activation='linear'))
model.add(keras.layers.Dense(200,
                             activation='linear'))
model.add(keras.layers.Dense(300,
                             activation='linear'))
model.add(keras.layers.Dense(300,
                             activation='linear'))
model.add(keras.layers.Dense(300,
                             activation='linear'))
model.add(keras.layers.Dense(300,
                             activation='linear'))
model.add(keras.layers.Dense(300,
                             activation='linear'))
model.add(keras.layers.Dense(1))
model.compile(optimizer=optimizer,loss='mean_squared_error')
process=model.fit(x=trajectory_matrix,
          y=target,
          epochs=3000,
          validation_split=0.1)
model.save(str(instrument)+'_'+str(time_frame)+'_model.h5')
