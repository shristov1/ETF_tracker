# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import investpy
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

# # Get funds in Germany

funds = investpy.get_etfs(country='germany')

print(f"There are {len(funds)} funds avaliable in Germany")

# ## I am mostly interested in accumulating BlackRock (and later Amundi) ETFs

# So we are searching for iShares with Acc fields in the names. 

n = 0
for fund in funds.name:
    if (fund.find('iShares') != -1 and fund.find('Acc') != -1):
        if n == 0:
            df = investpy.etfs.get_etf_information(etf=fund, country='germany', as_json=False)
            n += 1
        else:
            df_2 = investpy.etfs.get_etf_information(etf=fund, country='germany', as_json=False)
            df = pd.concat([df,df_2])

# There seems to be a lot of ETFs which are duplicated in the dataset. Let us first remove the rows with duplicate names.

df.drop_duplicates(subset='ETF Name', keep='first', inplace=True)

# Check for NaNs in the information dataframes

df.head()

nan_columns = set(df.columns[df.isnull().mean() > 0])
all_nan_cols = set(df.columns[df.isnull().mean() == 1])
print(f"The columns that have NaNs are: {nan_columns}. And the fields which are all NaNs are: {all_nan_cols}. We drop the fields with all NaNs")

df = df.drop(all_nan_cols, axis=1);

print(f"We need to now sort out the {nan_columns-all_nan_cols} columns")

# Some of the columns which have NaNs are categorical - we leave them NaNs, the numerical columns we exchange NaNs with 0. 

for column in df.columns:
    print(f"{column} - {df[column].dtypes}")

df[['Today-low','Today-high']] = df['Todays Range'].str.split('-',expand=True).astype('float')
df[['52w-low','52w-high']] = df['52 wk Range'].str.split('-',expand=True).astype('float')

df = df.drop(['Todays Range', '52 wk Range'], axis=1)

df[['Average Vol. (3m)', 'Volume']] = df[['Average Vol. (3m)', 'Volume']].astype('float')

df.head()

df['1-Year Change'] = df['1-Year Change'].str.replace('- ', '-')
df['1-Year Change'] = df['1-Year Change'].str.rstrip(' % ').astype('float') / 100.0

for column in ['Volume', 'Average Vol. (3m)']:
    df[column] = df[column].fillna(0)

# Fixing of data is done. Now we start with the analysis of the ETFs

df.describe()

sns.heatmap(df.corr(), annot=True)

# Not surprising there is a correlation between the volume and the 1-year change - more traded ETFs seem to be making more money for the investors.

# ## Let's have a look at which ETFs shall I invest in based on the historical values

# Considering I do not have unlimited funds I will get the ETFs which have > 30% year to year change in the past year. This will be later extended to more old historical values. 

df_high_roi = df[df['1-Year Change'] > 0.3]

df_high_roi

# ### We can see that there are a lot of high RoI over the past year. But how does this compare over the historical data

for etf in df_high_roi["ETF Name"]:
    df_temp = investpy.etfs.get_etf_historical_data(etf=etf, country='germany', from_date='01/01/2010', to_date='01/04/2021', interval='Weekly')
    plt.plot(df_temp.index[:-1],np.diff(df_temp['Close']), label=etf)
    plt.legend()


