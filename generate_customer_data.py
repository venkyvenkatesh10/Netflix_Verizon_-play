import pandas as pd
import numpy as np
import random
import os
import urllib.parse

# Constants for Data Generation
NUM_CUSTOMERS = 1000
SUBSCRIPTION_TYPES = ['Standard with Ads', 'Standard', 'Premium']
DEVICE_TYPES = ['Setup Box', 'Wi-Fi Router', 'Mobile']
DEVICE_MAKE_MODEL = {
    'Setup Box': ['Verizon VMS1100', 'Verizon VMS4100'],
    'Wi-Fi Router': ['Verizon Quantum Gateway', 'Verizon 5G Home Router'],
    'Mobile': ['iPhone 14', 'Samsung Galaxy S23', 'Google Pixel 7']
}
CITIES = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
STATES = ['NY', 'CA', 'IL', 'TX', 'AZ']
REGULAR_PERKS = ['Discounted Subscription', 'Bundled Streaming Services', 'Unlimited Data Streaming', 'Free HD Streaming Upgrade', 'Priority Customer Support']
CONTENT_TYPES = ['Series', 'Movie', 'Live Event']

# Additional Content Titles
SERIES_TITLES = ['Stranger Things', 'The Crown', 'Money Heist', 'Ozark', 'The Witcher', 'Breaking Bad', 
                 'Narcos', 'Bridgerton', 'Black Mirror', 'The Umbrella Academy']
MOVIE_TITLES = ['The Irishman', 'Bird Box', 'Extraction', 'Marriage Story', 'The Old Guard', 
                '6 Underground', 'Enola Holmes', 'Army of the Dead', 'Red Notice', 'Don\'t Look Up']
LIVE_EVENT_TITLES = ['Billboard Music Awards', 'The Oscars', 'Super Bowl Halftime Show', 'New Year\'s Eve Countdown', 
                     'Concert Live Stream: Taylor Swift', 'Concert Live Stream: BTS', 'Netflix Global Fan Event: TUDUM',
                     'Golden Globe Awards', 'World Cup Final', 'Grammy Awards']

# Generate Customer Data
def generate_customer_data(num_customers):
    data = []
    for _ in range(num_customers):
        customer_id = random.randint(100000, 999999)
        subscription_type = random.choice(SUBSCRIPTION_TYPES)
        device_type = random.choice(DEVICE_TYPES)
        device_make_model = random.choice(DEVICE_MAKE_MODEL[device_type])
        location = {
            'address': f"{random.randint(1000, 9999)} Main St",
            'city': random.choice(CITIES),
            'state': random.choice(STATES),
            'zipcode': random.randint(10000, 99999)
        }
        days_before_perks = random.randint(1, 30)
        days_after_perks = random.randint(1, 30)
        total_data_usage = round(random.uniform(10, 100), 2)
        usage_days = random.sample(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], random.randint(1, 7))
        peak_hours = random.sample(range(24), random.randint(1, 4))
        received_regular_perks = random.choice([True, False])
        perks_description = random.choice(REGULAR_PERKS) if received_regular_perks else None
        content_type = random.choice(CONTENT_TYPES)
        
        # Assigning random titles based on content type
        if content_type == 'Series':
            content_title = random.choice(SERIES_TITLES)
        elif content_type == 'Movie':
            content_title = random.choice(MOVIE_TITLES)
        else:  # Live Event
            content_title = random.choice(LIVE_EVENT_TITLES)
        
        # Generate URL-friendly version of the title
        encoded_title = urllib.parse.quote(content_title.replace(" ", "-").lower())
        content_url = f"https://www.netflix.com/title/{encoded_title}"
        
        # Add additional fields for offer eligibility
        plus_play_status = random.choice([0, 1])  # 0 = Not using Plus Play, 1 = Using Plus Play
        streaming_hours = random.randint(0, 100)
        data_usage_gb = round(random.uniform(100, 500), 2)
        
        data.append({
            'Customer ID': customer_id,
            'Subscription Type': subscription_type,
            'Device Type': device_type,
            'Device Make/Model': device_make_model,
            'Address': location['address'],
            'City': location['city'],
            'State': location['state'],
            'Zipcode': location['zipcode'],
            'Days Before Perks': days_before_perks,
            'Days After Perks': days_after_perks,
            'Total Data Usage (GB)': total_data_usage,
            'Usage Days': usage_days,
            'Peak Hours': peak_hours,
            'Received Regular Perks': received_regular_perks,
            'Perks Description': perks_description,
            'Content Type': content_type,
            'Content Title': content_title,  # New field for the content title
            'Content URL': content_url,
            'PlusPlayStatus': plus_play_status,
            'StreamingHours': streaming_hours,
            'DataUsageGB': data_usage_gb
        })
    
    return pd.DataFrame(data)

