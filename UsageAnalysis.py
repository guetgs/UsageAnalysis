import panel as pn

from DatabaseInteraction import Database 
from Analysis import *
from Dashboard import *

def main():
    prices = {'Gas': [0.0718, 79.68], 
              'Wasser': [1.79*1.07 + 2.14, 74.16],
              'Strom Guetg': [np.nan, np.nan],
              'Strom Mieter': [np.nan, np.nan]}
    real_db = Database(name='zahler')
    cols = ['zahler_name', 'date', 'entry']
    table = 'readings JOIN zahler ON readings.zahler_id = zahler.zahler_id'
    readings = real_db.DatabaseToDataFrame(cols, table).sort_values('date')
    readings = prepareDataFrame(readings)
    holo_df = prepareHoloviewDf(readings, prices)
    panel = MakePanel(holo_df)
    server = pn.serve(panel)
    return server


if __name__ == '__main__':
    main()