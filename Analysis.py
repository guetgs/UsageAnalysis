import pandas as pd

def getIndividualFrames(readings,  
                        col_name='name'):
    meters = readings[col_name].unique()
    dfs = {}
    for meter in meters:
        df = readings[readings[col_name] == meter].copy()
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.drop(col_name, axis=1)
        dfs[meter] = df
    return dfs

def getIntervalData(meter_readings, interval):
    df = meter_readings.resample('1d').interpolate()
    resampler = df.resample(interval, label='left')
    starts = resampler.first()
    ends = starts[1:].values
    return starts[:-1]*-1 + ends

def getAverageConsumption(meter_readings, interval):
    interval_data = getIntervalData(meter_readings, interval)
    return interval_data.mean().values[0]

def getMonthlyCost(utility, readings, prices):
    gas_conversion = 0.9674 * 11.2920
    meter_readings = getIndividualFrames(readings)[utility]
    if utility == 'Gas':
        meter_readings = meter_readings * gas_conversion
    yearly = getAverageConsumption(meter_readings, '365d')
    ut_price = prices[utility]
    yearly_cost = ut_price[1]*12 + ut_price[0]*yearly
    return yearly_cost/12