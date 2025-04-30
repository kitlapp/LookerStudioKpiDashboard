# PREPROCESSING FOR is_canceled TARGET
import os

# IMPORT LIBRARIES
from dotenv import load_dotenv
load_dotenv()
# Import SQLAlchemy to manage database connections
from sqlalchemy import create_engine

# Import datetime to display the time of creation of the cleaned dataset
from datetime import datetime

import pandas as pd                         # For data handling with DataFrames

# Import custom modules containing reusable cleaning, testing, and dictionary logic
from cleaning import (
    explore_outliers,  # Function to detect outliers in features
    month_components_calculation,  # Function to extract month components (e.g., sin/cos)
    day_components_calculation  # Function to extract day components (e.g., sin/cos)
)

# from testing import (
#     plot_circular_month,  # Function to visualize month components on a circle
#     plot_circular_day,  # Function to visualize day components on a circle
#     test_month_components_calculation,  # Unit test for month component extraction
#     test_day_components_calculation  # Unit test for day component extraction
# )

from dictionaries import country_to_category  # Dictionary that maps countries to predefined categories

# Suppress future warnings that may clutter output
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Import statistical functions and tools from statsmodels for multicollinearity checks
# from statsmodels.stats.outliers_influence import variance_inflation_factor  # Calculates VIF
# from statsmodels.tools.tools import add_constant                            # Adds constant column for regression

# Allow display of all DataFrame columns (useful when inspecting wide datasets)
pd.options.display.max_columns = 999
# =====================================================================================================================
# FETCH DATA FROM THE DATABASE

username = os.getenv('postgresuser')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')
db_name = os.getenv('db_name')

# Set up the connection to the local PostgreSQL database
engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{db_name}')

# Fetch data from the 'hotel_booking' table
query = "SELECT * FROM hotel_booking"
df_raw = pd.read_sql(query, engine)

# Create a second file for KPIs calculation
dfdash = df_raw.copy()
# =====================================================================================================================
# HANDLING NaNs
# Explore the NaNs:
# df_raw.isna().sum()
# Make a working copy of the raw dataset to avoid altering the original
df2 = df_raw.copy()

# Fill missing values in 'children' column with the most frequent value (mode)
df2['children'] = df2['children'].fillna(value=df2['children'].mode()[0])

# Replace missing values in 'agent' with 0, indicating direct bookings without a travel agent
df2['agent'] = df2['agent'].fillna(value=0)

# Replace missing values in 'company' with 0, meaning bookings not linked to any company
df2['company'] = df2['company'].fillna(value=0)

# Drop all rows with missing 'country' values, since location info is important for analysis
df2 = df2.drop(labels=df2.loc[df2['country'].isna()].index)

# DASHBOARD DATAFRAME CLEANING (same logic as above) #####
dfdash2 = dfdash.copy() 

# Fill missing values similarly for dashboard DataFrame
dfdash2['children'] = dfdash2['children'].fillna(value=dfdash2['children'].mode()[0])
dfdash2['agent'] = dfdash2['agent'].fillna(value=0)
dfdash2['company'] = dfdash2['company'].fillna(value=0)
dfdash2 = dfdash2.drop(labels=dfdash2.loc[dfdash2['country'].isna()].index)
# =====================================================================================================================
# HANDLING DATE-RELATED COLUMNS
df3 = df2.copy()

# Create a dictionary to convert month names to their corresponding numeric values (as strings)
month_mapping = {
    "January": '1', "February": '2', "March": '3', "April": '4', "May": '5', "June": '6',
    "July": '7', "August": '8', "September": '9', "October": '10', "November": '11', "December": '12'
}

# Map month names in 'arrival_date_month' column to their numeric equivalents and convert them to integers
df3['arrival_date_month'] = df3['arrival_date_month'].map(month_mapping).astype(int)

# DASHBOARD DATAFRAME
dfdash3 = dfdash2.copy()

