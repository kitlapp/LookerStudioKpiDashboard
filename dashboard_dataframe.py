# Import libraries for data manipulation and numerical operations

# Import SQLAlchemy to enable interaction with PostgreSQL databases
from sqlalchemy import create_engine

import pandas as pd
import numpy as np

# Suppress specific warning messages (e.g., deprecation or future warnings)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
# =====================================================================================================================
# Set up the connection to the local PostgreSQL database
engine = create_engine('postgresql://postgres:root@localhost:5432/hotel_booking')

# Fetch data from the 'hotel_booking' table
query = "SELECT * FROM dashboard_data"
df = pd.read_sql(query, engine)
# =====================================================================================================================
filter_city_hotel = df[df['hotel'] == 'City Hotel']
filter_resort_hotel = df[df['hotel'] == 'Resort Hotel']

total_obs = df.shape[0]
total_obs_city_hotel = df[df['hotel'] == 'City Hotel'].shape[0]
total_obs_resort_hotel = df[df['hotel'] == 'Resort Hotel'].shape[0]

# AVERAGE CANCELLATION RATE
avg_canc_rate = round(df['is_canceled'].mean() * 100, 2)
avg_canc_rate_city_hotel = round(filter_city_hotel['is_canceled'].mean() * 100, 2)
avg_canc_rate_resort_hotel = round(filter_resort_hotel['is_canceled'].mean() * 100, 2)
print(f"Average Cancellation Rate: {avg_canc_rate} %")
print(f"Average Cancellation Rate City Hotel: {avg_canc_rate_city_hotel} %")
print(f"Average Cancellation Rate Resort Hotel: {avg_canc_rate_resort_hotel} %")

# AVERAGE PREVIOUS CANCELLATION RATE
avg_previous_canc_rate = round(df['previous_cancellations'].mean() * 100, 2)
avg_previous_canc_rate_city_hotel = round(filter_city_hotel['previous_cancellations'].mean() * 100, 2)
avg_previous_canc_rate_resort_hotel = round(filter_resort_hotel['previous_cancellations'].mean() * 100, 2)
print(f"Average Previous Cancellation Rate: {avg_previous_canc_rate} %")
print(f"Average Previous Cancellation Rate City Hotel: {avg_previous_canc_rate_city_hotel} %")
print(f"Average Previous Cancellation Rate Resort Hotel: {avg_previous_canc_rate_resort_hotel} %")


# TOTAL REVENUE
total_revenue = round(df['adr'].sum())
total_revenue_city_hotel = round(filter_city_hotel['adr'].sum())
total_revenue_resort_hotel = round(filter_resort_hotel['adr'].sum())
print(f"Total Revenue: {total_revenue} €")
print(f"Total Revenue City Hotel: {total_revenue_city_hotel} €")
print(f"Total Revenue Resort Hotel: {total_revenue_resort_hotel} €")

# AVERAGE DAILY RATE
adr = round(df['adr'].mean(), 2)
adr_city_hotel = round(filter_city_hotel['adr'].mean(), 2)
adr_resort_hotel = round(filter_resort_hotel['adr'].mean(), 2)
print(f"Average Daily Rate: {adr} €")
print(f"Average Daily Rate City Hotel: {adr_city_hotel} €")
print(f"Average Daily Rate Resort Hotel: {adr_resort_hotel} €")

# AVERAGE LEAD TIME
avg_lead_time = round(df['lead_time'].mean(), 2)
avg_lead_time_city_hotel = round(filter_city_hotel['lead_time'].mean(), 2)
avg_lead_time_resort_hotel = round(filter_resort_hotel['lead_time'].mean(), 2)
print(f"Average Lead Time: {avg_lead_time} days")
print(f"Average Lead Time City Hotel: {avg_lead_time_city_hotel} days")
print(f"Average Lead TIme Resort Hotel: {avg_lead_time_resort_hotel} days")

# REVENUE PER GUEST
total_guests = df['adults'].sum() + df['total_kids'].sum()
total_guests_city_hotel = filter_city_hotel['adults'].sum() + filter_city_hotel['total_kids'].sum()
total_guests_resort_hotel = filter_resort_hotel['adults'].sum() + filter_resort_hotel['total_kids'].sum()

