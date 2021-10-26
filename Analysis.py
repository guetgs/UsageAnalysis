from typing import Dict

import numpy as np
import pandas as pd


def getIndividualFrames(readings: pd.DataFrame,  
                        col_name: str = 'name') -> Dict:
    meters = readings[col_name].unique()
    dfs = {}
    for meter in meters:
        df = readings[readings[col_name] == meter].copy()
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.drop(col_name, axis=1)
        dfs[meter] = df
    return dfs


def getIntervalData(meter_readings: pd.DataFrame,
                    interval: str) -> pd.Series:
    df = meter_readings.resample('1d').interpolate()
    resampler = df.resample(interval, label='left')
    starts = resampler.first()
    ends = starts[1:].values
    return -starts[:-1] + ends


def getAverageConsumption(meter_readings: pd.DataFrame, 
                          interval: str) -> float:
    interval_data = getIntervalData(meter_readings, interval)
    return interval_data.mean().values[0]


def getMonthlyCost(utility: str, readings: pd.DataFrame, 
                   prices: Dict) -> float:
    gas_conversion = 0.9674 * 11.2920
    meter_readings = getIndividualFrames(readings)[utility]
    if utility == 'Gas':
        meter_readings = meter_readings * gas_conversion
    daily = getIntervalData(meter_readings, '1d')
    yearly = []
    for i in range(len(daily)-365):
        yearly.append(daily.iloc[i:i+365].sum().values[0])
    yearly = np.mean(yearly)
    ut_price = prices[utility]
    yearly_cost = ut_price[1] * 12 + ut_price[0] * yearly
    return yearly_cost / 12


def prepare_holoview_df(readings: pd.DataFrame) -> pd.DataFrame:
    meters = getIndividualFrames(readings)
    d_use = {}
    for meter, df in meters.items():
        d_use[meter] = getIntervalData(df, '1d')
    d_use = pd.concat(d_use, axis=1).droplevel(1, axis=1)
    d_use = d_use.stack().reset_index()
    d_use = d_use.rename({'level_1': 'Utility', 0: 'Consumption'}, axis=1)
    return d_use