# Map month names to integers using the same dictionary
dfdash3['arrival_date_month'] = dfdash3['arrival_date_month'].map(month_mapping).astype(int)

# Combine year, month, and day columns into a single date string in 'YYYY-MM-DD' format
dfdash3['arrival_date'] = (
    dfdash3['arrival_date_year'].astype(str) + '-' +
    dfdash3['arrival_date_month'].astype(str) + '-' +
    dfdash3['arrival_date_day_of_month'].astype(str)
)

# Convert the date strings into proper datetime objects for easier time-based analysis
dfdash3['arrival_date'] = pd.to_datetime(dfdash3['arrival_date'], format='%Y-%m-%d')

# As expected, the month of arrival is very strongly correlated with the week number of arrival.
# Let's confirm this by calculating their correlation:
df3['arrival_date_month'].corr(df3['arrival_date_week_number'])

# Since they are highly correlated, we can safely drop 'arrival_date_week_number' to reduce redundancy.
df3 = df3.drop(columns='arrival_date_week_number')

# Apply custom functions to perform cyclic encoding on the 'arrival_date_month' and 'arrival_date_day_of_month' column.
# This helps machine learning models better understand the cyclical nature of months and days of months.
df4 = month_components_calculation(dataframe=df3, month_columns=['arrival_date_month'])
df5 = day_components_calculation(dataframe=df4,
                                 year_columns=['arrival_date_year'],
                                 month_columns=['arrival_date_month'],
                                 day_columns=['arrival_date_day_of_month'])
# =====================================================================================================================
# Functions for Testing

# test_month_components_calculation(df4, month_columns=['arrival_date_month'])

# test_day_components_calculation(dataframe=df5, year_columns=['arrival_date_year'],
#                                 month_columns=['arrival_date_month'],
#                                 day_columns=['arrival_date_day_of_month']
#                            )
# =====================================================================================================================
# CHECK FOR DUPLICATES

# Count the number of fully duplicated rows in the preprocessed main dataframe
df5.duplicated().sum()
# =====================================================================================================================
# DROP UNIMPORTANT AND FUTURE INFORMATION COLUMNS
df6 = df5.copy()

# List of columns to be dropped as they are not needed for analysis
cols_to_be_dropped = ['name', 'email', 'arrival_date_month', 'arrival_date_day_of_month', 'phone-number',
                      'credit_card', 'reservation_status', 'reservation_status_date', 'assigned_room_type',
                      'deposit_type', 'required_car_parking_spaces']

# Drop the columns specified in 'cols_to_be_dropped'
df6 = df6.drop(columns=cols_to_be_dropped)

# DASHBOARD DATAFRAME
# List of columns to be dropped from the dashboard dataframe
dashcols_to_be_dropped = ['name', 'email', 'arrival_date_month', 'arrival_date_day_of_month', 'phone-number',
                          'credit_card', 'reservation_status', 'reservation_status_date', 'assigned_room_type',
                          'deposit_type', 'required_car_parking_spaces', 'arrival_date_week_number']

# Create a copy of the dashboard dataframe for further processing
dfdash4 = dfdash3.copy()

# Drop the unimportant columns from the dashboard dataframe
dfdash4 = dfdash4.drop(columns=dashcols_to_be_dropped)
# =====================================================================================================================
# CREATING total_kids COLUMN
df7 = df6.copy()

# Merge the 'children' and 'babies' columns to create a new column 'total_kids' representing the total number of kids
df7['total_kids'] = df7['children'].astype(int) + df7['babies'].astype(int)

# Drop the original 'children' and 'babies' columns after merging
df7 = df7.drop(columns=['children', 'babies'])

# Drop rows with outliers (total kids > 3) and reset index
df7 = df7.loc[df7['total_kids'] <= 3].reset_index(drop=True)

# DASHBOARD DATAFRAME
# Create a copy of the dashboard dataframe to perform the same operations
dfdash5 = dfdash4.copy()

