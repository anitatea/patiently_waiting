# scrape.py
# cleaning as well
import urllib.request, json
import json
import numpy as np
import pandas as pd


def get_hospital_data(hosp_id):
    url = f"https://drivepublic.hqontario.ca/Report/GetWaitTimesEDData?ResultType=PIA&org_ID={hosp_id}"
    print(url)
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())
        wait_time = pd.DataFrame(data)
        df_hospital = wait_time[wait_time['orgSort'] == 1]
    return df_hospital

# concat current_df & df_hosp
def concat_hosp_data(df, hospital_id):
    df_new = pd.DataFrame()
    for h in hospital_id:
        df_temp = get_hospital_data(h)
        df_new = pd.concat([df_new, df_temp]) # can put original and then new one to new df
    return df_new

df = pd.DataFrame()
hospital_id_list = [1364, 1359, 4935, 3742, 4824, 4931, 4800, 4831, 4850]
df_wait_times = concat_hosp_data(df, hospital_id_list)


# --------------------------------------------------------
# data cleaning
# drop consistent columns, we will take out of df
df_wait_times['WaitTime_percent_within_target'].unique()
df_wait_times['PriorityDescription'].unique()

# removes the RI (null rows)
df_wait_times = df_wait_times[~df_wait_times.select_dtypes(['object']).eq('RI').any(1)]

# converts obj to num
df_wait_times['WaitTime_mean'] = df_wait_times['WaitTime_mean'].astype(float)
df_wait_times['WaitTime_90percentile'] = df_wait_times['WaitTime_90percentile'].astype(float)
df_wait_times['number_of_cases'] = df_wait_times['number_of_cases'].astype(float)
df_wait_times.info()

df_wait_times = df_wait_times.rename(columns={"number_of_cases":"case_per_month"})

df_wait_times['case_per_month'].sum()

df_wait_times['day'] = ""

df_wait_times['case_per_day'] = ""
# df_wait_times['case_per_day'] = pd.to_numeric(df['case_per_day'], errors='coerce').fillna(0)


df_wait_times.head(1)
# to test one sample
df_test = df_wait_times

# based on numbers from CIHI (reference in README)
d = {'Monday': 0.151593223,'Tuesday':0.148917637,'Wednesday':0.147174568,'Thursday':0.146813667,'Friday':0.143226496,'Saturday':0.129701107,'Sunday':0.132573301}

days_of_week = pd.DataFrame(data=d, index=[0])
days_of_week

df_test.head(1)

df_test2 = pd.DataFrame()

# loop to add in days of week & cases per week
for row in range(len(df_test)):
    # adds day of week
    for x in range(len(days_of_week.columns)):
        # inserting day of week
        df_test['day'].iloc[row] = days_of_week.columns[x]
        # inserting case per day
        per_day = days_of_week.iloc[0][days_of_week.columns[x]] * df_test['case_per_month'].iloc[row]
        df_test['case_per_day'].iloc[row] = per_day
        # appending row together
        df_test2 = df_test2.append(df_test.iloc[row]) # appending to df_test_2

df_test2.info()


# convert to CSV
df_test2.to_csv(r'data_final.csv', index=False)