# Apply Offer Assignment Logic
def assign_offers(df):
    df['Offer_DiscountedUpgrade'] = np.where(
        (df['Subscription Type'] != 'Premium') & (df['PlusPlayStatus'] == 1), 
        "Eligible for 20% Discount on Premium Upgrade", 
        "Not Eligible"
    )

    df['Offer_BundleSavings'] = np.where(
        (df['PlusPlayStatus'] == 1), 
        "Eligible for $10 Bundle Savings", 
        "Not Eligible"
    )

    df['Offer_FamilyPlanPerk'] = np.where(
        (df['Subscription Type'] == 'Standard') & (df['PlusPlayStatus'] == 1), 
        "Eligible for Free Netflix Standard on Family Plan", 
        "Not Eligible"
    )

    df['Offer_DataBoost'] = np.where(
        (df['StreamingHours'] > 50) & (df['PlusPlayStatus'] == 1), 
        "Eligible for Data Boost for HD Streaming", 
        "Not Eligible"
    )

    df['Offer_ExclusiveContent'] = np.where(
        (df['PlusPlayStatus'] == 1), 
        "Eligible for Exclusive Netflix Content Access", 
        "Not Eligible"
    )

    df['Offer_LimitedTime'] = np.where(
        (df['Subscription Type'] == 'Standard with Ads') & (df['PlusPlayStatus'] == 1), 
        "Eligible for First Month Free on Premium", 
        "Not Eligible"
    )

    df['Offer_LoyaltyRewards'] = np.where(
        (df['PlusPlayStatus'] == 1) & (df['DataUsageGB'] > 300), 
        "Eligible for 50% Off for 6 Months", 
        "Not Eligible"
    )

    df['Offer_GiftingOpportunity'] = np.where(
        (df['PlusPlayStatus'] == 1), 
        "Eligible to Gift 3-Month Netflix Subscription", 
        "Not Eligible"
    )

    df['Offer_StudentDiscount'] = np.where(
        (df['PlusPlayStatus'] == 1) & (df['Subscription Type'] == 'Standard with Ads'), 
        "Eligible for 30% Student Discount", 
        "Not Eligible"
    )

    df['Offer_WeekendStreamingPass'] = np.where(
        (df['StreamingHours'] > 20) & (df['PlusPlayStatus'] == 1), 
        "Eligible for Unlimited Weekend Streaming", 
        "Not Eligible"
    )
    return df

# Generate the data
df = generate_customer_data(NUM_CUSTOMERS)

# Apply the offer logic
df = assign_offers(df)

# Ensure the directory exists
output_directory = r'C:\Users\venka\Desktop\Netflix_Verizon_+play'
os.makedirs(output_directory, exist_ok=True)

# Save the modified DataFrame to a CSV file
output_path = os.path.join(output_directory, 'verizon_netflix_raw.csv')
df.to_csv(output_path, index=False)

print(f"Data saved to {output_path}")

# Optional: Display the first few rows of the final DataFrame
print(df.head())