# Merge the 'children' and 'babies' columns to create a new column 'total_kids' representing the total number of kids
dfdash5['total_kids'] = dfdash5['children'].astype(int) + dfdash5['babies'].astype(int)

# Drop the original 'children' and 'babies' columns after merging
dfdash5 = dfdash5.drop(columns=['children', 'babies'])

# Drop rows with outliers (total kids > 3) and reset index in the dashboard dataframe
dfdash5 = dfdash5.loc[dfdash5['total_kids'] <= 3].reset_index(drop=True)
# =====================================================================================================================
# HANDLING adults COLUMN

# There are observations where both adults and total_kids equal 0. This can't be explained and therefore all rows where
# adults=0 will be dropped. Additionally, in all cases where adults were greater than 4 the bookings were canceled and
# the adr equals 0. For this reason, values for adults from 1 to 4 are considered the most explainable and normal.
# We will drop all other values.

df8 = df7.copy()

# Exclude bookings where the number of adults is 0. Also, ensure that the number of adults is between 1 and 4.
df8 = df8[(df8['adults'] > 0) & (df8['adults'] <= 4)].reset_index(drop=True)

# DASHBOARD DATAFRAME
# Create a copy of the dashboard dataframe to perform the same operations
dfdash6 = dfdash5.copy()

# Exclude bookings where the number of adults is 0. Also, ensure that the number of adults is between 1 and 4.
dfdash6 = dfdash6[(dfdash6['adults'] > 0) & (dfdash6['adults'] <= 4)].reset_index(drop=True)
# =====================================================================================================================
# HANDLING meal COLUMN
df9 = df8.copy()

# Drop rows where the 'meal' column is 'Undefined', indicating no meal choice
df9 = df9.drop(labels=df9[df9['meal'] == 'Undefined'].index).reset_index(drop=True)

# Rename the 'meal' column to 'number_of_meals' for clarity
df9 = df9.rename(columns={'meal': 'number_of_meals'})

# Create a dictionary to map meal types to numerical values
meal_mapping = {'BB': 1, 'HB': 2, 'SC': 0, 'FB': 3}

# Map the dictionary to the 'number_of_meals' column, reducing complexity
df9['number_of_meals'] = df9['number_of_meals'].map(meal_mapping).astype(int)

# *** Ultimately, the 'meal' feature was reduced from 5 categories to 3 categories! ***

# DASHBOARD DATAFRAME
# Create a copy of the dashboard dataframe to perform the same operations
dfdash7 = dfdash6.copy()

# Drop rows where the 'meal' column is 'Undefined', indicating no meal choice
dfdash7 = dfdash7.drop(labels=dfdash7[dfdash7['meal'] == 'Undefined'].index).reset_index(drop=True)

# Rename the 'meal' column to 'number_of_meals' for clarity
dfdash7 = dfdash7.rename(columns={'meal': 'number_of_meals'})

# Map the dictionary to the 'number_of_meals' column, reducing complexity
dfdash7['number_of_meals'] = dfdash7['number_of_meals'].map(meal_mapping).astype(int)
# =====================================================================================================================
# HANDLING country COLUMN
df10 = df9.copy()

# Map the 'country' column values to a smaller set of categories using the 'country_to_category' dictionary.
# This reduces 177 unique country values to only 15.
df10['country'] = df10['country'].map(country_to_category).astype('category')

# Drop the rows where the 'country' column is 'Antarctica', as it represents very few bookings and will reduce
# model complexity.
df10 = df10.drop(labels=df10[df10['country'] == 'Antarctica'].index, axis=0).reset_index(drop=True)

# Remove 'Antarctica' from the category list, as it has been dropped.
df10['country'] = df10['country'].cat.remove_categories('Antarctica')

# Drop any rows with NaN values to ensure clean data.
df10 = df10.dropna()

