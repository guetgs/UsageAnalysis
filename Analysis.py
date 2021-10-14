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
    return interval_data.mean()