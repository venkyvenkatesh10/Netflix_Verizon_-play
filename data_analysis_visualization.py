import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the transformed data
df = pd.read_csv(r'C:\Users\venka\Desktop\Netflix_Verizon_+play\verizon_netflix_transformed.csv')

# Define the output path
output_path = r'C:\Users\venka\Desktop\Netflix_Verizon_+play'

# 1. Distribution of Total Data Usage
plt.figure(figsize=(10, 6))
sns.histplot(df['Total Data Usage (GB)'], kde=True)
plt.title('Distribution of Total Data Usage (GB)')
plt.xlabel('Total Data Usage (GB)')
plt.ylabel('Frequency')
plot_path = os.path.join(output_path, 'distribution_total_data_usage.png')
plt.savefig(plot_path)
print(f"Saved plot: {plot_path}")
plt.show()

# 2. Average Data Usage by Subscription Category
plt.figure(figsize=(10, 6))
sns.barplot(x='Subscription Category', y='Total Data Usage (GB)', data=df)
plt.title('Average Data Usage by Subscription Category')
plt.xlabel('Subscription Category')
plt.ylabel('Average Data Usage (GB)')
plot_path = os.path.join(output_path, 'avg_data_usage_subscription_category.png')
plt.savefig(plot_path)
print(f"Saved plot: {plot_path}")
plt.show()

# 3. User Count by City
# Correct the user count calculation and renaming
user_count_by_city = df.groupby('City').size().reset_index(name='User Count')
plt.figure(figsize=(12, 8))
sns.barplot(x='User Count', y='City', data=user_count_by_city.sort_values('User Count', ascending=False))
plt.title('User Count by City')
plt.xlabel('User Count')
plt.ylabel('City')
plot_path = os.path.join(output_path, 'user_count_by_city.png')
plt.savefig(plot_path)
print(f"Saved plot: {plot_path}")
plt.show()

# 4. Relationship Between Streaming Hours and Data Usage
plt.figure(figsize=(10, 6))
sns.scatterplot(x='StreamingHours', y='Total Data Usage (GB)', hue='Subscription Category', data=df)
plt.title('Streaming Hours vs Total Data Usage (GB)')
plt.xlabel('Streaming Hours')
plt.ylabel('Total Data Usage (GB)')
plot_path = os.path.join(output_path, 'streaming_hours_vs_data_usage.png')
plt.savefig(plot_path)
print(f"Saved plot: {plot_path}")
plt.show()