# *** Ultimately, the 'country' feature was reduced from 177 categories to only 15 categories! ***
# =====================================================================================================================
# HANDLING market_segment COLUMN
df11 = df10.copy()

# Drop all rows where the 'market_segment' column has the category 'Undefined', as it includes very few observations
df11 = df11.drop(labels=df11[df11['market_segment'] == 'Undefined'].index).reset_index(drop=True)

# Replace the 'Complementary' and 'Aviation' categories in the 'market_segment' column with 'Other' to consolidate
# rare categories
df11['market_segment'] = df11['market_segment'].replace(
    {'Complementary': 'Other', 'Aviation': 'Other'}).astype('category')

# *** Ultimately, the 'market_segment' feature was reduced from 8 to 5 categories! ***

# DASHBOARD DATAFRAME
# Copy the dashboard dataframe
dfdash8 = dfdash7.copy()

# Drop all rows where the 'market_segment' column has the category 'Undefined'
dfdash8 = dfdash8.drop(labels=dfdash8[dfdash8['market_segment'] == 'Undefined'].index).reset_index(drop=True)

# Replace the 'Complementary' and 'Aviation' categories in the 'market_segment' column with 'Other'
dfdash8['market_segment'] = dfdash8['market_segment'].replace(
    {'Complementary': 'Other', 'Aviation': 'Other'}).astype('category')
# =====================================================================================================================
# HANDLING distribution_channel COLUMN
df12 = df11.copy()

# Drop all rows where the 'distribution_channel' column has the category 'Undefined', as it includes very few
# observations
df12 = df12.drop(labels=df12[df12['distribution_channel'] == 'Undefined'].index).reset_index(drop=True)

# Convert the 'distribution_channel' column to categorical type
df12['distribution_channel'] = df12['distribution_channel'].astype('category')

# *** Ultimately, the 'distribution_channel' feature was reduced from 5 to 3 categories! ***

# DASHBOARD DATAFRAME
# Copy the dashboard dataframe
dfdash9 = dfdash8.copy()

# Drop all rows where the 'distribution_channel' column has the category 'Undefined'
dfdash9 = dfdash9.drop(labels=dfdash9[dfdash9['distribution_channel'] == 'Undefined'].index).reset_index(drop=True)

# Convert the 'distribution_channel' column to categorical type
dfdash9['distribution_channel'] = dfdash9['distribution_channel'].astype('category')
# =====================================================================================================================
# HANDLING reserved_room_type COLUMN
df13 = df12.copy()

# Merge categories in the 'reserved_room_type' column, combining multiple categories into 'Other'
df13['reserved_room_type'] = df13['reserved_room_type'].replace(
    {'C': 'Other', 'B': 'Other', 'H': 'Other', 'L': 'Other'}).astype('category')

# DASHBOARD DATAFRAME
# Copy the dashboard dataframe
dfdash10 = dfdash9.copy()

# Merge categories in the 'reserved_room_type' column, combining multiple categories into 'Other'
dfdash10['reserved_room_type'] = dfdash10['reserved_room_type'].replace(
    {'C': 'Other', 'B': 'Other', 'H': 'Other', 'L': 'Other'}).astype('category')

# *** Ultimately, the 'reserved_room_type' feature was reduced from 9 to 6 categories! ***
# =====================================================================================================================
# HANDLING agent & company COLUMNS
df14 = df13.copy()

# Convert 'agent' column to binary: 1 if not 0, else 0
df14['agent'] = df14['agent'].apply(lambda x: 1 if x != 0 else 0)

# Convert 'company' column to binary: 1 if not 0, else 0
df14['company'] = df14['company'].apply(lambda x: 1 if x != 0 else 0)

# Rename the columns to more intuitive names
df14 = df14.rename(columns={'agent': 'has_agent', 'company': 'has_company'})

# DASHBOARD DATAFRAME
# Copy the dashboard dataframe
dfdash11 = dfdash10.copy()

