import pandas as pd
import numpy as np
import os

# Load the raw data (assuming it's saved as 'verizon_netflix_offers.csv')
df = pd.read_csv(r'C:\Users\venka\Desktop\Netflix_Verizon_+play\verizon_netflix_raw.csv')

# 1. Data Cleaning
print("Initial Data Info:")
print(df.info())

# Check for missing values
missing_values = df.isnull().sum()
print("\nMissing Values:")
print(missing_values)

# Fill missing values or drop rows with missing values
df['Perks Description'] = df['Perks Description'].fillna('No Perks')
df = df.dropna(subset=['Content Title'])

# Remove duplicate rows
df = df.drop_duplicates()

# Ensure correct data types
df['Total Data Usage (GB)'] = df['Total Data Usage (GB)'].astype(float)

print("\nCleaned Data Info:")
print(df.info())

# Save the cleaned data
cleaned_path = r'C:\Users\venka\Desktop\Netflix_Verizon_+play\verizon_netflix_cleaned.csv'
df.to_csv(cleaned_path, index=False)
print(f"Cleaned data saved to {cleaned_path}")

# 2. Data Transformation
# Create a new column indicating heavy users (based on data usage)
df['Heavy User'] = df['Total Data Usage (GB)'] > 300

# Categorize subscription types
subscription_map = {
    'Standard with Ads': 'Basic',
    'Standard': 'Standard',
    'Premium': 'Premium'
}
df['Subscription Category'] = df['Subscription Type'].map(subscription_map)

# Extract peak hour range as a feature
df['Peak Hour Range'] = df['Peak Hours'].apply(lambda x: f"{min(x)}-{max(x)}" if isinstance(x, list) else x)

# Save the transformed data
transformed_path = r'C:\Users\venka\Desktop\Netflix_Verizon_+play\verizon_netflix_transformed.csv'
df.to_csv(transformed_path, index=False)
print(f"Transformed data saved to {transformed_path}")

# 3. Data Aggregation
# Calculate the average data usage per subscription category
avg_data_usage = df.groupby('Subscription Category')['Total Data Usage (GB)'].mean().reset_index()
print("\nAverage Data Usage per Subscription Category:")
print(avg_data_usage)

# Count the number of users in each city
user_count_by_city = df.groupby('City')['Customer ID'].count().reset_index()
user_count_by_city.rename(columns={'Customer ID': 'User Count'}, inplace=True)
print("\nUser Count by City:")
print(user_count_by_city)

# Sum of data usage by device type
total_usage_by_device = df.groupby('Device Type')['Total Data Usage (GB)'].sum().reset_index()
print("\nTotal Data Usage by Device Type:")
print(total_usage_by_device)

# Save the aggregated data
aggregated_path = r'C:\Users\venka\Desktop\Netflix_Verizon_+play\verizon_netflix_aggregated.csv'
avg_data_usage.to_csv(aggregated_path.replace('.csv', '_avg_usage.csv'), index=False)
user_count_by_city.to_csv(aggregated_path.replace('.csv', '_user_count.csv'), index=False)
total_usage_by_device.to_csv(aggregated_path.replace('.csv', '_usage_by_device.csv'), index=False)
print(f"Aggregated data saved to {aggregated_path}")
