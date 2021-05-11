import pandas as pd
import datetime 
import math
from pytz import timezone

#reads excel file and converts the file into a dataframe
excel_file_path = 'scout_test_data.csv'
df = pd.read_csv(excel_file_path)


#this function searches through the dataframe to find missing VTWS values
#it collects the ids of the missing VTWS values and returns of set of those ids
def locate_missing_VTWS(df):
    result = set()
    for index, row in df.iterrows():
        if math.isnan(row['VTWS_AVG']):
            result.add(row['id'])   
    return result


#this function takes in a dataframe and then returns a version of the dataframe with all of its timestamps listed
def fill_timestamps(df):
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    df_expanded = df.reindex(pd.date_range(start=df.index[0].astimezone(timezone('US/Central')),
                            end=df.index[-1].astimezone(timezone('US/Central')),freq='3600s'))
    
    return df_expanded

#finds which rows were missing timestamps and fills in the id for those rows
#takes the dataframe as input
def locate_missing_timestamps(df):
    result = set()
    for index, row in df.iterrows():
        if (math.isnan(row['VTWS_AVG']) and math.isnan(row['WIND_SPEED']) and math.isnan(row['WIND_SPEED_2'])
            and math.isnan(row['windspeed5']) and math.isnan(row['Windspeed3a'])):
            row['id'] = prevrow['id'] + 1
            result.add(row['id'])
        prevrow = row   
    return result

#creates and adds flag columns onto dataframe
#takes expanded dataframe and the missing sets for VTWS data and the timestamps
def create_flag_columns(df_expanded,missing_VTWS,missing_TS):
    timezone_flag = []
    vtws_flag = []
    for index, row in df_expanded.iterrows():
        print(row['id'])
        if row['id'] in missing_TS:
            timezone_flag.append('missing from original')
            vtws_flag.append('Erroneous')
        elif row['id'] in missing_VTWS:
            vtws_flag.append('Erroneous')
            timezone_flag.append('not missing')
        else:
            timezone_flag.append('not missing')
            vtws_flag.append('Valid')
    df_expanded['Timezone Flags'] = timezone_flag
    df_expanded['data qc flag VTWS_AVG'] = vtws_flag
    return df_expanded
 



#takes dataframe as input and utilizes previous functions to locate the missing timestamps and VTWS_AVG values
#creates new dataframe with missing timestamps and flag columns for VTWS_AVG/timestamps to signal where errors/missing values occur
#returns new dataframe and also exports dataframe as csv file to current path
def check_results(df):
    df_expanded = fill_timestamps(df)
    print(df_expanded)
    missing_VTWS = locate_missing_VTWS(df)
    missing_TS = locate_missing_timestamps(df_expanded)
    df_final = create_flag_columns(df_expanded,missing_VTWS,missing_TS)
    df_final['time'] = df_final.index
    df_final.reset_index()
    df_final = df_final[['id','time','VTWS_AVG','WIND_SPEED','WIND_SPEED_2','windspeed5','Windspeed3a','Timezone Flags','data qc flag VTWS_AVG']]
    df_final.to_csv(r'check_results.csv',index= False)
    return df_final


#function call
check_results(df)





