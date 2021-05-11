
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
def locate_missing(df,df_index):
    result = set()
    for index, row in df.iterrows():
        if math.isnan(row[df_index]):
            result.add(row['id'])   
    return result

print(locate_missing(df,'VTWS_AVG'))


df['time'] = pd.to_datetime(df['time'])
df = df.set_index('time')
print(df)
print(df.reindex(pd.date_range(start=df.index[0].astimezone(timezone('MST')),
                end=df.index[-1].astimezone(timezone('MST')),freq='3600s')))






