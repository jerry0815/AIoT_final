import pandas as pd

df = pd.read_csv('./solar_data_202003_202007.csv')
df.insert(4, 'timedelta', 0)
df.insert(5, 'kwh', 0)
df['Local_Time'] = df['Local_Time'].str.replace('.000', '')

df['Local_Time'] = pd.to_datetime(df['Local_Time'], format='%Y-%m-%d %H:%M:%S')
df['timedelta'] = (df['Local_Time'].values.astype('int64')  // 10**9) \
                    - (df['Local_Time'].shift(1).values.astype('int64') // 10**9)
df['timedelta'][0] = 0

df['kwh'] = df['OPTPWR'].rolling(2).sum() / 2
df['kwh'] = (df['kwh'] * df['timedelta'] / 3600).round(3)

df2 = pd.DataFrame()
df2 = df[['Local_Time','OPTPWR','timedelta','kwh','ACV1','ACV2','ACCL1','ACCL2','ACF1','IIT','IHT','DCVL1','DCVL2','DCCL1','DCCL2','IPA','IPB','TOTALKWH']]

df2 = df2.groupby(pd.Grouper(key='Local_Time', freq='60Min')).max().reset_index()

df3 = df.groupby(pd.Grouper(key='Local_Time', freq='60Min')).sum().reset_index()
df2['kwh'] = df3['kwh']
print(df2)
kwh = list(df3.loc[1:,'kwh'])
df3 = df3.iloc[:-1,:]
df2 = df2.iloc[:-1,:]
df3['kwh'] = kwh
df2['kwh'] = df3['kwh']
df2 = df2.drop(df2[df2['kwh'] < 0].index)
df2 = df2.drop(columns='timedelta')
df2 = df2.dropna()

df2.insert(1, 'HOUR', 0)
df2.insert(1, 'DAY', 0)
df2.insert(1, 'MONTH', 0)
df2.insert(1, 'YEAR', 0)
df2['YEAR'] = pd.DatetimeIndex(df2['Local_Time']).year
df2['MONTH'] = pd.DatetimeIndex(df2['Local_Time']).month
df2['DAY'] = pd.DatetimeIndex(df2['Local_Time']).day
df2['HOUR'] = pd.DatetimeIndex(df2['Local_Time']).hour

df2.to_csv('./solar_data_202003_202007_processed.csv')
print(df2)
print(df2.isnull().sum())