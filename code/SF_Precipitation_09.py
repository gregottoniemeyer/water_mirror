import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

filename = "../data/SFO_preciptation_2023.csv"
df = pd.read_csv(filename, delimiter=',')
keep = ['DATE', 'HourlyDryBulbTemperature', 'HourlyVisibility', 'HourlyWindSpeed','HourlyWindDirection', 'HourlyPrecipitation']
df = df[keep]
df.ffill(inplace=True)
df['timestamp']=pd.to_datetime(df['DATE'], format='%Y-%m-%dT%H:%M:%S')
df.set_index(df['timestamp'], inplace=True)
df.drop(columns=['DATE'], inplace=True)
# Drop the 'STATION' column
df.drop(columns=['timestamp'], inplace=True)
# Convert object columns to numeric
df = df.apply(pd.to_numeric, errors='coerce')
# Replace NaN values with 0.0
df.fillna(0.0, inplace=True)
df = df.iloc[2:]
#normalize each column: 
df_normalized = df.copy()  # Create a copy of the original DataFrame
columns_to_normalize = ['HourlyDryBulbTemperature', 'HourlyVisibility', 'HourlyWindSpeed', 'HourlyWindDirection', 'HourlyPrecipitation']
for column in columns_to_normalize:
    df_normalized[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
df_normalized.head()

plt.figure(figsize =(15,5))
plt.plot(df_normalized.index, df_normalized["HourlyPrecipitation"])
plt.show()

df_normalized.to_csv('../data/precipitation.csv')