import pandas as pd


def ConsumptionOverTime(zahler_name, df):
    '''
    INPUT: text, pandas DataFrame
    OUTPUT: pandas DataFrame

    Filters data to represent only readings from a single usage meter with
    the timeline as index.
    '''
    filtered_db = df[df.zahler_name == zahler_name].loc[:, ['date', 'entry']]
    filtered_db.set_index('date', drop=True, inplace=True)
    filtered_db.sort_index(inplace=True)

    return filtered_db