revpg = round(total_revenue / total_guests, 2)
revpg_city_hotel = round(total_revenue_city_hotel / total_guests_city_hotel, 2)
revpg_resort_hotel = round(total_revenue_resort_hotel / total_guests_resort_hotel, 2)
print(f"Average Revenue per Guest: {revpg} €")
print(f"Average Revenue per Guest City Hotel: {revpg_city_hotel} €")
print(f"Average Revenue per Guest Resort Hotel: {revpg_resort_hotel} €")

# LENGTH OF STAY
total_nights = df['stays_in_week_nights'].sum() + df['stays_in_weekend_nights'].sum()
total_nights_city_hotel = (filter_city_hotel['stays_in_week_nights'].sum() +
                           filter_city_hotel['stays_in_weekend_nights'].sum())
total_nights_resort_hotel = (filter_resort_hotel['stays_in_week_nights'].sum() +
                             filter_resort_hotel['stays_in_weekend_nights'].sum())

length_of_stay = round(total_nights / total_obs, 2)
length_of_stay_city_hotel = round(total_nights_city_hotel / total_obs_city_hotel, 2)
length_of_stay_resort_hotel = round(total_nights_resort_hotel / total_obs_resort_hotel, 2)
print(f"Length of Stay: {length_of_stay} days")
print(f"Length of Stay City Hotel: {length_of_stay_city_hotel} days")
print(f"Length of Stay Resort Hotel: {length_of_stay_resort_hotel} days")

# BOOKINGS BY SOURCE (DATAFRAME)
values = df['market_segment'].value_counts().values
values_perc = np.round(100 * (values / total_obs), 2)
values_city_hotel = df[df['hotel'] == 'City Hotel']['market_segment'].value_counts().values
values_perc_city_hotel = np.round(100 * (values_city_hotel / total_obs_city_hotel), 2)
values_resort_hotel = df[df['hotel'] == 'Resort Hotel']['market_segment'].value_counts().values
values_perc_resort_hotel = np.round(100 * (values_resort_hotel / total_obs_resort_hotel), 2)

index = df['market_segment'].value_counts().keys()
columns = ['Total Counts', 'Total Counts (%)', 'City Hotel Counts', 'City Hotel Counts (%)', 'Resort Hotel Counts',
           'Resort Hotel Counts (%)']
data = list(zip(
    values, values_perc, values_city_hotel, values_perc_city_hotel, values_resort_hotel, values_perc_resort_hotel))

market_df = pd.DataFrame(index=index, data=data, columns=columns)
market_df.index.name = 'Market Segment'
# =====================================================================================================================
# KPIs Summary Table (One-row DataFrame)
kpis = {
    'Total Bookings': total_obs,
    'Total Bookings City Hotel': total_obs_city_hotel,
    'Total Bookings Resort Hotel': total_obs_resort_hotel,
    'Cancellation Rate (%)': avg_canc_rate,
    'Cancellation Rate City Hotel (%)': avg_canc_rate_city_hotel,
    'Cancellation Rate Resort Hotel (%)': avg_canc_rate_resort_hotel,
    'Previous Cancellation Rate (%)': avg_previous_canc_rate,
    'Previous Cancellation Rate City Hotel (%)': avg_previous_canc_rate_city_hotel,
    'Previous Cancellation Rate Resort Hotel (%)': avg_previous_canc_rate_resort_hotel,
    'Total Revenue (€)': total_revenue,
    'Total Revenue City Hotel (€)': total_revenue_city_hotel,
    'Total Revenue Resort Hotel (€)': total_revenue_resort_hotel,
    'ADR (€)': adr,
    'ADR City Hotel (€)': adr_city_hotel,
    'ADR Resort Hotel (€)': adr_resort_hotel,
    'Average Lead Time (days)': avg_lead_time,
    'Average Lead Time City Hotel (days)': avg_lead_time_city_hotel,
    'Average Lead Time Resort Hotel (days)': avg_lead_time_resort_hotel,
    'Revenue per Guest (€)': revpg,
    'Revenue per Guest City Hotel (€)': revpg_city_hotel,
    'Revenue per Guest Resort Hotel (€)': revpg_resort_hotel,
    'Length of Stay (days)': length_of_stay,
    'Length of Stay City Hotel (days)': length_of_stay_city_hotel,
    'Length of Stay Resort Hotel (days)': length_of_stay_resort_hotel
}

kpis_df = pd.DataFrame([kpis])

# Save to CSV
kpis_df.to_csv('hotel_kpis.csv', index=False)
market_df.to_csv('hotel_market_segments.csv')
