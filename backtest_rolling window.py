import keras
import pandas as pd
import numpy as np
from oandapyV20 import API
import oandapyV20.endpoints.instruments as oanda_instruments
print('Please run the file in the Python Shell.\nInputs:')
m_token = input('Oanda account tocken:')
acc_id = input('account ID:')

api = API(access_token=m_token)
instrument=input('Currency Pair(should be same as training input): ')
granularity=input('The desired time frame (Oanda format,should be same as training input): '

def historical_data(instrument, granularity, Ask_Bid):
    r = oanda_instruments.InstrumentsCandles(instrument=instrument,
                                             params=dict(count=31, granularity=granularity, price=Ask_Bid))
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

backtest_data=historical_data(instrument,granularity,'A')['ask'][:30]
target_data=np.array(historical_data(instrument,granularity,'A')['ask'][-1])
target_data=np.array(target_data).reshape((1,))
backtest_data=np.array(backtest_data)
backtest_data=backtest_data.reshape(1,30)
model=keras.models.load_model(str(instrument)+'_'+str(time_frame)+'_model.h5')
prediction=model.predict(backtest_data)
loss=model.train_on_batch(backtest_data,target_data)
print('Prediction:\n'+prediction+'\ntarget:\n'+target_data)