# Convert 'agent' column to binary: 1 if not 0, else 0
dfdash11['agent'] = dfdash11['agent'].apply(lambda x: 1 if x != 0 else 0)

# Convert 'company' column to binary: 1 if not 0, else 0
dfdash11['company'] = dfdash11['company'].apply(lambda x: 1 if x != 0 else 0)

# Rename the columns to more intuitive names
dfdash11 = dfdash11.rename(columns={'agent': 'has_agent', 'company': 'has_company'})
# =====================================================================================================================
# HANDLING previous_cancellations AND previous_bookings_not_canceled COLUMNS
df15 = df14.copy()

# Apply transformation to 'previous_cancellations' column:
# Set to 2 if greater than or equal to 2, 0 if less than 1, else leave as is
df15['previous_cancellations'] = df15['previous_cancellations'].apply(lambda x: 2 if x >= 2 else (0 if x < 1 else x))

# Apply transformation to 'previous_bookings_not_canceled' column:
# Set to 2 if greater than or equal to 2, 0 if less than 1, else leave as is
df15['previous_bookings_not_canceled'] = df15['previous_bookings_not_canceled'].apply(
    lambda x: 2 if x >= 2 else (0 if x < 1 else x))

# Rename the columns to more intuitive names
df15 = df15.rename(columns={'previous_cancellations': 'number_of_previous_cancellations',
                            'previous_bookings_not_canceled': 'number_of_previous_bookings_not_canceled'})
# =====================================================================================================================
# HANDLING booking_changes AND total_of_special_requests COLUMNS
df16 = df15.copy()

# Apply transformation to 'booking_changes' column:
# Set to 3 if greater than 2, 2 if equal to 2, 1 if equal to 1, else leave as is
df16['booking_changes'] = df16['booking_changes'].apply(
    lambda x: 3 if x > 2 else (2 if x == 2 else (1 if x == 1 else x)))

# Apply transformation to 'total_of_special_requests' column:
# Set to 3 if greater than 2, 2 if equal to 2, 1 if equal to 1, else leave as is
df16['total_of_special_requests'] = df16['total_of_special_requests'].apply(
    lambda x: 3 if x > 2 else (2 if x == 2 else (1 if x == 1 else x)))

# Rename the columns to more intuitive names
df16 = df16.rename(columns={'booking_changes': 'number_of_booking_changes',
                            'total_of_special_requests': 'number_of_special_requests'})
# =====================================================================================================================
# HANDLING days_in_waiting_list COLUMN
df17 = df16.copy()

# Apply transformation to 'days_in_waiting_list' column:
# Set to 1 if greater than 0, else leave as is
df17['days_in_waiting_list'] = df17['days_in_waiting_list'].apply(lambda x: 1 if x > 0 else x)

# Rename the 'days_in_waiting_list' column to 'has_waited'
df17 = df17.rename(columns={'days_in_waiting_list': 'has_waited'})
# =====================================================================================================================
# HANDLING OUTLIERS
# Calling the explore_outliers function to visualize the distribution of some features
explore_outliers(dataframe=df17, column='lead_time', number_of_bins=60, negative=False)

df18 = df17.copy()

# Set the threshold values for ADR (average daily rate) and lead_time outliers:
adr_outlier_value = 5400  # Maximum acceptable value for ADR
lead_time_outlier_border = 640  # Maximum acceptable value for lead time

# Remove rows where ADR is higher than the defined threshold or negative:
df18 = df18.loc[(df18['adr'] < adr_outlier_value) & (df18['adr'] >= 0)].reset_index(drop=True)

# Remove rows where lead_time exceeds the defined threshold:
df18 = df18.loc[df18['lead_time'] < lead_time_outlier_border].reset_index(drop=True)

# Create a copy of the dashboard dataframe (dfdash11) for outlier removal:
dfdash12 = dfdash11.copy()

