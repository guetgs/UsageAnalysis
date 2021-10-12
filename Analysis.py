import pandas as pd

def getIndividualFrames(zahler, readings, 
                        zahler_name='zahler_name', 
                        readings_name='name'):
    meters = zahler[zahler_name].unique()
    dfs = {}
    for meter in meters:
        df = readings[readings[readings_name] == meter].copy()
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.drop(readings_name, axis=1)
        dfs[meter] = df
    return dfs

def getIntervalData(meter_readings, interval):
    df = meter_readings.resample('1d').interpolate()
    resampler = df.resample(interval, label='left')
    starts = resampler.first()
    ends = resampler.last()

    return ends[:-1]-starts[:-1]