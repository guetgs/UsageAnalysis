from typing import Dict, List
from IPython.display import display

import numpy as np
import pandas as pd


def getIndividualFrames(readings: pd.DataFrame,  
                        name_col: str = 'name',
                        date_col: str = 'date') -> Dict:
    meters = readings[name_col].unique()
    dfs = {}
    for meter in meters:
        df = readings[readings[name_col] == meter].copy()
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.set_index(date_col)
        df = df.drop(name_col, axis=1)
        dfs[meter] = df
    return dfs


def getIntervalData(meter_readings: pd.DataFrame,
                    interval: str,
                    date_col: str = 'date') -> pd.Series:
    meter_readings = meter_readings.sort_values(date_col)
    df = meter_readings.resample('1d').interpolate()
    resampler = df.resample(interval, label='left')
    starts = resampler.first()
    ends = starts[1:].values
    return -starts[:-1] + ends


def getAverageConsumption(meter_readings: pd.DataFrame, 
                          interval: str) -> float:
    interval_data = getIntervalData(meter_readings, interval)
    return interval_data.mean().values[0]


def getMonthlyCost(utility: str, 
                   readings: pd.DataFrame, 
                   prices: Dict,
                   gas_label: str = 'Gas') -> float:
    gas_conversion = 0.9674 * 11.2920
    meter_readings = getIndividualFrames(readings)[utility]
    if utility == gas_label:
        meter_readings = meter_readings * gas_conversion
    daily = getIntervalData(meter_readings, '1d')
    yearly = daily.rolling(365).sum()
    yearly = yearly.mean().values[0]
    ut_price = prices[utility]
    yearly_cost = ut_price[1] * 12 + ut_price[0] * yearly
    return yearly_cost / 12


def prepareHoloviewDf(readings: pd.DataFrame,
                      date_col: str = 'date') -> pd.DataFrame:
    meters = getIndividualFrames(readings)
    d_use = {}
    for meter, df in meters.items():
        d_use[meter] = getIntervalData(df, '1d')
    d_use = pd.concat(d_use, axis=1).droplevel(1, axis=1)
    d_use = d_use.stack().reset_index()
    d_use = d_use.rename({'level_1': 'Utility', 0: '1 day'}, axis=1)
    d_use = d_use.groupby('Utility').apply(
        lambda sl: getRollingSum(sl, '1 day', [7, 30]))
    d_use = d_use.set_index([date_col, 'Utility']).stack().reset_index()
    d_use = d_use.rename({'level_2': 'Interval', 0: 'Consumption'}, axis=1)
    return d_use


def getRollingSum(d_use: pd.DataFrame,
                  col: str,
                  intervals: List) -> pd.DataFrame:
    for n_days in intervals:
        d_use[f'{n_days} days'] = d_use[col].rolling(n_days, center=True).sum()
    return d_use
