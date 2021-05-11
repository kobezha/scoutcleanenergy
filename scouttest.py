
import pandas as pd
import datetime 
import math
from pytz import timezone

excel_file_path = 'scout_test_data.csv'
df = pd.read_csv(excel_file_path)
df_info = df.info()

#df is the main dataframe
#df_index is the string of column you want to search
#this function returns set of indices where the column is missing data
def locate_missing_VTWS(df,df_index):
    result = set()
    for index, row in df.iterrows():
        if math.isnan(row[df_index]):
            result.add(row['id'])   
    return result



def fill_timestamps(df):
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    df_expanded = df.reindex(pd.date_range(start=df.index[0].astimezone(timezone('US/Central')),
                            end=df.index[-1].astimezone(timezone('US/Central')),freq='3600s'))
    return df_expanded

def locate_missing_timestamps(df):
    result = set()
    for index, row in df.iterrows():
        if (math.isnan(row['VTWS_AVG']) and math.isnan(row['WIND_SPEED']) and math.isnan(row['WIND_SPEED_2'])
            and math.isnan(row['windspeed5']) and math.isnan(row['Windspeed3a'])):
            row['id'] = prevrow['id'] + 1
            result.add(row['id'])
        prevrow = row   
    return result

def main():
    df_expanded = fill_timestamps(df)
    print(df_expanded)
    missing_VTWS = locate_missing_VTWS(df,'VTWS_AVG')
    missing_TS = locate_missing_timestamps(df_expanded)
    print(missing_TS)




main();