# Remove rows where ADR is higher than the defined threshold or negative in the dashboard dataframe:
dfdash12 = dfdash12.loc[(dfdash12['adr'] < adr_outlier_value) & (dfdash12['adr'] >= 0)].reset_index(drop=True)

# Remove rows where lead_time exceeds the defined threshold in the dashboard dataframe:
dfdash12 = dfdash12.loc[dfdash12['lead_time'] < lead_time_outlier_border].reset_index(drop=True)
# =====================================================================================================================
# Final Check on dtypes
df19 = df18.copy()

# Specify columns to be converted to categorical data type:
cols_to_be_categorized = ['hotel', 'arrival_date_year', 'customer_type']

# Convert the specified columns to categorical data type:
df19[cols_to_be_categorized] = df19[cols_to_be_categorized].astype('category')

# Create a copy of the dashboard dataframe (dfdash12) to apply categorization:
dfdash13 = dfdash12.copy()

# Specify columns in the dashboard dataframe to be converted to categorical data type:
dashcols_to_be_categorized = ['hotel', 'customer_type', 'country']

# Convert the specified columns in the dashboard dataframe to categorical data type:
dfdash13[dashcols_to_be_categorized] = dfdash13[dashcols_to_be_categorized].astype('category')
# =====================================================================================================================
# ENCODE CATEGORIES
# Specify the list of columns to be one-hot encoded:
categories = ['hotel', 'arrival_date_year', 'country', 'market_segment', 'distribution_channel', 'reserved_room_type',
              'customer_type']

# Apply one-hot encoding on the selected columns in df19 and drop the first category to avoid multicollinearity:
df20 = pd.get_dummies(data=df19, columns=categories, drop_first=True)

# Identify columns with boolean data type:
boolean_cols = df20.columns[df20.dtypes == 'bool']

# Convert boolean columns to integers (True becomes 1, False becomes 0):
df20[boolean_cols] = df20[boolean_cols].astype(int)
# =====================================================================================================================
# CHECK FOR MULTICOLINEARITY
# X = df20.copy()
# # Add a constant (intercept) column to the DataFrame X to use in regression models:
# X_with_const = add_constant(X)
# # Initialize an empty DataFrame to store the features and their corresponding VIF values:
# vif = pd.DataFrame()
# # Assign column names to the DataFrame: one for features and the other for VIF values:
# vif["Feature"] = X_with_const.columns
# # Calculate the Variance Inflation Factor (VIF) for each feature in the dataset
# # and store the values in the "VIF" column of the DataFrame:
# vif["VIF"] = [variance_inflation_factor(X_with_const.values, i) for i in range(X_with_const.shape[1])]
# # Sort the DataFrame 'vif' in descending order based on the VIF values to identify
# # the features with the highest multicollinearity (i.e., those with the highest VIF).
# vif_sorted = vif.sort_values(by="VIF", ascending=False)
# # Filter the sorted 'vif' DataFrame to display only the features with a VIF greater than 5
# vif_sorted[vif_sorted['VIF'] > 5]
# =====================================================================================================================
# EXPORT CLEANED FILES
# Establish a connection to the PostgreSQL database using SQLAlchemy engine
engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{db_name}')

# Upload the 'df20' dataframe (Logistic Regression and Random Forest dataset) to the PostgreSQL database.
# If the table "logreg_rf_data" already exists, it will be replaced with the new data.
df20['last_updated'] = datetime.now()  # To check if the update happens properly
df20.to_sql("logreg_rf_data", engine, if_exists="replace", index=False)

# Upload the 'dfdash13' dataframe (KPIs dataset for the dashboard) to the PostgreSQL database.
# If the table "dashboard_data" already exists, it will be replaced with the new data.
dfdash13['last_updated'] = datetime.now()  # To check if the update happens properly
dfdash13.to_sql("dashboard_data", engine, if_exists="replace", index=False)
# =====================================================================================================================
