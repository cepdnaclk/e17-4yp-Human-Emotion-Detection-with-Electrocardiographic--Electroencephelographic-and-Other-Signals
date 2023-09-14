import pandas as pd
import numpy as np

# Read data from colon-separated CSV file
df = pd.read_csv('../DATA_FILES/ECG/1001/ecg_1001_NEUTRAL_2023-08-28 14_54_42.txt', sep=':', header=None, names=['timestamp', 'value'])

# Convert 'timestamp' column to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

print(df['timestamp'].min())
print(df['timestamp'].max())
resampled_index = pd.date_range(start=df['timestamp'].min(), end=df['timestamp'].max(), freq='ms')
resampled_df = pd.DataFrame(index=resampled_index)
resampled_df['timestamp'] = resampled_df.index
resampled_df['timestamp_seconds'] = (resampled_df['timestamp'] - pd.Timestamp('1970-01-01')) / pd.Timedelta(seconds=1)
resampled_df.sort_values(by='timestamp_seconds', inplace=True)
resampled_df.drop(columns=['timestamp'], inplace=True)
# resampled_df.to_csv('output_data1.csv', index=False)

# Calculate seconds since the Unix epoch
df['timestamp_seconds'] = (df['timestamp'] - pd.Timestamp('1970-01-01')) / pd.Timedelta(seconds=1)

# Sort the DataFrame by 'timestamp_seconds'
df.sort_values(by='timestamp_seconds', inplace=True)

# Fill missing values with the previous value
df['value'] = df['value'].fillna(method='ffill')

# Calculate the average value for duplications
df = df.groupby(['timestamp_seconds', 'value']).size().reset_index(name='count')
df['avg_value'] = df.groupby('timestamp_seconds')['value'].transform('mean')

df.drop(columns=['value', 'count'], inplace=True)
df.rename(columns={'avg_value': 'value'}, inplace=True)

df.drop_duplicates(subset=['timestamp_seconds', 'value'], inplace=True)

# Save the modified DataFrame to a new CSV file
df.to_csv('output_data.csv', index=False)

# Merge resampled DataFrame with the grouped data
merged_df = pd.merge(resampled_df, df, on='timestamp_seconds', how='left')

# Drop the index column
merged_df.reset_index(drop=True, inplace=True)

# Fill missing values using forward fill (ffill)
merged_df['value'] = merged_df['value'].ffill()

# Save the modified DataFrame to a new CSV file
merged_df.to_csv('merged_data_filled.csv', index=False)

# Read your merged CSV file (assuming it's named 'merged_data_filled.csv')
merged_df = pd.read_csv('merged_data_filled.csv')

# Convert 'timestamp_seconds' to datetime format
merged_df['timestamp_seconds'] = pd.to_datetime(merged_df['timestamp_seconds'], unit='s')

# Set 'timestamp_seconds' as the index
merged_df.set_index('timestamp_seconds', inplace=True)

# Resample to 256Hz
resampled_df = merged_df.resample('4ms').mean()

# Reset the index
resampled_df.reset_index(inplace=True)

resampled_df['timestamp_seconds'] = (resampled_df['timestamp_seconds'] - pd.Timestamp('1970-01-01')) / pd.Timedelta(seconds=1)

# Save the resampled DataFrame to a new CSV file
resampled_df.to_csv('resampled_data.csv', index=False)
